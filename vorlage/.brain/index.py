#!/usr/bin/env python3
"""Erzeugt _index.md neu: jede Wiki-Seite genau einmal, nach Bereich, mit ihrer beschreibung.
Quellen, Eingang und Tagebuch werden nur gezählt. Nur Standardbibliothek.

Aufruf (aus jedem Ordner):  python3 -I "<Brain>/.brain/index.py"
"""
import datetime
import os
import re
import unicodedata

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEREICHE = [("wiki/ich", "Ich"), ("wiki/privat", "Privat"), ("wiki/business", "Business"), ("wiki/shops", "Shops"),
            ("wiki/projekte", "Projekte"), ("wiki/aufgaben", "Aufgaben"),
            ("wiki/personen", "Personen"), ("wiki/themen", "Themen"), ("wiki/entscheidungen", "Entscheidungen"),
            ("wiki/synthesen", "Synthesen")]
GEZAEHLT = [("sources", "Quellen"), ("inbox", "Eingang"), ("journal", "Tagebuch")]


def dateien(ordner):
    voll = os.path.join(BRAIN, ordner)
    out = []
    for root, dirs, files in os.walk(voll):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        out += [os.path.join(root, f) for f in files if f.endswith(".md")]
    return sorted(out, key=lambda p: os.path.basename(p).lower())


def beschreibung(path):
    txt = open(path, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if m:
        f = re.search(r"^beschreibung:\s*(.*?)\s*$", m.group(1), re.M)
        if f:
            v = f.group(1).strip()
            return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'" else v
    return ""


heute = datetime.date.today().isoformat()
z = ["---", 'beschreibung: "Katalog aller Wiki-Seiten – automatisch erzeugt, nicht von Hand bearbeiten"', "typ: index",
     f"aktualisiert: {heute}", "---", "# Index", "",
     f"*Automatisch erzeugt am {heute} von `.brain/index.py`. Claude liest diese Seite zuerst.*"]
anzahl = 0
for ordner, titel in BEREICHE:
    seiten = dateien(ordner)
    if not seiten:
        continue
    z += ["", f"## {titel}"]
    shop = None
    for p in seiten if ordner != "wiki/shops" else sorted(seiten, key=lambda q: (os.path.relpath(q, os.path.join(BRAIN, ordner)).replace(os.sep, "/").split("/")[0].lower(), q.count(os.sep), os.path.basename(q).lower())):
        if ordner == "wiki/shops":
            s = os.path.relpath(p, os.path.join(BRAIN, ordner)).replace(os.sep, "/").split("/")[0]
            s = os.path.splitext(s)[0]
            if s != shop:
                shop = s
                z += ["", f"### {unicodedata.normalize('NFC', s)}"]
        name = unicodedata.normalize("NFC", os.path.splitext(os.path.basename(p))[0])
        b = beschreibung(p)
        z.append(f"- [[{name}]]" + (f" – {b}" if b else ""))
        anzahl += 1
z += ["", "## Gezählt", ""] + [f"- {t}: {len(dateien(o))}" for o, t in GEZAEHLT]
open(os.path.join(BRAIN, "_index.md"), "w", encoding="utf-8", newline="\n").write("\n".join(z) + "\n")
print(f"_index.md: {anzahl} Wiki-Seiten")
