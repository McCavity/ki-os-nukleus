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

## Schnellstart

```bash
git clone https://github.com/McCavity/ki-os-nukleus.git
cd ki-os-nukleus
claude
```

Dann im Chat: `/setup` — der Rest läuft geführt. Du beantwortest ein paar Fragen (wo dein
Vault liegen soll, wer du bist, woran du arbeitest), und `/setup` legt Vault-Struktur,
Kontext-Dateien und deine persönliche `CLAUDE.md` an.

> **Hinweis zur `CLAUDE.md`:** Dieses Repo liefert nur `CLAUDE.md.template` aus — eine
> generische Fassung ohne Personenbezug. `/setup` erzeugt daraus deine persönliche,
> operative `CLAUDE.md` im Workspace-Root. Diese Datei ist bewußt **nicht versioniert**
> (siehe `.gitignore`): Sie enthält deinen Namen und deine Beschreibung, und der Workspace
> ist genau das Verzeichnis, das du geklont hast — eine getrackte, personalisierte
> `CLAUDE.md` würde bei einem eigenen `git add -A` deine Daten in dein Repo committen.

## Die fünf Befehle

| Command | Wann nutzen |
|---|---|
| `/setup` | Einmalig: Vault anlegen und einrichten |
| `/start` | Jede neue Session starten |
| `/capture` | Schnell etwas festhalten |
| `/plan` | Projekt planen |
| `/review` | Wöchentliches Review |
| `/shutdown` | Session beenden |

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
