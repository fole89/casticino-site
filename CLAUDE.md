# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static website for the Ticino section of the Swiss Alpine Club (CAS Ticino), published via GitHub Pages from `main` / root of `fole89/casticino-site` (`.nojekyll` → files are served as-is). Currently live at `https://fole89.github.io/casticino-site/`; the `CNAME` file (`casticino.ch`) was removed on purpose until the DNS switch, because with it the github.io URL redirects to the old site — don't re-add it unless asked. Since the site is served from a subpath, use relative links only (no `/…` root-absolute paths). Plain HTML/CSS/JS: no framework, no build step, no package manager, no tests, no linter. All site content, code comments, commit messages and the README are in **Italian** — keep it that way.

## Commands

```bash
# Local preview (required for Foto.html: opening via file:// blocks the fetch of data/foto.json)
python -m http.server 8000          # then http://localhost:8000/

# Regenerate data/foto.json from the Droptour FTP (needs credentials)
FTP_HOST=… FTP_USER=… FTP_PASSWORD=… python scripts/update_foto.py
```

The script uses only the Python standard library (`.venv` exists but has no dependencies to install).

## Architecture

### Pages are generated from Python (scripts/redesign/)
Every page is still a top-level static `*.html` file served as-is, but the HTML is **generated**: `python scripts/redesign/pages.py` rewrites all 21 pages (pass file names, e.g. `pages.py Corsi.html`, to rebuild only those). **Edit the generator, not the HTML** — a hand edit to a page is lost on the next run.
- `scripts/redesign/shared.py`: `head()`, `nav()` (menu from `MENU`, `aria-current` on the current page, `is-current` on its parent), `footer()` with sponsor logos, `page_hero()`, `crumbs()`, `subnav()` (sibling pages of La Sezione / Attività), `pic()`/`img()` for `assets/img/*.webp`.
- `scripts/redesign/pages.py`: one function per page with its content (Italian copy lives here), hut data in `HUTS` (home cards) and `HUT_PAGES` (hut pages, one generic `hut()` template), `PAGES` maps file name → function.
- All styling is in `assets/site.css` (tokens on `:root`, always light: no dark theme on purpose, Geist/Geist Mono self-hosted in `assets/fonts/`, square corners). No inline colors. The visual system is documented in `DESIGN.md` (product context in `PRODUCT.md`).
- Logo: `assets/logo-cas-ticino.webp`, the crest with «CAS Ticino / Club Alpino Svizzero» already drawn in (made transparent from the source `assets/img/originali/logo-cas-ticino.png`); the text is not repeated in HTML. `assets/logo-cas.webp` (crest only) remains the favicon.
- Images: `assets/img/<tema>/` — `paesaggi/` (landscape photos, each as `-1000`, `-2000`, `-4x3` mobile crop, `-4x5` vertical crop), `capanne/`, `attivita/`, `corsi/`, `news/` (from the import), `pubblicazioni/` (covers). Names are lowercase, hyphenated, no prefix (the folder says what it is), suffix = size or ratio. In `pages.py` they are referenced without `assets/img/` and `.webp` (e.g. `pic("paesaggi/seraccata", …)`, `img("capanne/adula-3x2", …)`). High-res originals go in `assets/img/originali/` (git-ignored, never published); convert them to WebP in those sizes before use.
- `assets/sponsor/*.webp` are generated from `assets/sponsor/originali/`: trimmed, roughly equal area (max 48px tall), exported at 2x; the footer `<img>` width/height must match.
- Portraits: `assets/img/persone/<gruppo>/<nome-cognome>.webp` (240×280; groups `comitato`, `infrastruttura`, `sport-di-montagna`, `giovani`, `senior`, `comunicazione`). shown as circles, 96px in Comitato (`COMITATO` in `pages.py`) and 60px in Organizzazione: the file is found from the member's name (`slug_nome()`), so a new photo only needs the right name and folder. Without a photo the initials are shown.
- Long `h1.fit` titles are shrunk at runtime by `site.js` when a word doesn't fit. Verify there's no horizontal scroll at 320–430px after layout changes.

### JavaScript
- `assets/site.js` (loaded `defer` on every page): toggles `.scrolled` on the sticky nav (IntersectionObserver), reveals `[data-reveal]` blocks on scroll, fits `.fit` titles, and builds the mobile menu at runtime by cloning the desktop nav (`nav[aria-label="Principale"] .hide-sm`, `.dd` / `.dd-trigger` / `.dd-menu`, `a.btn` CTA). It relies on that markup and on the `button[aria-label="Apri menu"]` toggle — keep those selectors intact when editing the nav.
- `assets/foto.js` (only `Foto.html`): fetches `data/foto.json` and renders albums into `#albums` with a gallery per album, paginated 5 at a time via `#load-more`.

### Photo pipeline
`scripts/update_foto.py` → `data/foto.json` → `assets/foto.js`.
- The script lists via FTP(S) the image files directly inside `<FTP_BASE>/<year>/AAAA-MM-GG-titolo---luogo/` (current and previous year; `FTP_BASE` is `/photo/gite` for this FTP account). Over FTP there are no `thumbnails/`/`mysize/` subfolders — those exist only on the web server, with the same file names — so it writes public URLs `<PUBLIC_BASE>/…/thumbnails/<file>` and `…/mysize/<file>` on ssl.dropnet.ch. Keeps the newest `MAX_ALBUMS` (default 15) non-empty folders; future trips have empty folders and are skipped. If nothing is found it exits with an error instead of emptying `foto.json`. The Droptour FTP server answers 450 (not 550) for missing paths. **Images are never copied into the repo.**
- Title, place, report text (`text`) and `link` come from `fetch_droptour()`, which scrapes the public Droptour gallery page (`GALLERY_URL`, no login; the admin `member_bericht` page needs login and is not used). Each `<div id="dropapp-tours-galery-<nr>">` block is matched to a folder via its `/…/<folder>/mysize/` URL; title is the last `<h2>` split on the last ` - ` into title/place; text is `droptours-description-<nr>` converted to plain text with `
` between paragraphs (rendered with `white-space:pre-line`); link is the public `page=detail&touren_nummer=<nr>` page. If the page is unreachable it falls back to the folder slug (`---` separates title from place; canton codes uppercased). `data/foto-overrides.json` (key = folder name, fields `title`, `place`, `text`, `link`; keys starting with `_` ignored) always wins over both — keep it for real exceptions only.
- The file is only rewritten when `albums` changes.
- `.github/workflows/update-foto.yml` runs it daily (04:17 UTC) and on manual dispatch, then (if it changed) regenerates `data/cerca.json`, `index.html` and `Cerca.html` and commits them with `data/foto.json` as `casticino-bot` if it changed. Config comes from secrets `FTP_HOST`/`FTP_USER`/`FTP_PASSWORD` and optional vars `FTP_BASE`, `FTP_TLS`, `PUBLIC_BASE`, `MAX_ALBUMS`.

Don't hand-edit `data/foto.json` for lasting changes — edit `data/foto-overrides.json` instead.

## Known pending work (from README)
- PDFs live in `docs/<tema>/` (`statuto-visione`, `scale-difficolta`, `promemoria`, `cartine`, `moduli`, `corsi`, `noleggio`, `annuari`, `informazione`, `news`) with lowercase hyphenated Italian names, no accents or version suffixes, year only when the document is year-specific (e.g. `corsi/sci-alpinismo-base-2027.pdf`); they are linked from `pages.py` as `DOC + "<tema>/<file>.pdf"`. Replacing a document keeps its name so links stay valid; never link to `casticino.ch/wp-content/…`, which disappears at the domain switch.
- Placeholders still to fill (HQ photo, committee photos, a few course PDFs).
- Menu: La Sezione, News (goes to the `#news` section of the home, whose «Tutte le news» link opens `News.html`), Attività (Giovani, Senior, Corsi, Noleggio; the trip programme is only the red «Programma gite» button), Le Capanne, Media (Foto, Annuari, Informazione, Documenti; the «Media» item itself goes to the `#media` section of the home), Adesione — all from `MENU` in `shared.py` (nav, footer columns and the `subnav()` rows follow it).
- News: all articles live in `data/news.json` (imported once from the old WordPress with `scripts/import_news.py`: images to `assets/img/news/`, attachments to `docs/news/`). `pages.py` builds `News.html` (latest + archive by year), one page per article in `news/<anno>/<AAAA-MM-GG>-<titolo-breve>.html` (short name from `nome_breve()` in `import_news.py`: no leading weekdays/dates, no articles/prepositions, ≤40 chars; relative paths fixed with `in_sottocartella(…, su="../../")`) and the 3 latest on the home. To add a news item, add an entry at the top of `data/news.json` (same fields; `file` follows the scheme above) and regenerate.
- Annuari / Informazione: drop the PDF in `docs/annuari/annuario-<anno>.pdf` or `docs/informazione/informazione-<anno>-<mese>.pdf`, run `python scripts/copertine.py` (needs PyMuPDF + Pillow, only for that script) to render the cover into `assets/img/pubblicazioni/`, then regenerate: the pages list every file, newest first.
- Search: `pages.py` writes `data/cerca.json` (title, url, type and plain text of every generated page except `News.html`/`Cerca.html`, plus PDFs, annuari, Informazione, Link utili and the photo albums in `data/foto.json`) on every run; `Cerca.html` + `assets/cerca.js` search it in the browser (accent-insensitive, all words must match, title weighs more). The magnifier in the top bar links to it. When `data/foto.json` changes, the daily photo workflow also runs `pages.py index.html Cerca.html`, so new albums reach the search index and the home «Media» tile without touching other pages.
- DNS: only the site records move to GitHub; MX/TXT mail records and hut subdomains (e.g. `capannacristallina.casticino.ch`) must not be touched.
