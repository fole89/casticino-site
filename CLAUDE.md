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

### Pages are self-contained and duplicated
Every page is a top-level `*.html` file with **no templating or includes**. Each page carries its own copy of:
- the `<head>` (Google Fonts: Archivo, Newsreader, IBM Plex Mono) and an identical `<style>` block with the shared classes (`.disp`, `.mono`, `.serif`, `.navlink`, `.btn`, `.card-link`, `.dd*` dropdowns, `.mnav*` mobile menu, `.hide-sm`/`.show-sm` at 960px);
- the header with `<nav aria-label="Principale">` — identical except for `aria-current="page"` on the current page's link;
- the footer (byte-identical across all pages).

So any change to shared CSS, navigation items or the footer must be applied to **all 21 HTML files**. Most layout styling is written as inline `style="…"` attributes; the palette is hard-coded (`#15201B` dark, `#EFEDE6` paper, `#C42A1E`/`--accent` red).

### JavaScript
- `assets/site.js` (loaded `defer` on every page): builds the mobile menu at runtime by cloning the desktop nav (`nav[aria-label="Principale"] .hide-sm`, `.dd` / `.dd-trigger` / `.dd-menu`, `a.btn` CTA). It relies on that markup and on the `button[aria-label="Apri menu"]` toggle — keep those selectors intact when editing the nav.
- `assets/foto.js` (only `Foto.html`): fetches `data/foto.json` and renders albums into `#albums` with a gallery per album, paginated 5 at a time via `#load-more`.

### Photo pipeline
`scripts/update_foto.py` → `data/foto.json` → `assets/foto.js`.
- The script lists via FTP(S) the trip folders `<FTP_BASE>/<year>/AAAA-MM-GG-titolo---luogo/thumbnails/` for the current and previous year, keeps the newest `MAX_ALBUMS` (default 15) that have thumbnails, and writes public URLs for `thumbnails/<file>` and `mysize/<file>` on ssl.dropnet.ch. **Images are never copied into the repo.**
- Title/place come from the folder slug (`---` separates title from place; canton codes uppercased). `data/foto-overrides.json` (key = folder name, fields `title`, `place`, `text`, `link`; keys starting with `_` ignored) always wins. `fetch_droptour()` is a TODO stub for the Droptour XML API.
- The file is only rewritten when `albums` changes.
- `.github/workflows/update-foto.yml` runs it daily (04:17 UTC) and on manual dispatch, then commits `data/foto.json` as `casticino-bot` if it changed. Config comes from secrets `FTP_HOST`/`FTP_USER`/`FTP_PASSWORD` and optional vars `FTP_BASE`, `FTP_TLS`, `PUBLIC_BASE`, `MAX_ALBUMS`.

Don't hand-edit `data/foto.json` for lasting changes — edit `data/foto-overrides.json` instead.

## Known pending work (from README)
- PDFs in Documenti, Corsi and Noleggio still link to `casticino.ch/wp-content/…`; they must be moved into a `docs/` folder in the repo and links updated before the domain switch.
- Placeholders still to fill (hut/HQ photos, committee photos, Statuto, Organigramma, Annuario, etc.).
- News is static: adding an item means editing `News.html` **and** the «Dalla sezione» block in `index.html`.
- DNS: only the site records move to GitHub; MX/TXT mail records and hut subdomains (e.g. `capannacristallina.casticino.ch`) must not be touched.
