"""Programma gite da Droptour -> data/gite.json (copia di riserva per gite.html, la ricerca e chi non ha JavaScript).

La pagina gite.html legge comunque le gite in tempo reale dalla stessa interfaccia pubblica di Droptour (assets/gite.js);
questo file serve solo come punto di partenza. Iscrizioni, login e dettagli restano su Droptour.
Dall'interfaccia si prendono solo i dati della gita e il nome dei capigita: mai e-mail o altri dati personali.
Solo libreria standard. Uso: python scripts/update_gite.py   (poi pages.py gite.html cerca.html)"""
import json, os, re, sys, urllib.request
from html import unescape
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "gite.json")
API = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItems&limit=500&language=it"

STATO = {"3": "completa", "2": "annullata"}  # tour_status di Droptour


def data(v):
    """AAAA-MM-GG, oppure "" per le date vuote di Droptour (0000-00-00)."""
    return v if v and not v.startswith("0000") else ""


def testo(v):
    """Testo semplice: senza tag HTML e spazi doppi."""
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", v or ""))).strip()


def numero(v):
    try:
        return int(float(v or 0))
    except ValueError:
        return 0


def gita(it):
    capigita = [testo(f"{a.get('fname', '')} {a.get('lname', '')}") for a in it.findall("address")
                if a.get("type", "").startswith("tour_guide")]
    return {
        "id": it.get("id"),
        "titolo": testo(it.get("name")),
        "link": it.get("link", ""),
        "dal": data(it.get("date_start")),
        "al": data(it.get("date_end")),
        "tipo": testo(it.get("category_description")),
        "sigla": it.get("category", ""),
        "gruppi": [g for g in (it.get("group") or "").split("|") if g],
        "capigita": [c for c in capigita if c] or ([testo(it.get("author"))] if it.get("author") else []),
        "cond": it.get("requirements_kond", ""),
        "tecn": it.get("requirements_techn", ""),
        "descrizione": testo(it.get("description")),
        "iscrizione": it.get("register_type") != "0",
        "iscrizione_dal": data(it.get("register_start_date")),
        "iscrizione_al": data(it.get("register_end_date")),
        "modalita": testo(it.get("register_formalities")),
        "iscritti": numero(it.get("participants_nr")),
        "posti": numero(it.get("participants_max")),
        "stato": STATO.get(it.get("tour_status"), ""),
    }


def main():
    req = urllib.request.Request(API, headers={"User-Agent": "casticino-site (aggiornamento programma gite)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        root = ET.fromstring(r.read())
    gite = [gita(it) for it in root.iter("item") if it.get("type") == "tour"]
    if not gite:
        sys.exit("Nessuna gita da Droptour: data/gite.json resta com'è.")
    gite.sort(key=lambda g: (g["dal"], g["titolo"]))
    nuovo = {"gite": gite}
    try:
        vecchio = json.load(open(OUT, encoding="utf-8"))
    except (OSError, ValueError):
        vecchio = None
    if vecchio == nuovo:
        print(f"Nessun cambiamento ({len(gite)} gite).")
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nuovo, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"scritto data/gite.json ({len(gite)} gite)")


if __name__ == "__main__":
    main()
