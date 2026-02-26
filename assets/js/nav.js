/**
 * MB Capital Strategies – Shared Navigation + Scroll Reveal
 * Handles: hamburger menu, dropdown toggles, click-outside-close, scroll reveal
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', init);

  function init() {
    setupHamburger();
    setupDropdowns();
    setupScrollReveal();
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
}());
