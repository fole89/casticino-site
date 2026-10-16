"""Traduce in tedesco, francese e inglese, con DeepL, i testi che la redazione scrive in italiano: l'avviso in cima al sito
(data/avviso.json), gli avvisi delle capanne (data/avvisi-capanne/*.json) e il testo dei guardiani
(data/testi/capanne/*.json, campo «guardiani», Markdown).

Gira in .github/workflows/news.yml prima di rigenerare le pagine. Regole, campo per campo (es. testo → testo_de):
- campo tradotto vuoto e italiano presente → si traduce;
- campo tradotto automaticamente (impronta in «traduzioni») e italiano cambiato → si ritraduce;
- campo cambiato a mano dopo la traduzione automatica (o scritto a mano) → resta com'è; per riavere la traduzione
  automatica basta svuotarlo;
- italiano svuotato → si svuota anche la traduzione automatica.
«traduzioni» tiene, per ogni campo tradotto, l'impronta dell'italiano e quella della traduzione («aaaa:bbbb»); in
admin/config.yml è un campo nascosto, così la redazione lo conserva al salvataggio.

Chiave: variabile d'ambiente DEEPL_KEY (secret API_DEEPL su GitHub). Senza chiave, o se DeepL non risponde, non cambia
niente e il sito mostra l'italiano dove manca la traduzione: la pubblicazione non si ferma.

    DEEPL_KEY=… python scripts/traduci.py            # traduce quello che serve
    python scripts/traduci.py --adotta               # segna come automatiche le traduzioni già presenti (una volta)

Solo libreria standard.
"""
import glob
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINGUE = {"de": "DE", "fr": "FR", "en": "EN-GB"}

# file → campi italiani da tradurre
FILE = [(os.path.join(RADICE, "data", "avviso.json"), ["testo"])]
FILE += [(f, ["testo"]) for f in sorted(glob.glob(os.path.join(RADICE, "data", "avvisi-capanne", "*.json")))]
FILE += [(f, ["guardiani"]) for f in sorted(glob.glob(os.path.join(RADICE, "data", "testi", "capanne", "*.json")))]

# nomi propri che DeepL non deve tradurre («Capanna Campo Tencia» resta così anche in tedesco, francese e inglese, come nel sito)
NOMI = re.compile(r"\b(?:Capanna|Capanne|Baita)(?:\s+(?:del|della|dei|di|d’|d')?\s*[A-ZÀ-Ý][\w’'-]*)+")


def impronta(s):
    # senza segni Markdown, barre inverse e spazi: l'editor della redazione può riscrivere la formattazione (* ↔ _,
    # elenchi) senza che il testo cambi, e non deve sembrare una correzione a mano
    return hashlib.sha1(re.sub(r"[\s*_\\#>+-]", "", s).encode("utf-8")).hexdigest()[:12]


# --- Markdown / testo → XML per DeepL e ritorno ------------------------------------------------------------------
# Si traduce riga per riga (così a capo, paragrafi ed elenchi restano identici). In ogni riga grassetto, corsivo e
# link diventano tag che DeepL sposta con le parole; indirizzi, e-mail e nomi delle capanne vanno in <k>, che DeepL
# lascia com'è.
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
INDIRIZZO = re.compile(r"(?:https?://|www\.)[^\s<]+[^\s<.,;:!?)]|[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
ELENCO = re.compile(r"^(\s*(?:[-*+]|\d+[.)])\s+|\s*)(.*)$")


def a_xml(riga):
    pezzi = []

    def tieni(s):
        pezzi.append(s)
        return f"\x00{len(pezzi) - 1}\x00"

    riga = LINK.sub(lambda m: tieni(f'<l u="{html.escape(m.group(2))}">') + m.group(1) + tieni("</l>"), riga)
    riga = INDIRIZZO.sub(lambda m: tieni("<k>" + html.escape(m.group(0), quote=False) + "</k>"), riga)
    riga = NOMI.sub(lambda m: tieni("<k>" + html.escape(m.group(0), quote=False) + "</k>"), riga)
    riga = html.escape(riga, quote=False)
    riga = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", riga)
    riga = re.sub(r"(?<![\w*])[*_](?=\S)(.+?)(?<=\S)[*_](?![\w*])", r"<i>\1</i>", riga)
    return re.sub("\x00(\\d+)\x00", lambda m: pezzi[int(m.group(1))], riga)


def da_xml(riga):
    riga = re.sub(r'<l u="([^"]*)">(.*?)</l>', lambda m: f"[{m.group(2)}]({html.unescape(m.group(1))})", riga)
    riga = re.sub(r"</?k>", "", riga)
    riga = re.sub(r"</?b>", "**", riga)
    riga = re.sub(r"</?i>", "*", riga)
    return html.unescape(riga)


def deepl(chiave, testi, lingua):
    url = "https://api-free.deepl.com/v2/translate" if chiave.endswith(":fx") else "https://api.deepl.com/v2/translate"
    dati = json.dumps({"text": testi, "source_lang": "IT", "target_lang": LINGUE[lingua], "tag_handling": "xml",
                       "ignore_tags": ["k"], "preserve_formatting": True}).encode("utf-8")
    req = urllib.request.Request(url, data=dati, headers={"Authorization": f"DeepL-Auth-Key {chiave}",
                                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return [t["text"] for t in json.load(r)["translations"]]


def traduci(chiave, testo, lingua):
    righe = [ELENCO.match(r).groups() for r in testo.split("\n")]
    da_fare = [i for i, (_, corpo) in enumerate(righe) if corpo.strip()]
    tradotte = deepl(chiave, [a_xml(righe[i][1]) for i in da_fare], lingua) if da_fare else []
    fuori = [inizio + corpo for inizio, corpo in righe]
    for i, t in zip(da_fare, tradotte):
        fuori[i] = righe[i][0] + da_xml(t)
    out = "\n".join(fuori)
    return out.replace("ß", "ss") if lingua == "de" else out   # tedesco svizzero


def main():
    adotta = "--adotta" in sys.argv
    chiave = os.environ.get("DEEPL_KEY", "").strip()
    if not chiave and not adotta:
        print("DEEPL_KEY mancante: nessuna traduzione automatica (il sito mostra l'italiano dove manca).")
        return
    errori = 0
    for percorso, campi in FILE:
        if not os.path.exists(percorso):
            continue
        with open(percorso, encoding="utf-8") as f:
            d = json.load(f)
        segni = dict(d.get("traduzioni") or {})
        prima = json.dumps(d, ensure_ascii=False, sort_keys=True)
        for campo in campi:
            it = (d.get(campo) or "").strip()
            for lingua in LINGUE:
                k = f"{campo}_{lingua}"
                attuale = (d.get(k) or "").strip()
                segno = segni.get(k, "")
                auto = bool(segno) and segno.split(":")[-1] == impronta(attuale)
                if adotta:
                    if it and attuale and not segno:
                        segni[k] = f"{impronta(it)}:{impronta(attuale)}"
                    continue
                if not it:
                    if auto and attuale:
                        d[k] = ""
                    segni.pop(k, None)
                elif attuale and not auto:
                    segni.pop(k, None)          # scritta o corretta a mano: resta
                elif not attuale or segno.split(":")[0] != impronta(it):
                    try:
                        nuovo = traduci(chiave, it, lingua)
                    except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
                        print(f"DeepL non ha tradotto {os.path.relpath(percorso, RADICE)} › {k}: {e}")
                        errori += 1
                        continue
                    d[k] = nuovo
                    segni[k] = f"{impronta(it)}:{impronta(nuovo)}"
                    print(f"tradotto {os.path.relpath(percorso, RADICE)} › {k}")
        if segni:
            d["traduzioni"] = segni
        else:
            d.pop("traduzioni", None)
        if json.dumps(d, ensure_ascii=False, sort_keys=True) != prima:
            with open(percorso, "w", encoding="utf-8", newline="\n") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
    if errori:
        print(f"{errori} traduzioni non riuscite: dove mancano il sito mostra l'italiano.")


if __name__ == "__main__":
    main()
