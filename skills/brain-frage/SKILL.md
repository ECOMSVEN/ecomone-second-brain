---
name: brain-frage
description: >-
  {{VORNAME}}s Second Brain befragen und mit Belegen antworten. Auslöser: "was weiss mein Brain über", "frag mein Brain", "was habe ich zu ... notiert", "steht in meinem Brain".
---

# brain-frage

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

1. Zuerst `_index.md`, dann die passenden Seiten und bei Bedarf die Quellen lesen.
2. Antworten mit Wikilinks als Beleg. Steht etwas nicht drin, das sagen statt raten.
3. Ist die Antwort wertvoll (Vergleich, Analyse, neue Verbindung), kurz fragen und als `wiki/synthesen/JJJJ-MM-TT Titel.md` ablegen. Nur dann `ansicht.py` und Log.
