#!/usr/bin/env python3
"""leak_check.py — Vorfilter gegen versehentliche Veröffentlichung.

Ersetzt den naheliegenden Ad-hoc-Grep vor einem Push:

    git diff origin/main..HEAD | grep -nEi "/Users/|~/|192\\.168\\.|token|secret"

Zwei Dinge macht dieses Skript anders, und beide sind der eigentliche Punkt:

1. ES DRUCKT DEN FUND NICHT AUS.
   Der Ad-hoc-Grep gibt die TREFFERZEILE aus — und holt damit genau das ins
   Sitzungsprotokoll, wogegen er schützen soll. Ein Meßmittel, das zerstört,
   was es mißt. Hier wird maskiert: Regelname, Fundstelle, Längenangabe,
   erste und letzte zwei Zeichen. Wer das Original sehen will, sagt --show
   und trifft damit eine bewußte Entscheidung.

2. ES IST KALIBRIERT — in BEIDE Richtungen.
   `--selftest` fährt ein eingebautes Korpus: Fälle, die anschlagen MÜSSEN,
   und Fälle, die schweigen MÜSSEN. Ein Suchlauf ohne einen Treffer, der
   treffen muß, ist von einem blinden Lauf nicht zu unterscheiden.

Ein Treffer ist ein PRÜFAUFTRAG, kein Urteil. Der eigene Name in einer
Copyright-Zeile ist Urheberschaft, keine Veröffentlichung.

Exit-Codes (fail closed):
    0  nichts gefunden
    1  Funde vorhanden  -> ansehen
    2  interner Fehler   -> NICHT als "sauber" werten

Aufrufe:
    leak_check.py DATEI... | VERZEICHNIS...
    leak_check.py -                        # aus einer Pipe (stdin)
    leak_check.py --staged                 # git-Index (pre-commit)
    leak_check.py --diff origin/main..HEAD # Was ein Push veröffentlichen würde
    leak_check.py --selftest               # Kalibrierung beweisen
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------- Regelwerk

# severity: "hoch"   = fast immer ein echter Fund
#           "mittel" = häufig echt, aber Kontext entscheidet
#           "hinweis"= sehr oft harmlos; bewußt laut, weil billig zu prüfen
@dataclass(frozen=True)
class Rule:
    name: str
    severity: str
    pattern: re.Pattern
    hint: str


def _r(name, severity, pattern, hint, flags=0):
    return Rule(name, severity, re.compile(pattern, flags), hint)


RULES: list[Rule] = [
    _r("private_key", "hoch",
       r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----",
       "Privater Schlüssel im Klartext."),
    _r("anthropic_key", "hoch",
       r"sk-ant-[A-Za-z0-9_\-]{20,}",
       "Anthropic-API-Schlüssel."),
    _r("openai_key", "hoch",
       r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}",
       "OpenAI-API-Schlüssel."),
    _r("github_token", "hoch",
       r"\bgh[pousr]_[A-Za-z0-9]{20,}",
       "GitHub-Token."),
    _r("aws_key_id", "hoch",
       r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
       "AWS-Zugriffsschlüssel."),
    _r("jwt", "hoch",
       r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}",
       "JSON Web Token."),
    _r("secret_assignment", "hoch",
       r"(?:token|secret|passwor[dt]|passwd|api[_\-]?key|credential)"
       r"\s*[:=]\s*[\"']?([^\s\"',;]{6,})",
       "Zuweisung eines Geheimnisses mit Wert.", re.I),
    _r("iban", "hoch",
       r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){3,7}\b",
       "IBAN."),

    _r("email", "mittel",
       r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
       "Mailadresse — bei fremden Adressen heikel."),
    _r("mac_address", "mittel",
       r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b",
       "MAC-Adresse — gerätegebunden."),
    _r("geo_precise", "mittel",
       r"-?\d{1,3}\.\d{6,}\s*,\s*-?\d{1,3}\.\d{6,}",
       "Koordinatenpaar mit hoher Genauigkeit — Wohnort-Verdacht."),
    _r("home_path", "mittel",
       r"/(?:Users|home)/(?!runner\b|user\b)[A-Za-z0-9._\-]+",
       "Absoluter Pfad mit Benutzernamen."),
    _r("phone_de", "mittel",
       r"(?:\+49|\b0)\s?1\d{2}[\s.\-/]?\d{3,}[\s.\-/]?\d{3,}\b",
       "Deutsche Mobilnummer."),

    _r("private_ipv4", "hinweis",
       r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b",
       "Private IP — oft harmlos, in Prosa aber verräterisch."),
    _r("secret_word", "hinweis",
       r"\b(?:passwort|credentials?)\b",
       "Schlüsselwort ohne Wert — nur ein Leseanstoß.", re.I),
]

# Adressen/Hosts, die als Platzhalter gelten und nie anschlagen sollen.
PLACEHOLDER = re.compile(
    r"(?:@(?:example\.(?:com|org|net)|test|localhost|invalid)\b"
    r"|\b(?:noreply|no-reply)@)", re.I)

# Werte, die ein Geheimnis nur BESCHREIBEN statt es zu sein. Gemessen am
# 24.08.2026 an Vault und Workspace: alle 15 HOCH-Treffer im Vault waren
# solche Formen (`<wert>`, ein CLI-Flag in Backticks, deutsche Prosa).
# Ohne diese Ausnahme schreit das Werkzeug so oft, daß es niemand liest —
# und ein Wachposten, den man wegklickt, schützt nichts.
PLACEHOLDER_VALUE = re.compile(
    r"""^(?:
          .*[<>`${}]                      # <wert>, ${VAR}, {{x}}, `--flag`
        | [*x.…_\-]+$                     # ****, xxxx, ----, ...
        | (?:redacted|changeme|geheim\w*|passwor[dt]|secret|token|wert|value
           |dein\w*|ihre?\w*|your\w*|hier\w*|beispiel\w*|example|placeholder
           |none|null|true|false|xxx\w*)\W*$
      )""",
    re.I | re.X)

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
             ".mypy_cache", ".pytest_cache", "dist", "build", ".next"}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip",
               ".gz", ".tgz", ".bz2", ".xz", ".mp4", ".mov", ".mp3", ".wav",
               ".woff", ".woff2", ".ttf", ".otf", ".ico", ".icns", ".pyc",
               ".so", ".dylib", ".lock"}

MAX_BYTES = 8 * 1024 * 1024


@dataclass
class Finding:
    rule: Rule
    where: str
    line_no: int
    raw: str


def mask(value: str) -> str:
    """Maskiert den Fund. Gibt Form und Länge preis, nie den Inhalt."""
    n = len(value)
    if n <= 4:
        return "•" * n + f" ({n})"
    return f"{value[:2]}{'•' * (n - 4)}{value[-2:]} ({n})"


# ---------------------------------------------------------------- Allowlist

def load_allowlist(root: Path) -> list[tuple[str, re.Pattern]]:
    """`.leakcheckignore`: je Zeile `<regelname|*> <regex>`. `#` ist Kommentar."""
    out: list[tuple[str, re.Pattern]] = []
    f = root / ".leakcheckignore"
    if not f.is_file():
        return out
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            out.append((parts[0], re.compile(parts[1])))
        except re.error:
            print(f"leak_check: unlesbares Muster in .leakcheckignore: {ln}",
                  file=sys.stderr)
    return out


def allowed(rule_name: str, value: str, line: str,
            allowlist: list[tuple[str, re.Pattern]]) -> bool:
    if "leakcheck: allow" in line:
        tail = line.split("leakcheck: allow", 1)[1]
        if rule_name in tail or tail.strip() in ("", "*"):
            return True
    for name, pat in allowlist:
        if name in ("*", rule_name) and pat.search(value):
            return True
    return False


# ------------------------------------------------------------------ Scannen

def scan_text(text: str, where: str,
              allowlist: list[tuple[str, re.Pattern]],
              min_sev: set[str]) -> list[Finding]:
    found: list[Finding] = []
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 4000:
            line = line[:4000]
        for rule in RULES:
            if rule.severity not in min_sev:
                continue
            for m in rule.pattern.finditer(line):
                value = m.group(m.lastindex or 0)
                if PLACEHOLDER.search(m.group(0)):
                    continue
                if rule.name == "secret_assignment" and \
                        PLACEHOLDER_VALUE.match(value):
                    continue
                if allowed(rule.name, value, line, allowlist):
                    continue
                found.append(Finding(rule, where, i, value))
    return found


class MissingPath(RuntimeError):
    pass


class EmptyDiff(RuntimeError):
    """Leerer Diff — nichts angesehen. Nicht als sauber werten."""
    pass


def iter_files(paths: list[str]):
    """Ein nicht existierender Pfad ist ein FEHLER, kein leeres Ergebnis.

    Sonst meldet ein Tippfehler im Pfad "nichts gefunden" mit Exit 0 — ein
    blinder Lauf, der wie ein sauberer aussieht. Belegt 24.08.2026 beim
    Erstlauf dieses Skripts, gefunden durch absichtliche Fehlbedienung;
    der grüne Selbsttest hat es nicht gesehen und konnte es nicht sehen.
    """
    for p in paths:
        path = Path(p)
        if path.is_file():
            yield path
        elif path.is_dir():
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in sorted(files):
                    yield Path(root) / name
        else:
            raise MissingPath(f"Pfad existiert nicht: {p}")


def read_textfile(path: Path) -> str | None:
    try:
        if path.suffix.lower() in SKIP_SUFFIX:
            return None
        if path.stat().st_size > MAX_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:8000]:
        return None
    return data.decode("utf-8", errors="replace")


def git_output(args: list[str]) -> str:
    res = subprocess.run(["git"] + args, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip() or "git-Aufruf fehlgeschlagen")
    return res.stdout


def added_lines(diff: str) -> str:
    """Nur hinzugefügte Zeilen — was ein Push wirklich neu veröffentlicht."""
    keep = []
    for ln in diff.splitlines():
        if ln.startswith("+") and not ln.startswith("+++"):
            keep.append(ln[1:])
        else:
            keep.append("")
    return "\n".join(keep)


# -------------------------------------------------------------- Kalibrierung

MUST_HIT = [
    ("anthropic_key", "ANTHROPIC_API_KEY=sk-ant-api03-AAAAAAAAAAAAAAAAAAAAAAAA"),  # leakcheck: allow
    ("github_token",  "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),  # leakcheck: allow
    ("aws_key_id",    "id = AKIAIOSFODNN7EXAMPLE"),  # leakcheck: allow
    ("private_key",   "-----BEGIN OPENSSH PRIVATE KEY-----"),  # leakcheck: allow
    ("jwt",           "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NX0.dBjftJeZ4CVPmB92"),  # leakcheck: allow
    ("secret_assignment", 'mqtt_password = "hunter2xyz"'),
    ("iban",          "DE89 3704 0044 0532 0130 00"),  # leakcheck: allow
    ("email",         "Bitte an d.mustermann@fremdefirma.com schicken"),  # leakcheck: allow
    ("mac_address",   "Client 00:11:22:33:44:55 im Netz"),  # leakcheck: allow
    ("geo_precise",   "Standort 50.1234567890123456, 8.6543210987654321"),  # leakcheck: allow
    ("home_path",     "liegt unter /Users/mustermann/Documents/x.md"),  # leakcheck: allow
    ("private_ipv4",  "Gateway ist 192.168.1.1"),
    ("phone_de",      "mobil +49 170 0000000"),  # leakcheck: allow
]

# (Text, Regeln die hier anschlagen DÜRFEN). Leer = gar nichts darf feuern.
# Die zweite Spalte ist nötig, weil `secret_word` bestimmungsgemäß auf jedes
# Vorkommen von "Passwort" anspringt — eine Erwartung "gar nichts" wäre dort
# schlicht falsch. Belegt 24.08.2026: der Selbsttest wurde ROT und hatte recht.
MUST_NOT_HIT: list[tuple[str, set[str]]] = [
    ("Copyright (c) 2026 Max Mustermann — MIT License", set()),
    ("Kontakt über user@example.com oder noreply@anthropic.com", set()),
    ("Public resolver 8.8.8.8 und 1.1.1.1 antworten", set()),
    ("Wir laufen auf Version 10.2.3 (vorher 9.8.1)", set()),
    ("Der Pfad /home/runner/work ist CI-Standard", set()),
    ("Das Wort Token kommt hier ohne Wert vor", set()),
    ("Siehe ~/Downloads und ./scripts/ für die Ablage", set()),
    ("curl http://localhost:11434/api/tags", set()),
    # Doku-Platzhalter: secret_assignment darf NICHT feuern.
    ("password: <dein-passwort-hier>", {"secret_word"}),
    ("api_key = ${API_KEY}", set()),
    ("token: CHANGEME", set()),
    ("secret = ****", set()),
    ("Das Passwort setzt man mit `--password`", {"secret_word"}),
    ("Passwort: beispielwert", {"secret_word"}),
    ("Zugangsdaten stehen im Passwortmanager", {"secret_word"}),
]


def selftest() -> int:
    sev = {"hoch", "mittel", "hinweis"}
    ok = True

    print("Kalibrierung — Fälle, die ANSCHLAGEN müssen:")
    for expect, sample in MUST_HIT:
        hits = {f.rule.name for f in scan_text(sample, "<selftest>", [], sev)}
        good = expect in hits
        ok &= good
        print(f"  [{'OK ' if good else 'ROT'}] {expect:<20}"
              f"{'' if good else '  -> nicht erkannt!'}")

    print("\nKalibrierung — Fälle, die SCHWEIGEN müssen:")
    for sample, tolerated in MUST_NOT_HIT:
        hits = {f.rule.name for f in scan_text(sample, "<selftest>", [], sev)}
        unexpected = sorted(hits - tolerated)
        good = not unexpected
        ok &= good
        label = sample[:44] + ("…" if len(sample) > 44 else "")
        print(f"  [{'OK ' if good else 'ROT'}] {label:<46}"
              f"{'' if good else '  -> Fehlalarm: ' + ','.join(unexpected)}")

    print("\n" + ("=> KALIBRIERT (beide Richtungen belegt)" if ok
                  else "=> ROT — dem Ergebnis dieses Skripts NICHT trauen"))
    return 0 if ok else 2


# ---------------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Vorfilter gegen versehentliche Veröffentlichung. "
                    "Maskiert Funde grundsätzlich.")
    ap.add_argument("paths", nargs="*",
                    help="Dateien oder Verzeichnisse; `-` liest aus stdin")
    ap.add_argument("--staged", action="store_true", help="git-Index prüfen")
    ap.add_argument("--diff", metavar="REF",
                    help="git-Diff-Bereich, z.B. origin/main..HEAD")
    ap.add_argument("--selftest", action="store_true",
                    help="Kalibrierung in beide Richtungen beweisen")
    ap.add_argument("--severity", default="mittel",
                    choices=["hoch", "mittel", "hinweis"],
                    help="Ab welcher Stufe melden (Vorgabe: mittel)")
    ap.add_argument("--show", action="store_true",
                    help="Funde UNMASKIERT ausgeben — bewußte Entscheidung")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    order = ["hoch", "mittel", "hinweis"]
    min_sev = set(order[: order.index(args.severity) + 1])

    try:
        root = Path(git_output(["rev-parse", "--show-toplevel"]).strip())
    except Exception:
        root = Path.cwd()
    allowlist = load_allowlist(root)

    if not (args.staged or args.diff or args.paths):
        ap.print_usage()
        return 2

    findings: list[Finding] = []
    scanned = 0        # tatsächlich gelesene Dateien
    skipped = 0        # binär, zu groß, unlesbar
    sources: list[str] = []
    try:
        # Ein LEERER Diff ist kein sauberer Diff. `--diff main..HEAD` liefert
        # 0 Byte, solange auf dem Branch nichts committet ist — und meldete
        # früher "nichts gefunden". Belegt 24.08.2026 am eigenen Erstlauf:
        # der Lauf sah aus wie ein Freibrief und hatte nichts angesehen.
        if args.staged:
            diff = git_output(["diff", "--cached"])
            if not diff.strip():
                raise EmptyDiff("git-Index ist leer — nichts zu prüfen.")
            findings += scan_text(added_lines(diff), "git-index",
                                  allowlist, min_sev)
            sources.append("git-index")
        if args.diff:
            diff = git_output(["diff", args.diff])
            if not diff.strip():
                raise EmptyDiff(
                    f"Diff-Bereich '{args.diff}' ist leer — nichts zu prüfen. "
                    "Stimmt der Bereich (schon committet)?")
            findings += scan_text(added_lines(diff), f"git-diff {args.diff}",
                                  allowlist, min_sev)
            sources.append(f"git-diff {args.diff}")
        file_paths = [p for p in args.paths if p != "-"]
        if "-" in args.paths:
            data = sys.stdin.read()
            if not data.strip():
                raise EmptyDiff("stdin ist leer — nichts zu prüfen.")
            findings += scan_text(data, "<stdin>", allowlist, min_sev)
            sources.append("stdin")
        for f in iter_files(file_paths):
            text = read_textfile(f)
            if text is None:
                skipped += 1
                continue
            scanned += 1
            findings += scan_text(text, str(f), allowlist, min_sev)
        if file_paths:
            sources.append(f"{scanned} Datei(en)")
    except EmptyDiff as exc:
        print(f"leak_check: {exc}", file=sys.stderr)
        print("leak_check: ABBRUCH — ein leerer Lauf ist kein Nullbefund.",
              file=sys.stderr)
        return 2
    except MissingPath as exc:
        print(f"leak_check: {exc}", file=sys.stderr)
        print("leak_check: ABBRUCH — kein Urteil über die übrigen Ziele.",
              file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"leak_check: {exc}", file=sys.stderr)
        return 2

    # Ein Lauf über null Dateien ist kein sauberer Lauf.
    if file_paths and scanned == 0:
        print(f"leak_check: 0 Dateien gelesen ({skipped} übersprungen: "
              f"binär/zu groß). NICHTS geprüft — das ist kein Nullbefund.",
              file=sys.stderr)
        return 2

    if not findings:
        print(f"leak_check: nichts gefunden. Geprüft: {', '.join(sources)}"
              + (f", {skipped} übersprungen" if skipped else "") + ".")
        print("  Hinweis: kein Fund ist kein Freibrief — geprüft wird nur, "
              "was das Regelwerk kennt.")
        return 0

    by_sev: dict[str, list[Finding]] = {}
    for f in findings:
        by_sev.setdefault(f.rule.severity, []).append(f)

    print(f"leak_check: {len(findings)} Fund(e) — PRÜFAUFTRAG, kein Urteil.\n")
    for sev in order:
        group = by_sev.get(sev)
        if not group:
            continue
        print(f"── {sev.upper()} ──")
        for f in group:
            shown = f.raw if args.show else mask(f.raw)
            print(f"  {f.where}:{f.line_no}  [{f.rule.name}]  {shown}")
            print(f"      {f.rule.hint}")
        print()
    if not args.show:
        print("Funde sind maskiert. Original ansehen: dieselbe Zeile in der "
              "Datei öffnen, oder --show (holt den Wert ins Protokoll).")
    print("Fehlalarm dauerhaft stummschalten: .leakcheckignore "
          "(`<regel> <regex>`) oder `# leakcheck: allow <regel>` in der Zeile.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
