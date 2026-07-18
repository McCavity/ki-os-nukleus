# 04-Projects

Jedes aktive Projekt bekommt einen eigenen Unterordner mit einer Notiz, die wie das Projekt
heißt (`{projektname}.md`, derselbe kebab-case-Slug wie der Ordnername) — nicht `README.md`.
Grund: Obsidian löst Wikilinks über den Dateinamen auf, und `[[README]]` wäre bei mehreren
Projekten mehrdeutig.

**Struktur pro Projekt:**
```
04-projects/{projektname}/
  {projektname}.md    — Ziel, Status, nächste Schritte
  plan-YYYY-MM-DD.md  — Implementierungspläne (erstellt durch `/plan`)
  [weitere Dateien]    — Notizen, Recherche, Drafts
```

**Lebenszyklus:**
- Neues Projekt: `/plan` oder manuell Ordner anlegen
- Abgeschlossen: Ordner nach `09-reference/` verschieben, Eintrag in `completed-projects.md`

**Tipp:** Die `{projektname}.md` ist der Einstiegspunkt. Halte sie kurz: Ziel, Status, nächste
Schritte.
