/**
 * MB Capital Strategies – Shared Navigation + Scroll Reveal + Reading Progress
 * Handles: hamburger menu, dropdown toggles, click-outside-close, scroll reveal, reading bar
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', init);

  function init() {
    setupHamburger();
    setupDropdowns();
    setupScrollReveal();
    setupReadingProgress();
    setupActiveNav();
  }

  /* ── Hamburger / Mobile Nav ── */
  function setupHamburger() {
    var hamburger = document.getElementById('navHamburger');
    var mobileNav = document.getElementById('navMobile');
    if (!hamburger || !mobileNav) return;

    hamburger.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = mobileNav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    document.addEventListener('click', function (e) {
      if (!mobileNav.contains(e.target) && !hamburger.contains(e.target)) {
        mobileNav.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ── Dropdowns ── */
  function setupDropdowns() {
    var dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function (dropdown) {
      var btn = dropdown.querySelector('.dropdown-btn');
      if (!btn) return;

      /* Mobile: toggle on click */
      btn.addEventListener('click', function (e) {
        if (window.innerWidth < 700) {
          e.stopPropagation();
          dropdown.classList.toggle('open');
        }
      });
    });

    /* Click outside → close all dropdowns */
    document.addEventListener('click', function (e) {
      dropdowns.forEach(function (d) {
        if (!d.contains(e.target)) d.classList.remove('open');
      });
    });
  }

  /* ── Scroll Reveal ── */
  function setupScrollReveal() {
    var reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

    if (!('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('visible'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach(function (el) { observer.observe(el); });
  }

  /* ── Reading Progress Bar ── */
  function setupReadingProgress() {
    /* Only activate on blog articles (not hub/index pages) */
    var isArticle = document.querySelector('.article-body, article, .article-hero');
    if (!isArticle) return;

    var bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.id = 'readingProgress';
    document.body.insertBefore(bar, document.body.firstChild);

    function updateProgress() {
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var pct = docHeight > 0 ? Math.min(100, (scrollTop / docHeight) * 100) : 0;
      bar.style.width = pct + '%';
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  /* ── Mark current nav link as active ── */
  function setupActiveNav() {
    var path = window.location.pathname;
    var links = document.querySelectorAll('.nav-links a, .nav-mobile a');
    links.forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href) return;
      /* Exact or starts-with match for directory paths */
      if (
        (path === href) ||
        (href.length > 1 && path.startsWith(href) && href !== '/')
      ) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
  }
}());
