---
name: CAS Ticino
description: Sito della Sezione Ticino del Club Alpino Svizzero, sistema grafico del redesign (assets/site.css).
colors:
  neve: "#FFFFFF"
  granito-chiaro: "#F0F2F0"
  granito: "#E2E6E2"
  ardesia: "#121816"
  ardesia-2: "#36403C"
  lichene: "#5B6661"
  rosso-cas: "#EF1C24"
  rosso-cas-deep: "#C9141B"
  bianco-su-foto: "#F4F5F2"
typography:
  display:
    fontFamily: "Geist, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "clamp(46px, 7.6vw, 116px)"
    fontWeight: 720
    lineHeight: 0.92
    letterSpacing: "-0.05em"
  headline:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "clamp(34px, 4.6vw, 64px)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "-0.04em"
  title:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "clamp(22px, 2vw, 28px)"
    fontWeight: 650
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  lead:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "clamp(18px, 1.5vw, 21px)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 550
    lineHeight: 1.4
    letterSpacing: "0.02em"
  data:
    fontFamily: "'Geist Mono', ui-monospace, Consolas, monospace"
    fontSize: "15px"
    fontWeight: 500
    letterSpacing: "-0.02em"
    fontFeature: "tnum"
rounded:
  none: "0px"
spacing:
  gutter: "clamp(20px, 4vw, 48px)"
  section: "clamp(72px, 10vw, 136px)"
  gap-sm: "12px"
  gap-md: "16px"
  gap-lg: "24px"
  gap-xl: "40px"
  nav-h: "72px"
  maxw: "1320px"
components:
  button-primary:
    backgroundColor: "{colors.rosso-cas}"
    textColor: "#FFFFFF"
    rounded: "{rounded.none}"
    padding: "0 22px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.rosso-cas-deep}"
    textColor: "#FFFFFF"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ardesia}"
    rounded: "{rounded.none}"
    padding: "0 22px"
    height: "48px"
  button-light:
    backgroundColor: "{colors.bianco-su-foto}"
    textColor: "{colors.ardesia}"
    rounded: "{rounded.none}"
    padding: "0 22px"
    height: "48px"
  navlink:
    textColor: "{colors.ardesia-2}"
    typography: "{typography.body}"
    padding: "0 12px"
    height: "44px"
  navlink-current:
    textColor: "{colors.rosso-cas}"
  callout:
    backgroundColor: "{colors.granito-chiaro}"
    rounded: "{rounded.none}"
    padding: "clamp(24px, 3vw, 36px)"
---

# Design System: CAS Ticino

## Overview

**Creative North Star: "Il Libro di Capanna"**

The site reads like the logbook kept in a mountain hut: plain, exact, written by people who have been there. Real numbers carry the authority (altitudes, walking times, beds, founding years), set in a sharp grotesque and a monospaced figure face. The mountain itself speaks through real photography of the huts, courses and trips; the interface around it stays cold and mineral, snow, granite and slate, so the photos and the CAS red are the only warm things on the page.

Density is generous and editorial: big display headings set tight, wide sections, a 12-column feel inside a 1320px container. Every corner is square. The site is always light, on a white page, whatever the device theme: the section confirmed it prefers a bright site (reference: caslocarno.ch).

The system is moving towards two decisions confirmed by the section that the current pages express only in part: **the CAS red may be more present** than a rare signpost, and **components should feel solid and tactile**, with real weight and depth on interactive elements rather than the current mostly-flat surfaces. New work should push in that direction; refinements of existing pages should bring them closer to it.

**Key Characteristics:**
- Cold mineral neutrals (neve, granito, ardesia) with one warm voice: rosso CAS.
- Square corners everywhere (0px radius).
- Geist for everything readable, Geist Mono for data: altitudes, years, times, counts.
- Real photography only, under dark gradient scrims when text sits on it.
- Solid, tactile interactive elements; depth earned by state and by photos.
- Always light: white page, pale granite bands, no dark theme.

## Colors

A cold, desaturated mountain-stone palette carrying a single saturated red.

### Primary
- **Rosso CAS** (#EF1C24): the club's voice. Primary buttons, the current page in navigation, years in timelines, news dates, hut status, the accent word in hero headlines, text selection, focus rings. It may also take larger areas (bands, blocks, full-bleed accents) when a section needs emphasis.
- **Rosso CAS profondo** (#C9141B): hover and pressed state of red surfaces.

### Neutral
- **Neve** (#FFFFFF): page background.
- **Granito chiaro** (#F0F2F0): alternate section background, footer, callouts, contact blocks, dropdown hover.
- **Granito** (#E2E6E2): image placeholders behind photos, deeper surfaces.
- **Ardesia** (#121816): headings and primary text; also the solid base of photo bands.
- **Ardesia 2** (#36403C): body copy in leads, cards and nav links.
- **Lichene** (#5B6661): labels, metadata, captions, breadcrumbs.
- **Bianco su foto** (#F4F5F2): text and light buttons placed on photographs.
- Lines are ardesia at 14% (`--line`) and 32% (`--line-strong`) opacity, never a separate grey.

### Named Rules
**The Warm-Only-Red Rule.** Neutrals stay cold and grey-green. The red and the photographs are the only warm elements; never add beige, cream or a second accent hue.

**The Present-Red Rule.** Red is not reserved for one button per screen. Use it to orient (current page, dates, status) and to carry emphasis blocks, as long as text on red stays white (#FFFFFF) and readable.

## Typography

**Display Font:** Geist (self-hosted, variable 100–900, fallback system-ui)
**Body Font:** Geist
**Label/Mono Font:** Geist Mono (self-hosted, 400–600)

**Character:** One sharp, neutral grotesque used at extreme weights and tight tracking for headlines, relaxed for reading; the mono face makes every number look measured, like a value written in a hut book.

### Hierarchy
- **Display** (720, clamp(46px, 7.6vw, 116px), 0.92): hero headlines only; one per page.
- **Headline** (700, clamp(34px, 4.6vw, 64px), 0.98): section titles.
- **Title** (650, clamp(22px, 2vw, 28px), 1.08): card, hut and course names, fact group headings.
- **Lead** (400, clamp(18px, 1.5vw, 21px), 1.5): intro paragraphs, max 56ch.
- **Body** (400, 17px, 1.6): running text; cards use 15–15.5px.
- **Label** (550, 13px, +0.02em): category tags above titles, in lichene.
- **Data** (Geist Mono, 15px, tabular figures): altitudes, years, times; big stats use Geist 650 at clamp(42px, 5vw, 72px) with tabular figures.

### Named Rules
**The Measured Number Rule.** Every factual number (quota, anno, tempo di salita, posti) is set in Geist Mono or with tabular figures. Numbers are evidence; they must look exact.

**The Tight Headline Rule.** Headings use negative tracking (-0.025em to -0.05em) and line-height at or below 1.08, with `text-wrap: balance`. Never set a heading loose.

## Layout

Content sits in a centred container (max 1320px) with a fluid gutter of clamp(20px, 4vw, 48px). Sections breathe with clamp(72px, 10vw, 136px) vertical padding; consecutive plain sections drop the top padding, alternate granite sections restore it. Splits use asymmetric 5/7 or 4/8 columns with clamp(40px, 6vw, 96px) gaps and a sticky intro column on desktop. Huts use a 12-column grid (two big cards of 6, then cards of 3); activities use a 3-column bento with a tall photo tile; courses use a horizontal snap rail. The fixed nav is 72px tall with a blurred translucent background; anchors scroll with that offset.

Breakpoints are content-driven: 1180px (desktop nav collapses to the menu button), 900px (splits and bento stack), 600px and 560px (single column, nav CTA hidden), 480px (fact lists stack). No horizontal page scroll at 320–430px.

## Elevation & Depth

Depth comes from three sources: photographs with dark scrims, tonal layering between neve and granite surfaces, and one shadow (`0 22px 44px -24px rgba(18,30,26,.45)`) used today for dropdown menus and, softer, for the nav once scrolled. Following the confirmed "solid and tactile" direction, interactive cards and buttons may gain real weight: a pressed state (already `translateY(1px) scale(.985)` on buttons), lift and shadow on hover for cards, firmer borders. Static text blocks stay flat.

### Shadow Vocabulary
- **Rilievo** (`box-shadow: 0 22px 44px -24px rgba(18,30,26,.45)`): floating layers (dropdowns) and hovered interactive cards.
- **Nav scrolled** (`box-shadow: 0 10px 30px -22px rgba(18,24,22,.5)`): the fixed nav after scrolling.

### Named Rules
**The Depth-Means-Touch Rule.** Shadow and lift belong to things you can press or that float. Text, sections and static facts never get a shadow.

## Shapes

Square corners everywhere (0px radius): buttons, cards, images, inputs, tiles, menus. Borders are 1px hairlines in `--line` or 1.5px in `--line-strong` on secondary buttons and menu toggles. Photos are cropped to fixed ratios (3:2 huts, 4:5 courses, 4:3 bands on mobile) and zoom slightly (1.03–1.04) on hover inside their frame.

## Components

### Buttons
- **Shape:** square (0px), min height 48px, 22px horizontal padding, Geist 600 15px.
- **Primary:** rosso CAS fill, white text; hover rosso CAS profondo; press nudges down 1px and scales to 0.985.
- **Secondary:** transparent with 1.5px `--line-strong` border, ardesia text; border turns ardesia on hover.
- **Light / Ghost-light:** for use on photos: bianco-su-foto fill with ardesia text, or a translucent white outline.
- **Arrow:** buttons and text links may carry a → that slides 3px on hover.

### Text links
- **Style:** 600 15px, no underline, trailing →, min height 44px; turn red on hover.

### Cards / Containers
- **Hut, course and news cards:** whole card is the link; photo in a granite frame above, title turns red on hover, metadata in lichene, numbers (altitude, beds, times) in mono. On hover the photo lifts 4px with the rilievo shadow and settles back when pressed. On phones the four small huts of the home become compact rows (square photo left, no description).
- **Photo tiles (bento):** image fills the tile under a bottom-up dark gradient; text in bianco-su-foto.
- **Callout / contact:** granite-chiaro block, generous fluid padding, no border. `.callout--accent` is the red variant (white text, light button, white focus ring) for a call to action such as the home's volunteer appeal.

### Navigation
- Fixed top bar, 72px, translucent neve with blur; gains a hairline and soft shadow once scrolled. Logo: the crest `assets/logo-cas-stemma.webp` (44px tall in the bar, 52px in the footer) with HTML text in Geist beside it, «CAS Ticino» 20px bold on top and «Club Alpino Svizzero» 12px in ardesia-2 below (23/13.5px in the footer). Links in ardesia-2, current page in red; dropdowns are square panels with the rilievo shadow. Under 1180px the links fold into a full-screen menu (large 30px group titles) built by `site.js`; the red CTA stays at the bottom.

### Signature: Key facts
Hut pages open with a row of big facts (quota, posti, tempo d'accesso) at clamp(26px, 2.6vw, 36px), labels above in lichene: the hut-book entry made visible.

## Do's and Don'ts

### Do:
- **Do** keep every corner at 0px radius. The one exception, chosen by the section: profile portraits (Comitato, Organizzazione, Capigita) are squircles (`corner-shape: squircle` at 50% radius, falling back to a 30% rounded square).
- **Do** set altitudes, years, times and counts in Geist Mono or tabular figures.
- **Do** use real photographs from `assets/img/` and Droptour; put text on photos only over the dark scrim gradients.
- **Do** give interactive elements weight: pressed states, hover lift, firm borders.
- **Do** let red carry orientation and emphasis, including larger blocks when a section needs it.
- **Do** keep every color in the `:root` tokens; don't reintroduce an automatic dark theme.

### Don't:
- **Don't** introduce rounded corners, pills or soft blobs.
- **Don't** add warm neutrals (beige, cream) or a second accent color.
- **Don't** use stock or illustrative imagery in place of real section photos.
- **Don't** put shadows on static text blocks or whole sections.
- **Don't** hard-code colors in inline styles; use the custom properties in `assets/site.css`.
