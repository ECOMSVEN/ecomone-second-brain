---
name: brain-tagebuch
description: >-
  Einen Tagebuch-Eintrag in {{VORNAME}}s Second Brain schreiben oder ergänzen. Auslöser: "Tagebuch", "heute war", "Tageseintrag", "schreib ins Tagebuch".
---

# brain-tagebuch

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

`journal/JJJJ-MM-TT.md` (heute) aus `templates/Tagebuch.md` anlegen oder ergänzen, in {{VORNAME}}s Worten. Erwähnte Personen, Projekte und den Shop verlinken.
