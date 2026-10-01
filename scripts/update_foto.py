#!/usr/bin/env python3
"""
Aggiorna data/foto.json con le ultime gite pubblicate sul portale Droptour.

Legge via FTP l'elenco delle cartelle  <FTP_BASE>/<anno>/<AAAA-MM-GG-titolo---luogo>/thumbnails/
e costruisce gli indirizzi pubblici HTTPS delle foto:
  miniatura   <PUBLIC_BASE>/<anno>/<cartella>/thumbnails/<file>
  foto grande <PUBLIC_BASE>/<anno>/<cartella>/mysize/<file>

Le immagini NON vengono copiate: restano su ssl.dropnet.ch.

Titolo, luogo e testo:
  1. data/foto-overrides.json  (correzioni manuali, chiave = nome cartella)  ← vince sempre
  2. API Droptour              (TODO: da collegare, vedi fetch_droptour())
  3. nome della cartella       (fallback: "valsolda-bassa-500-m---italia" → "Valsolda Bassa 500 m", "Italia")

Variabili d'ambiente (in GitHub: Settings › Secrets and variables › Actions):
  FTP_HOST       obbligatoria   es. ftp.dropnet.ch
  FTP_USER       obbligatoria
  FTP_PASSWORD   obbligatoria
  FTP_BASE       percorso FTP della cartella delle gite   (default: /casticino/dropbox/photo/gite)
  FTP_TLS        "1" per FTPS esplicito, "0" per FTP semplice (default: 1)
  PUBLIC_BASE    URL pubblico corrispondente a FTP_BASE   (default: https://ssl.dropnet.ch/casticino/dropbox/photo/gite)
  MAX_ALBUMS     quante gite tenere                      (default: 15)
"""
import datetime as dt
import ftplib
import json
import os
import posixpath
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "foto.json")
OVERRIDES = os.path.join(ROOT, "data", "foto-overrides.json")

FTP_BASE = os.environ.get("FTP_BASE", "/casticino/dropbox/photo/gite").rstrip("/")
PUBLIC_BASE = os.environ.get("PUBLIC_BASE", "https://ssl.dropnet.ch/casticino/dropbox/photo/gite").rstrip("/")
MAX_ALBUMS = int(os.environ.get("MAX_ALBUMS", "15"))

FOLDER_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)$")
IMAGE_RE = re.compile(r"\.(jpe?g|png|webp|gif)$", re.I)
SMALL_WORDS = {"di", "del", "della", "dei", "delle", "da", "dal", "dalla", "e", "ed", "al", "alla", "ai", "in", "sul", "sulla", "per", "con", "la", "il", "lo", "le", "gli", "m"}
REGIONS = {"ti": "TI", "gr": "GR", "ur": "UR", "vs": "VS", "be": "BE", "sz": "SZ", "gl": "GL", "ow": "OW", "nw": "NW", "lu": "LU", "sg": "SG"}


# ------------------------------------------------------------------ titoli dai nomi cartella
def pretty_title(slug):
    words = [w for w in slug.split("-") if w]
    out = []
    for i, w in enumerate(words):
        if i > 0 and w in SMALL_WORDS:
            out.append(w)
        elif w.isdigit():
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def pretty_place(slug):
    slug = slug.strip("-")
    if slug in REGIONS:
        return REGIONS[slug]
    return " ".join(w[:1].upper() + w[1:] for w in slug.split("-") if w)


def parse_folder(name):
    m = FOLDER_RE.match(name)
    if not m:
        return None
    y, mo, d, rest = m.groups()
    try:
        date = dt.date(int(y), int(mo), int(d))
    except ValueError:
        return None
    title_slug, _, place_slug = rest.partition("---")
    return {"date": date.isoformat(), "title": pretty_title(title_slug), "place": pretty_place(place_slug) if place_slug else ""}


# ------------------------------------------------------------------ FTP
def connect():
    host = os.environ.get("FTP_HOST")
    user = os.environ.get("FTP_USER")
    pwd = os.environ.get("FTP_PASSWORD")
    if not (host and user and pwd):
        sys.exit("Mancano FTP_HOST, FTP_USER o FTP_PASSWORD.")
    use_tls = os.environ.get("FTP_TLS", "1") != "0"
    ftp = ftplib.FTP_TLS(host, timeout=60) if use_tls else ftplib.FTP(host, timeout=60)
    ftp.login(user, pwd)
    if use_tls:
        ftp.prot_p()
    ftp.encoding = "utf-8"
    return ftp


def listdir(ftp, path):
    """Nomi (non percorsi) contenuti in una cartella; [] se non esiste."""
    try:
        names = ftp.nlst(path)
    except (ftplib.error_perm, ftplib.error_temp) as e:  # alcuni server rispondono 450 invece di 550
        print(f"  {path}: {e}", file=sys.stderr)
        return []
    return sorted({posixpath.basename(n.rstrip("/")) for n in names} - {".", ".."})


def collect(ftp, today=None):
    today = today or dt.date.today()
    folders = []
    for year in (today.year, today.year - 1):
        for name in listdir(ftp, f"{FTP_BASE}/{year}"):
            info = parse_folder(name)
            if info:
                folders.append((info["date"], str(year), name, info))
    folders.sort(key=lambda t: (t[0], t[2]), reverse=True)
    print(f"{len(folders)} cartelle di gite trovate in {FTP_BASE}.")

    albums = []
    for _, year, name, info in folders:
        if len(albums) >= MAX_ALBUMS:
            break
        files = [f for f in listdir(ftp, f"{FTP_BASE}/{year}/{name}/thumbnails") if IMAGE_RE.search(f)]
        if not files:
            # cartella ancora vuota o senza miniature: la riprendiamo al prossimo giro
            print(f"  {name}: nessuna miniatura; contenuto: {listdir(ftp, f'{FTP_BASE}/{year}/{name}')[:10]}")
            continue
        base = f"{PUBLIC_BASE}/{year}/{name}"
        albums.append({
            "id": name,
            **info,
            "text": "",
            "link": "",
            "photos": [{"thumb": f"{base}/thumbnails/{f}", "large": f"{base}/mysize/{f}"} for f in files],
        })
    return albums


# ------------------------------------------------------------------ testi
def fetch_droptour(albums):
    """
    TODO: collegare l'API XML di Droptour per avere titolo esatto, testo del resoconto e link alla gita.
    Deve restituire {id_cartella: {"title": ..., "place": ..., "text": ..., "link": ...}}.
    Abbinamento suggerito: stessa data e titolo simile al nome della cartella.
    """
    return {}


def load_overrides():
    if not os.path.exists(OVERRIDES):
        return {}
    with open(OVERRIDES, encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def merge(albums, *sources):
    for a in albums:
        for src in sources:
            for k, v in src.get(a["id"], {}).items():
                if k in ("title", "place", "text", "link") and v:
                    a[k] = v
    return albums


# ------------------------------------------------------------------ main
def write_if_changed(albums):
    old = None
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
    if old and old.get("albums") == albums:
        print("Nessuna novità: foto.json invariato.")
        return False
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "albums": albums},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"foto.json aggiornato: {len(albums)} gite, {sum(len(a['photos']) for a in albums)} foto.")
    return True


def main():
    ftp = connect()
    try:
        albums = collect(ftp)
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()
    if not albums:
        sys.exit("Nessuna gita con foto trovata: foto.json non modificato.")
    albums = merge(albums, fetch_droptour(albums), load_overrides())
    write_if_changed(albums)


if __name__ == "__main__":
    main()
