"""Mercatino: lettura di data/mercatino/*.json e scelta degli annunci da mostrare.

Ogni annuncio è un file data/mercatino/<AAAA-MM-GG>-<titolo>.json, scritto dall'area di redazione (admin/) o a mano:
  tipo      Vendo, Cerco o Regalo
  title     titolo
  date      AAAA-MM-GG, giorno di pubblicazione
  scadenza  AAAA-MM-GG, facoltativa: se manca l'annuncio resta online GIORNI_DEFAULT giorni dalla pubblicazione
  concluso  true quando l'oggetto è venduto, trovato o regalato: l'annuncio esce subito dalla pagina
  prezzo    testo libero, facoltativo («Fr. 120.–», «da concordare»)
  luogo     facoltativo
  testo     descrizione, testo semplice (gli a capo restano)
  foto      fino a 3 foto (assets/img/mercatino/<nome-del-file>-N.webp, ce le mette prepara_mercatino.py)
  nome      chi pubblica, facoltativo
  contatto  e-mail e/o telefono da pubblicare (con il consenso di chi scrive)
Gli annunci scaduti o conclusi restano nel repository (si possono rinnovare cambiando la scadenza) ma non si vedono.
Solo libreria standard: lo usano pages.py e scripts/prepara_mercatino.py."""
import datetime, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARTELLA = os.path.join(ROOT, "data", "mercatino")
GIORNI_DEFAULT = 90
TIPI = ["Vendo", "Cerco", "Regalo"]


def scadenza(a):
    """Ultimo giorno online (AAAA-MM-GG)."""
    if a.get("scadenza"):
        return a["scadenza"][:10]
    return (datetime.date.fromisoformat(a["date"][:10]) + datetime.timedelta(days=GIORNI_DEFAULT)).isoformat()


def leggi_tutti():
    """Tutti gli annunci, dal più recente: dizionari con i campi del file più «percorso» (il file JSON)."""
    out = []
    for p in glob.glob(os.path.join(CARTELLA, "*.json")):
        with open(p, encoding="utf-8") as f:
            a = json.load(f)
        a["percorso"] = p
        out.append(a)
    out.sort(key=lambda a: (a.get("date", ""), os.path.basename(a["percorso"])), reverse=True)
    return out


def attivi(oggi=None):
    """Gli annunci da mostrare oggi: già pubblicati, non scaduti e non conclusi."""
    oggi = oggi or datetime.date.today().isoformat()
    return [a for a in leggi_tutti() if a.get("title") and not a.get("concluso")
            and a.get("date", "")[:10] <= oggi <= scadenza(a)]
