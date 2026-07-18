# Vault-Struktur

## Ordner erstellen

```bash
mkdir -p 00-inbox
mkdir -p 01-context
mkdir -p 02-brand
mkdir -p 03-strategy
mkdir -p 04-projects
mkdir -p 05-daily
mkdir -p 06-team
mkdir -p 07-intelligence/decisions
mkdir -p 07-intelligence/meetings
mkdir -p 08-resources/prompts
mkdir -p 08-resources/frameworks
mkdir -p 09-reference
```

## Dateien die erstellt werden

| Datei | Quelle | Platzhalter |
|---|---|---|
| `00-inbox/capture.md` | Inline (leerer Header) | — |
| `00-inbox/_guide.md` | `folder-guides/00-inbox.md` | — |
| `01-context/ich.md` | `context-templates/ich.md` | NAME, KURZBESCHREIBUNG |
| `01-context/business.md` | `context-templates/business.md` | ANGEBOT, ZIELGRUPPE, HERAUSFORDERUNG |
| `01-context/_guide.md` | `folder-guides/01-context.md` | — |
| `02-brand/brand-voice.md` | Inline (minimales Template) | — |
| `02-brand/_guide.md` | `folder-guides/02-brand.md` | — |
| `03-strategy/current-priorities.md` | `context-templates/strategie.md` | KW, DATUM |
| `03-strategy/open-loops.md` | `context-templates/open-loops.md` | DATUM |
| `03-strategy/_guide.md` | `folder-guides/03-strategy.md` | — |
| `04-projects/README.md` | `context-templates/projekte.md` | PROJEKTE |
| `04-projects/{name}/README.md` | Inline (pro Projekt) | Projektname, Ziel |
| `04-projects/_guide.md` | `folder-guides/04-projects.md` | — |
| `05-daily/{{DATUM}}.md` | Inline (erster Daily Log) | DATUM |
| `05-daily/_guide.md` | `folder-guides/05-daily.md` | — |
| `06-team/_guide.md` | `folder-guides/06-team.md` | — |
| `07-intelligence/_guide.md` | `folder-guides/07-intelligence.md` | — |
| `08-resources/_guide.md` | `folder-guides/08-resources.md` | — |
| `09-reference/weekly-log.md` | Inline (leerer Log) | — |
| `09-reference/completed-projects.md` | Inline (leeres Archiv) | — |
| `09-reference/_guide.md` | `folder-guides/09-reference.md` | — |
| `CLAUDE.md` | `claude-md-template.md` | NAME, KURZBESCHREIBUNG, PROJEKTE |
