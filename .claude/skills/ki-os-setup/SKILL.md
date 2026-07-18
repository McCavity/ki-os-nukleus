---
name: ki-os-setup
description: KI OS Setup — Erstellt die Vault-Struktur, führt ein 4-Fragen-Onboarding durch und personalisiert alle Dateien. Verwende wenn der Nutzer /setup ausführt, "einrichten", "setup", "bootstrap" oder "initialisieren" sagt.
---

# KI OS — Setup + Onboarding

## Pre-flight Check

1. Prüfe, ob `vaults.json` und `.claude/skills/ki-os/SKILL.md` im aktuellen Verzeichnis
   existieren. Fehlt eines: "Dieses Verzeichnis ist kein KI-OS-Workspace. Wechsle in den
   geklonten Nukleus-Ordner und rufe `/setup` dort erneut auf." — dann STOP.
2. Prüfe, ob eine `.env` mit gesetztem `VAULT_PRIVAT` existiert und der Pfad ein Verzeichnis ist.
   Falls ja: "Es ist bereits ein Vault registriert (`<pfad>`). Onboarding erneut durchlaufen
   (Phase B überschreibt keine vorhandene Datei — nur fehlende werden ergänzt) oder abbrechen?"
3. Sonst: weiter mit Phase A.

---

## Phase A: Onboarding (4 Fragen)

Lies `references/onboarding-questions.md` für die exakten Fragen (Frage 0 bis 3) und
Anweisungen — dort stehen alle vier an einem Ort, in der Reihenfolge, in der sie gestellt
werden.

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

> **Grundregel für ganz Phase B — gilt für jeden Schritt, der eine Datei schreibt (0, 2, 3, 4,
> 5, 6): keine vorhandene Datei wird überschrieben.** Vor jedem Schreiben prüfen, ob die
> Zieldatei bereits existiert. Existiert sie: **überspringen**, nichts schreiben, den
> Vault-relativen Pfad zu einer Liste „übersprungen" hinzufügen (für Phase C). Existiert sie
> nicht: schreiben wie beschrieben. Das gilt unverändert bei einem wiederholten `/setup`-Lauf
> nach einem Abbruch oder bewußten erneuten Onboarding — nur fehlende Dateien werden ergänzt,
> nichts Bestehendes geht verloren.

### Schritt 0: Vault registrieren

1. **Sicherheitsprüfung wiederholen:** Löse `{{VAULT_PFAD}}` erneut zu einem absoluten,
   aufgelösten Pfad auf (Tilde, relative Angaben, Symlinks). Liegt er innerhalb des
   Workspace-Root oder ist mit ihm identisch: **hier stoppen**, nichts anlegen — dieselbe
   Begründung wie bei Frage 0 zeigen und zurück zu Frage 0 springen. (Zweite Prüfung als
   Sicherheitsnetz, falls Frage 0 übersprungen wurde oder sich der Pfad danach änderte.)
2. Verzeichnis `{{VAULT_PFAD}}` anlegen — existiert es bereits (siehe Frage 0), unverändert
   lassen, nur fehlende Unterordner werden in Schritt 1 ergänzt.
3. `.env` im Workspace-Root schreiben (überschreibt eine vorhandene Zeile, legt sie sonst an):

   ```
   VAULT_PRIVAT={{VAULT_PFAD}}
   ```

   (Die `.env`-Zeile selbst fällt nicht unter die Grundregel oben — sie ist Registry-Zustand
   des Workspace, keine Vault-Wissensdatei, und muß bei jedem Lauf auf den aktuellen Pfad
   zeigen.)

4. Auflösung sofort verifizieren:

   ```bash
   python3 scripts/resolve_vault.py start
   ```

   Erwartet: der Pfad aus `{{VAULT_PFAD}}` auf stdout, exit 0. Schlägt es fehl, **hier stoppen**
   und den Fehler zeigen — ein nicht auflösbarer Vault macht jeden folgenden Schritt wertlos.

### Schritt 1: Ordner erstellen

Erstelle alle 10 nummerierten Ordner und Unterordner unter `{{VAULT_PFAD}}/` wie in
`vault-structure.md` definiert (`mkdir -p` — legt nur fehlende Ordner an, rührt bestehende
Inhalte nicht an).

### Schritt 2: Folder-Guides schreiben

Lies jeden Guide aus `references/folder-guides/` und schreibe ihn als `_guide.md` in den
entsprechenden Ordner — **pro Datei einzeln die Grundregel anwenden:** existiert die
`_guide.md` schon, überspringen und zur Liste „übersprungen" hinzufügen; sonst schreiben.
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

Lies die Templates aus `references/context-templates/` und ersetze die Platzhalter mit den
Onboarding-Antworten. **Für jede der folgenden Zieldateien einzeln die Grundregel anwenden:**
existiert sie bereits, überspringen und zur Liste „übersprungen" hinzufügen; sonst schreiben.
Eine bereits vorhandene Datei blockiert die anderen nicht — jede wird für sich geprüft.

- `references/context-templates/ich.md` → `{{VAULT_PFAD}}/01-context/ich.md` (mit {{NAME}}, {{KURZBESCHREIBUNG}})
- `references/context-templates/business.md` → `{{VAULT_PFAD}}/01-context/business.md` (mit {{ANGEBOT}}, {{ZIELGRUPPE}}, {{HERAUSFORDERUNG}})
- `references/context-templates/strategie.md` → `{{VAULT_PFAD}}/03-strategy/current-priorities.md` (mit {{KW}}, {{DATUM}}, siehe „Erste Prioritäten ableiten" unten)
- `references/context-templates/open-loops.md` → `{{VAULT_PFAD}}/03-strategy/open-loops.md` (mit {{DATUM}})
- `references/context-templates/projekte.md` → `{{VAULT_PFAD}}/04-projects/README.md` (mit {{PROJEKTE}}; Spalte „Nächster Schritt" siehe „Erste Prioritäten ableiten" unten)

**Erste Prioritäten ableiten (statt Platzhalter stehenlassen) — nur relevant, wenn
`current-priorities.md` bzw. `04-projects/README.md` laut Grundregel tatsächlich geschrieben
werden (nicht übersprungen):**
- Für jedes in Frage 3 genannte Projekt einen konkreten ersten Schritt als Priorität
  eintragen, abgeleitet aus dem genannten Ziel — keine Platzhalter (`[Priorität N]`)
  stehenlassen.
- Nennt der Nutzer mehr als drei Projekte: die drei wichtigsten für „Business (Top 3)"
  wählen und das in der Abschluß-Zusammenfassung (Phase C) erwähnen.
- Nennt er gar keine Projekte: einen ehrlichen Startpunkt eintragen (z.B. „Vault einrichten
  und erste Woche planen") statt eines Platzhalters.

Derselbe abgeleitete erste Schritt füllt auch die Spalte „Nächster Schritt" des jeweiligen
Projekts in `04-projects/README.md` — eine Ableitung, zwei Stellen.

Erstelle zusätzlich für jedes genannte Projekt einen Unterordner mit `README.md`
(`{{VAULT_PFAD}}/04-projects/{projektname-kebab}/README.md`, mit Ziel und Status "Aktiv",
verlinkt mit `[[ich]]` und ggf. `[[business]]`) — **auch hier pro Projekt einzeln die
Grundregel anwenden:** existiert die `README.md` des Projekts schon, überspringen; sonst
schreiben.

### Schritt 4: Weitere Seed-Dateien

Schreibe die folgenden vier Dateien (Platzhalter ersetzen, sonst wortgleich) — **pro Datei
einzeln die Grundregel anwenden:** existiert eine der vier schon, diese eine überspringen und
zur Liste „übersprungen" hinzufügen, mit den übrigen drei normal fortfahren.

`{{VAULT_PFAD}}/00-inbox/capture.md`:
```markdown
# Capture

> Letzte Aktualisierung: {{DATUM}}
> Siehe auch: [[current-priorities]]

Quick Capture — landet hier bis zum nächsten `/review`.
```

`{{VAULT_PFAD}}/02-brand/brand-voice.md`:
```markdown
# Brand Voice

> Letzte Aktualisierung: {{DATUM}}
> Siehe auch: [[ich]]

## Ton

<!-- Wie klingst du? Locker, sachlich, humorvoll... -->

## Stil

<!-- Kurze Sätze? Lange Ausführungen? Aktiv/Passiv? -->

## Regeln

<!-- Was vermeiden? Lieblingsformulierungen? -->
```

`{{VAULT_PFAD}}/09-reference/weekly-log.md`:
```markdown
# Weekly Log

> Letzte Aktualisierung: {{DATUM}}
> Siehe auch: [[current-priorities]]
> Rolling Log — max. 8 Einträge, ältester wird beim `/review` gelöscht.

| KW | Datumsbereich | Zusammenfassung |
|---|---|---|
```

`{{VAULT_PFAD}}/09-reference/completed-projects.md`:
```markdown
# Abgeschlossene Projekte

> Letzte Aktualisierung: {{DATUM}}
> Siehe auch: [[current-priorities]]

| Projekt | Abgeschlossen |
|---|---|
```

### Schritt 5: CLAUDE.md schreiben — zwei Dateien, zwei Zwecke

Für beide gilt die Grundregel unverändert: existiert die Zieldatei schon, überspringen und zur
Liste „übersprungen" hinzufügen; sonst schreiben. Die beiden Dateien sind unabhängig
voneinander — die eine kann übersprungen werden, während die andere geschrieben wird.

**a) Workspace-Root — die operative Landkarte.**
Existiert bereits eine `CLAUDE.md` im Workspace-Root: überspringen (sie enthält ggf. bereits
gewachsenen, personalisierten Inhalt aus einer vorherigen Session — siehe Grundregel). Sonst:
Lies `references/claude-md-template.md`, ersetze alle Platzhalter und schreibe das Ergebnis
als `CLAUDE.md` in den **Workspace-Root** (nicht in den Vault). Claude Code lädt diese Datei
bei jedem Start automatisch — das ist der einzige Ort, an dem sie wirkt.

**b) Vault-Root — ein Wegweiser.**
Existiert `{{VAULT_PFAD}}/CLAUDE.md` bereits: überspringen. Sonst schreibe nach
`{{VAULT_PFAD}}/CLAUDE.md`:

    # {{NAME}}s Vault

    > Dies ist ein **Wissens-Vault**, kein Workspace.
    > Die Mechanik (Skills, Commands) lebt im KI-OS-Workspace.
    > Starte Claude Code dort und rufe `/start` auf — nicht hier.
    >
    > In Obsidian öffnest du diesen Ordner als Vault.

### Schritt 6: Erster Daily Log

Existiert `{{VAULT_PFAD}}/05-daily/{{DATUM}}.md` bereits — z.B. weil ein `/shutdown` heute
schon einen Log-Eintrag geschrieben hat, oder weil ein vorheriger `/setup`-Lauf ihn schon
angelegt hat — **nicht anfassen**: zur Liste „übersprungen" hinzufügen, fertig mit Schritt 6.
Kein Nachtragen, kein Zusammenführen — die Grundregel gilt hier genauso wie überall in Phase B.

Existiert die Datei noch nicht: Erstelle sie mit **genau einem** Abschnitt — kein
„Nächste Schritte"-Abschnitt, der steht bereits in `03-strategy/current-priorities.md`:
```markdown
# {{DATUM}}

> Siehe auch: [[ich]], [[current-priorities]]

## Einrichtung
[Kurze Zusammenfassung in 2-3 Stichpunkten: welche Vault-Struktur, welche Kontext-Dateien
und welche Projekte beim Setup angelegt wurden]
```

Einrichtung und Arbeitssession sind verschiedene Ereignisse — deshalb eigener Abschnittsname
`## Einrichtung`, nicht `## Session` (das gehört `/shutdown`, siehe dort).

---

## Phase C: Abschluß

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
[Falls mehr als 3 Projekte genannt wurden: 1 Zeile, welche drei als „Business (Top 3)" gewählt wurden]
[Falls die Liste „übersprungen" aus Phase B mindestens einen Eintrag hat: Zeile
„Unangetastet gelassen (existierten bereits): <vault-relative Pfade, kommasepariert>" — sonst
diese Zeile komplett weglassen, nicht als leere Liste zeigen]

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
- **Notation in dieser Datei:** `{{PLATZHALTER}}` steht für einen echten Wert, der eingesetzt
  wird (Onboarding-Antwort, Datum, KW) — reine Textersetzung. Eckige Klammern `[...]` in
  Anweisungen (z.B. Schritt 6, Phase C) sind Hinweise ans Modell, was inhaltlich hingehört —
  sie werden beim Schreiben durch echten, abgeleiteten Text ersetzt, nie wörtlich übernommen.
  Das ist etwas anderes als die `[...]`-Einträge in den Context-Templates (`ich.md`,
  `business.md`): die bleiben absichtlich als Platzhalter für den Nutzer stehen, weil dafür
  keine Onboarding-Antwort existiert — nicht verwechseln.
