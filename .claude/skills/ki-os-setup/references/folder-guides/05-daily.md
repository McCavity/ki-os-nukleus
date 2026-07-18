# 05-Daily

Tages-Logs im Format `YYYY-MM-DD.md`. Werden automatisch durch `/shutdown` erstellt.

**Was reinkommt:**
- Was in der Session passiert ist
- Entscheidungen die getroffen wurden
- Offene Punkte für die nächste Session

**Regel:** Daily Logs sind append-only — bestehende Einträge nicht überschreiben, nur ergänzen.

**Tipp:** Claude liest die letzten 2 Daily Logs bei jedem `/start` für Kontinuität.
