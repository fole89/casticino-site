"""Oggetti disegnati a tratto per le tappe della pagina Storia (storia.html): un SVG per tappa, nel colore del testo
con un dettaglio rosso CAS. Tutto è fatto di <path> con pathLength="1", così il CSS può «disegnarli» quando la tappa
entra nello schermo (stroke-dashoffset da 1 a 0); site.js fa ruotare il rampone e oscillare la piccozza con lo scorrimento.
Riquadro 120×120, tratto 3 (diventa più sottile quando l'SVG è piccolo, sempre leggibile)."""


def rett(x, y, w, h):
    return f"M{x} {y}h{w}v{h}h{-w}z"


def cerchio(cx, cy, r):
    return f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0"


def ellisse(cx, cy, rx, ry):
    return f"M{cx - rx} {cy}a{rx} {ry} 0 1 0 {2 * rx} 0a{rx} {ry} 0 1 0 {-2 * rx} 0"


def rett_tondo(x, y, w, h, r):
    return (f"M{x + r} {y}h{w - 2 * r}a{r} {r} 0 0 1 {r} {r}v{h - 2 * r}a{r} {r} 0 0 1 {-r} {r}"
            f"h{-(w - 2 * r)}a{r} {r} 0 0 1 {-r} {-r}v{-(h - 2 * r)}a{r} {r} 0 0 1 {r} {-r}z")


# nome: lista di (tracciato, rosso?); l'ordine è quello in cui si disegnano
OGGETTI = {
    # 1886, la fondazione nell'anno del centenario del Monte Bianco: la vetta con la bandiera
    "vetta": [
        ("M8 102H112", False),
        ("M14 102L44 52L58 70L78 36L106 102", False),
        ("M36 66L44 60L50 66", False),
        ("M78 36V12", False),
        ("M78 13h22l-6 7l6 7h-22", True),
    ],
    # 1887, l'ingresso nel Club Alpino Svizzero: lo scudo con la croce
    "croce": [
        ("M28 16h64v42c0 26-17 40-32 48c-15-8-32-22-32-48z", False),
        ("M54 36h12v14h14v12h-14v14h-12v-14h-14v-12h14z", True),
    ],
    # 1911, il vessillo sezionale
    "bandiera": [
        ("M30 110V14", False),
        (cerchio(30, 10, 4), False),
        ("M30 18C50 8 68 30 94 18V60C68 72 50 50 30 60", True),
        ("M18 110H42", False),
    ],
    # 1913, la sezione femminile: lo scarpone
    "scarpone": [
        ("M34 16H62V60L90 72C97 75 100 80 100 88V96H30V22C30 19 31 16 34 16z", False),
        ("M28 106H102", False),
        ("M36 106v-10M52 106v-10M68 106v-10M84 106v-10", False),
        ("M44 28H62M44 38H62M44 48H62", True),
    ],
    # 1918, le stazioni di soccorso: la lanterna
    "lanterna": [
        (cerchio(60, 14, 6), False),
        ("M44 34L50 24H70L76 34z", False),
        (rett(42, 34, 36, 54), False),
        ("M52 34V88M68 34V88", False),
        ("M60 48C67 56 67 68 60 74C53 68 53 56 60 48z", True),
        (rett(36, 88, 48, 10), False),
    ],
    # anni '30, l'arrampicata: un vecchio rampone di profilo, denti sotto e punte avanti (ruota con lo scorrimento)
    "rampone": [
        ("M12 56H86C94 56 100 60 104 66", False),
        ("M16 56L21 76L26 56M38 56L43 76L48 56M60 56L65 76L70 56M80 56L86 75L91 58", False),
        ("M104 66L116 74M100 70L108 84", True),
        ("M18 56V42H40V56M72 56V42H96V62", False),
        ("M29 42C29 26 84 26 84 42", False),
    ],
    # 1936, l'Himalaya: la piccozza (oscilla con lo scorrimento)
    "piccozza": [
        ("M60 26V104", False),
        ("M60 22C44 22 28 28 14 40", True),
        ("M60 22H86L92 32H64", False),
        ("M56 104L60 116L64 104z", False),
        ("M60 22V14", False),
    ],
    # 1940, il gruppo Seniori: lo zaino
    "zaino": [
        ("M34 38C34 26 44 20 60 20C76 20 86 26 86 38V106H34z", False),
        ("M52 20C52 11 68 11 68 20", False),
        ("M34 42C46 54 74 54 86 42", False),
        (rett(56, 50, 8, 10), True),
        (rett(44, 70, 32, 24), False),
    ],
    # anni '60, la gioventù e la colonna di soccorso: la corda arrotolata
    "corda": [
        (ellisse(60, 58, 42, 32), False),
        (ellisse(60, 58, 32, 23), False),
        (ellisse(60, 58, 22, 14), False),
        ("M100 68C108 84 100 100 84 110", True),
    ],
    # 1980, la fusione delle due sezioni: due moschettoni agganciati
    "moschettoni": [
        (rett_tondo(10, 34, 62, 36, 18), False),
        (rett_tondo(48, 50, 62, 36, 18), True),
    ],
    # 1982, la settimana mini: la tenda
    "tenda": [
        ("M6 102H114", False),
        ("M16 102L60 26L104 102", False),
        ("M60 26L60 18", False),
        ("M50 102L60 72L70 102", True),
        ("M16 102L8 110M104 102L112 110", False),
    ],
    # 2003, la nuova Capanna Cristallina: la capanna
    "capanna": [
        ("M4 104H116", False),
        ("M18 104V58L60 28L102 58V104", False),
        ("M10 64L60 26L110 64", True),
        (rett(30, 66, 14, 12) + rett(53, 66, 14, 12) + rett(76, 66, 14, 12), False),
        (rett(53, 86, 14, 18), False),
    ],
    # 2016, la nuova Capanna Monte Bar: il volume moderno rivestito di listoni
    "capanna-moderna": [
        ("M4 104H116", False),
        (rett(14, 42, 92, 52), False),
        ("M14 54H106M14 66H106M14 82H106", False),
        (rett(24, 68, 28, 12), True),
        (rett(62, 68, 34, 12), True),
        ("M30 94V104M90 94V104", False),
    ],
}


# oggetti da centrare o ingrandire nel riquadro (il rampone, largo e basso, ruota attorno al centro)
RIQUADRO = {"rampone": "translate(60 60) scale(1.08) translate(-64 -55)"}


def oggetto(nome, moto=None):
    """SVG decorativo (aria-hidden) dell'oggetto; moto «ruota» o «oscilla» lo lega allo scorrimento (site.js, --p sul
    <g> esterno), il <g> interno serve solo a centrare il disegno."""
    rosso = ' class="r"'
    tratti = "".join(f'<path d="{d}" pathLength="1"{rosso if r else ""}/>' for d, r in OGGETTI[nome])
    if nome in RIQUADRO:
        tratti = f'<g transform="{RIQUADRO[nome]}">{tratti}</g>'
    attr = f' data-moto="{moto}"' if moto else ""
    return (f'<svg class="oggetto" viewBox="0 0 120 120" aria-hidden="true" focusable="false"{attr}>'
            f'<g class="oggetto-moto">{tratti}</g></svg>')
