"""Notifiche del sito (un solo canale: «Notizie importanti della sezione»), dal workflow .github/workflows/news.yml.

  python scripts/notifiche.py prepara FILE   prima della pubblicazione: le news (data/news/*.json) e l'avviso
                                             (data/avviso.json) con la casella «Invia anche come notifica»
                                             ("notifica": true) diventano messaggi in FILE (fuori dal repository);
                                             nei JSON la casella si spegne e "notifica_inviata" segna data e ora,
                                             così una modifica successiva non rimanda la notifica
  python scripts/notifiche.py invia FILE     dopo la pubblicazione: invia i messaggi a tutti gli iscritti
  python scripts/notifiche.py prova "testo"  un messaggio di prova a tutti gli iscritti

«invia» e «prova» richiedono pywebpush (pip install pywebpush) e i segreti NOTIFICHE_TOKEN e VAPID_PRIVATE (chiave
privata in PEM); indirizzo del Worker scripts/notifiche/ e chiave pubblica sono NOTIFICHE_API e NOTIFICHE_CHIAVE in
scripts/redesign/shared.py. Gli indirizzi scaduti (telefono cambiato, app tolta) vengono tolti dal Worker."""
import datetime, glob, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "redesign"))
from shared import SITO, NOTIFICHE_API  # noqa: E402
import news_util  # noqa: E402

LINGUE = ("it", "de", "en")
TITOLO_AVVISO = {"it": "CAS Ticino", "de": "CAS Ticino", "en": "CAS Ticino"}
SOGGETTO = "mailto:webmaster@casticino.ch"   # contatto per i servizi di notifica (Google, Apple, Mozilla)


def leggi(path):
    testo = open(path, encoding="utf-8").read()
    righe = testo.split("\n")
    rientro = len(righe[1]) - len(righe[1].lstrip(" ")) if len(righe) > 1 else 2
    return json.loads(testo), rientro or 2, testo.endswith("\n")


def scrivi(path, dati, rientro, a_capo):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(dati, ensure_ascii=False, indent=rientro) + ("\n" if a_capo else ""))


def breve(t, n=140):
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"


def url_pagina(pagina, lang):
    """Indirizzo completo di una pagina del sito nella lingua (la versione tradotta, se esiste)."""
    if lang != "it" and os.path.exists(os.path.join(ROOT, lang, pagina)):
        pagina = f"{lang}/{pagina}"
    return SITO + pagina


def prepara(uscita):
    adesso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M")
    messaggi = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "news", "*.json"))):
        d, rientro, a_capo = leggi(path)
        if not d.get("notifica"):
            continue
        corpo = news_util.md_html(d["testo"]) if (d.get("testo") or "").strip() else d.get("html", "")
        testo = breve(d.get("excerpt") or news_util.estratto(corpo))
        pagina = d.get("file") or news_util.nome_file(d)
        messaggi.append({"tag": "news-" + os.path.basename(path)[:-5],
                         **{l: {"titolo": d["title"].strip(), "testo": testo, "url": url_pagina(pagina, l)} for l in LINGUE}})
        d["notifica"], d["notifica_inviata"] = False, adesso
        scrivi(path, d, rientro, a_capo)
        print("notifica:", d["title"])
    path = os.path.join(ROOT, "data", "avviso.json")
    d, rientro, a_capo = leggi(path)
    if d.get("notifica") and (d.get("testo") or "").strip():
        link = (d.get("link") or "").strip()
        msg = {"tag": "avviso"}
        for l in LINGUE:
            testo = (d.get(f"testo_{l}") or "").strip() if l != "it" else ""
            url = link if link.startswith("http") else url_pagina(link or "index.html", l)
            msg[l] = {"titolo": TITOLO_AVVISO[l], "testo": breve(testo or d["testo"]), "url": url}
        messaggi.append(msg)
        d["notifica"], d["notifica_inviata"] = False, adesso
        scrivi(path, d, rientro, a_capo)
        print("notifica: avviso")
    with open(uscita, "w", encoding="utf-8") as f:
        json.dump(messaggi, f, ensure_ascii=False)
    print(f"{len(messaggi)} notifiche da inviare")


def api(percorso, dati=None):
    base = os.environ.get("NOTIFICHE_API") or NOTIFICHE_API
    req = urllib.request.Request(base.rstrip("/") + percorso, method="POST" if dati is not None else "GET",
                                 data=json.dumps(dati).encode() if dati is not None else None,
                                 headers={"Authorization": "Bearer " + os.environ["NOTIFICHE_TOKEN"], "Content-Type": "application/json",
                                          "User-Agent": "casticino-notifiche"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def invia(messaggi):
    if not messaggi:
        print("Nessuna notifica da inviare.")
        return
    mancano = [v for v in ("NOTIFICHE_TOKEN", "VAPID_PRIVATE") if not os.environ.get(v)]
    if mancano:
        print("Notifiche non configurate (mancano " + ", ".join(mancano) + "): nessun invio.")
        return
    from py_vapid import Vapid
    from pywebpush import webpush, WebPushException
    chiave = Vapid.from_pem(os.environ["VAPID_PRIVATE"].encode())
    iscrizioni = api("/iscrizioni")["iscrizioni"]
    scaduti, inviate, errori = set(), 0, 0
    for msg in messaggi:
        for s in iscrizioni:
            if s["endpoint"] in scaduti:
                continue
            lingua = s.get("lingua") if s.get("lingua") in LINGUE else "it"
            dati = json.dumps({**msg[lingua], "tag": msg["tag"], "lingua": lingua}, ensure_ascii=False)
            try:
                webpush({"endpoint": s["endpoint"], "keys": {"p256dh": s["p256dh"], "auth": s["auth"]}}, data=dati,
                        vapid_private_key=chiave, vapid_claims={"sub": SOGGETTO}, ttl=86400, timeout=15)
                inviate += 1
            except WebPushException as e:
                if e.response is not None and e.response.status_code in (404, 410):
                    scaduti.add(s["endpoint"])    # iscrizione non più valida: si toglie
                else:
                    errori += 1
                    print("non inviata:", e.response.status_code if e.response is not None else e)
            except Exception as e:  # rete o servizio di notifica irraggiungibile
                errori += 1
                print("non inviata:", e)
    if scaduti:
        api("/rimuovi", {"endpoints": sorted(scaduti)})
    print(f"{len(messaggi)} messaggi, {len(iscrizioni)} iscritti: {inviate} inviate, {len(scaduti)} iscrizioni scadute tolte, {errori} errori")
    if errori and not inviate:
        sys.exit("Nessuna notifica inviata.")


if __name__ == "__main__":
    azione = sys.argv[1] if len(sys.argv) > 1 else ""
    if azione == "prepara" and len(sys.argv) == 3:
        prepara(sys.argv[2])
    elif azione == "invia" and len(sys.argv) == 3:
        invia(json.load(open(sys.argv[2], encoding="utf-8")) if os.path.exists(sys.argv[2]) else [])
    elif azione == "prova" and len(sys.argv) == 3:
        invia([{"tag": "prova", **{l: {"titolo": "CAS Ticino", "testo": sys.argv[2], "url": SITO} for l in LINGUE}}])
    else:
        sys.exit(__doc__)
