#!/usr/bin/env python3
"""Baut «Mein Brain.html» (3D-Ansicht) aus allen Notizen des Brains. Nur Standardbibliothek.

Aufruf (aus jedem Ordner):  python3 -I "<Brain>/.brain/ansicht.py"
Liest .brain/brain.json (vorname, ss), setzt die Daten in .brain/ansicht-vorlage.html ein
und erneuert danach _index.md über .brain/index.py.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import unicodedata

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VORLAGE = os.path.join(BRAIN, ".brain", "ansicht-vorlage.html")
ZIEL = os.path.join(BRAIN, "Mein Brain.html")
PLATZHALTER = "__BRAIN_DATEN__"
LINK = re.compile(r"\[\[([^\]\n]+?)\]\]")
WIKI = {"ich": "ich", "privat": "privat", "business": "business", "shops": "shops", "projekte": "projekte",
        "aufgaben": "aufgaben", "personen": "personen", "themen": "themen", "entscheidungen": "entscheidungen",
        "synthesen": "synthesen"}
MAX_INHALT = 20000


def nfc(s):
    return unicodedata.normalize("NFC", s)


def bereich(rel):
    """Bereich aus dem Ordner. Wurzeldateien (Index, Log, Schema, Start) zählen nicht als Notiz."""
    t = rel.split("/")
    if len(t) < 2:
        return None
    if t[0] == "wiki":
        return WIKI.get(t[1], "themen") if len(t) > 2 else "themen"
    return {"sources": "quellen", "journal": "tagebuch", "inbox": "eingang"}.get(t[0])


def lesen(path):
    txt = open(path, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    fm, body = {}, txt
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", txt, re.S)
    if m:
        body = txt[m.end():]
        for line in m.group(1).splitlines():
            mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if mm:
                v = mm.group(2).strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                fm[mm.group(1)] = v
    return txt, fm, body


def einstellungen():
    p = os.path.join(BRAIN, ".brain", "brain.json")
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        b = os.path.basename(BRAIN)
        return {"vorname": b[:-6] if b.endswith(" Brain") else "", "ss": True}


def main():
    pfade = []
    for root, dirs, files in os.walk(BRAIN):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("templates", "archive", "_cockpit")]
        for f in files:
            if f.endswith(".md"):
                rel = nfc(os.path.relpath(os.path.join(root, f), BRAIN).replace(os.sep, "/"))
                if bereich(rel):
                    pfade.append(rel)
    pfade.sort(key=str.lower)
    nach_name, nach_pfad = {}, {}
    for i, rel in enumerate(pfade):
        nach_name.setdefault(os.path.splitext(os.path.basename(rel))[0].lower(), i)
        nach_pfad[rel[:-3].lower()] = i

    notizen, kanten = [], set()
    for i, rel in enumerate(pfade):
        txt, fm, body = lesen(os.path.join(BRAIN, rel))
        links = []
        for roh in LINK.findall(txt):
            ziel = nfc(roh.replace("\\|", "|").split("|")[0].split("#")[0].strip())
            if not ziel:
                continue
            k = ziel[:-3] if ziel.lower().endswith(".md") else ziel
            j = nach_pfad.get(k.lower(), nach_name.get(os.path.basename(k).lower()))
            if j is not None and j != i and j not in links:
                links.append(j)
                kanten.add((min(i, j), max(i, j)))
        n = {"titel": os.path.splitext(os.path.basename(rel))[0], "pfad": rel, "bereich": bereich(rel),
             "typ": fm.get("typ", ""), "status": fm.get("status", ""), "beschreibung": fm.get("beschreibung", ""),
             "aktualisiert": fm.get("aktualisiert", ""), "links": links, "inhalt": body.strip()[:MAX_INHALT]}
        if n["bereich"] == "shops":
            t = rel.split("/")
            n["shop"] = t[2] if len(t) > 3 else os.path.splitext(t[2])[0]
        if n["bereich"] == "tagebuch" and not n["aktualisiert"]:
            n["aktualisiert"] = n["titel"][:10]
        if n["bereich"] == "aufgaben":
            for f in ("prio", "faellig", "zustaendig"):
                n[f] = fm.get(f, "")
        notizen.append(n)

    cfg = einstellungen()
    daten = {"vorname": cfg.get("vorname", ""), "ss": cfg.get("ss", True), "vault": os.path.basename(BRAIN),
             "stand": datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"), "notizen": notizen}
    js = json.dumps(daten, ensure_ascii=False, separators=(",", ":"))
    js = js.replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    html = open(VORLAGE, encoding="utf-8").read()
    if html.count(PLATZHALTER) != 1:
        sys.exit("Fehler: Platzhalter fehlt oder ist doppelt in .brain/ansicht-vorlage.html")
    with open(ZIEL, "w", encoding="utf-8", newline="\n") as f:
        f.write(html.replace(PLATZHALTER, js))
    print(f"Mein Brain.html: {len(notizen)} Notizen, {len(kanten)} Verknüpfungen", flush=True)
    subprocess.run([sys.executable, "-I", os.path.join(BRAIN, ".brain", "index.py")], check=True)


if __name__ == "__main__":
    main()
