# Aggiungere una pagina al sito

Le pagine HTML del sito sono **generate**: non si modificano a mano, si scrive una funzione Python che
restituisce la pagina e si rigenera. Servono solo Python 3 e un editor (non serve installare altro).

## 1. Scegli il modulo

Ogni gruppo del menu ha il suo file in `scripts/redesign/`:

| Gruppo del menu | Modulo |
|---|---|
| La Sezione | `pagine_sezione.py` |
| Attività | `pagine_attivita.py` |
| Capanne | `pagine_capanne.py` |
| Servizi | `pagine_servizi.py` |
| News e media | `pagine_media.py` |
| Adesione, privacy, altre | `pagine_altre.py` |

`comune.py` contiene le funzioni usate da tutti (impaginazione, menu, testi); `pages.py` elenca le pagine e scrive i file.

## 2. Scrivi la funzione

Esempio: una pagina «Rifugi invernali» sotto La Sezione, file `rifugi-invernali.html` (nome sempre in minuscolo, con trattini).

```python
def rifugi_invernali():
    titolo = tr("Rifugi invernali", "Winterräume", "Winter rooms")
    body = page_hero([sez_crumb(), (titolo, None)], titolo,
                     tr("Frase introduttiva…", "Einleitungssatz…", "Introductory sentence…")) + f"""

<section class="section" aria-labelledby="locali-h">
<div class="container prose" data-reveal>
<h2 id="locali-h" class="h2">{tr("I locali", "Die Räume", "The rooms")}</h2>
<p>{tr("Testo in italiano.", "Text auf Deutsch.", "Text in English.")}</p>
</div>
</section>

{subnav(SEZ_MENU(), L("rifugi-invernali.html"))}"""
    return sezione_page("rifugi-invernali.html", titolo + " | CAS Ticino",
                        tr("Descrizione per Google (1–2 frasi).", "Beschreibung…", "Description…"), body)
```

- `tr(italiano, tedesco, inglese)` sceglie il testo della lingua che si sta generando: una funzione sola vale per le tre lingue.
  Tedesco svizzero (ss, mai ß), inglese britannico.
- `page_hero(briciole, titolo, introduzione)` disegna l'intestazione. Le briciole del gruppo sono `sez_crumb()`, `att_crumb()`,
  `nm_crumb()`, `servizi_crumb()`.
- `sezione_page()` aggiunge testa, menu e footer e sistema i percorsi per `de/` ed `en/`. Per ora vale per tutte le pagine
  tradotte, anche fuori da La Sezione.
- Usa solo le classi già presenti in `assets/site.css` (`section`, `container`, `prose`, `h2`, `btn btn--primary`…) e niente
  colori nel codice. Prendi a modello una pagina simile (es. `soccorso()` in `pagine_sezione.py`).
- Link interni relativi e con `.html` (`href="sede.html"`, mai `/sede`): nelle pagine tedesche e inglesi diventano da soli `de/sede.html`, `en/sede.html`.
- Foto: `img("attivita/nome", alt, larghezza, altezza)` per `assets/img/attivita/nome.webp`. PDF: `DOC + "tema/nome.pdf"`.

## 3. Registra la pagina in `pages.py`

1. Importa la funzione in cima: `from pagine_sezione import …, rifugi_invernali`.
2. Aggiungila a `PAGES` (versione italiana): `"rifugi-invernali.html": rifugi_invernali,`.
3. Aggiungila anche a `_pagine`, nel ciclo «Versioni tradotte» più sotto, per creare `de/` ed `en/`.

## 4. Mettila nel menu

In `shared.py` aggiungi la voce nel gruppo giusto di **`MENU`, `MENU_DE` e `MENU_EN`** (stessa posizione nei tre).
Menu, footer e riquadro «tutte le pagine» (`subnav()`) si aggiornano da soli. Se le etichette si allungano, controlla
che il menu stia ancora su una riga sopra i 1280px (1360px in tedesco).

## 5. Rigenera e controlla

```bash
python scripts/redesign/pages.py rifugi-invernali.html de/rifugi-invernali.html en/rifugi-invernali.html cerca.html
python -m http.server 8000      # poi http://localhost:8000/rifugi-invernali.html
```

Se hai cambiato il menu, rigenera tutto (`python scripts/redesign/pages.py`): il menu è in ogni pagina.
Guarda la pagina nelle tre lingue e su telefono (larghezza 320–430px, niente scorrimento orizzontale).
Ricerca, sitemap e metadati (canonical, hreflang) si aggiornano da soli.

## Da sapere

- **Testi che la redazione deve poter cambiare:** mettili in `data/testi/<nome>.json` e leggili con `testi("<nome>")` e
  `testo_campo()` / `testo_md()`, poi aggiungi il file a `admin/config.yml` (collezione «Testi del sito»). Esempio: il testo dei guardiani, `data/testi/capanne/<cartella>.json`.
- **Servizi esterni, form, cookie o dati salvati nel browser:** aggiorna anche i testi della privacy (`PRIVACY` in
  `pagine_altre.py`, tre lingue).
- **Una funzione serve a due moduli?** Spostala in `comune.py`. Altrimenti importala per nome rispettando l'ordine
  comune → capanne → servizi → media → attivita → home → sezione → altre → ricerca: un modulo importa solo da quelli prima di lui.
- Commit con messaggio in italiano: includi il codice **e** le pagine `.html` rigenerate.
