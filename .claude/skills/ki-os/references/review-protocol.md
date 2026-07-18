# Weekly Review Protokoll

Am besten Sonntag abend oder Montag morgen. Jeden Schritt einzeln mit dem Nutzer durchgehen.

---

## Schritt 1: Inbox leeren

1. Lies `00-inbox/capture.md`
2. Falls leer: "Inbox ist leer — weiter zum nächsten Schritt."
3. Falls Items vorhanden: Jedes Item einzeln zeigen und fragen:
   - **Machen** → Als Task in `current-priorities.md` eintragen (passende Sektion: Business (Top 3) / Persönlich / Side Quests)
   - **Planen** → Projekt-Idee in `04-projects/`, aktiver Loop in `open-loops.md` (Sektion „Wartend auf...")
   - **Löschen** → Entfernen
4. Nach Verarbeitung: `capture.md` leeren (nur Header behalten)

---

## Schritt 2: Open Loops prüfen

1. Lies `03-strategy/open-loops.md`.
2. Loops älter als 2 Wochen markieren.
3. Pro altem Loop fragen: "Noch relevant? Erledigt? Oder eskalieren?"
   - **Erledigt** → Zeile aus der Tabelle entfernen (die Historie lebt im Daily Log
     und, falls der Vault versioniert ist, in Git).
   - **Irrelevant** → Zeile löschen.
   - **Eskalieren** → als Aufgabe nach `03-strategy/current-priorities.md` heben.

---

## Schritt 3: Projekte updaten

1. Frage: "Was hat sich bei deinen Projekten bewegt?"
2. Status in den jeweiligen Projekt-Notizen aktualisieren (`04-projects/{name}/{name}.md` —
   nicht `README.md`)
3. Abgeschlossene Projekte:
   - Eintrag in `09-reference/completed-projects.md`
   - Ordner kann später nach `09-reference/` verschoben werden

---

## Schritt 4: Reflexion

3 Fragen stellen (einzeln):

1. **Was lief gut diese Woche?**
2. **Was war schwierig?**
3. **Was nimmst du mit? (Key Learning)**

Antworten werden im Weekly Log festgehalten.

---

## Schritt 5: Weekly Log schreiben

In `09-reference/weekly-log.md` eine Zeile ergänzen:

```markdown
| [KW] | [Datumsbereich] | [1-3 Sätze: Was passiert ist. Key Insight.] |
```

**Regel:** Max 8 Einträge. Wenn mehr: Ältesten löschen.

---

## Schritt 6: Nächste Woche planen

1. Frage: "Was sind deine Top 3 für nächste Woche?"
2. In `03-strategy/current-priorities.md` unter neuer KW eintragen:
   - Top 3 Business
   - Top 1 Persönlich
   - Optional: Side Quests

   **Regel:** Max. 4 KW-Blöcke gleichzeitig (aktueller + 3 vorherige). Wird mit dem neuen
   Block ein fünfter fällig, den ältesten KW-Block komplett entfernen — seine Zusammenfassung
   lebt bereits in `09-reference/weekly-log.md` (Schritt 5), verloren geht nichts. Analog zur
   Deckelung in `weekly-log.md`, damit `current-priorities.md` nicht unbegrenzt wächst.
3. Abschluß: "Review fertig. Guter Start in die Woche!"

---

## Regeln

- Geduldig — nicht hetzen
- Jeden Schritt einzeln durchgehen, nicht alles auf einmal
- Wiki-Links in alle Einträge
- Timestamps aktualisieren
