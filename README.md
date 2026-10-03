# AST Ventures — website

Static multi-page site for **AST Ventures (AI Skills & Training)**, Jalandhar, Punjab.
No build step, no dependencies. Upload the folder to any web host and it runs.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home — education (schools, colleges, universities) → Intellistudio → GCCs in Punjab → projects, sessions, advisors, media, FAQ |
| `schools.html` | AI Campus-in-a-Box (CBSE 2026–27 mandate) + school enquiry form |
| `colleges.html` | NEP-aligned AI & blockchain courses for colleges + enquiry form |
| `universities.html` | Centre for Applied AI + campus enquiry form |
| `programs.html` | AI Career Program & Young AI Innovators + application form |
| `intellistudio.html` | Intellistudio — the AI company brain for manufacturers, with an interactive savings estimator + walkthrough form |
| `gcc.html` | Start a GCC in Punjab — for companies opening a capability centre + feasibility form |
| `about.html` | The thesis, convictions, partnerships |
| `contact.html` | Contact details + general enquiry form |

The site tells one story, in this order:

1. **AI enablement for education** — schools, colleges and universities (plus career programs for students). These sit under the *Education* menu.
2. **Practical implementation** — Intellistudio, our platform deployed with manufacturers.
3. **GCCs in Punjab** — capability centres built on a build–operate–transfer basis.

The thesis lives on `about.html` only; the home page does not repeat it.

## Assets

```
assets/
  logo.svg                  horizontal lockup — navy (primary logo, site header)
  logo-white.svg            horizontal lockup — reversed, for dark backgrounds (footer)
  logo-stacked.svg          stacked lockup — for square placements
  logo-stacked-white.svg    stacked lockup, reversed
  logo-mark.svg             the steel AST tile (app icon, social avatar)
  logo-wordmark.svg         AST on its own, black
  logo-wordmark-steel.svg   AST on its own, steel
  favicon.svg               browser favicon
  *.png                     transparent raster exports (see Logo below)
  styles.css          the whole design system
  site.js             nav, scroll reveals, count-ups, photo fallbacks, form handling
  fonts/              self-hosted Plus Jakarta Sans + Inter (woff2)
  people/             advisor and program-team photos (see below)
  sessions/           photos from delivered sessions (see below)
```

### Photos — just drop the files in

Every photo slot on the site already has a placeholder that disappears the moment
the real file exists. Nothing to edit, no rebuild needed: **add the file at the exact
path below and reload.** A missing file shows an initials disc (people) or a captioned
navy tile (sessions) instead of a broken image.

| Drop the file at | Shows as |
|---|---|
| `assets/people/rachit-garg.jpg` | Dr. Rachit Garg — advisory board |
| `assets/people/anita-venaik.jpg` | Anita Venaik — advisory board |
| `assets/people/ajay.jpg` | Prof. Ajay — advisory board |
| `assets/people/palakpreet-singh.jpg` | Palakpreet Singh — Chief Coordinator, Atria project |
| `assets/people/prakash-shelar.jpg` | Prakash Shelar — Trainer, Atria project |
| `assets/sessions/nift-panchkula.jpg` | AI & Blockchain teacher training, NIFT Panchkula |
| `assets/sessions/gna-university.jpg` | AI in fraud detection, GNA University |
| `assets/sessions/lpu.jpg` | Blockchain for beginners, LPU |
| `assets/sessions/nit-patna.jpg` | First global FDP on Blockchain, NIT Patna |

`assets/sessions/gulzar-ggi.jpg` (Gulzar Group of Institutes) is already in place — it is the featured *spotlight* session on the home page.

People photos: **square**, around 600×600, face centred. Session photos: **landscape
4:3**, around 1200×800. JPG or PNG (keep the `.jpg` filename or update the `src` in
`parts/index.html`).

The advisors currently show "Advisor" as their role — add each designation and
institution in the `person-role` line in `parts/index.html`, then rebuild.

## Outbound links and video

The **From the field** cards each link to the post about that session, and the
**Talks & media** section (`#media` on the home page) carries the videos, the TEDx
announcement, the book and the BRICS CCI keynote. All of it lives in `parts/index.html`.

Videos are **click-to-play**: the page shows a YouTube thumbnail and builds the player
only when a visitor clicks it, using `youtube-nocookie.com`. Nothing is requested from
YouTube's player before that. To swap a video, change `data-yt="<video id>"` on the
`.video` block and the two `i.ytimg.com` thumbnail URLs inside it. If you would rather
not hotlink Google's thumbnails, save them locally and point the `src` at your own file —
the fallback tile appears if a thumbnail ever fails to load.

### Brand

Logo palette (from the brand pack):

- **Logo navy** `#1d2d3d` — the lockup
- **Steel** `#5980a6` — the icon tile

Site palette (the UI, unchanged):

- **Navy** `#0A2145` — headings, footer
- **Blue** `#1F6FEB` — primary actions, links, accents
- **Blue light** `#3B86F7` / **Blue dark** `#123A8F` — gradients
- **Sky** `#EAF2FE` / `#F5F8FF` — section backgrounds
- **Type**: Plus Jakarta Sans (headings, wordmark), Inter (body)

> The logo and the UI are currently on two slightly different blues — the logo's steel
> `#5980a6` is muted next to the interface's vivid `#1F6FEB`. Nothing looks broken, but
> if you want them unified, retune the `--blue` / `--navy` tokens at the top of
> `assets/styles.css` (and `theme-color` in `build_site.py`) to the pack's colours.

### Logo

The lockup is **AST | VENTURES** over **AI SKILLS & TRAINING**, set in Plus Jakarta Sans.

The lettering is stored as **outlines, not `<text>`** — deliberately. An SVG loaded through
`<img>` cannot reach the page's fonts, so a `<text>` logo with no `font-family` falls back
to the browser's default serif (it renders as Times). Everything is generated:

```bash
python3 build_logo.py   # SVGs — outlines the type with fontTools (needs fontTools + brotli)
python3 build_png.py    # transparent PNG exports (macOS only — uses qlmanage + Pillow)
```

Never hand-edit the SVGs in `assets/`; change `build_logo.py` and re-run both. Geometry is
computed from real glyph widths, so the divider rule and the right-hand column stay aligned
if the type ever changes. Minimum clear space around the lockup = the height of the "A".

## Before you publish — replace these placeholders

1. **Address** — `Jalandhar, Punjab 144001, India`
2. **Forms** — currently front-end only: they validate and show a confirmation
   message but do not send anywhere. Point each `<form data-enquiry="...">` at your
   handler (Formspree, Google Forms, your CRM endpoint) by adding `action` and `method`,
   then delete the `data-enquiry` attribute so `site.js` stops intercepting the submit.
3. **NASSCOM wording** — the site says certification is available "in select areas under a
   signed memorandum of understanding". Confirm this matches the executed MoU before
   going live.
4. **Fees** — deliberately not stated anywhere; all pages say "shared on enquiry".
5. **Photos** — eight of the slots listed above still show placeholders.
6. **Advisor designations** — each advisor currently reads just "Advisor".
7. **Founder attribution** — the Talks & media section credits "our founder, Harman
    Puri". Correct the wording if that is not the right title.

8. **Intellistudio claims** — the product page describes capabilities in general terms
    (connects to "accounting, ERP, spreadsheets, email and messaging"). Name specific
    integrations, add customer names or real case-study figures once they are cleared.
9. **Savings estimator assumptions** — defaults are 10 staff, 15 h/week, ₹35,000/month,
    40% automated, ₹50 lakh billing, 5 days faster. Tune them in `parts/intellistudio.html`
    (slider `value`s) and keep the home page's worked example in step — it quotes the
    same defaults.

## Editing

Pages are generated from `parts/*.html` (body content only) wrapped by the shared
header/footer in `build_site.py`. Edit a file in `parts/`, then:

```bash
python3 build_site.py      # regenerates the nine HTML files
python3 build_logo.py      # regenerates the logo SVGs (needs fontTools + brotli)
```

You can also edit the generated `.html` files directly if you prefer — just remember the
header and footer are duplicated across all nine.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Use a server rather than opening the files directly — the self-hosted fonts are blocked
by the browser under `file://`.
