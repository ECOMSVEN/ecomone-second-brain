---
name: brain-ansicht
description: >-
  {{VORNAME}}s Second Brain als 3D-Gehirn zeigen und neu zeichnen. Auslöser: "zeig mein Brain", "Brain-Ansicht", "aktualisiere die Ansicht", "wie gross ist mein Brain".
---

# brain-ansicht

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

1. `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` ausführen. Die Ausgabe nennt Notizen und Verknüpfungen.
2. `Mein Brain.html` im Browser öffnen (Mac `open`, Windows `cmd //c start "" "<Datei>"` bzw. in PowerShell `Start-Process`).
3. Hast du ein Werkzeug zum Veröffentlichen von Artifacts: Steht in `_CLAUDE.md` ein Artifact-Link, zuerst dieses Artifact lesen (read), dann `Mein Brain.html` unter demselben Link neu veröffentlichen. Sonst als neues privates Artifact «Mein Brain» veröffentlichen und den Link in `_CLAUDE.md` eintragen. Die Seite ist bewusst nur dunkel.
4. Einen Satz: Anzahl Notizen, Verknüpfungen, was seit dem letzten Mal dazugekommen ist.
