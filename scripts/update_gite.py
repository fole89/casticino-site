"""Programma gite da Droptour -> data/gite.json (copia di riserva per gite.html, gita.html, la ricerca e chi non ha JavaScript).

La pagina gite.html legge comunque le gite in tempo reale dalla stessa interfaccia pubblica di Droptour (assets/gite.js);
questo file serve solo come punto di partenza. Iscrizioni e login restano su Droptour.
Per ogni gita si salva anche la scheda di dettaglio («scheda»: righe [etichetta, HTML]) ridotta come fa righeScheda()
in assets/gite.js (tenerle allineate): gita.html la mostra subito e la sostituisce con quella in tempo reale appena
Droptour risponde, che a volte è lento. Se una scheda non si riesce a leggere resta quella del giorno prima.
Dall'interfaccia si prendono solo i dati della gita e il nome dei capigita: mai e-mail o altri dati personali
(le righe «Capogita» della scheda si saltano).
Solo libreria standard. Uso: python scripts/update_gite.py   (poi pages.py gite.html cerca.html)"""
import json, os, re, sys, urllib.parse, urllib.request
from html import escape, unescape
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "gite.json")
API = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItems&limit=500&language=it"
DETTAGLIO = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItem&language=it&item_id="
ETICHETTE_FUORI = {"Data", "Gruppo", "Tipo di attività", "Tipo/Aggiunta", "Iscrizione"}  # già nell'intestazione della pagina

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
        "link": it.get("link", "") if it.get("link", "").startswith("https://ssl.dropnet.ch/") else "",
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


def leggi(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "casticino-site (aggiornamento programma gite)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def link_buono(href):
    """Link della scheda da tenere (file allegati come i PDF, pagine esterne): quelli interni all'interfaccia
    Droptour (scheda del capogita, scala delle esigenze) restano solo testo. Come linkBuono() in gite.js."""
    u = urllib.parse.urlsplit(urllib.parse.urljoin("https://ssl.dropnet.ch/", unescape(href)))
    if u.scheme not in ("http", "https") or "/api/" in u.path:
        return ""
    return urllib.parse.urlunsplit((u.scheme, u.netloc, urllib.parse.quote(u.path, safe="/%:@!$&'()*+,;=~-._"), u.query, ""))


def con_link(t):
    """Testo già sicuro (escape) con gli indirizzi web resi cliccabili, come conLink() in gite.js."""
    t = re.sub(r"\b(https?://[^\s<]+[^\s<.,;:)])", r'<a href="\1" rel="noopener">\1</a>', t)
    return re.sub(r"(^|[\s(])(www\.[^\s<]+[^\s<.,;:)])", r'\1<a href="https://\2" rel="noopener">\2</a>', t)


SEGNO = re.compile(r"\x01(\d+)\x02")  # segnaposto di un link buono, rimesso come <a> alla fine


def scheda(html):
    """Righe [etichetta, HTML sicuro] della tabella #droptours-detail, ridotte a testo con i soli link buoni."""
    m = re.search(r'<table id="droptours-detail".*?</table>', html, flags=re.S)
    out = []
    for riga in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(0) if m else "", flags=re.S):
        celle = re.findall(r"<td[^>]*>(.*?)</td>", riga, flags=re.S)
        if len(celle) < 2:
            continue
        et = testo(celle[0]).removesuffix(":").strip()
        if not et or et.startswith("Capogita") or et in ETICHETTE_FUORI:
            continue
        link = []

        def segnaposto(a):
            href = link_buono(a.group(1))
            nome = re.sub(r"\.pdf$", "", testo(a.group(2)), flags=re.I)  # «Gita 44 Castagnata.pdf» -> «Gita 44 Castagnata»
            if not href or not nome:
                return a.group(0)
            link.append(f'<a href="{escape(href)}" rel="noopener">{escape(nome)}</a>')
            return f"\x01{len(link) - 1}\x02"

        parti = []
        for c in celle[1:]:
            c = re.sub(r"<(script|style)\b.*?</\1>|<img[^>]*>", "", c, flags=re.S | re.I)
            c = re.sub(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', segnaposto, c, flags=re.S | re.I)
            c = re.sub(r"[\r\n]+", " ", c)            # gli a capo del sorgente sono solo spazi:
            c = re.sub(r"<br\s*/?>", "\n", c, flags=re.I)  # contano solo i <br>
            parti.append(unescape(re.sub(r"<[^>]+>", "", c)))
        righe = [re.sub(r"[ \t\xa0]+", " ", r).strip() for r in "\n".join(parti).split("\n")]
        righe = [r for r in righe if not re.fullmatch(r"(Cond|Tecn)\.", r)]  # esigenza senza valore
        t = re.sub(r"\n{3,}", "\n\n", "\n".join(righe)).strip()
        if not t:
            continue
        pezzi = re.split(r"(\x01\d+\x02)", t)
        t = "".join(link[int(SEGNO.fullmatch(p).group(1))] if SEGNO.fullmatch(p) else con_link(escape(p))
                    for p in pezzi)
        out.append([et, t])
    return out


def main():
    root = ET.fromstring(leggi(API))
    # solo gite con un numero vero: finisce negli id e negli indirizzi delle pagine
    gite = [gita(it) for it in root.iter("item") if it.get("type") == "tour" and (it.get("id") or "").isascii() and (it.get("id") or "").isdigit()]
    if not gite:
        sys.exit("Nessuna gita da Droptour: data/gite.json resta com'è.")
    gite.sort(key=lambda g: (g["dal"], g["titolo"]))
    try:
        vecchio = json.load(open(OUT, encoding="utf-8"))
    except (OSError, ValueError):
        vecchio = None
    prima = {g["id"]: g.get("scheda") for g in (vecchio or {}).get("gite", [])}
    for g in gite:
        try:
            g["scheda"] = scheda(leggi(DETTAGLIO + urllib.parse.quote(g["id"]), timeout=15).decode("utf-8", "replace"))
        except Exception as e:  # Droptour lento o irraggiungibile: resta la scheda del giorno prima
            print(f"scheda {g['id']} non letta ({e})")
            if prima.get(g["id"]):
                g["scheda"] = prima[g["id"]]
    nuovo = {"gite": gite}
    if vecchio == nuovo:
        print(f"Nessun cambiamento ({len(gite)} gite).")
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nuovo, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"scritto data/gite.json ({len(gite)} gite)")


if __name__ == "__main__":
    main()
