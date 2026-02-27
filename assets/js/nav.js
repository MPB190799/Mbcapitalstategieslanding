/**
 * MB Capital Strategies – Shared Navigation + Scroll Reveal + Reading Progress
 * + Cookie Consent (DSGVO/GDPR) + Author Bio Injection + Article Schema Injection
 *
 * v3 – Nav HTML injection: one source of truth for navigation across all 100+ pages
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
    injectNav();          /* must run first – creates nav DOM */
    setupHamburger();
    setupDropdowns();
    setupScrollReveal();
    setupReadingProgress();
    setupActiveNav();
    setupAuthorBio();
    injectArticleSchema();
    if (!existingConsent) setupCookieBanner();
  });

  /* ═══════════════════════════════════════════════════════════
     NAV INJECTION
     Replaces the nav element on every page with the canonical
     navigation HTML from the homepage (gold standard).
     One change here = consistent nav on all 100+ pages.
  ═══════════════════════════════════════════════════════════ */
  function injectNav() {
    var existing = document.querySelector('nav.nav, header.nav');
    if (!existing) return;

    var html =
      '<nav class="nav" id="main-nav">' +
        '<div class="nav-inner">' +
          '<a href="/" class="nav-brand">' +
            '<img src="/Logo.png" alt="MB Capital Strategies" width="44" height="44">' +
            '<span>MB Capital Strategies</span>' +
          '</a>' +
          '<div class="nav-links">' +
            '<a href="/">Startseite</a>' +
            '<a href="/depot-strategie/">Depot</a>' +
            '<a href="/hard-asset-guide/">Hard Asset Guide</a>' +
            '<div class="dropdown">' +
              '<button class="dropdown-btn" aria-haspopup="true">Themen &#x25be;</button>' +
              '<div class="dropdown-content">' +
                '<a href="/shipping-aktien/">🚢 Shipping Aktien</a>' +
                '<a href="/midstream/">🛢️ Pipelines / Midstream</a>' +
                '<a href="/mining-aktien/">⛏️ Mining Aktien</a>' +
                '<a href="/upstream-aktien/">🛢️ Upstream Aktien</a>' +
                '<a href="/dividendenstrategie/">💰 Dividendenstrategie</a>' +
                '<hr>' +
                '<a href="/kategorien/high-yield-aktien.html">🏦 High-Yield &amp; BDC</a>' +
                '<a href="/rohstoff-superzyklus-master.html">🌋 Rohstoff Superzyklus</a>' +
                '<hr>' +
                '<a href="/bestenlisten/beste-lng-aktien-2025.html">🔥 Beste LNG-Aktien 2026</a>' +
                '<a href="/bestenlisten/beste-tanker-aktien-2025.html">🚢 Beste Tanker-Aktien 2026</a>' +
                '<a href="/bestenlisten/top-5-high-yield-aktien-2025.html">💸 Top 5 High-Yield 2026</a>' +
              '</div>' +
            '</div>' +
            '<div class="dropdown">' +
              '<button class="dropdown-btn" aria-haspopup="true">Podcast &#x25be;</button>' +
              '<div class="dropdown-content">' +
                '<a href="/podcast/">🎧 Alle Podcasts</a>' +
                '<hr>' +
                '<a href="/podcast/der-finanzfeuer-talk.html">🔥 Finanzfeuer Talk</a>' +
                '<a href="/podcast/mein-weg-zur-dividendenstrategie-2025.html">💰 Dividenden-Journey</a>' +
                '<a href="/podcast/timing-ist-alles-dividendenstrategie-podcast-2025.html">⏱️ Timing &amp; Zyklen</a>' +
                '<hr>' +
                '<a href="/podcast/maritime-investments-schifffahrtsaktien-2025.html">🚢 Maritime / Shipping</a>' +
                '<a href="/podcast/bdc-aktien-erklaert-2025.html">🏦 BDC Aktien</a>' +
                '<a href="/podcast/mining-serie-high-dividend-ressourcen-2025-2028.html">⛏️ Mining Serie</a>' +
              '</div>' +
            '</div>' +
            '<a href="/blog/">Blog</a>' +
            '<a href="/investing-analysen.html">Investing.com</a>' +
            '<a href="/rechner/" class="nav-highlight">Rechner</a>' +
          '</div>' +
          '<button class="nav-hamburger" id="navHamburger" aria-label="Menü öffnen" aria-expanded="false">' +
            '<span></span><span></span><span></span>' +
          '</button>' +
        '</div>' +
        '<nav class="nav-mobile" id="navMobile" aria-label="Mobile Navigation">' +
          '<div class="mob-label">Navigation</div>' +
          '<a href="/">🏠 Startseite</a>' +
          '<a href="/depot-strategie/">📊 Depot-Strategie</a>' +
          '<a href="/hard-asset-guide/">🧱 Hard Asset Guide</a>' +
          '<a href="/blog/">📰 Blog</a>' +
          '<a href="/rechner/">🧮 Alle Rechner</a>' +
          '<a href="/investing-analysen.html">🔗 Investing.com</a>' +
          '<a href="/toolbox.html">🧰 Toolbox</a>' +
          '<a href="/glossar/">📗 Glossar</a>' +
          '<div class="mob-label">Themen</div>' +
          '<a href="/shipping-aktien/">🚢 Shipping Aktien</a>' +
          '<a href="/midstream/">🛢️ Midstream / Pipelines</a>' +
          '<a href="/mining-aktien/">⛏️ Mining Aktien</a>' +
          '<a href="/upstream-aktien/">🛢️ Upstream Aktien</a>' +
          '<a href="/dividendenstrategie/">💰 Dividendenstrategie</a>' +
          '<a href="/kategorien/high-yield-aktien.html">🏦 High-Yield &amp; BDC</a>' +
          '<a href="/rohstoff-superzyklus-master.html">🌋 Rohstoff Superzyklus</a>' +
          '<div class="mob-label">Podcast</div>' +
          '<a href="/podcast/">🎧 Alle Podcasts</a>' +
          '<a href="/podcast/der-finanzfeuer-talk.html">🔥 Finanzfeuer Talk</a>' +
          '<a href="/podcast/mining-serie-high-dividend-ressourcen-2025-2028.html">⛏️ Mining Serie</a>' +
        '</nav>' +
      '</nav>';

    /* Replace the existing nav element (works for both <nav> and <header>) */
    existing.outerHTML = html;
  }

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

  /* ═══════════════════════════════════════════════════════════
     AUTHOR BIO INJECTION
     Automatically injects a visible author bio on all blog
     article pages. Skips index and tool-listing pages.
  ═══════════════════════════════════════════════════════════ */
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

    /* Try multiple selectors to find a good insertion point */
    var anchor = (
      document.querySelector('nav.breadcrumb') ||
      document.querySelector('nav.breadcrumbs') ||
      document.querySelector('.breadcrumb') ||
      document.querySelector('.breadcrumbs') ||
      document.querySelector('section.container') ||
      document.querySelector('.page-wrapper') ||
      document.querySelector('.container h1') ||
      null
    );

    /* Fallback: insert after the main nav */
    if (!anchor) {
      anchor = document.querySelector('#main-nav, nav.nav');
    }
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

  /* ═══════════════════════════════════════════════════════════
     ARTICLE SCHEMA INJECTION
     Automatically adds BlogPosting JSON-LD to blog articles
     that don't already have an Article/BlogPosting schema.
     This fixes YMYL / E-E-A-T anonymity for legacy articles.
  ═══════════════════════════════════════════════════════════ */
  function injectArticleSchema() {
    var path = window.location.pathname;

    var isBlogArticle = (
      path.startsWith('/blog/') &&
      path !== '/blog/' &&
      !path.endsWith('index.html') &&
      !path.endsWith('alle-finanzrechner.html') &&
      !path.endsWith('meine-toolbox-broker-tools-plattformen-2025.html') &&
      !path.endsWith('wise-airalo-vietnam-erfahrungen.html')
    );
    if (!isBlogArticle) return;

    /* Check if Article/BlogPosting schema already exists */
    var scripts = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < scripts.length; i++) {
      try {
        var data = JSON.parse(scripts[i].textContent || scripts[i].innerText);
        if (data['@type'] === 'Article' || data['@type'] === 'BlogPosting') return;
        if (data['@graph']) {
          for (var j = 0; j < data['@graph'].length; j++) {
            var t = data['@graph'][j]['@type'];
            if (t === 'Article' || t === 'BlogPosting') return;
          }
        }
      } catch (e) { /* skip malformed JSON */ }
    }

    /* Extract headline from h1 or title */
    var h1El = document.querySelector('h1');
    var headline = h1El ? h1El.textContent.trim().replace(/^[^\w]+/, '') : document.title;

    /* Extract description from meta description */
    var descMeta = document.querySelector('meta[name="description"]');
    var description = descMeta ? descMeta.getAttribute('content') : '';

    /* Extract date from URL (year pattern) or og:updated_time */
    var datePublished = extractDateFromPage();

    /* Extract canonical URL */
    var canonicalEl = document.querySelector('link[rel="canonical"]');
    var url = canonicalEl ? canonicalEl.getAttribute('href') : window.location.href;

    /* Extract image from og:image */
    var imgMeta = document.querySelector('meta[property="og:image"]');
    var image = imgMeta ? imgMeta.getAttribute('content') : 'https://mbcapitalstrategies.com/marco.jpg';

    var schema = {
      '@context': 'https://schema.org',
      '@type': 'BlogPosting',
      'headline': headline.substring(0, 110),
      'description': description,
      'url': url,
      'image': image,
      'datePublished': datePublished,
      'dateModified': datePublished,
      'author': {
        '@type': 'Person',
        'name': 'Marco Bozem',
        'url': 'https://mbcapitalstrategies.com/ueber-marco-bozem/',
        'sameAs': [
          'https://www.youtube.com/@mbcapitalstrategies',
          'https://www.linkedin.com/in/marco-bozem-182173295'
        ]
      },
      'publisher': {
        '@type': 'Organization',
        'name': 'MB Capital Strategies',
        'url': 'https://mbcapitalstrategies.com/',
        'logo': {
          '@type': 'ImageObject',
          'url': 'https://mbcapitalstrategies.com/Logo.png'
        }
      },
      'mainEntityOfPage': {
        '@type': 'WebPage',
        '@id': url
      }
    };

    var script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  }

  function extractDateFromPage() {
    /* 1. Try article:published_time meta */
    var pt = document.querySelector('meta[property="article:published_time"]');
    if (pt) return pt.getAttribute('content');

    /* 2. Try datePublished in existing ld+json */
    var scripts = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < scripts.length; i++) {
      try {
        var d = JSON.parse(scripts[i].textContent || scripts[i].innerText);
        if (d.datePublished) return d.datePublished;
      } catch (e) {}
    }

    /* 3. Extract from URL: analyse-2026, februar-2026, etc. */
    var path = window.location.pathname;
    var m2026 = path.match(/\b2026\b/);
    var m2025 = path.match(/\b2025\b/);

    if (m2026) {
      /* Month hints in URL */
      if (/januar/.test(path))   return '2026-01-15';
      if (/februar/.test(path))  return '2026-02-15';
      if (/maerz/.test(path))    return '2026-03-15';
      return '2026-01-01';
    }
    if (m2025) return '2025-06-01';

    return '2025-01-01';
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
