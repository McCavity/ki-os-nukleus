---
name: ki-os
description: KI OS — täglicher Arbeitspartner. Routet nach Sub-Befehl. "start" → Session starten mit Kontext und Status. "capture" → Schnelle Erfassung. "plan" → Projekt planen. "review" → Wöchentliches Review. "shutdown" → Session beenden mit Daily Log. Trigger wenn /start, /capture, /plan, /review oder /shutdown aufgerufen wird.
---

# KI OS — Täglicher Betrieb

## Pre-flight Check

1. Vault auflösen wie in der Preamble unten beschrieben. Scheitert die Auflösung: "Es ist noch kein Vault eingerichtet. Führe zuerst `/setup` aus." — dann **STOP**.
2. Prüfe, ob `$KIOS_VAULT/01-context/ich.md` existiert. Fehlt sie: "Dein Vault ist noch nicht befüllt. Führe zuerst `/setup` aus." — dann **STOP**.
3. Sonst: Weiter mit Routing.

## Routing

Erkenne den Sub-Befehl aus `$ARGUMENTS` oder der Nutzer-Nachricht:

| Nutzer sagt... | Sub-Befehl |
|---|---|
| "start", "prime", "los", "starte session", "guten morgen" | → [Start](#start) |
| "capture", "festhalten", "notiz", "merken" | → [Capture](#capture) |
| "plan", "planen", "strukturieren" | → [Plan](#plan) |
| "review", "rückblick", "wochenreview" | → [Review](#review) |
| "shutdown", "ende", "fertig", "session beenden" | → [Shutdown](#shutdown) |

Falls unklar: Diese Tabelle zeigen und fragen was gebraucht wird.

---

## Vault-Auflösung (Preamble — vor jedem Sub-Befehl ausführen)

Launch erfolgt aus dem `ki-os`-Workspace (hier liegt `.claude/`); der Wissens-Vault ist **externe Daten**. Jeder Sub-Befehl löst seinen Vault deterministisch über die Registry auf — kein Laufzeit-State.

1. **Override prüfen:** Enthält `$ARGUMENTS` ein `--vault <slug>`, den Slug an den Resolver durchreichen.
2. **Vault auflösen** (aus dem Workspace-Root):
   `KIOS_VAULT=$(python3 scripts/resolve_vault.py <sub-befehl> [--vault <slug>])`
   `<sub-befehl>` ist der Name des gerade laufenden Sub-Befehls (`start`, `capture`, `plan`,
   `review` oder `shutdown`) — jeder Sub-Befehl übergibt seine eigene Route; `vaults.json`
   kennt für alle fünf einen Eintrag, aktuell alle auf den Vault-Slug `privat` gemappt.
   Dieser absolute Pfad ist ab jetzt **`$KIOS_VAULT`**. **ALLE** Vault-Datei-Zugriffe der Sub-Befehle laufen über `$KIOS_VAULT/…` (Read/Glob/Write mit dem aufgelösten Pfad).
3. **Fehlerfall:** Scheitert die Auflösung (Pfad fehlt, Slug unbekannt → Resolver exit 1), **STOP** mit klarer Meldung. **Kein Fallback auf CWD** — sonst schreibt ein Command still in den Workspace statt in den Vault.

---

## Start

Session starten. Kontext laden, Status zeigen.

### Schritte

1. Lies die operative `CLAUDE.md` (Workspace-Root, ist bereits geladen — bestätigen)
2. **Systemzeit abrufen:** `date "+%A %d.%m.%Y %H:%M"` — Wochentag, Datum und Uhrzeit für das Dashboard und zeitabhängige Entscheidungen verwenden
3. Lies `$KIOS_VAULT/01-context/ich.md` und `$KIOS_VAULT/01-context/business.md`
4. Lies `$KIOS_VAULT/03-strategy/current-priorities.md`
5. Lies `$KIOS_VAULT/03-strategy/open-loops.md`
6. Lies `$KIOS_VAULT/00-inbox/capture.md`
7. Lies die letzten 2 Daily Logs aus `$KIOS_VAULT/05-daily/` (nach Dateiname sortiert, neueste zuerst)
8. Zeige kompaktes Dashboard (max 20 Zeilen):

```
## KI OS — [Wochentag], [Datum], [Uhrzeit]

**Top 3 heute:**
1. [höchste Priorität aus current-priorities]
2. [...]
3. [...]

**Open Loops:** [X] aktive Loops, davon [Y] älter als 2 Wochen
**Inbox:** [X] Items

Bereit. Was steht an?
```

### Regeln
- NIE zusammenfassen wer der Nutzer ist
- Nur Status und Handlungsempfehlungen zeigen
- Falls Loops älter als 2 Wochen: explizit warnen
- Falls Inbox voll: erwähnen

---

## Capture

Schnelle Erfassung von Gedanken, Aufgaben, Loops.

Lies `references/capture-routing.md` für die Kategorisierungs-Logik.

### Schritte

1. Falls kein Inhalt mitgegeben: Frage "Was willst du festhalten?"
2. Kategorisiere automatisch:
   - **TASK** → `$KIOS_VAULT/03-strategy/current-priorities.md` (unter passende Sektion: Business (Top 3) / Persönlich / Side Quests)
   - **IDEE** → `$KIOS_VAULT/00-inbox/capture.md` (append)
   - **LOOP (aktiv)** → `$KIOS_VAULT/03-strategy/open-loops.md` (Sektion "Wartend auf")
   - **ENTSCHEIDUNG** → `$KIOS_VAULT/03-strategy/open-loops.md` (Sektion "Offene Entscheidungen")
3. Bestätigung: "Gespeichert in [[dateiname]] als [Kategorie]. Noch was?"
4. Loop bis Nutzer fertig ist

### Regeln
- Im Zweifel: als IDEE in Inbox — wird beim Review sortiert
- Relative Daten in absolute umwandeln ("Donnerstag" → konkretes Datum)
- Wiki-Links setzen wenn Projekte oder Personen erwähnt werden

---

## Plan

Implementierungsplan für ein Projekt erstellen.

### Schritte

1. Frage: "Welches Projekt? Was ist das Ziel?"
2. Falls Projekt in `$KIOS_VAULT/04-projects/` existiert: README.md lesen für Kontext
3. Falls neues Projekt: Ordner unter `$KIOS_VAULT/04-projects/` anlegen mit README.md
4. Plan schreiben in `$KIOS_VAULT/04-projects/{name}/plan-{{DATUM}}.md`:

```markdown
# Plan: [Titel]

> Erstellt: {{DATUM}}
> Projekt: [[projektname]]
> Status: Offen

## Ziel
[Was soll erreicht werden]

## Kontext
[Aktuelle Situation, relevante Infos]

## Schritte
1. [Schritt 1]
2. [Schritt 2]
3. [...]

## Risiken
- [Was könnte schiefgehen]

## Erfolgskriterien
- [ ] [Woran erkennt man daß es fertig ist]
```

5. Bestätigung: "Plan erstellt in [[projektname]]. [X] Schritte. Soll ich anfangen?"

---

## Review

Wöchentliches Review — am besten Sonntag oder Montag.

Lies `references/review-protocol.md` für den vollständigen Ablauf.

### Schritte

1. **Inbox leeren** — Lies `$KIOS_VAULT/00-inbox/capture.md`. Für jedes Item fragen: Machen, Planen, oder Löschen?
2. **Open Loops prüfen** — Lies `$KIOS_VAULT/03-strategy/open-loops.md`. Loops älter als 2 Wochen: Eskalieren oder schließen? (Voller Ablauf: `references/review-protocol.md`.)
3. **Projekte updaten** — Frage: "Was hat sich bei deinen Projekten bewegt?" Status in den READMEs aktualisieren. Erledigtes → `$KIOS_VAULT/09-reference/completed-projects.md`
4. **Reflexion** — 3 Fragen:
   - Was lief gut diese Woche?
   - Was war schwierig?
   - Was nimmst du mit (Key Learning)?
5. **Weekly Log** — 1-3 Zeilen in `$KIOS_VAULT/09-reference/weekly-log.md` schreiben (max 8 Einträge, älteste löschen)
6. **Nächste Woche planen** — Top 3 Business + Top 1 Persönlich in `$KIOS_VAULT/03-strategy/current-priorities.md` unter neuer KW eintragen

### Regeln
- Jeden Schritt mit dem Nutzer durchgehen — nicht alles auf einmal
- Geduldig sein — Review braucht Zeit
- Am Ende: "Review fertig. Guter Start in die Woche!"

---

## Shutdown

Session beenden. Status sichern.

### Schritte

1. Frage: "Was hat sich bewegt? Neue Aufgaben oder Blocker?"
2. `$KIOS_VAULT/03-strategy/current-priorities.md` aktualisieren — erst `Read`en.
3. Frage: "Offene Gedanken oder Loops?"
4. `$KIOS_VAULT/03-strategy/open-loops.md` aktualisieren falls nötig — erst `Read`en.
5. Daily Log schreiben/ergänzen in `$KIOS_VAULT/05-daily/{{DATUM}}.md`
   (Vorlage siehe unten; existiert die Datei bereits, wird nur angehängt — append-only):

```markdown
# {{DATUM}}

> Siehe auch: [[ich]], [[current-priorities]]

## Session
- [Was passiert ist — Stichpunkte]
- [Entscheidungen]
- [Was erstellt/geändert wurde]

## Nächste Session
- [Was als nächstes ansteht]
```

6. **Vault sichern, falls er ein Git-Repo ist:**
   - `git -C "$KIOS_VAULT" rev-parse --git-dir` schlägt fehl → Schritt überspringen,
     einmal erwähnen: "Dein Vault ist kein Git-Repo — Versionierung lohnt sich."
   - Sonst: `git -C "$KIOS_VAULT" status` zeigen, dann
     `git -C "$KIOS_VAULT" add -A && git -C "$KIOS_VAULT" commit -m "…"`.
   - Push nur, wenn ein Remote konfiguriert ist.
7. Zeige: "Session gesichert. Bis zum nächsten Mal!"

---

## Allgemeine Regeln

- **Engine vs. Vault (Pflicht):** Launch aus dem `ki-os`-Workspace. **Alle Wissens-/Vault-Pfade** — hier UND in den `references/…`-Protokollen (`00–09`, Projekte, Loops) — sind relativ zu **`$KIOS_VAULT`** (Preamble aufgelöst). **Engine-interne Pfade** (`.claude/…`, `references/…`, `scripts/…`, die operative `CLAUDE.md`) sind **Workspace-relativ**. Steht in einer Referenz ein bloßer Vault-Pfad wie `03-strategy/…`, ist `$KIOS_VAULT/` davorzusetzen.
- **Read vor Edit (Pflicht):** Die großen Vault-Dateien (`03-strategy/current-priorities.md`, `03-strategy/open-loops.md`, Vault-`CLAUDE.md`) **immer erst frisch `Read`en, bevor du editierst** — auch bei vermeintlichen Ein-Zeilen-Änderungen. Ein Edit ohne vorheriges Read bricht mit „File has not been read yet" ab.
- **Wiki-Links überall:** Jede Referenz auf eine Vault-Datei, Person oder Projekt → `[[wikilink]]`
- **Nie fragen "Soll ich speichern?"** — Einfach machen und berichten
- **Deutsch:** Alle Ausgaben auf Deutsch, technische Begriffe dürfen Englisch bleiben
- **Kurz:** Wenn 1 Satz reicht, keinen Absatz schreiben
- **Timestamps:** Nach jedem File-Update: `> Letzte Aktualisierung: YYYY-MM-DD`
- **Dateinamen:** kebab-case, keine Emojis, keine Umlaute
