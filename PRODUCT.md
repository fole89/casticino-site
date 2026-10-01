# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Four audiences, all confirmed as primary; none is subordinate to the others:

- **Current members (soci):** check the gite program, news, courses, documents, the committee and who to contact.
- **Prospective members:** hikers, climbers and families in Ticino discovering the section and deciding whether to join the CAS through it.
- **Hut guests:** anyone, member or not, planning a night at one of the section's six capanne and needing altitude, access, places, opening status and how to reach the guardiano.
- **Volunteers and capigita:** the people who run the section (committee, capigita, monitori, guardiani and their helpers, the "api operaie") looking for organisational material and calls for help.

## Product Purpose

The public website of the Ticino section of the Swiss Alpine Club (CAS Ticino, founded 1886, about 3000 members). It presents the section, its activities, its six huts and its history, and routes each visitor to the action that matters to them. Success means:

- new memberships (Adesione);
- sign-ups to section trips (registration happens on Droptour, an external system);
- hut visits (contact with the guardiano or the hut's own site);
- course enrolments and volunteers for the huts.

## Positioning

The only CAS section serving Italian-speaking Switzerland: six huts from Passo Cristallina to the Denti della Vecchia (Campo Tencia, Cristallina, Adula, Motterascio, Monte Bar, Baita del Luca), courses taught by professionals, a trip program for every age (Giovani since the 1960s, Senior since 1940), and a continuous history since 1886.

## Operating Context

- Trip program and registrations live on Droptour (`ssl.dropnet.ch/casticino/gite/…`); the site links out to it.
- Trip photos and reports come automatically from the public Droptour gallery via `scripts/update_foto.py` → `data/foto.json` (daily GitHub Action). Images stay hosted on ssl.dropnet.ch.
- Huts have their own sites on subdomains (e.g. `capannacristallina.casticino.ch`) that are not part of this repo.
- News is static and edited by hand (`News.html` plus the «Dalla sezione» block on the home page).
- Published with GitHub Pages, currently at `fole89.github.io/casticino-site/`, moving to `casticino.ch` at the DNS switch.

## Capabilities and Constraints

- Static site: plain HTML/CSS/JS, no framework, no build step; relative links only (served from a subpath).
- All content is in Italian. Whether the site must stay Italian-only is **not decided** (not confirmed as binding).
- Who will maintain content after launch (technical vs. non-technical editors) is **not decided**.
- Open before launch: PDFs still hosted on the old WordPress site must move into the repo; placeholders remain (Statuto, Visione e strategia, Organigramma, Annuario, some course PDFs, two committee portraits, the Motterascio inspector).
- A redesign is in progress on the `redesign` branch (home and Campo Tencia prototyped).

## Brand Commitments

- **Binding:** the section belongs to the Swiss Alpine Club; the national CAS/SAC logo and identity must be respected. The section crest is `assets/logo-cas.webp`.
- Name as used on the site: "CAS Ticino", full form "Club Alpino Svizzero, Sezione Ticino".
- Voice: plain, warm, factual Italian ("In montagna con noi", "Sali con noi"); no marketing hype.

## Evidence on Hand

- Real facts: founding 1886 (Birraria Gambrinus, Bellinzona), ≈3000 members, 6 huts with 362 beds, 5 course disciplines, historical timeline (Storia.html), hut data (altitude, valley, places, access times).
- Real photography: huts, activities and courses in `assets/img/` (WebP); committee portraits in `assets/comitato/`; trip photos from Droptour via `data/foto.json`.
- Sponsor logos in `assets/sponsor/`.
- Absent, must not be fabricated: member testimonials, statistics beyond those above, photos for placeholders listed under Constraints, prices or opening dates not supplied by the huts.

## Product Principles

1. **Serve four audiences without burying any.** Members, prospects, hut guests and volunteers each need a short path to their action; no single funnel dominates.
2. **Route, don't duplicate.** Droptour and the hut sites own their data; the site points to them clearly instead of copying information that would go stale.
3. **Mountain truth first.** Altitudes, access times, conditions and safety notes are factual and current; when unsure, send people to the guardiano.
4. **A club, not a company.** Volunteer-run, 140 years of history, CAS identity respected; the tone stays that of a section talking to its members.
