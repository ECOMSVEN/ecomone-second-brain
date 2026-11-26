---
name: brain-adtest
description: >-
  Ad-Tests in {{VORNAME}}s Second Brain festhalten und auswerten. Auslöser: "neuer Ad-Test", "Ad-Ergebnis", "Creative-Test", "Kampagne eintragen", "was haben meine Ads gezeigt".
---

# brain-adtest

**Brain:** `{{BRAIN}}` (fester Pfad, nicht suchen). Zuerst `_CLAUDE.md` lesen (Regeln), dann `_index.md`. Datum immer vom System holen. Ansprache: {{TON}}
Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{{NIE_ZUSATZ}}. Nichts löschen, `sources/` nie ändern.
Nach jeder Änderung: `{{PY}} "{{BRAIN}}/.brain/ansicht.py"` (erneuert Index und 3D-Ansicht) und einen Eintrag in `_log.md`.

1. Neuer Test: `wiki/shops/<Shop>/ads/<Titel>.md` (bei mehreren Shops und unklarer Angabe kurz fragen, welcher) aus `templates/Ad-Test.md` mit Hypothese, Setup, `produkt`, `start`, `budget`.
2. Ergebnis: Zahlen eintragen (nur genannte, nie erfinden), `ergebnis` und Learning in einem Satz, `status: erledigt`.
3. Learning zusätzlich in der Shop-Übersicht (Abschnitt Ads), beim Produkt und bei Bedarf in `Mein Business` nachtragen.
4. Auf Wunsch: alle Learnings aus den `ads/`-Ordnern zu einer Synthese bündeln.
