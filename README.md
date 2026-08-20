# AST Ventures — website

Static multi-page site for **AST Ventures (AI Skills & Training)**, Jalandhar, Punjab.
No build step, no dependencies. Upload the folder to any web host and it runs.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home — thesis, the four models, why Punjab, platform, FAQ |
| `schools.html` | AI Campus-in-a-Box (CBSE 2026–27 mandate) + school enquiry form |
| `universities.html` | Centre for Applied AI + campus enquiry form |
| `programs.html` | AI Career Program & Young AI Innovators + application form |
| `franchise.html` | Franchise licence model + franchise-pack request form |
| `about.html` | The thesis, convictions, partnerships |
| `contact.html` | Contact details + general enquiry form |

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
  site.js             nav, scroll reveals, count-ups, form handling
  fonts/              self-hosted Plus Jakarta Sans + Inter (woff2)
```

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
