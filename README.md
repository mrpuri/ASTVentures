# AST Ventures — website

Static multi-page site for **AST Ventures (AI Skills & Training)**, Jalandhar, Punjab.
No build step, no dependencies. Upload the folder to any web host and it runs.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home — thesis, the four models, active projects, sessions, advisors, FAQ |
| `schools.html` | AI Campus-in-a-Box (CBSE 2026–27 mandate) + school enquiry form |
| `colleges.html` | NEP-aligned AI & blockchain courses for colleges + enquiry form |
| `universities.html` | Centre for Applied AI + campus enquiry form |
| `programs.html` | AI Career Program & Young AI Innovators + application form |
| `about.html` | The thesis, convictions, partnerships |
| `contact.html` | Contact details + general enquiry form |

The four models are **Schools · Colleges · Universities · Students & Parents**.

## Assets

```
assets/
  logo.svg            horizontal lockup — navy text (primary logo)
  logo-white.svg      horizontal lockup — for dark/blue backgrounds
  logo-stacked.svg    stacked lockup — for square placements
  logo-mark.svg       the monogram tile alone (app icon, social avatar)
  favicon.svg         browser favicon
  *.png               6× raster exports of each of the above (transparent)
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

- **Navy** `#0A2145` — headings, footer
- **Blue** `#1F6FEB` — primary actions, links, accents
- **Blue light** `#3B86F7` / **Blue dark** `#123A8F` — gradients
- **Sky** `#EAF2FE` / `#F5F8FF` — section backgrounds
- **Type**: Plus Jakarta Sans (headings, wordmark), Inter (body)

The mark is a geometric **A** — an ascending chevron with two network nodes at its feet
and a circuit-trace crossbar: rising talent, connected into a network. It reads down to
24 px. Minimum clear space around the lockup = the height of the monogram's corner radius.

## Before you publish — replace these placeholders

1. **Email** — `hello@astventures.in` (appears in the footer and on `contact.html`)
2. **Phone** — `+91 98XXX XXXXX`
3. **Address** — `Jalandhar, Punjab 144001, India`
4. **Forms** — currently front-end only: they validate and show a confirmation
   message but do not send anywhere. Point each `<form data-enquiry="...">` at your
   handler (Formspree, Google Forms, your CRM endpoint) by adding `action` and `method`,
   then delete the `data-enquiry` attribute so `site.js` stops intercepting the submit.
5. **NASSCOM wording** — the site says certification is available "in select areas under a
   signed memorandum of understanding". Confirm this matches the executed MoU before
   going live.
6. **Fees** — deliberately not stated anywhere; all pages say "shared on enquiry".
7. **Photos** — the nine slots listed above still show placeholders.
8. **Advisor designations** — each advisor currently reads just "Advisor".
9. **Book title** — the Amazon card on the home page reads "Our founder's book";
   replace it with the real title (marked with a `TODO` comment in `parts/index.html`).
10. **Founder attribution** — the Talks & media section credits "our founder, Harman
    Puri". Correct the wording if that is not the right title.

## Editing

Pages are generated from `parts/*.html` (body content only) wrapped by the shared
header/footer in `build_site.py`. Edit a file in `parts/`, then:

```bash
python3 build_site.py      # regenerates the seven HTML files
python3 build_logo.py      # regenerates the logo SVGs (needs fontTools + brotli)
```

You can also edit the generated `.html` files directly if you prefer — just remember the
header and footer are duplicated across all seven.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Use a server rather than opening the files directly — the self-hosted fonts are blocked
by the browser under `file://`.
