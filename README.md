# Ecomone Second Brain – Bausatz

Persönliches Second Brain für Studenten der **Ecomone Academy**, nach Andrej Karpathys «LLM-Wiki»: Du sammelst und fragst, Claude schreibt, verknüpft und hält alles aktuell. Obsidian zeigt die Notizen, eine 3D-Ansicht zeigt dein Brain als leuchtendes Gehirn.

Du musst hier nichts von Hand tun. Den Masterprompt aus dem Kurs in Claude (Desktop-App, Tab «Code») einfügen, Claude lädt diesen Bausatz und richtet alles ein.

## Für Claude: Ablauf

```
<PY> einrichten.py brain --vorname "<Vorname>" --ss ja|nein --ton "<Ansprache>" --nie "<nie speichern>" --shops "<Shop A; Shop B>"
# danach die persönlichen Seiten schreiben (siehe Masterprompt, Schritt 4)
<PY> "<Brain>/.brain/ansicht.py"     # Index + 3D-Ansicht «Mein Brain.html»
<PY> "<Brain>/.brain/pruefen.py"     # bis «ALLES OK»
<PY> einrichten.py werkzeuge                     # Plugins + stop-slop, aktiv ab dem nächsten neuen Chat
<PY> einrichten.py obsidian --brain "<Brain>"   # Obsidian vorher beenden
```

`<PY>` = Mac `python3 -I`, Windows `py -3 -I`. Nur Python-Standardbibliothek, keine Pakete.

## Inhalt

| Pfad | Was |
|---|---|
| `einrichten.py` | legt das Brain an, installiert die Befehle, meldet es bei Obsidian an. Überschreibt nie etwas. |
| `vorlage/` | Gerüst des Brains: Regeln (`CLAUDE.md`, `_CLAUDE.md`), Cockpit, Vorlagen, Obsidian-Einstellungen |
| `vorlage/.brain/ansicht-vorlage.html` | die 3D-Ansicht (eine Datei, keine Bibliotheken) |
| `vorlage/.brain/ansicht.py` | baut `Mein Brain.html` aus den Notizen und erneuert `_index.md` |
| `vorlage/.brain/index.py` | erzeugt `_index.md` |
| `vorlage/.brain/pruefen.py` | prüft das Brain, meldet ✓/✗ |
| `skills/` | 9 Claude-Befehle: brain-merken, brain-ingest, brain-frage, brain-aufgabe, brain-person, brain-adtest, brain-tagebuch, brain-pruefen, brain-ansicht |

## Werkzeuge, die mitinstalliert werden

| Werkzeug | Quelle | Wofür |
|---|---|---|
| Obsidian-Skills | obsidianmd/obsidian-skills | Claude schreibt sauberes Obsidian (Markdown, Bases, Canvas) |
| UI/UX Pro Max | nextlevelbuilder/ui-ux-pro-max-skill | Design: Shop-Seiten, Banner, Farben, Schriften |
| claude-mem | thedotmack/claude-mem | Gedächtnis über alle Chats (braucht Node.js 20+) |
| HyperFrames | heygen-com/hyperframes | Videos und Animationen aus Code, z. B. für Ads |
| stop-slop | hardikpandya/stop-slop | Texte ohne typische KI-Floskeln |

Alle Open Source (MIT bzw. Apache-2.0). Mit dem Befehl `claude` werden sie direkt installiert, sonst in `~/.claude/settings.json` angemeldet; Claude Code lädt sie beim nächsten neuen Chat.

## Struktur des Brains

`wiki/ich` · `wiki/privat` · `wiki/business` · `wiki/shops/<Shop>/{produkte,ads,lieferanten}` · `wiki/projekte` · `wiki/aufgaben` · `wiki/personen` · `wiki/themen` · `wiki/entscheidungen` · `wiki/synthesen` · `sources/` (unveränderlich) · `journal/` · `inbox/` · `archive/`

Dein Brain bleibt auf deinem Computer. Nur die 3D-Ansicht kann Claude zusätzlich als privates Artifact in deinem Claude-Konto veröffentlichen; sehen kann es nur, wem du es freigibst.

© Ecomone GmbH · Ecomone Academy
