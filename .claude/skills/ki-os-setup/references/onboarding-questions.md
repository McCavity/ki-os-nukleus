# Onboarding-Fragen

## Anweisungen für Claude

- Stelle jede Frage einzeln. Warte auf die Antwort.
- Akzeptiere jedes Format: kurzer Satz, langer Text, LinkedIn-Profil, hochgeladene Datei, oder "skip".
- Keine Nachfragen oder Drill-Downs. Extrahiere was du kannst.
- Nach jeder Antwort: 1 Satz Bestätigung, dann nächste Frage.
- Bei "skip": Platzhalter lassen, Nutzer kann später ergänzen.

---

## Frage 0: Wo soll dein Wissen leben?

> **Dein KI-OS besteht aus zwei Hälften: diesem Workspace hier (die Mechanik) und einem
> Vault (dein Wissen).** Sie bleiben getrennt, damit du den Workspace aktualisieren kannst,
> ohne dein Wissen anzufassen — und damit du dein Wissen in Obsidian öffnen kannst, ohne die
> Mechanik zu sehen.
>
> Wo soll der Vault liegen? (Vorschlag: `~/ki-os-vault`)

Extrahiere daraus:
- `{{VAULT_PFAD}}` — Zielverzeichnis des Vaults. Tilde expandieren. Existiert der Pfad
  bereits und ist nicht leer: nachfragen, nicht überschreiben.

---

## Frage 1: Wer bist du?

> **Erzähl mir kurz von dir.**
> Name, was du machst, für wen du arbeitest. 2-3 Sätze reichen — oder paste dein LinkedIn-Profil, deine Website-Bio, oder was du hast.

Extrahiere daraus:
- `{{NAME}}` — Vorname oder voller Name
- `{{KURZBESCHREIBUNG}}` — Was die Person macht + für wen (1-2 Sätze)

---

## Frage 2: Was ist dein Business?

> **Was bietest du an?**
> Dein Angebot, deine Zielgruppe, ungefähre Preise wenn du magst. Und: Was ist gerade deine größte Herausforderung?

Extrahiere daraus:
- `{{ANGEBOT}}` — Produkte/Dienstleistungen
- `{{ZIELGRUPPE}}` — Für wen
- `{{HERAUSFORDERUNG}}` — Größtes aktuelles Problem/Engpass

---

## Frage 3: Aktive Projekte?

> **Woran arbeitest du gerade?**
> Nenn mir 2-3 Projekte oder Vorhaben, die bei dir aktuell laufen. Pro Projekt reicht: Name + was das Ziel ist.

Extrahiere daraus:
- `{{PROJEKTE}}` — Liste mit Name + Ziel pro Projekt

---

## Nach allen Fragen

Sage: "Alles klar, ich richte jetzt dein KI OS ein." — dann weiter mit Phase B (Vault erstellen).
