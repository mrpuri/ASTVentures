#!/usr/bin/env python3
"""Assemble the AST Ventures static site from shared shell + page bodies."""
import os, re

SITE = "AST Ventures"
EMAIL = "palak@astventures.in"
PHONE = "+91 98776 88718"
ADDRESS = "Jalandhar, Punjab 144001, India"

NAV = [
    ("Education", [
        ("schools.html", "Schools", "AI labs, curriculum and teachers"),
        ("colleges.html", "Colleges", "NEP credit courses in AI and blockchain"),
        ("universities.html", "Universities", "A Centre for Applied AI on campus"),
        ("programs.html", "Students &amp; Parents", "Career program and weekend batches"),
    ]),
    ("intellistudio.html", "Intellistudio"),
    ("gcc.html", "GCCs in Punjab"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

ICONS = {
    "school": '<path d="M3 9.5 12 4l9 5.5-9 5.5-9-5.5Z"/><path d="M7 12.4V17c0 1.2 2.2 2.4 5 2.4s5-1.2 5-2.4v-4.6"/><path d="M21 9.5V15"/>',
    "campus": '<path d="M4 20V9.6L12 5l8 4.6V20"/><path d="M9.5 20v-5.2h5V20"/><path d="M2.5 20h19"/>',
    "student": '<path d="M12 3 2.8 7.8 12 12.6l9.2-4.8L12 3Z"/><path d="M6.4 10.2v4.6c0 1.7 2.5 3.1 5.6 3.1s5.6-1.4 5.6-3.1v-4.6"/><path d="M21.2 7.8v5.4"/>',
    "college": '<path d="M12 3.2 3.4 7.6h17.2L12 3.2Z"/><path d="M6 10.4v6.4M10 10.4v6.4M14 10.4v6.4M18 10.4v6.4"/><path d="M4.2 16.8h15.6M2.8 20.4h18.4"/>',
    "project": '<path d="M4.5 6.4A1.9 1.9 0 0 1 6.4 4.5h3.1l1.7 2.4h6.4a1.9 1.9 0 0 1 1.9 1.9v8.7a1.9 1.9 0 0 1-1.9 1.9H6.4a1.9 1.9 0 0 1-1.9-1.9V6.4Z"/><path d="m9.6 13.4 1.9 1.9 3.4-3.9"/>',
    "chain": '<path d="M10.1 13.9a3.6 3.6 0 0 0 5.4.4l2.4-2.4a3.6 3.6 0 0 0-5.1-5.1l-1.4 1.4"/><path d="M13.9 10.1a3.6 3.6 0 0 0-5.4-.4l-2.4 2.4a3.6 3.6 0 0 0 5.1 5.1l1.4-1.4"/>',
    "factory": '<path d="M3 20.5V10.2l5 3v-3l5 3v-3l5 3V4h3v16.5H3Z"/><path d="M6.5 17h2M11 17h2M15.5 17h2"/>',
    "truck": '<path d="M2.8 6.2h10.6v10.2H2.8z"/><path d="M13.4 9.6h4.2l3.4 3.4v3.4h-7.6"/><circle cx="6.6" cy="17.6" r="1.9"/><circle cx="17" cy="17.6" r="1.9"/>',
    "rupee": '<path d="M7 4.5h10M7 9h10"/><path d="M7 4.5h3.6a4.5 4.5 0 0 1 0 9H7l7.6 7"/>',
    "receipt": '<path d="M6 3.5h12v17l-2.4-1.6-2.4 1.6-2.4-1.6-2.4 1.6L6 20.5v-17Z"/><path d="M9 8h6M9 11.5h6M9 15h3.6"/>',
    "chat": '<path d="M4.5 5.5h15v10.2h-8.4L6.8 19.5v-3.8H4.5V5.5Z"/><path d="M8.5 9.6h7M8.5 12.3h4.5"/>',
    "chip": '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "book": '<path d="M4 5.2A2.2 2.2 0 0 1 6.2 3H19v14.6H6.2A2.2 2.2 0 0 0 4 19.8V5.2Z"/><path d="M4 19.8A2.2 2.2 0 0 0 6.2 22H19"/>',
    "teacher": '<circle cx="12" cy="7.5" r="3.4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
    "spark": '<path d="M12 3.2 13.9 9l5.9 1.9-5.9 1.9L12 18.7l-1.9-5.9L4.2 10.9 10.1 9 12 3.2Z"/><path d="M18.6 3v3.4M20.3 4.7h-3.4"/>',
    "shield": '<path d="M12 3.2 20 6v6.1c0 4.4-3.2 7.4-8 8.7-4.8-1.3-8-4.3-8-8.7V6l8-2.8Z"/><path d="m9 12 2.2 2.2L15.4 10"/>',
    "network": '<circle cx="6" cy="7" r="2.6"/><circle cx="18" cy="7" r="2.6"/><circle cx="12" cy="18" r="2.6"/><path d="M7.9 8.9 10.6 16M16.1 8.9 13.4 16M8.6 7h6.8"/>',
    "growth": '<path d="M4 19.5h16"/><path d="M6.5 19.5V13M11 19.5V8.4M15.5 19.5v-4.6M20 19.5V4.5"/>',
    "globe": '<circle cx="12" cy="12" r="8.6"/><path d="M3.6 12h16.8M12 3.4c2.3 2.4 3.5 5.4 3.5 8.6S14.3 18.2 12 20.6c-2.3-2.4-3.5-5.4-3.5-8.6S9.7 5.8 12 3.4Z"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.3V12l3.2 2"/>',
    "hand": '<path d="M12 21c-4.4 0-7.5-2.7-7.5-6.6V9.2a1.6 1.6 0 0 1 3.2 0V6.1a1.6 1.6 0 0 1 3.2 0V4.8a1.6 1.6 0 0 1 3.2 0v1.7a1.6 1.6 0 0 1 3.2 0v6.1c0 4.8-2 8.4-5.3 8.4Z"/>',
}


def icon(name):
    return f'<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg></span>'


def head(title, desc, page):
    navlinks, mnavlinks = [], []
    for item in NAV:
        if isinstance(item[1], list):
            label, children = item
            menu = "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in children)
            navlinks.append(
                f'<div class="nav-group"><button class="nav-trigger" type="button" aria-expanded="false">'
                f'{label}<span class="caret" aria-hidden="true"></span></button>'
                f'<div class="nav-menu">{menu}</div></div>')
            mnavlinks.append(f'<span class="mnav-label">{label}</span>' +
                             "".join(f'<a class="mnav-sub" href="{h}">{t}</a>' for h, t, _ in children))
        else:
            h, t = item
            navlinks.append(f'<a href="{h}">{t}</a>')
            mnavlinks.append(f'<a href="{h}">{t}</a>')
    navlinks, mnavlinks = "".join(navlinks), "".join(mnavlinks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1F6FEB">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/logo-mark.png">
<link rel="preload" href="assets/fonts/plus-jakarta-sans-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="AST Ventures home"><img src="assets/logo.svg" alt="AST Ventures — AI Skills &amp; Training"></a>
    <nav class="nav">{navlinks}</nav>
    <div class="header-cta">
      <a class="btn btn-primary btn-sm" href="contact.html">Talk to us</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-nav">{mnavlinks}<a class="btn btn-primary" href="contact.html">Talk to us</a></div>
<main>
"""


FOOTER = f"""</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img class="flogo" src="assets/logo-white.svg" alt="AST Ventures">
        <p class="desc">AI Skills &amp; Training. AI enablement for schools, colleges and universities &mdash; proven in industry through Intellistudio and the GCCs we bring to Punjab.</p>
      </div>
      <div>
        <h5>Education</h5>
        <a href="schools.html">Schools</a>
        <a href="colleges.html">Colleges</a>
        <a href="universities.html">Universities</a>
        <a href="programs.html">Students &amp; Parents</a>
      </div>
      <div>
        <h5>Industry</h5>
        <a href="intellistudio.html">Intellistudio</a>
        <a href="intellistudio.html#estimate">Savings estimator</a>
        <a href="gcc.html">GCCs in Punjab</a>
        <a href="gcc.html#how">Build&ndash;operate&ndash;transfer</a>
      </div>
      <div>
        <h5>Company</h5>
        <a href="about.html">About AST</a>
        <a href="index.html#projects">Active projects</a>
        <a href="index.html#advisors">Advisory board</a>
        <a href="index.html#media">Talks &amp; media</a>
        <a href="contact.html">Contact</a>
      </div>
      <div>
        <h5>Reach us</h5>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="tel:+919877688718">{PHONE}</a>
        <a href="contact.html">{ADDRESS}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 AST Ventures. AI Skills &amp; Training. All rights reserved.</span>
      <span>Built in Jalandhar, Punjab.</span>
    </div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


PAGES = [
    ("index.html", "AST Ventures — AI enablement for schools, colleges and universities",
     "AST Ventures brings AI to schools, colleges and universities in Punjab and beyond — and proves it in industry with Intellistudio, its AI platform for manufacturers, and global capability centres built in Punjab."),
    ("schools.html", "AI Campus-in-a-Box for Schools | AST Ventures",
     "Meet the CBSE AI mandate properly. AST Ventures installs the lab, the curriculum and the trained teachers, run on our platform — for schools across Punjab."),
    ("colleges.html", "NEP-aligned AI &amp; Blockchain programs for Colleges | AST Ventures",
     "Credit-bearing AI and blockchain courses for degree and polytechnic colleges, delivered under NEP 2020 — taught by industry trainers, with faculty enablement built in."),
    ("universities.html", "Centre for Applied AI for Universities | AST Ventures",
     "An industry-grade Centre for Applied AI on your campus, badged with your institution. Curriculum, labs, faculty enablement and placement-ready student projects."),
    ("programs.html", "AI Career Program &amp; Young AI Innovators | AST Ventures",
     "Learn at the AST flagship in Jalandhar: a 6-month AI Career Program for graduates and Young AI Innovators weekend batches for school students."),
    ("intellistudio.html", "Intellistudio — the AI company brain for manufacturers | AST Ventures",
     "Intellistudio connects a manufacturer's systems and automates the repetitive work across production, sales, procurement, finance and running account bills. Estimate the hours and money it would save your plant."),
    ("gcc.html", "Start a GCC in Punjab | AST Ventures",
     "Open a Global Capability Centre in Punjab. AST builds and trains the team — feasibility, hiring from partner campuses, pre-hire bootcamps on your stack, launch support and handover."),
    ("about.html", "About AST Ventures | The thesis behind AI-native education in India",
     "We are building the operating system for AI-native education in India, starting from Jalandhar, Punjab — where India's AI mandate lands first."),
    ("contact.html", "Contact AST Ventures | Jalandhar, Punjab",
     "Talk to the AST Ventures team about school labs, NEP college courses, university centres or student programs."),
]


def render(body):
    def sub(m):
        return icon(m.group(1))
    return re.sub(r"\{\{icon:([a-z]+)\}\}", sub, body)


def main():
    for filename, title, desc in PAGES:
        with open(os.path.join("parts", filename)) as f:
            body = render(f.read())
        html = head(title, desc, filename) + body + FOOTER
        with open(filename, "w") as f:
            f.write(html)
        print("wrote", filename, f"{len(html)/1024:.1f} KB")


if __name__ == "__main__":
    main()
