---
name: ki-os-setup
description: KI OS Setup — Erstellt die Vault-Struktur, führt ein 4-Fragen-Onboarding durch und personalisiert alle Dateien. Verwende wenn der Nutzer /setup ausführt, "einrichten", "setup", "bootstrap" oder "initialisieren" sagt.
---

# KI OS — Setup + Onboarding

## Pre-flight Check

1. Prüfe, ob `vaults.json` und `.claude/skills/ki-os/SKILL.md` im aktuellen Verzeichnis
   existieren. Fehlt eines: "Dieses Verzeichnis ist kein KI-OS-Workspace. Wechsle in den
   entpackten Nukleus-Ordner und rufe `/setup` dort erneut auf." — dann STOP.
2. Prüfe, ob eine `.env` mit gesetztem `VAULT_PRIVAT` existiert und der Pfad ein Verzeichnis ist.
   Falls ja: "Es ist bereits ein Vault registriert (`<pfad>`). Onboarding erneut durchlaufen
   (bestehende Dateien bleiben) oder abbrechen?"
3. Sonst: weiter mit Phase A.

---

## Phase A: Onboarding (4 Fragen)

### Frage 0 — Wo soll dein Wissen leben?

"Dein KI-OS besteht aus zwei Hälften: diesem Workspace hier (die Mechanik) und einem Vault
(dein Wissen). Sie bleiben getrennt, damit du den Workspace aktualisieren kannst, ohne dein
Wissen anzufassen — und damit du dein Wissen in Obsidian öffnen kannst, ohne die Mechanik zu sehen.

Wo soll der Vault liegen? (Vorschlag: `~/ki-os-vault`)"

Antwort als `{{VAULT_PFAD}}` merken. Tilde expandieren. Existiert der Pfad bereits und ist
nicht leer: nachfragen, nicht überschreiben.

Lies `references/onboarding-questions.md` für die exakten Fragen und Anweisungen.

**Wichtig:**
- Stelle jede Frage einzeln. Warte auf die Antwort bevor du weitergehst.
- Akzeptiere jedes Format: kurzer Satz, Wall of Text, LinkedIn-Profil, "skip"
- Keine Nachfragen. Extrahiere was du kannst.
- Nach jeder Antwort: kurze Bestätigung (1 Satz), dann nächste Frage

Speichere die Antworten intern als:
- `{{VAULT_PFAD}}` — Zielverzeichnis des Vaults (aus Frage 0, Tilde bereits expandiert)
- `{{NAME}}` — Name des Nutzers
- `{{KURZBESCHREIBUNG}}` — Was er/sie macht, für wen
- `{{ANGEBOT}}` — Produkte/Dienstleistungen
- `{{ZIELGRUPPE}}` — Für wen
- `{{HERAUSFORDERUNG}}` — Größte aktuelle Herausforderung
- `{{PROJEKTE}}` — Liste aktiver Projekte (Name + Ziel)
- `{{DATUM}}` — Heutiges Datum (YYYY-MM-DD)
- `{{KW}}` — Aktuelle Kalenderwoche

---

## Phase B: Vault erstellen

Lies `references/vault-structure.md` für die vollständige Ordner- und Dateistruktur. Alle dort
genannten Pfade sind relativ zu `{{VAULT_PFAD}}/`.

### Schritt 0: Vault registrieren

1. Verzeichnis `{{VAULT_PFAD}}` anlegen.
2. `.env` im Workspace-Root schreiben (überschreibt eine vorhandene Zeile, legt sie sonst an):

   ```
   VAULT_PRIVAT={{VAULT_PFAD}}
   ```

3. Auflösung sofort verifizieren:

   ```bash
   python3 scripts/resolve_vault.py start
   ```

   Erwartet: der Pfad aus `{{VAULT_PFAD}}` auf stdout, exit 0. Schlägt es fehl, **hier stoppen**
   und den Fehler zeigen — ein nicht auflösbarer Vault macht jeden folgenden Schritt wertlos.

### Schritt 1: Ordner erstellen

Erstelle alle 10 nummerierten Ordner und Unterordner unter `{{VAULT_PFAD}}/` wie in
`vault-structure.md` definiert.

### Schritt 2: Folder-Guides schreiben

Lies jeden Guide aus `references/folder-guides/` und schreibe ihn als `_guide.md` in den entsprechenden Ordner:
- `references/folder-guides/00-inbox.md` → `{{VAULT_PFAD}}/00-inbox/_guide.md`
- `references/folder-guides/01-context.md` → `{{VAULT_PFAD}}/01-context/_guide.md`
- `references/folder-guides/02-brand.md` → `{{VAULT_PFAD}}/02-brand/_guide.md`
- `references/folder-guides/03-strategy.md` → `{{VAULT_PFAD}}/03-strategy/_guide.md`
- `references/folder-guides/04-projects.md` → `{{VAULT_PFAD}}/04-projects/_guide.md`
- `references/folder-guides/05-daily.md` → `{{VAULT_PFAD}}/05-daily/_guide.md`
- `references/folder-guides/06-team.md` → `{{VAULT_PFAD}}/06-team/_guide.md`
- `references/folder-guides/07-intelligence.md` → `{{VAULT_PFAD}}/07-intelligence/_guide.md`
- `references/folder-guides/08-resources.md` → `{{VAULT_PFAD}}/08-resources/_guide.md`
- `references/folder-guides/09-reference.md` → `{{VAULT_PFAD}}/09-reference/_guide.md`

### Schritt 3: Context-Dateien erstellen

Lies die Templates aus `references/context-templates/` und ersetze die Platzhalter mit den Onboarding-Antworten:

- `references/context-templates/ich.md` → `{{VAULT_PFAD}}/01-context/ich.md` (mit {{NAME}}, {{KURZBESCHREIBUNG}})
- `references/context-templates/business.md` → `{{VAULT_PFAD}}/01-context/business.md` (mit {{ANGEBOT}}, {{ZIELGRUPPE}}, {{HERAUSFORDERUNG}})
- `references/context-templates/strategie.md` → `{{VAULT_PFAD}}/03-strategy/current-priorities.md` (mit {{KW}}, {{DATUM}})
- `references/context-templates/open-loops.md` → `{{VAULT_PFAD}}/03-strategy/open-loops.md` (mit {{DATUM}})
- `references/context-templates/projekte.md` → `{{VAULT_PFAD}}/04-projects/README.md` (mit {{PROJEKTE}})

Erstelle zusätzlich für jedes genannte Projekt einen Unterordner mit `README.md`:
- `{{VAULT_PFAD}}/04-projects/{projektname-kebab}/README.md` mit Ziel und Status "Aktiv"
- Verlinke das Projekt mit `[[ich]]` und ggf. `[[business]]`

### Schritt 4: Weitere Seed-Dateien

- `{{VAULT_PFAD}}/00-inbox/capture.md` — Leere Inbox mit Header
- `{{VAULT_PFAD}}/02-brand/brand-voice.md` — Minimales Template (Ton, Stil, Regeln)
- `{{VAULT_PFAD}}/09-reference/weekly-log.md` — Leerer Weekly Log mit Tabellenheader
- `{{VAULT_PFAD}}/09-reference/completed-projects.md` — Leeres Archiv mit Header

### Schritt 5: CLAUDE.md schreiben — zwei Dateien, zwei Zwecke

**a) Workspace-Root — die operative Landkarte.**
Lies `references/claude-md-template.md`, ersetze alle Platzhalter und schreibe das Ergebnis
als `CLAUDE.md` in den **Workspace-Root** (nicht in den Vault). Claude Code lädt diese Datei
bei jedem Start automatisch — das ist der einzige Ort, an dem sie wirkt.

**b) Vault-Root — ein Wegweiser.**
Schreibe nach `{{VAULT_PFAD}}/CLAUDE.md`:

    # {{NAME}}s Vault

    > Dies ist ein **Wissens-Vault**, kein Workspace.
    > Die Mechanik (Skills, Commands) lebt im KI-OS-Workspace.
    > Starte Claude Code dort und rufe `/start` auf — nicht hier.
    >
    > In Obsidian öffnest du diesen Ordner als Vault.

### Schritt 6: Erster Daily Log

Erstelle `{{VAULT_PFAD}}/05-daily/{{DATUM}}.md`:
```markdown
# {{DATUM}}

> Siehe auch: [[ich]], [[current-priorities]]

## Setup
- KI OS eingerichtet
- Vault-Struktur erstellt
- Kontext personalisiert

## Nächste Schritte
[Basierend auf den genannten Projekten die wichtigsten 2-3 nächsten Schritte auflisten]
```

---

## Phase C: Abschluss

Zeige eine kompakte Zusammenfassung:

```
KI OS eingerichtet für [Name].

Workspace (Mechanik):  <workspace-pfad>
Vault (dein Wissen):   {{VAULT_PFAD}}

Erstellt:
- 10 Vault-Ordner mit Guides
- [X] Kontext-Dateien (ich, business, strategie, open-loops)
- [X] Projekt-Ordner ([Projektnamen])
- CLAUDE.md im Workspace, Wegweiser im Vault

Nächste Schritte:
1. Öffne den VAULT-Ordner in Obsidian als Vault
2. Starte Claude Code im WORKSPACE-Ordner
3. Jede Session mit /start beginnen, mit /shutdown beenden

Alle Commands: /start | /capture | /plan | /review | /shutdown
```

---

## Regeln

- Nie den Nutzer fragen "Soll ich das speichern?" — einfach machen
- Alle Dateien auf Deutsch, technische Begriffe (kebab-case, wiki-links) auf Englisch
- Wiki-Links ([[dateiname]]) in JEDER erstellten Datei
- Dateinamen: kebab-case, keine Emojis, keine Umlaute
- Keine leeren Placeholder-Dateien — jede Datei hat mindestens einen sinnvollen Header
