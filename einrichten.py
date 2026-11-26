#!/usr/bin/env python3
"""Ecomone Second Brain – richtet das Brain aus dem Bausatz ein. Nur Standardbibliothek, Mac und Windows.

  python3 -I einrichten.py brain --vorname Lena --ss nein --ton "Du-Form, locker und kurz" --nie "Bankdaten"
  python3 -I einrichten.py obsidian --brain "<Pfad>"      (Obsidian vorher beenden)

Überschreibt nie etwas: Vorhandene Dateien bleiben, das wird gemeldet.
"""
import argparse
import datetime
import json
import os
import platform
import re
import secrets
import shutil
import sys
import time
import urllib.parse

KIT = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
WIN = platform.system() == "Windows"
ORDNER = ["inbox", "sources/articles", "sources/conversations", "sources/documents", "sources/kurs", "sources/assets",
          "wiki/ich", "wiki/privat", "wiki/business", "wiki/shops", "wiki/projekte", "wiki/aufgaben",
          "wiki/personen", "wiki/themen", "wiki/entscheidungen", "wiki/synthesen", "journal", "archive"]
TEXT = (".md", ".base", ".css")
START, ENDE = "<!-- second-brain:start -->", "<!-- second-brain:end -->"


def py_befehl():
    return "py -3 -I" if WIN and shutil.which("py") else ("python -I" if WIN else "python3 -I")


def genitiv(name):
    return name + ("’" if name[-1:].lower() in "sxzß" else "s")


SZ = [("weiss", "weiß"), ("Weiss", "Weiß"), ("ausser", "außer"), ("Ausser", "Außer"), ("schliess", "schließ"),
      ("Schliess", "Schließ"), ("grosszügig", "großzügig"), ("gross", "groß"), ("Gross", "Groß"), ("heisst", "heißt"),
      ("heissen", "heißen"), ("Grösse", "Größe"), ("Strasse", "Straße"), ("fliess", "fließ"), ("Begrüss", "Begrüß")]


def ersetzen(text, werte):
    if werte.get("SZ") == "ja":
        for alt, neu in SZ:
            text = text.replace(alt, neu)
    text = text.replace("{{VORNAME}}s", genitiv(werte["VORNAME"]))
    for k, v in werte.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def ok(t):
    print("✓ " + t)


def warn(t):
    print("! " + t)


def brain(a):
    ziel = os.path.abspath(os.path.expanduser(a.ziel)) if a.ziel else os.path.join(HOME, "Brains", f"{a.vorname} Brain")
    if os.path.isdir(ziel) and os.listdir(ziel) and not a.ergaenzen:
        print(f"STOP Ordner existiert schon und ist nicht leer: {ziel}")
        print("     Frag, ob ergänzt werden soll (--ergaenzen) oder ein anderer Ort (--ziel).")
        sys.exit(3)
    pfad = ziel.replace("\\", "/")
    heute = datetime.date.today().isoformat()
    werte = {"VORNAME": a.vorname, "BRAIN": pfad, "PY": py_befehl(), "TON": a.ton, "NIE": a.nie or "nichts weiter",
             "NIE_ZUSATZ": "", "SZ": "ja" if a.ss == "nein" else "nein",
             "HEUTE": heute, "VAULT_URL": urllib.parse.quote(os.path.basename(ziel)), "ARTIFACT": "(noch keiner)"}
    shops = [re.sub(r'[\\/:*?"<>|#^\[\]]', "-", s).strip(" .-") for s in (a.shops or "").split(";")]
    shops = [s for s in dict.fromkeys(shops) if s] or ["Mein erster Shop"]
    standard = {"passwort", "passwörter", "schlüssel", "tokens", "token", "bankdaten", "kartendaten", "bank- und kartendaten"}
    nie = [x.strip() for x in re.split(r"[,;]| und ", a.nie or "") if x.strip() and x.strip().lower() not in standard]
    werte["NIE"] = ", ".join(nie) or "nichts weiter"
    werte["NIE_ZUSATZ"] = (", " + ", ".join(nie)) if nie else ""
    werte["SHOP_LINKS"] = "".join(f"> - [[{s}]]\n" for s in shops)

    # 1. Gerüst kopieren, Platzhalter füllen, nie überschreiben
    vorlage = os.path.join(KIT, "vorlage")
    neu = behalten = 0
    for root, _dirs, files in os.walk(vorlage):
        rel = os.path.relpath(root, vorlage)
        os.makedirs(os.path.join(ziel, rel), exist_ok=True)
        for f in files:
            q, z = os.path.join(root, f), os.path.join(ziel, rel, f)
            if os.path.exists(z):
                behalten += 1
                continue
            if f.endswith(TEXT):
                with open(q, encoding="utf-8") as fh:
                    inhalt = ersetzen(fh.read(), werte)
                with open(z, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(inhalt)
            else:
                shutil.copy2(q, z)
            neu += 1
    for o in ORDNER:
        os.makedirs(os.path.join(ziel, o), exist_ok=True)
    for s in shops:
        for u in ("produkte", "ads", "lieferanten"):
            os.makedirs(os.path.join(ziel, "wiki", "shops", s, u), exist_ok=True)
    ok(f"Brain angelegt: {ziel} ({neu} Dateien neu" + (f", {behalten} schon vorhanden und behalten)" if behalten else ")"))

    # 2. Einstellungen für die 3D-Ansicht
    with open(os.path.join(ziel, ".brain", "brain.json"), "w", encoding="utf-8") as fh:
        json.dump({"vorname": a.vorname, "ss": a.ss == "ja"}, fh, ensure_ascii=False)
    ok("Einstellungen .brain/brain.json")

    # 3. Befehle (Skills)
    sk_ziel = os.path.join(HOME, ".claude", "skills")
    os.makedirs(sk_ziel, exist_ok=True)
    gesetzt, uebersprungen = [], []
    for name in sorted(os.listdir(os.path.join(KIT, "skills"))):
        q = os.path.join(KIT, "skills", name, "SKILL.md")
        if not os.path.isfile(q):
            continue
        with open(q, encoding="utf-8") as fh:
            inhalt = ersetzen(fh.read(), werte)
        zd = os.path.join(sk_ziel, name)
        zf = os.path.join(zd, "SKILL.md")
        if os.path.exists(zf):
            with open(zf, encoding="utf-8") as fh:
                if fh.read() != inhalt and not a.skills_ersetzen:
                    uebersprungen.append(name)
                    continue
        os.makedirs(zd, exist_ok=True)
        with open(zf, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(inhalt)
        gesetzt.append(name)
    ok(f"{len(gesetzt)} Befehle in {sk_ziel}")
    if uebersprungen:
        warn("Schon vorhanden, nicht überschrieben: " + ", ".join(uebersprungen))

    # 4. Gedächtnis-Block in ~/.claude/CLAUDE.md
    cm = os.path.join(HOME, ".claude", "CLAUDE.md")
    block = (f"{START}\n# Mein Second Brain\n"
             f"Mein Second Brain liegt unter `{pfad}` (Obsidian). Ansprache: {a.ton}\n"
             f"- Vor Antworten über mich, mein Business, meine Shops, meine Ziele, Projekte oder Personen zuerst dort nachschauen: `_index.md`, dann die Seiten.\n"
             f"- Entsteht im Gespräch etwas, das ich behalten sollte (Learning, Entscheid, Zahl, Idee), kurz vorschlagen und nach meinem Ja mit /brain-merken ablegen.\n"
             f"- Befehle: /brain-merken, /brain-ingest, /brain-frage, /brain-aufgabe, /brain-person, /brain-adtest, /brain-tagebuch, /brain-pruefen, /brain-ansicht.\n"
             f"- Nie speichern: Passwörter, Schlüssel, Tokens, Bank- und Kartendaten{werte['NIE_ZUSATZ']}.\n{ENDE}\n")
    alt = open(cm, encoding="utf-8").read() if os.path.exists(cm) else ""
    if START in alt and ENDE in alt:
        neu_text = alt[:alt.index(START)] + block + alt[alt.index(ENDE) + len(ENDE):].lstrip("\n")
    else:
        neu_text = alt + ("\n\n" if alt and not alt.endswith("\n\n") else "") + block
    with open(cm, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(neu_text)
    ok(f"Gedächtnis-Block in {cm}")

    # 5. Chronik
    with open(os.path.join(ziel, "_log.md"), "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"\n## [{heute}] einrichten | Brain angelegt\nGerüst, Vorlagen, Cockpit, 3D-Ansicht und {len(gesetzt)} Befehle eingerichtet.\n")
    ok("Chronik _log.md")
    print(f"BRAIN={pfad}")
    print(f"PY={py_befehl()}")
    print("SHOPS=" + "; ".join(shops))


PLUGINS = [("obsidianmd/obsidian-skills", "obsidian-skills", "obsidian"),
           ("nextlevelbuilder/ui-ux-pro-max-skill", "ui-ux-pro-max-skill", "ui-ux-pro-max"),
           ("thedotmack/claude-mem", "thedotmack", "claude-mem"),
           ("heygen-com/hyperframes", "hyperframes", "hyperframes")]
SKILLS = [("hardikpandya/stop-slop", "stop-slop")]


def werkzeuge(a):
    """Installiert die Claude-Erweiterungen, die auch die Ecomone Academy nutzt. Wirksam ab dem nächsten neuen Chat."""
    import subprocess
    import tempfile
    import urllib.request
    import zipfile
    claude = shutil.which("claude")
    if claude:
        for repo, markt, plugin in PLUGINS:
            r1 = subprocess.run([claude, "plugin", "marketplace", "add", repo], capture_output=True, text=True)
            r2 = subprocess.run([claude, "plugin", "install", f"{plugin}@{markt}", "--scope", "user"], capture_output=True, text=True)
            if r2.returncode == 0:
                ok(f"Plugin {plugin} installiert")
            else:
                warn(f"Plugin {plugin}: {(r2.stderr or r2.stdout or r1.stderr).strip()[:160]}")
    else:
        # Ohne CLI: in den Benutzer-Einstellungen anmelden; Claude Code lädt sie beim nächsten Start selbst.
        p = os.path.join(HOME, ".claude", "settings.json")
        daten = {}
        if os.path.exists(p):
            shutil.copy2(p, p + ".sicherung")
            try:
                daten = json.load(open(p, encoding="utf-8"))
            except ValueError:
                print(f"STOP {p} ist kein gültiges JSON, nichts geändert.")
                sys.exit(4)
        mk = daten.setdefault("extraKnownMarketplaces", {})
        ep = daten.setdefault("enabledPlugins", {})
        for repo, markt, plugin in PLUGINS:
            mk.setdefault(markt, {"source": {"source": "github", "repo": repo}})
            ep.setdefault(f"{plugin}@{markt}", True)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(daten, fh, ensure_ascii=False, indent=2)
        ok("Plugins in .claude/settings.json angemeldet (laden beim nächsten neuen Chat): " + ", ".join(x[2] for x in PLUGINS))
    for repo, name in SKILLS:
        ziel = os.path.join(HOME, ".claude", "skills", name)
        if os.path.exists(os.path.join(ziel, "SKILL.md")):
            ok(f"Skill {name} schon da")
            continue
        try:
            with tempfile.TemporaryDirectory() as tmp:
                zp = os.path.join(tmp, "s.zip")
                urllib.request.urlretrieve(f"https://codeload.github.com/{repo}/zip/refs/heads/main", zp)
                with zipfile.ZipFile(zp) as z:
                    z.extractall(tmp)
                quelle = next(os.path.join(tmp, d) for d in os.listdir(tmp) if os.path.isdir(os.path.join(tmp, d)))
                shutil.copytree(quelle, ziel, ignore=shutil.ignore_patterns(".git*", ".github"))
            ok(f"Skill {name} installiert")
        except Exception as e:  # noqa: BLE001
            warn(f"Skill {name} nicht installiert ({e.__class__.__name__}): von github.com/{repo} nach {ziel} kopieren")
    node = shutil.which("node")
    v = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip() if node else ""
    print("NODE=" + (v or "fehlt"))


def obsidian_json():
    if WIN:
        return os.path.join(os.environ.get("APPDATA", os.path.join(HOME, "AppData", "Roaming")), "obsidian", "obsidian.json")
    if platform.system() == "Darwin":
        return os.path.join(HOME, "Library", "Application Support", "obsidian", "obsidian.json")
    return os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.join(HOME, ".config")), "obsidian", "obsidian.json")


def obsidian(a):
    ziel = os.path.abspath(os.path.expanduser(a.brain))
    p = obsidian_json()
    daten = {}
    if os.path.exists(p):
        shutil.copy2(p, p + ".sicherung")
        try:
            daten = json.load(open(p, encoding="utf-8"))
        except ValueError:
            print(f"STOP {p} ist kein gültiges JSON, nichts geändert.")
            sys.exit(4)
    vaults = daten.setdefault("vaults", {})
    for v in vaults.values():
        v.pop("open", None)
    vid = next((k for k, v in vaults.items() if os.path.normcase(os.path.abspath(v.get("path", ""))) == os.path.normcase(ziel)), None)
    if not vid:
        vid = secrets.token_hex(8)
        while vid in vaults:
            vid = secrets.token_hex(8)
    vaults[vid] = {"path": ziel, "ts": int(time.time() * 1000), "open": True}
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(daten, fh, ensure_ascii=False)
    ok(f"Brain bei Obsidian angemeldet ({p})")
    print("URI=obsidian://open?vault=" + urllib.parse.quote(os.path.basename(ziel)) + "&file=Start")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brain")
    b.add_argument("--vorname", required=True)
    b.add_argument("--ss", choices=["ja", "nein"], default="ja", help="ja = Schweiz (ss statt ß)")
    b.add_argument("--ton", default="Du-Form, locker und kurz.")
    b.add_argument("--nie", default="")
    b.add_argument("--shops", default="", help="Shopnamen, mit ; getrennt")
    b.add_argument("--ziel")
    b.add_argument("--ergaenzen", action="store_true")
    b.add_argument("--skills-ersetzen", action="store_true")
    sub.add_parser("werkzeuge")
    o = sub.add_parser("obsidian")
    o.add_argument("--brain", required=True)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    {"brain": brain, "werkzeuge": werkzeuge, "obsidian": obsidian}[a.cmd](a)


if __name__ == "__main__":
    main()
