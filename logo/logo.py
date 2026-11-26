#!/usr/bin/env python3
"""Ecomone Academy – schlichte Shop-Logos als Wortmarke in Poppins, schwarz (Lektion 8.4 «Logo»).

Aufruf:
  python3 logo.py --name "Glowbox" [--ziel "<Ordner>"] [--gewicht SemiBold]

Braucht: fonttools, pillow  (pip install --user fonttools pillow)
Lädt Poppins (SIL Open Font License) einmalig von github.com/google/fonts.
Die Buchstaben werden in Formen umgewandelt: Die SVGs sehen überall gleich aus, auch ohne installierte Schrift.

Pro Gewicht (Medium, SemiBold, Bold) entstehen:
  logo-quer.svg/.png          transparent, schwarz  → Shop-Kopf, Checkout, E-Mails, Rechnungen, Pop-up
  logo-quer-weiss.svg/.png    transparent, weiss    → auf dunklen Flächen (Ad-Abspann, dunkle Bilder)
  logo-quadrat.svg/.png       1080×1080, weiss      → Profilbild Facebook/Instagram, Shop «Allgemein»
  favicon.svg/.png            512×512, transparent  → weisser Kreis mit Anfangsbuchstabe (Browser-Tab)
  favicon-name.svg/.png       512×512, transparent  → weisser Kreis mit ganzem Namen (wie Canva-Vorlage)
Dazu vorschau.html mit allen Varianten nebeneinander.
"""
import argparse
import html
import os
import sys
import urllib.request

try:
    from fontTools.pens.basePen import BasePen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    from PIL import Image, ImageChops, ImageDraw
except ImportError:
    sys.exit("Fehlt: fonttools und pillow. Installieren mit:  <python> -m pip install --user fonttools pillow")

GEWICHTE = ["Medium", "SemiBold", "Bold"]
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-{}.ttf"
SCHWARZ, WEISS = "#000000", "#FFFFFF"


# ---------- Schrift ----------
def schrift(ordner, gewicht):
    os.makedirs(ordner, exist_ok=True)
    p = os.path.join(ordner, f"Poppins-{gewicht}.ttf")
    if not os.path.exists(p) or os.path.getsize(p) < 50000:
        urllib.request.urlretrieve(FONT_URL.format(gewicht), p)
    return TTFont(p)


def kern_tabelle(font):
    """Paar-Unterschneidung aus GPOS (PairPos Format 1 und 2, auch in Extension-Lookups)."""
    paare, klassen = {}, []
    if "GPOS" not in font:
        return paare, klassen
    gpos = font["GPOS"].table
    if not gpos.LookupList:
        return paare, klassen
    for lk in gpos.LookupList.Lookup:
        for st in lk.SubTable:
            typ = lk.LookupType
            if typ == 9:
                typ, st = st.ExtensionLookupType, st.ExtSubTable
            if typ != 2:
                continue
            if st.Format == 1:
                for i, links in enumerate(st.Coverage.glyphs):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = getattr(pvr.Value1, "XAdvance", 0) if pvr.Value1 else 0
                        if v:
                            paare.setdefault((links, pvr.SecondGlyph), v)
            elif st.Format == 2:
                klassen.append(st)
    return paare, klassen


def kern(paare, klassen, a, b):
    if (a, b) in paare:
        return paare[(a, b)]
    for st in klassen:
        if a not in st.Coverage.glyphs:
            continue
        c1 = st.ClassDef1.classDefs.get(a, 0)
        c2 = st.ClassDef2.classDefs.get(b, 0)
        rec = st.Class1Record[c1].Class2Record[c2]
        v = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
        if v:
            return v
    return 0


def setzen(font, text, sperrung):
    """Glyphen mit Abständen: Liste (glyphname, x) in Schrift-Einheiten."""
    cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    paare, klassen = kern_tabelle(font)
    namen = [cmap.get(ord(ch), ".notdef") for ch in text]
    x, out = 0, []
    for i, g in enumerate(namen):
        out.append((g, x))
        x += hmtx[g][0] + sperrung * upm
        if i + 1 < len(namen):
            x += kern(paare, klassen, g, namen[i + 1])
    return out


class Flach(BasePen):
    """Sammelt Konturen als Punktlisten (Kurven fein unterteilt)."""

    def __init__(self, glyphset, schritte=12):
        super().__init__(glyphset)
        self.konturen, self.k, self.s = [], [], schritte

    def _moveTo(self, p):
        self.k = [p]

    def _lineTo(self, p):
        self.k.append(p)

    def _qCurveToOne(self, p1, p2):
        p0 = self.k[-1]
        for i in range(1, self.s + 1):
            t = i / self.s
            self.k.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                           (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))

    def _curveToOne(self, p1, p2, p3):
        p0 = self.k[-1]
        for i in range(1, self.s + 1):
            t, u = i / self.s, 1 - i / self.s
            self.k.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                           u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))

    def _closePath(self):
        if len(self.k) > 2:
            self.konturen.append(self.k)
        self.k = []

    _endPath = _closePath


class Wortmarke:
    def __init__(self, font, text, sperrung):
        self.gs = font.getGlyphSet()
        self.lauf = setzen(font, text, sperrung)
        self.konturen = []
        for g, x in self.lauf:
            p = Flach(self.gs)
            self.gs[g].draw(TransformPen(p, (1, 0, 0, 1, x, 0)))
            self.konturen += p.konturen
        if not self.konturen:
            sys.exit("Der Name ergibt keine sichtbaren Zeichen.")
        xs = [q[0] for k in self.konturen for q in k]
        ys = [q[1] for k in self.konturen for q in k]
        self.box = (min(xs), min(ys), max(xs), max(ys))  # Schrift-Einheiten, y nach oben

    def b(self):
        return self.box[2] - self.box[0]

    def h(self):
        return self.box[3] - self.box[1]

    def svg_pfad(self, s, ox, oy):
        """Pfad, so skaliert, dass die Box-Ecke links oben bei (ox, oy) liegt."""
        pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        x0, _, _, y1 = self.box
        for g, x in self.lauf:
            self.gs[g].draw(TransformPen(pen, (s, 0, 0, -s, ox + (x - x0) * s, oy + y1 * s)))
        return pen.getCommands()

    def maske(self, breite, hoehe, s, ox, oy, aa=4):
        """Kantenglatte Graustufen-Maske (Gerade-Ungerade-Füllung wie in Schriften)."""
        W, H = breite * aa, hoehe * aa
        m = Image.new("1", (W, H), 0)
        x0, _, _, y1 = self.box
        for k in self.konturen:
            e = Image.new("1", (W, H), 0)
            ImageDraw.Draw(e).polygon([((ox + (x - x0) * s) * aa, (oy + (y1 - y) * s) * aa) for x, y in k], fill=1)
            m = ImageChops.logical_xor(m, e)
        return m.convert("L").resize((breite, hoehe), Image.LANCZOS)


# ---------- Ausgaben ----------
def svg(breite, hoehe, inhalt):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}">'
            f"{inhalt}</svg>\n")


def png(pfad, breite, hoehe, schichten):
    """schichten: Liste (maske, farbe) über transparentem Grund."""
    bild = Image.new("RGBA", (breite, hoehe), (0, 0, 0, 0))
    for maske, farbe in schichten:
        f = Image.new("RGBA", (breite, hoehe), farbe)
        bild = Image.composite(f, bild, maske)
    bild.save(pfad, optimize=True)


def kreis_maske(n, aa=4):
    m = Image.new("L", (n * aa, n * aa), 0)
    ImageDraw.Draw(m).ellipse((0, 0, n * aa - 1, n * aa - 1), fill=255)
    return m.resize((n, n), Image.LANCZOS)


def flaeche(n):
    return Image.new("L", (n, n), 255)


def einpassen(wm, breite, hoehe, max_b, max_h):
    s = min(max_b / wm.b(), max_h / wm.h())
    return s, (breite - wm.b() * s) / 2, (hoehe - wm.h() * s) / 2


def schreib(pfad, text):
    with open(pfad, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def erzeugen(wm, erster, ordner):
    os.makedirs(ordner, exist_ok=True)
    dateien = {}
    # 1. Querformat transparent: Schrift füllt die Fläche, kleiner Rand
    H = 400
    s = (H * 0.8) / wm.h()
    B = round(wm.b() * s + H * 0.2)
    ox, oy = (B - wm.b() * s) / 2, H * 0.1
    for farbe, name in ((SCHWARZ, "logo-quer"), (WEISS, "logo-quer-weiss")):
        schreib(os.path.join(ordner, name + ".svg"), svg(B, H, f'<path fill="{farbe}" d="{wm.svg_pfad(s, ox, oy)}"/>'))
        f = 3000 / B
        png(os.path.join(ordner, name + ".png"), 3000, round(H * f), [(wm.maske(3000, round(H * f), s * f, ox * f, oy * f), farbe)])
        dateien[name] = name
    # 2. Quadrat 1080, weiss, Name sicher im Kreis (Facebook schneidet rund zu)
    N = 1080
    s, ox, oy = einpassen(wm, N, N, N * 0.68, N * 0.24)
    schreib(os.path.join(ordner, "logo-quadrat.svg"),
            svg(N, N, f'<rect width="{N}" height="{N}" fill="{WEISS}"/><path fill="{SCHWARZ}" d="{wm.svg_pfad(s, ox, oy)}"/>'))
    png(os.path.join(ordner, "logo-quadrat.png"), N, N, [(flaeche(N), WEISS), (wm.maske(N, N, s, ox, oy), SCHWARZ)])
    # 3. Favicons 512: weisser Kreis, transparent aussen
    F = 512
    for wm_f, name, mb, mh in ((erster, "favicon", F * 0.5, F * 0.5), (wm, "favicon-name", F * 0.7, F * 0.3)):
        s, ox, oy = einpassen(wm_f, F, F, mb, mh)
        schreib(os.path.join(ordner, name + ".svg"),
                svg(F, F, f'<circle cx="{F / 2}" cy="{F / 2}" r="{F / 2}" fill="{WEISS}"/><path fill="{SCHWARZ}" d="{wm_f.svg_pfad(s, ox, oy)}"/>'))
        png(os.path.join(ordner, name + ".png"), F, F, [(kreis_maske(F), WEISS), (wm_f.maske(F, F, s, ox, oy), SCHWARZ)])
    return ordner


VORSCHAU = """<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logo {name}</title><style>
:root{{--bg:#f4f4f6;--fg:#111;--mut:#6b6b76;--card:#fff;--line:#e4e4ea}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#0d0d12;--fg:#f2f2f5;--mut:#9a9aa8;--card:#17171f;--line:#2a2a35}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif;padding:32px 16px}}
main{{max-width:1100px;margin:0 auto}}h1{{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}}p.sub{{color:var(--mut);margin:0 0 28px}}
.v{{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:22px;margin-bottom:22px}}
.v h2{{font-size:17px;margin:0 0 14px;display:flex;gap:10px;align-items:center}}.v h2 span{{font-size:12px;font-weight:600;background:#111;color:#fff;border-radius:99px;padding:3px 10px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}
.t{{border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:10px}}
.t small{{color:var(--mut);font-size:12.5px}}.box{{border-radius:10px;display:grid;place-items:center;min-height:120px;padding:16px}}
.box img{{max-width:100%;max-height:90px}}.weiss{{background:#fff;border:1px solid #eee}}.dunkel{{background:#111}}
.kreis img{{width:120px;height:120px;max-height:none;border-radius:50%;box-shadow:0 0 0 1px #ddd}}
.tab{{background:#dfe3e8;border-radius:10px;padding:10px;display:flex;gap:8px;align-items:center;color:#222;font-size:13px}}
.tab .r{{background:#fff;border-radius:8px 8px 0 0;padding:6px 12px;display:flex;gap:8px;align-items:center}}.tab img{{width:16px;height:16px}}
</style></head><body><main>
<h1>Logo «{name}»</h1><p class="sub">Schlichte Wortmarke in Poppins, immer schwarz (Ecomone Academy, Lektion 8.4). Drei Strichstärken zur Wahl. Empfohlen: <b>SemiBold</b>.</p>
{karten}
</main></body></html>
"""


def datei_uri(pfad):
    import base64
    with open(pfad, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()


def vorschau(name, ziel, gewichte):
    karten = ""
    for g in gewichte:
        u = {n: datei_uri(os.path.join(ziel, g, n + ".svg")) for n in ("logo-quer", "logo-quer-weiss", "logo-quadrat", "favicon", "favicon-name")}
        karten += f"""<section class="v"><h2>{g}{'<span>Empfohlen</span>' if g == 'SemiBold' else ''}</h2><div class="grid">
<div class="t"><div class="box weiss"><img src="{u['logo-quer']}" alt=""></div><small>Querformat transparent: Shop-Kopf, Checkout, E-Mails, Rechnungen, Pop-up</small></div>
<div class="t"><div class="box dunkel"><img src="{u['logo-quer-weiss']}" alt=""></div><small>Weiss für dunkle Flächen, z. B. Abspann der Video-Ads</small></div>
<div class="t"><div class="box weiss kreis"><img src="{u['logo-quadrat']}" alt=""></div><small>Quadrat 1080 px: Profilbild Facebook und Instagram (so rund zugeschnitten)</small></div>
<div class="t"><div class="tab"><div class="r"><img src="{u['favicon']}" alt="">{html.escape(name)}</div><div class="r"><img src="{u['favicon-name']}" alt="">Name</div></div><small>Favicon im Browser-Tab: Anfangsbuchstabe (gut lesbar) oder ganzer Name</small></div>
</div></section>"""
    schreib(os.path.join(ziel, "vorschau.html"), VORSCHAU.format(name=html.escape(name), karten=karten))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="Shopname, genau so geschrieben, wie er im Logo stehen soll")
    ap.add_argument("--ziel", help="Ausgabeordner (Standard: ~/Ecomone Logos/<Name>)")
    ap.add_argument("--gewicht", choices=GEWICHTE, help="nur dieses Gewicht erzeugen (Standard: alle drei)")
    ap.add_argument("--fertig", choices=GEWICHTE, default="SemiBold", help="dieses Gewicht als «Fertig» bereitlegen (Standard SemiBold)")
    ap.add_argument("--sperrung", type=float, default=-0.01, help="Buchstabenabstand in em (Standard -0.01)")
    ap.add_argument("--fonts", default=os.path.join(os.path.expanduser("~"), ".ecomone-fonts"))
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    name = a.name.strip()
    if not name:
        sys.exit("Name fehlt.")
    sicher = "".join("-" if c in '\\/:*?"<>|' else c for c in name).strip(" .")
    ziel = os.path.abspath(os.path.expanduser(a.ziel or os.path.join("~", "Ecomone Logos", sicher)))
    gewichte = [a.gewicht] if a.gewicht else GEWICHTE
    for g in gewichte:
        font = schrift(a.fonts, g)
        fehlt = [c for c in name if c != " " and ord(c) not in font.getBestCmap()]
        if fehlt:
            sys.exit("Diese Zeichen hat Poppins nicht: " + " ".join(fehlt))
        wm = Wortmarke(font, name, a.sperrung)
        erster = Wortmarke(font, name.lstrip()[0], 0)
        erzeugen(wm, erster, os.path.join(ziel, g))
        print(f"✓ {g}: {os.path.join(ziel, g)}")
    vorschau(name, ziel, gewichte)
    if a.fertig in gewichte:
        import shutil
        quelle, fertig = os.path.join(ziel, a.fertig), os.path.join(ziel, "Fertig")
        if os.path.isdir(fertig):
            shutil.rmtree(fertig)
        os.makedirs(fertig)
        for alt, neu in (("logo-quer", "Logo Shop (transparent)"), ("logo-quer-weiss", "Logo weiss für dunkle Flächen (transparent)"),
                         ("logo-quadrat", "Profilbild Facebook und Instagram"), ("favicon", "Favicon Anfangsbuchstabe"),
                         ("favicon-name", "Favicon Name")):
            for end in (".png", ".svg"):
                shutil.copy2(os.path.join(quelle, alt + end), os.path.join(fertig, f"{sicher} – {neu}{end}"))
        print(f"FERTIG={fertig} ({a.fertig})")
    print(f"VORSCHAU={os.path.join(ziel, 'vorschau.html')}")


if __name__ == "__main__":
    main()
