# ki-os-nukleus

Ein Start-Kit für dein persönliches KI-Betriebssystem auf Basis von Claude Code. Es besteht
aus zwei getrennten Teilen: dem **Workspace** (Skills, Commands, Vault-Registry — dieser
Ordner hier) und deinem **Vault** (dein Wissen als Markdown, in Obsidian zu öffnen). `/setup`
richtet beides in wenigen Minuten geführt ein.

## Warum getrennt?

Der Workspace ist die Mechanik: Du kannst ihn aktualisieren, ohne dein Wissen anzufassen.
Der Vault ist reines Wissen: Du öffnest ihn in Obsidian, ohne je die Mechanik dahinter zu
sehen. Beide leben in unterschiedlichen Verzeichnissen und werden unabhängig voneinander
versioniert.

## Voraussetzungen

- [Claude Code](https://claude.com/product/claude-code) installiert
- Python 3 im PATH (für die Vault-Auflösung)
- Optional: [Obsidian](https://obsidian.md) — zum Öffnen deines Vaults
- Optional: Git — zum Versionieren deines Vaults
- Optional: [uv](https://docs.astral.sh/uv/) — zum Ausführen der Resolver-Testsuite (siehe unten)

## Schnellstart

```bash
git clone https://github.com/McCavity/ki-os-nukleus.git
cd ki-os-nukleus
claude
```

Dann im Chat: `/setup` — der Rest läuft geführt. Du beantwortest ein paar Fragen (wo dein
Vault liegen soll, wer du bist, woran du arbeitest), und `/setup` legt Vault-Struktur,
Kontext-Dateien und deine persönliche `CLAUDE.md` an.

> **Hinweis zur `CLAUDE.md`:** Dieses Repo liefert im Workspace-Root **keine** `CLAUDE.md`
> aus. `/setup` erzeugt deine persönliche, operative `CLAUDE.md` aus einer Skill-internen
> Vorlage (`.claude/skills/ki-os-setup/references/claude-md-template.md`) und schreibt das
> Ergebnis in den Workspace-Root. Diese Datei ist bewußt **nicht versioniert** (siehe
> `.gitignore`): Sie enthält deinen Namen und deine Beschreibung, und der Workspace ist genau
> das Verzeichnis, das du geklont hast — eine getrackte, personalisierte `CLAUDE.md` würde bei
> einem eigenen `git add -A` deine Daten in dein Repo committen.

## Die sechs Befehle

| Command | Wann nutzen |
|---|---|
| `/setup` | Einmalig: Vault anlegen und einrichten |
| `/start` | Jede neue Session starten |
| `/capture` | Schnell etwas festhalten |
| `/plan` | Projekt planen |
| `/review` | Wöchentliches Review |
| `/shutdown` | Session beenden |

## Vor dem Veröffentlichen: `leak_check.py`

Ein KI-OS schreibt laufend Dateien, und ein Agent übernimmt dabei gern Pfade, Hostnamen
oder Zugangsdaten aus dem Kontext. `scripts/leak_check.py` ist ein Vorfilter dagegen —
vor jedem Commit oder Push eines Repos, das andere sehen können:

```bash
python3 scripts/leak_check.py --staged                 # was der nächste Commit enthält
python3 scripts/leak_check.py --diff origin/main..HEAD # was ein Push veröffentlichen würde
python3 scripts/leak_check.py --selftest               # Kalibrierung beweisen
```

- **Funde werden maskiert.** Das Werkzeug holt den Fund nicht ins Sitzungsprotokoll; erst
  `--show` gibt ihn frei, und das ist eine bewußte Entscheidung.
- **Exit 0** heißt „nichts gefunden", **Exit 1** „Funde ansehen", **Exit 2** „nichts
  geprüft" (leerer Diff, falscher Pfad) — Exit 2 ist **nie** ein sauberer Lauf.
- Ein Treffer ist ein Prüfauftrag, kein Urteil. Fehlalarme am Fundort mit
  `# leakcheck: allow <regel>` stummschalten, nur im Ausnahmefall über `.leakcheckignore`.
- Kein Fund ist kein Freibrief: geprüft wird nur, was das Regelwerk kennt.

Dazu zeigt ein Hook in `.claude/settings.json` vor jedem `git commit`, das Claude ausführt,
`git diff --stat` und `git status` an. Er braucht [`jq`](https://jqlang.org) im PATH.

## Testsuite

`scripts/resolve_vault.py` und `scripts/leak_check.py` bringen je eine pytest-Suite mit
(`scripts/test_*.py`). Läuft ohne lokale Installation über `uv`:

```bash
uv run --no-project --with pytest -- python -m pytest scripts/ -q
```

## Wie es weitergeht

- **Eigene Skills:** Lege weitere Skills unter `.claude/skills/` an, wie `ki-os` und
  `ki-os-setup` es vormachen.
- **Eigene Ordner:** Die zehn nummerierten Vault-Ordner (`00-inbox` bis `09-reference`) sind
  ein Vorschlag, kein Zwang — erweitere sie, wie dein Wissen wächst.
- **Versionierung des Vaults:** Dein Vault ist ein eigenständiges Verzeichnis außerhalb
  dieses Repos. Initialisiere dort bei Bedarf ein eigenes Git-Repo — `/shutdown` committet
  automatisch, sobald es eines erkennt.

## Lizenz

MIT — siehe [LICENSE](LICENSE).
