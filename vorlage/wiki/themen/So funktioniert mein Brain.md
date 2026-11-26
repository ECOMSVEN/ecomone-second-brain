---
beschreibung: "Wie mein Second Brain funktioniert: Karpathys LLM-Wiki, der Ablauf und die Befehle mit Beispielen"
typ: thema
status: aktuell
aktualisiert: "{{HEUTE}}"
quellen: []
---
# So funktioniert mein Brain

**Ich sammle und frage, Claude schreibt und verknüpft.** Das Prinzip stammt von Andrej Karpathy («LLM-Wiki»): Statt Notizen selbst zu sortieren, gibt man der KI Rohmaterial, und sie pflegt daraus ein Wiki, das mit jeder Quelle klüger wird.

## Drei Schichten
1. **Quellen** (`sources/`): Artikel, Calls, Kurs-Lektionen, PDFs. Bleiben unverändert.
2. **Wiki** (`wiki/`): Claude macht daraus verknüpfte Seiten, klar getrennt in **Privat**, **Business** und **jeden Shop für sich**, dazu Projekte, Aufgaben, Personen und Themen.
3. **Regeln** (`_CLAUDE.md`): wie Claude das Brain führt.

## Der Ablauf
Inbox → Quelle → Wiki. Alles Neue landet zuerst im Eingang oder als Quelle; Claude arbeitet es ein und führt [[_index|Index]] und [[_log|Chronik]] nach. Startpunkte: [[Profil]], [[Meine Ziele]], [[Mein Business]], [[Privat]].

## Was ich sagen kann
| Ich sage | Was passiert |
|---|---|
| «Merk dir: Mein bester Hook war …» | Claude legt es an der richtigen Stelle ab |
| «Arbeite diesen Link ins Brain ein: …» | Quelle ablegen, Kernpunkte, alle Seiten nachführen |
| «Was weiss mein Brain über meine Ads?» | Antwort mit Belegen aus dem Brain |
| «Neue Aufgabe: Produktfotos bis Freitag» | Aufgabe mit Frist und Prio |
| «Neuer Ad-Test: …» / «Ad-Ergebnis: …» | Test anlegen, Learning im Shop nachtragen |
| «Tagebuch: …» | Eintrag für heute |
| «Prüf mein Brain» | Wöchentlicher Check, Korrekturen nach OK |
| «Zeig mein Brain» | 3D-Ansicht neu zeichnen und öffnen |
