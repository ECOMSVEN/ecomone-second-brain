---
name: brain-person
description: >-
  Eine Personenseite in {{VORNAME}}s Second Brain anlegen oder ergänzen: Partner, Coach, Lieferant-Kontakt, Kunde, Familie. Auslöser: "leg eine Person an", "Person anlegen", "ergänze die Seite von".
---

# brain-person

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

`wiki/personen/<Vorname Nachname>.md` (ohne Nachnamen: `<Vorname> (<Rolle>)`) aus `templates/Person.md`: wer, Rolle, Beziehung zu {{VORNAME}}, Begegnungen mit Datum, offene Zusagen. Mit Projekten und Shop verlinken. Firmen (Lieferanten) gehören nach `wiki/shops/<Shop>/lieferanten/`.
