/* AST Ventures — site behaviour */
(function () {
  'use strict';

  // sticky header shadow
  var header = document.querySelector('.header');
  function onScroll() {
    if (!header) return;
    header.classList.toggle('scrolled', window.scrollY > 8);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // mobile nav
  var burger = document.querySelector('.burger');
  var mnav = document.querySelector('.mobile-nav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') mnav.classList.remove('open');
    });
  }

  // photo placeholders — a photo fades in only once it has actually loaded, and
  // an <img> whose file isn't there yet is dropped, leaving the initials disc /
  // captioned tile underneath. Add the real file at the src path and it appears.
  // (Without JS the images simply show as normal — see .js rules in styles.css.)
  document.documentElement.classList.add('js');
  document.querySelectorAll('.person-photo img, .shot-img img, .video-thumb img').forEach(function (img) {
    function fail() {
      // video thumbs carry a smaller YouTube size to fall back to before giving up
      var alt = img.getAttribute('data-fallback');
      if (alt) { img.removeAttribute('data-fallback'); img.src = alt; return; }
      if (img.parentNode) img.parentNode.removeChild(img);
    }
    function ok() {
      // YouTube answers a missing maxres thumbnail with a tiny grey placeholder
      // rather than a 404, so treat an implausibly small image as a miss too
      if (img.getAttribute('data-fallback') && img.naturalWidth < 200) { fail(); return; }
      img.classList.add('is-loaded');
    }
    img.addEventListener('load', ok);
    img.addEventListener('error', fail);
    if (img.complete) { img.naturalWidth > 0 ? ok() : fail(); }
  });

  // videos load only on click — nothing is requested from YouTube before that
  document.querySelectorAll('.video').forEach(function (card) {
    var btn = card.querySelector('.video-thumb');
    if (!btn || !card.dataset.yt) return;
    btn.addEventListener('click', function () {
      var frame = document.createElement('iframe');
      frame.className = 'video-frame';
      frame.src = 'https://www.youtube-nocookie.com/embed/' + card.dataset.yt + '?autoplay=1&rel=0';
      frame.title = btn.getAttribute('aria-label') || 'Video';
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      frame.allowFullscreen = true;
      btn.replaceWith(frame);
    });
  });

  // reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 4, 3) * 70 + 'ms';
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // count-up for stat numbers
  var stats = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && stats.length) {
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        so.unobserve(el);
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var dec = (String(target).split('.')[1] || '').length;
        var start = null, dur = 1300;
        function tick(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = (target * eased).toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.4 });
    stats.forEach(function (el) { so.observe(el); });
  }

  // enquiry forms — front-end only demo handling
  document.querySelectorAll('form[data-enquiry]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var box = form.querySelector('.form-success') ||
                (form.parentElement && form.parentElement.querySelector('.form-success'));
      if (box) {
        box.classList.add('show');
        box.textContent = 'Thanks — your enquiry has been recorded. The AST team will get back to you within two working days.';
        box.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      form.reset();
    });
  });

  // mark current nav item — and its dropdown group, if it lives in one
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a, .mobile-nav a').forEach(function (a) {
    if (a.getAttribute('href') !== here) return;
    a.classList.add('active');
    var group = a.closest('.nav-group');
    if (group) group.querySelector('.nav-trigger').classList.add('active');
  });

  // nav dropdowns — CSS opens them on hover/focus; this adds click/tap and Esc
  document.querySelectorAll('.nav-group').forEach(function (group) {
    var trigger = group.querySelector('.nav-trigger');
    function set(open) {
      group.classList.toggle('open', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      set(!group.classList.contains('open'));
    });
    group.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { set(false); trigger.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!group.contains(e.target)) set(false);
    });
  });

  // savings estimator — every figure derives from the visible inputs
  document.querySelectorAll('[data-estimator]').forEach(function (est) {
    var WEEKS_PER_MONTH = 52 / 12;
    var HOURS_PER_FTE_MONTH = 48 * WEEKS_PER_MONTH;   // six-day, 48-hour week
    var inputs = {};
    est.querySelectorAll('[data-in]').forEach(function (el) { inputs[el.dataset.in] = el; });
    function v(k) { return parseFloat(inputs[k].value); }
    function out(k, text) { var o = est.querySelector('[data-out="' + k + '"]'); if (o) o.textContent = text; }
    function res(k, text) { var o = est.querySelector('[data-res="' + k + '"]'); if (o) o.textContent = text; }
    function trim(s) { return s.replace(/\.0+$/, '').replace(/(\.\d*?)0+$/, '$1'); }
    function inr(n) {   // Indian grouping, lakh / crore for large sums
      if (n >= 1e7) return '₹' + trim((n / 1e7).toFixed(n >= 1e8 ? 1 : 2)) + ' crore';
      if (n >= 1e5) return '₹' + trim((n / 1e5).toFixed(n >= 1e6 ? 1 : 2)) + ' lakh';
      return '₹' + Math.round(n).toLocaleString('en-IN');
    }
    function update() {
      var staff = v('staff'), hours = v('hours'), cost = v('cost'),
          billing = v('billing') * 1e5, days = v('days'), share = v('share') / 100;
      out('staff', staff); out('hours', hours); out('cost', inr(cost));
      out('billing', inr(billing)); out('days', days); out('share', Math.round(share * 100) + '%');

      var freed = staff * hours * WEEKS_PER_MONTH * share;            // hours / month
      var perHour = cost / HOURS_PER_FTE_MONTH;
      var yearly = freed * perHour * 12;
      var cash = billing / 30 * days;                                  // one-time working capital

      res('hours', '~' + Math.round(freed).toLocaleString('en-IN'));
      res('people', (freed / HOURS_PER_FTE_MONTH).toFixed(1));
      res('money', inr(yearly));
      res('cash', inr(cash));
    }
    Object.keys(inputs).forEach(function (k) { inputs[k].addEventListener('input', update); });
    update();
  });
})();
