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

  // mark current nav item
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a, .mobile-nav a').forEach(function (a) {
    if (a.getAttribute('href') === here) a.classList.add('active');
  });
})();
