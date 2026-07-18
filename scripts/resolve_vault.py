#!/usr/bin/env python3
"""Zustandsloser Registry-Resolver: Route/Slug -> absoluter Vault-Pfad.

Liest vaults.json + .env relativ zum Workspace-Root (parent des scripts/-Ordners).
Jeder Command loest SEINEN Vault deterministisch auf; kein Laufzeit-State
(die Bash-Shell haelt zwischen Aufrufen ohnehin keinen exportierten State).

Usage:
  resolve_vault.py <route> [--vault <slug>]
    <route>        Routing-Key aus vaults.json (z.B. start, capture)
    --vault <slug> Override: nutzt vaults[slug].path direkt, ignoriert Routing

stdout: absoluter aufgeloester Vault-Pfad; exit 0
stderr + exit 1 bei: unbekannter Route/Slug, fehlender Env-Var, nicht existierendem Pfad
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
VAR = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")


def _strip_env_value(raw: str) -> str:
    """Entfernt umschließende Anführungszeichen und nachgestellte Kommentare.

    Konvention wie in verbreiteten .env-Parsern: ein Wert, der komplett in
    einfache oder doppelte Anführungszeichen gefasst ist, wird wörtlich
    übernommen — ein '#' darin ist Teil des Werts, kein Kommentar-Start.
    Ein unquotierter Wert endet am ersten ' #' (Leerzeichen + Raute).
    """
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] in "\"'":
        quote = raw[0]
        end = raw.find(quote, 1)
        if end != -1:
            return raw[1:end]
    idx = raw.find(" #")
    if idx != -1:
        raw = raw[:idx]
    return raw.strip()


def _load_env(env_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = _strip_env_value(val)
    return env


def _expand(value: str, env: dict[str, str]) -> str:
    def repl(m: "re.Match[str]") -> str:
        name = m.group(1)
        if name in env:
            return env[name]
        if name in os.environ:
            return os.environ[name]
        raise KeyError(f"Env-Variable ${{{name}}} nicht gesetzt (weder in .env noch os.environ)")
    return VAR.sub(repl, value)


def resolve(route: "str | None", override_slug: "str | None",
            registry: dict, env: dict[str, str]) -> Path:
    vaults = registry["vaults"]
    routing = registry.get("routing", {})
    if override_slug is not None:
        slug = override_slug
    else:
        if route not in routing:
            raise KeyError(f"Unbekannte Route '{route}' — vorhanden: {sorted(routing)}")
        slug = routing[route]
    if slug not in vaults:
        raise KeyError(f"Unbekannter Vault-Slug '{slug}' — vorhanden: {sorted(vaults)}")
    raw = vaults[slug]["path"]
    path = Path(_expand(raw, env)).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f"Vault-Pfad existiert nicht: {path}")
    return path


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Registry-Resolver")
    ap.add_argument("route", nargs="?", default=None)
    ap.add_argument("--vault", dest="override", default=None)
    args = ap.parse_args(argv[1:])
    try:
        registry = json.loads((WORKSPACE / "vaults.json").read_text(encoding="utf-8"))
        env = _load_env(WORKSPACE / ".env")
        path = resolve(args.route, args.override, registry, env)
    except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"resolve_vault: {e}", file=sys.stderr)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
