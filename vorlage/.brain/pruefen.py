#!/usr/bin/env python3
"""Prüft das Brain und meldet jeden Punkt mit ✓ oder ✗. Nur Standardbibliothek. Ändert nichts.

Aufruf (aus jedem Ordner):  python3 -I "<Brain>/.brain/pruefen.py"
"""
import json
import os
import re
import sys
import unicodedata

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
ORDNER = ["inbox", "sources/articles", "sources/conversations", "sources/documents", "sources/kurs", "sources/assets",
          "wiki/ich", "wiki/privat", "wiki/business", "wiki/shops", "wiki/projekte", "wiki/aufgaben",
          "wiki/personen", "wiki/themen", "wiki/entscheidungen", "wiki/synthesen", "journal", "templates", "archive", "_cockpit"]
WURZEL = ["CLAUDE.md", "_CLAUDE.md", "_index.md", "_log.md", "Start.md", "_cockpit/Cockpit.base", "Mein Brain.html"]
PFLICHT = ["beschreibung", "typ", "status", "aktualisiert", "quellen"]
WERKZEUG = {"_index.md", "_log.md", "Start.md", "CLAUDE.md", "_CLAUDE.md"}
LINK = re.compile(r"\[\[([^\]\n]+?)\]\]")
fehler = 0


def nfc(s):
    return unicodedata.normalize("NFC", s)


def punkt(gut, text, details=()):
    global fehler
    print(("✓ " if gut else "✗ ") + text)
    for d in list(details)[:12]:
        print("    – " + d)
    if not gut:
        fehler += 1


def ohne_code(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", t)


def md_dateien():
    out = []
    for root, dirs, files in os.walk(BRAIN):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("templates", "archive")]
        for f in files:
            if f.endswith((".md", ".base")):
                out.append(nfc(os.path.relpath(os.path.join(root, f), BRAIN).replace(os.sep, "/")))
    return sorted(out)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
fehlt = [o for o in ORDNER if not os.path.isdir(os.path.join(BRAIN, o))]
punkt(not fehlt, "Alle Ordner vorhanden", fehlt)
fehlt = [w for w in WURZEL if not os.path.isfile(os.path.join(BRAIN, w))]
punkt(not fehlt, "Grunddateien vorhanden", fehlt)

alle = md_dateien()
namen = {os.path.splitext(os.path.basename(p))[0].lower() for p in alle}
pfade = {os.path.splitext(p)[0].lower() for p in alle}
wiki = [p for p in alle if p.startswith("wiki/") and p.endswith(".md")]

schlecht = []
for p in wiki:
    t = open(os.path.join(BRAIN, p), encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if not m:
        schlecht.append(f"{p}: kein Frontmatter")
        continue
    leer = [k for k in PFLICHT if not re.search(rf"^{k}:\s*\S", m.group(1), re.M)]
    if leer:
        schlecht.append(f"{p}: fehlt {', '.join(leer)}")
    for zeile in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", zeile)
        if not mm or not mm.group(2):
            continue
        v = mm.group(2).strip()
        if v[0] == '"' and (not v.endswith('"') or len(v) < 2 or '"' in v[1:-1].replace('\\"', "")):
            if not (v.startswith('["') or v.startswith('"[')):
                schlecht.append(f"{p}: Anführungszeichen in «{mm.group(1)}» kaputt")
        elif v[0] not in "\"'[{" and (": " in v or " #" in v):
            schlecht.append(f"{p}: «{mm.group(1)}» braucht Anführungszeichen")
punkt(not schlecht, f"Frontmatter in allen {len(wiki)} Wiki-Seiten", schlecht)

kaputt, ein, aus = [], {}, {}
for p in alle:
    if p.endswith(".base"):
        continue
    roh_t = open(os.path.join(BRAIN, p), encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    fm_m = re.match(r"^---\n.*?\n---", roh_t, re.S)
    t = ohne_code(roh_t)
    fm_links = set(LINK.findall(fm_m.group(0))) if fm_m else set()
    for roh in LINK.findall(t):
        z = nfc(roh.replace("\\|", "|").split("|")[0].split("#")[0].strip())
        if not z:
            continue
        k = z[:-3] if z.lower().endswith(".md") else z
        k_base = k[:-5] if k.lower().endswith(".base") else k
        if k.lower() in pfade or os.path.basename(k).lower() in namen or os.path.basename(k_base).lower() in namen:
            if roh in fm_links or os.path.basename(p) in WERKZEUG:
                continue
            aus[p] = aus.get(p, 0) + 1
            ziel = next((q for q in alle if os.path.splitext(os.path.basename(q))[0].lower() == os.path.basename(k_base).lower()), None)
            if ziel:
                ein[ziel] = ein.get(ziel, 0) + 1
        else:
            kaputt.append(f"{p} → [[{roh}]]")
punkt(not kaputt, "Keine kaputten Links", kaputt)
einsam = [p for p in wiki if aus.get(p, 0) + ein.get(p, 0) < 2]
punkt(not einsam, "Jede Wiki-Seite hat mindestens zwei Verknüpfungen", einsam)

try:
    idx = open(os.path.join(BRAIN, "_index.md"), encoding="utf-8").read()
    gelistet = [nfc(x) for x in re.findall(r"^- \[\[([^\]|]+)", idx, re.M)]
    erwartet = [os.path.splitext(os.path.basename(p))[0] for p in wiki]
    falsch = [n for n in erwartet if gelistet.count(n) != 1]
    punkt(not falsch, "_index.md listet jede Wiki-Seite genau einmal", falsch)
except OSError:
    punkt(False, "_index.md lesbar")

try:
    h = open(os.path.join(BRAIN, "Mein Brain.html"), encoding="utf-8").read()
    m = re.search(r'<script id="brain-daten" type="application/json">(.*?)</script>', h, re.S)
    d = json.loads(m.group(1))
    drin = {n["pfad"] for n in d["notizen"]}
    fehlt = [p for p in wiki if p not in drin]
    punkt(not fehlt, f"3D-Ansicht: gültige Daten, {len(d['notizen'])} Notizen", fehlt)
except Exception as e:  # noqa: BLE001
    punkt(False, f"3D-Ansicht: Daten nicht lesbar ({e.__class__.__name__})")

sk = os.path.join(HOME, ".claude", "skills")
namen_sk = ["brain-merken", "brain-ingest", "brain-frage", "brain-aufgabe", "brain-person", "brain-adtest", "brain-tagebuch", "brain-pruefen", "brain-ansicht"]
fehlt = []
for n in namen_sk:
    f = os.path.join(sk, n, "SKILL.md")
    if not os.path.isfile(f) or not re.match(rf"^---\nname: {n}\ndescription: >-\n  \S", open(f, encoding="utf-8").read()):
        fehlt.append(n)
punkt(not fehlt, "9 Befehle installiert, Frontmatter gültig", fehlt)

cm = os.path.join(HOME, ".claude", "CLAUDE.md")
t = open(cm, encoding="utf-8").read() if os.path.exists(cm) else ""
punkt(t.count("<!-- second-brain:start -->") == 1 and t.count("<!-- second-brain:end -->") == 1, "Gedächtnis-Block genau einmal in .claude/CLAUDE.md")

print("")
print("ALLES OK" if not fehler else f"{fehler} PUNKT(E) OFFEN")
sys.exit(1 if fehler else 0)
