---
name: brain-pruefen
description: >-
  {{VORNAME}}s Second Brain prüfen und aufräumen (wöchentlich). Auslöser: "prüf mein Brain", "Brain-Check", "räum mein Brain auf", "lint".
---

# brain-pruefen

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

1. `{{PY}} "{{BRAIN}}/.brain/pruefen.py"` ausführen (kaputte Links, Seiten ohne Links, fehlendes Frontmatter).
2. Dazu prüfen: `status: aktuell` und `aktualisiert` älter als 90 Tage, `inbox/` älter als 7 Tage, überfällige Aufgaben, Quellen ohne Ingest-Eintrag im Log.
3. Kurzer Bericht mit Vorschlägen. Korrekturen erst nach {{VORNAME}}s OK. Log: `## [JJJJ-MM-TT] pruefen | Wochencheck`.
