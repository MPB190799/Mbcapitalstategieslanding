/**
 * MB Capital Strategies – Shared Navigation + Scroll Reveal + Reading Progress
 * + Cookie Consent (DSGVO/GDPR) + Author Bio Injection
 */
(function () {
  'use strict';

  /* ── Google Consent Mode v2 Defaults (set before AdSense) ── */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  var CONSENT_KEY = 'mbcs_consent_v1';
  var existingConsent = localStorage.getItem(CONSENT_KEY);

  gtag('consent', 'default', {
    'ad_storage':         existingConsent === 'granted' ? 'granted' : 'denied',
    'analytics_storage':  existingConsent === 'granted' ? 'granted' : 'denied',
    'ad_user_data':       existingConsent === 'granted' ? 'granted' : 'denied',
    'ad_personalization': existingConsent === 'granted' ? 'granted' : 'denied'
  });

  /* ── Boot ── */
  document.addEventListener('DOMContentLoaded', function () {
    setupHamburger();
    setupDropdowns();
    setupScrollReveal();
    setupReadingProgress();
    setupActiveNav();
    setupAuthorBio();
    if (!existingConsent) setupCookieBanner();
  });

  /* ── Hamburger / Mobile Nav ── */
  function setupHamburger() {
    var hamburger = document.getElementById('navHamburger');
    var mobileNav  = document.getElementById('navMobile');
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

      btn.addEventListener('click', function (e) {
        if (window.innerWidth < 700) {
          e.stopPropagation();
          dropdown.classList.toggle('open');
        }
      });
    });

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
    var isArticle = document.querySelector('.article-body, article, .article-hero');
    if (!isArticle) return;

    var bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.id = 'readingProgress';
    document.body.insertBefore(bar, document.body.firstChild);

    function updateProgress() {
      var scrollTop  = window.scrollY || document.documentElement.scrollTop;
      var docHeight  = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var pct        = docHeight > 0 ? Math.min(100, (scrollTop / docHeight) * 100) : 0;
      bar.style.width = pct + '%';
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  /* ── Mark current nav link as active ── */
  function setupActiveNav() {
    var path  = window.location.pathname;
    var links = document.querySelectorAll('.nav-links a, .nav-mobile a');
    links.forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href) return;
      if ((path === href) || (href.length > 1 && path.startsWith(href) && href !== '/')) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  /* ── Author Bio Injection ────────────────────────────────────
     Automatically injects a visible author bio on all blog
     article pages. Skips index and tool-listing pages.
  ─────────────────────────────────────────────────────────── */
  function setupAuthorBio() {
    var path = window.location.pathname;

    var isBlogArticle = (
      path.startsWith('/blog/') &&
      path !== '/blog/' &&
      !path.endsWith('index.html') &&
      !path.endsWith('alle-finanzrechner.html')
    );
    if (!isBlogArticle) return;
    if (document.querySelector('.author-bio-inject')) return;

    /* Insert after breadcrumbs nav, or before first section */
    var anchor = document.querySelector('nav.breadcrumbs');
    if (!anchor) anchor = document.querySelector('section.container, .page-wrapper');
    if (!anchor) return;

    var bio = document.createElement('div');
    bio.className = 'author-box author-bio-inject';
    bio.innerHTML =
      '<a href="/ueber-marco-bozem/" style="flex-shrink:0;">' +
        '<img src="/marco.jpg" alt="Marco Bozem – MB Capital Strategies"' +
          ' width="62" height="62" loading="lazy">' +
      '</a>' +
      '<div class="author-info">' +
        '<h4><a href="/ueber-marco-bozem/" style="color:inherit;text-decoration:none;">' +
          'Marco Bozem</a></h4>' +
        '<p>' +
          'Unabhängiger Investor &amp; Gründer von MB Capital Strategies. ' +
          'Fokus auf Hard Assets: Energie, Shipping, Mining &amp; Midstream-Pipelines. ' +
          '<a href="/ueber-marco-bozem/" style="color:#d4af37;">Über Marco →</a>' +
          '&nbsp;·&nbsp;' +
          '<a href="https://www.youtube.com/@mbcapitalstrategies"' +
            ' target="_blank" rel="noopener" style="color:#d4af37;">YouTube</a>' +
          '&nbsp;·&nbsp;' +
          '<a href="https://www.linkedin.com/in/marco-bozem-182173295"' +
            ' target="_blank" rel="noopener" style="color:#d4af37;">LinkedIn</a>' +
        '</p>' +
      '</div>';

    anchor.insertAdjacentElement('afterend', bio);
  }

  /* ── Cookie Consent Banner (DSGVO) ──────────────────────────
     Shows bottom-sticky banner on first visit.
     Uses Google Consent Mode v2.
  ─────────────────────────────────────────────────────────── */
  function setupCookieBanner() {
    var style = document.createElement('style');
    style.textContent =
      '#cookie-banner{' +
        'position:fixed;bottom:0;left:0;right:0;z-index:9999;' +
        'background:rgba(15,17,21,0.97);' +
        'border-top:1px solid rgba(212,175,55,0.35);' +
        'padding:16px 20px;' +
        'font-family:"Montserrat",system-ui,sans-serif;' +
        'font-size:0.85rem;color:#ccc;' +
        'backdrop-filter:blur(12px);' +
      '}' +
      '#cookie-banner-inner{' +
        'max-width:1100px;margin:0 auto;' +
        'display:flex;flex-wrap:wrap;align-items:center;gap:14px;' +
      '}' +
      '#cookie-banner-inner p{margin:0;flex:1;min-width:200px;line-height:1.6;}' +
      '#cookie-banner-inner a{color:#d4af37;}' +
      '#cookie-buttons{display:flex;gap:10px;flex-shrink:0;}' +
      '.cookie-btn{' +
        'padding:9px 18px;border:none;border-radius:8px;' +
        'font-weight:700;font-size:0.83rem;cursor:pointer;' +
        'font-family:inherit;' +
      '}' +
      '.cookie-btn-primary{background:#d4af37;color:#000;}' +
      '.cookie-btn-primary:hover{filter:brightness(1.1);}' +
      '.cookie-btn-secondary{' +
        'background:transparent;color:#9aa6c0;' +
        'border:1px solid rgba(212,175,55,0.25);' +
      '}' +
      '.cookie-btn-secondary:hover{color:#d4af37;border-color:#d4af37;}';

    document.head.appendChild(style);

    var banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie-Einstellungen');
    banner.innerHTML =
      '<div id="cookie-banner-inner">' +
        '<p>' +
          'Diese Website verwendet Cookies für Werbeanzeigen (Google AdSense), ' +
          'eingebettete YouTube-Videos und Affiliate-Links. ' +
          'Mehr dazu in der <a href="/datenschutz.html">Datenschutzerklärung</a>.' +
        '</p>' +
        '<div id="cookie-buttons">' +
          '<button id="cookie-accept" class="cookie-btn cookie-btn-primary">Alle akzeptieren</button>' +
          '<button id="cookie-decline" class="cookie-btn cookie-btn-secondary">Nur notwendige</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(banner);

    document.getElementById('cookie-accept').addEventListener('click', function () {
      localStorage.setItem(CONSENT_KEY, 'granted');
      gtag('consent', 'update', {
        'ad_storage':         'granted',
        'analytics_storage':  'granted',
        'ad_user_data':       'granted',
        'ad_personalization': 'granted'
      });
      banner.remove();
    });

    document.getElementById('cookie-decline').addEventListener('click', function () {
      localStorage.setItem(CONSENT_KEY, 'denied');
      banner.remove();
    });
  }

}());
