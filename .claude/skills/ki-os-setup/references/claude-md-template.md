# CLAUDE.md Template

Ersetze alle `{{PLATZHALTER}}` mit den Onboarding-Antworten und schreibe das Ergebnis als `CLAUDE.md` in den **Workspace-Root**.

---

```markdown
# {{NAME}}s KI OS

> Letzte Aktualisierung: {{DATUM}}

## Wer ich bin

{{KURZBESCHREIBUNG}}

---

> Dein Wissen liegt im Vault (Pfad siehe `.env`). Die Pfade unten sind relativ zum Vault-Root.

## Vault-Navigation

| Ich brauche... | Lese in... |
|---|---|
| Wer ich bin | `01-context/ich.md` |
| Mein Business | `01-context/business.md` |
| Brand + Stimme | `02-brand/brand-voice.md` |
| Wochenprioritäten | `03-strategy/current-priorities.md` |
| Offene Loops | `03-strategy/open-loops.md` |
| Quick Capture | `00-inbox/capture.md` |
| Meine Projekte | `04-projects/` |
| Tages-Logs | `05-daily/YYYY-MM-DD.md` |
| Team | `06-team/` |
| Entscheidungen | `07-intelligence/decisions/` |
| Meeting-Notizen | `07-intelligence/meetings/` |
| Ressourcen | `08-resources/` |
| Archiv | `09-reference/` |

---

## Commands

| Command | Wann nutzen |
|---|---|
| `/start` | Jede neue Session starten |
| `/capture` | Schnell etwas festhalten |
| `/plan` | Projekt planen |
| `/review` | Wöchentliches Review (So/Mo) |
| `/shutdown` | Session beenden |

---

## Regeln

1. **Wiki-Links:** `[[dateiname]]` wenn auf Vault-Dateien referenziert wird — immer
2. **Timestamps:** `> Letzte Aktualisierung: YYYY-MM-DD` nach Updates
3. **Daily Logs:** `05-daily/YYYY-MM-DD.md` ist append-only
4. **Neue Dateien:** In passenden Ordner anlegen, Navigation oben updaten
5. **Dateinamen:** kebab-case, keine Emojis, keine Sonderzeichen
6. **Sprache:** Deutsch, technische Begriffe dürfen Englisch bleiben
7. **Kurze Antworten:** Wenn ein Satz reicht, keinen Absatz schreiben
8. **Proaktiv:** Probleme flaggen, Empfehlungen geben, mitdenken
9. **Nie fragen "Soll ich das speichern?"** — einfach machen und berichten
10. **Session-Start:** Beim ersten Response `01-context/ich.md` und `03-strategy/current-priorities.md` lesen

---

## Obsidian Konventionen

- **Wikilinks:** `[[dateiname]]` für interne Vault-Links (Obsidian resolved automatisch)
- **Callouts:** `> [!type] Titel` für visuelle Struktur (tip, warning, important, todo)
- **Tags:** `#tag` inline oder in YAML Frontmatter
- **Dateinamen:** kebab-case, deutsch OK, keine Umlaute in Dateinamen

---

## KI OS Lernprotokoll

<!-- Korrekturen und Präferenzen werden hier automatisch ergänzt -->

```
