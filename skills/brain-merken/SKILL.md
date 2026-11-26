---
name: brain-merken
description: >-
  Etwas in {{VORNAME}}s Second Brain festhalten: Notiz, Idee, Erkenntnis, Learning, Zahl. Auslöser: "merk dir", "notier das", "schreib das ins Brain", "halt fest".
---

# brain-merken

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

1. Passende bestehende Seite suchen (`_index.md`, dann `grep`). Gibt es eine, dort ergänzen; sonst neue Seite aus `templates/Notiz.md` am richtigen Ort: Shop-Wissen in den Ordner des Shops unter `wiki/shops/<Shop>/` (Ads nach `ads/`, Produkte nach `produkte/`, Lieferanten nach `lieferanten/`), Business nach `wiki/business/`, Privates nach `wiki/privat/`, Personen nach `wiki/personen/`, Wissen nach `wiki/themen/`. Unklares nach `inbox/`. Ist nicht klar, welcher Shop gemeint ist, kurz nachfragen.
2. Mit mindestens zwei passenden Seiten verlinken, `aktualisiert` setzen.
3. Kurz bestätigen, wo es liegt (ein Satz).
Log-Format: `## [JJJJ-MM-TT] merken | Titel`.
