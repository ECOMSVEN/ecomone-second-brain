---
name: brain-aufgabe
description: >-
  Aufgaben in {{VORNAME}}s Second Brain anlegen, ändern, abschliessen oder zeigen. Auslöser: "neue Aufgabe", "to-do", "Aufgabe erledigt", "verschieb die Aufgabe", "meine offenen Aufgaben", "was steht an".
---

# brain-aufgabe

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

- Anlegen: `wiki/aufgaben/<Titel>.md` aus `templates/Aufgabe.md`; `zustaendig` (ich | Claude), `faellig` (nur wenn genannt), `prio` (hoch | mittel | tief), `projekt` als Wikilink.
- Erledigt: `status: erledigt`, nichts löschen.
- Zeigen: offene Aufgaben nach prio, dann Fälligkeit; Überfälliges zuerst markieren. Beim Zeigen nichts ändern.
