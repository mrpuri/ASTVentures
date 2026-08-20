#!/usr/bin/env python3
"""Build a single self-contained HTML preview of the whole site (all 7 pages,
fonts, logos, CSS and JS inlined) so it can be opened or shared as one file."""
import base64, os, re
from build_site import PAGES, render, EMAIL, PHONE, ADDRESS

BASE = os.path.dirname(os.path.abspath(__file__))


def b64(path, mime):
    with open(os.path.join(BASE, path), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


css = open(os.path.join(BASE, "assets/styles.css")).read()
# inline fonts
for m in sorted(set(re.findall(r"url\('(fonts/[^']+)'\)", css))):
    css = css.replace(f"url('{m}')", f"url('{b64('assets/' + m, 'font/woff2')}')")

logo = b64("assets/logo.svg", "image/svg+xml")
logo_white = b64("assets/logo-white.svg", "image/svg+xml")
favicon = b64("assets/favicon.svg", "image/svg+xml")

NAV = [("schools.html", "For Schools"), ("universities.html", "For Universities"),
       ("programs.html", "For Students"), ("franchise.html", "Franchise"),
       ("about.html", "About"), ("contact.html", "Contact")]

sections = []
for filename, title, desc in PAGES:
    body = render(open(os.path.join(BASE, "parts", filename)).read())
    sections.append(f'<div class="page" data-page="{filename}" hidden>{body}</div>')

js = open(os.path.join(BASE, "assets/site.js")).read()

nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)

html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AST Ventures — AI Skills &amp; Training | Site preview</title>
<link rel="icon" href="{favicon}">
<meta name="theme-color" content="#1F6FEB">
<style>{css}
.page[hidden]{{display:none}}
.preview-bar{{background:#0A2145;color:#BFD6FF;font:600 12px/1 'InterAST',system-ui;
  letter-spacing:.06em;text-transform:uppercase;padding:9px 26px;text-align:center}}
</style></head><body>
<div class="preview-bar">Single-file preview &mdash; all seven pages, click the navigation</div>
<header class="header"><div class="wrap header-inner">
  <a class="brand" href="index.html" aria-label="AST Ventures home"><img src="{logo}" alt="AST Ventures — AI Skills &amp; Training"></a>
  <nav class="nav">{nav}</nav>
  <div class="header-cta">
    <a class="btn btn-primary btn-sm" href="contact.html">Talk to us</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span></button>
  </div>
</div></header>
<div class="mobile-nav">{nav}<a class="btn btn-primary" href="contact.html">Talk to us</a></div>
<main>{''.join(sections)}</main>
<footer class="footer"><div class="wrap">
  <div class="footer-grid">
    <div><img class="flogo" src="{logo_white}" alt="AST Ventures">
      <p class="desc">AI Skills &amp; Training. We build the delivery infrastructure for AI education in Punjab and tier-2 and tier-3 India — labs, curriculum, teachers and career programs.</p></div>
    <div><h5>Work with us</h5><a href="schools.html">For Schools</a><a href="universities.html">For Universities</a><a href="programs.html">For Students &amp; Parents</a><a href="franchise.html">Franchise Partners</a></div>
    <div><h5>Company</h5><a href="about.html">About AST</a><a href="about.html">Our thesis</a><a href="contact.html">Contact</a></div>
    <div><h5>Reach us</h5><a href="mailto:{EMAIL}">{EMAIL}</a><a href="#">{PHONE}</a><a href="contact.html">{ADDRESS}</a></div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 AST Ventures. AI Skills &amp; Training. All rights reserved.</span><span>Built in Jalandhar, Punjab.</span></div>
</div></footer>
<script>
(function(){{
  var pages = document.querySelectorAll('.page');
  function show(name){{
    var found=false;
    pages.forEach(function(p){{
      var on = p.getAttribute('data-page')===name;
      p.hidden=!on; if(on) found=true;
    }});
    if(!found) pages[0].hidden=false;
    document.querySelectorAll('.nav a,.mobile-nav a').forEach(function(a){{
      a.classList.toggle('active', a.getAttribute('href')===name);
    }});
    window.scrollTo(0,0);
    document.querySelectorAll('.reveal').forEach(function(el){{el.classList.add('in')}});
  }}
  document.addEventListener('click', function(e){{
    var a = e.target.closest && e.target.closest('a[href]');
    if(!a) return;
    var href = a.getAttribute('href');
    if(!href || /^(https?:|mailto:|tel:)/.test(href)) return;
    if(href.charAt(0)==='#'){{
      var el=document.getElementById(href.slice(1));
      if(el){{e.preventDefault(); el.scrollIntoView({{behavior:'smooth'}});}}
      return;
    }}
    e.preventDefault();
    var parts = href.split('#');
    show(parts[0]);
    document.querySelector('.mobile-nav').classList.remove('open');
    if(parts[1]){{ var t=document.getElementById(parts[1]); if(t) setTimeout(function(){{t.scrollIntoView({{behavior:'smooth'}})}},60); }}
  }});
  show('index.html');
}})();
{js}
</script></body></html>"""

out = os.path.join(BASE, "ast-ventures-preview.html")
open(out, "w").write(html)
print("wrote", out, f"{len(html)/1024:.0f} KB")
