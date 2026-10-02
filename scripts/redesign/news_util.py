"""News: lettura di data/news/*.json, nome del file della pagina, testo Markdown → HTML, estratto.

Ogni news è un file data/news/<AAAA-MM-GG>-<titolo>.json, scritto a mano o dall'area di redazione (admin/):
  title     titolo
  date      AAAA-MM-GGTHH:MM (l’ora serve solo a ordinare le news dello stesso giorno)
  image     foto principale (assets/img/news/<anno>/<nome>.webp), facoltativa
  alt       descrizione della foto, facoltativa
  excerpt   riassunto per le schede, facoltativo (se manca: l'inizio del testo)
  testo     testo in Markdown (news nuove)
  html      testo in HTML (news importate dal vecchio sito; vale se «testo» è vuoto)
  allegati  PDF: lista di {"titolo", "file"} (docs/news/<anno>/…, ci li sposta prepara_news.py), facoltativi
  category  categoria, facoltativa
  file      pagina generata (news/<anno>/<AAAA-MM-GG>-<titolo-breve>.html); se manca la calcola nome_file()
Solo libreria standard: lo usano pages.py e scripts/prepara_news.py."""
import glob, html, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARTELLA = os.path.join(ROOT, "data", "news")

GIORNI_MESI = set("""lun mar mer gio ven sab dom lunedi martedi mercoledi giovedi venerdi sabato domenica ma
gen feb mag giu lug ago set ott nov dic gennaio febbraio marzo aprile maggio giugno luglio agosto settembre
ottobre novembre dicembre apr ore alle h""".split())
PAROLE_VUOTE = set("""il lo la i gli le l un una uno di del dello della dei degli delle d a al allo alla ai agli alle
da dal dallo dalla dai dagli dalle in nel nello nella nei negli nelle su sul sullo sulla sui sugli sulle con per tra fra
e ed o vs""".split())


def nome_breve(titolo, maxlen=40):
    """Titolo breve per il nome del file: senza giorni e date iniziali, senza articoli e preposizioni."""
    def pulisci(t):
        t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
        return [p for p in re.split(r"[^a-z0-9]+", t) if p]
    parole = pulisci(titolo)
    while parole and (parole[0] in GIORNI_MESI or parole[0] in PAROLE_VUOTE or parole[0].isdigit()):
        parole.pop(0)
    parole = [p for p in parole if p not in PAROLE_VUOTE] or pulisci(titolo)[:3] or ["news"]
    out = ""
    for p in parole:
        prova = f"{out}-{p}" if out else p
        if len(prova) > maxlen:
            break
        out = prova
    return out or parole[0][:maxlen]


def nome_file(n, presi=()):
    """news/<anno>/<AAAA-MM-GG>-<titolo-breve>.html, diverso da quelli già presi."""
    base = f"news/{n['date'][:4]}/{n['date'][:10]}-{nome_breve(n['title'])}"
    nome, k = base + ".html", 2
    while nome in presi:
        nome, k = f"{base}-{k}.html", k + 1
    return nome


def webp_size(path):
    """Larghezza e altezza di un file WebP, leggendo l'intestazione (senza librerie esterne)."""
    with open(path, "rb") as f:
        d = f.read(30)
    kind = d[12:16]
    if kind == b"VP8 ":
        return int.from_bytes(d[26:28], "little") & 0x3FFF, int.from_bytes(d[28:30], "little") & 0x3FFF
    if kind == b"VP8L":
        v = int.from_bytes(d[21:25], "little")
        return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    return int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1


# ------------------------------------------------------------------ Markdown → HTML
# Copre quello che produce l'editor dell'area di redazione: paragrafi, a capo, grassetto, corsivo, link,
# titoli, elenchi, citazioni e immagini. L'HTML scritto dentro il testo viene mostrato come testo.

def _inline(t):
    t = html.escape(t, quote=False)
    segnaposto = []

    def tieni(s):
        segnaposto.append(s)
        return f"\x00{len(segnaposto) - 1}\x00"
    t = re.sub(r"\\([\\`*_{}\[\]()#+\-.!>~|])", lambda m: tieni(m.group(1)), t)          # caratteri protetti con \
    t = re.sub(r"`([^`]+)`", lambda m: tieni(f"<code>{m.group(1)}</code>"), t)
    t = re.sub(r'!\[([^\]]*)\]\(([^)"]+?)(?:\s+"[^)]*")?\)',
               lambda m: tieni(f'<img src="{m.group(2).strip().replace(" ", "%20")}" alt="{m.group(1)}" loading="lazy" decoding="async">'), t)

    def link(m):
        url = m.group(2)
        if re.match(r"[a-z][a-z0-9+.-]*:", url, re.I) and not url.lower().startswith(("http://", "https://", "mailto:", "tel:")):
            return m.group(1)                    # niente javascript: e simili
        ext = ' rel="noopener"' if url.startswith(("http://", "https://")) else ""
        return f'<a href="{url}"{ext}>{m.group(1)}</a>'
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^)]*\")?\)", link, t)
    t = re.sub(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", r"<strong>\2</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w_])_(?=\S)(.+?)(?<=\S)_(?![\w_])", r"<em>\1</em>", t)
    t = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"<del>\1</del>", t)
    t = re.sub(r"(\\|  )\n", "<br>", t)       # a capo forzato
    t = t.replace("\n", "<br>")                 # a capo semplice: nell'editor è un a capo voluto
    return re.sub("\x00(\\d+)\x00", lambda m: segnaposto[int(m.group(1))], t)


def md_html(testo):
    righe = testo.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out, par, i = [], [], 0

    def chiudi():
        if par:
            blocco = "\n".join(par).strip()
            if blocco:
                img = re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", blocco)
                out.append(f"<figure>{_inline(blocco)}</figure>" if img else f"<p>{_inline(blocco)}</p>")
            par.clear()

    while i < len(righe):
        r = righe[i]
        if not r.strip():
            chiudi()
            i += 1
            continue
        m = re.match(r"(#{1,6})\s+(.*?)\s*#*\s*$", r)
        if m:
            chiudi()
            tag = "h2" if len(m.group(1)) <= 2 else "h3"
            out.append(f"<{tag}>{_inline(m.group(2))}</{tag}>")
            i += 1
            continue
        if re.match(r"\s*(-{3,}|\*{3,}|_{3,})\s*$", r):
            chiudi()
            out.append("<hr>")
            i += 1
            continue
        if r.lstrip().startswith(">"):
            chiudi()
            cit = []
            while i < len(righe) and righe[i].lstrip().startswith(">"):
                cit.append(re.sub(r"^\s*>\s?", "", righe[i]))
                i += 1
            out.append(f"<blockquote>{md_html(chr(10).join(cit))}</blockquote>")
            continue
        m = re.match(r"\s*([-*+]|\d+[.)])\s+", r)
        if m:
            chiudi()
            tag = "ol" if m.group(1)[0].isdigit() else "ul"
            voce = r"\s*\d+[.)]\s+" if tag == "ol" else r"\s*[-*+]\s+"   # voci dello stesso tipo di elenco
            voci = []
            while i < len(righe):
                m = re.match(voce + "(.*)", righe[i])
                if m:
                    voci.append(m.group(1))
                elif righe[i].strip() and voci and righe[i].startswith((" ", "\t")):
                    voci[-1] += "\n" + righe[i].strip()      # continuazione della voce
                elif not righe[i].strip() and i + 1 < len(righe) and re.match(voce, righe[i + 1]):
                    pass                                      # riga vuota tra due voci
                else:
                    break
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{_inline(v)}</li>" for v in voci) + f"</{tag}>")
            continue
        par.append(r)
        i += 1
    chiudi()
    return "\n".join(out)


def allegati_html(allegati):
    return "\n".join(f'<p><a class="file-link" href="{html.escape(a["file"])}">{html.escape(a.get("titolo") or os.path.basename(a["file"]))}</a></p>'
                     for a in allegati or [] if a.get("file"))


def solo_testo(frammento):
    t = re.sub(r"<(br|/p|/li|/h[23])>", " ", frammento)
    t = re.sub(r"<[^>]+>", " ", t)
    # «<strong>titolo</strong>, …» non deve diventare «titolo , …»
    return re.sub(r" ([,.;:!?])", r"\1", re.sub(r"\s+", " ", html.unescape(t))).strip()


def estratto(corpo, maxlen=220):
    t = solo_testo(corpo)
    if len(t) > maxlen:
        t = t[:maxlen].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return t


def leggi_tutte():
    """Tutte le news, dalla più recente: dizionari con i campi del file più «percorso» (il file JSON)."""
    news = []
    for p in glob.glob(os.path.join(CARTELLA, "*.json")):
        with open(p, encoding="utf-8") as f:
            n = json.load(f)
        n["percorso"] = p
        news.append(n)
    news.sort(key=lambda n: (n["date"], n.get("file") or ""), reverse=True)
    return news
