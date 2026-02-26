#!/usr/bin/env python3
"""
add_nav.py – Fügt kanonische Nav zu Seiten hinzu, die keine haben
oder eine veraltete einfache <header>-Nav verwenden.
"""

import os, re

BASE = '/home/user/Mbcapitalstategieslanding'

# Kanonische Nav HTML (identisch mit dem was fix_nav.py auf Content-Seiten setzt)
CANONICAL_NAV_HTML = """\
<header class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand">
      <img src="/Logo.png" alt="MB Capital Strategies Logo" width="44" height="44">
      <span>MB Capital Strategies</span>
    </a>
    <button class="nav-hamburger" id="navHamburger" aria-label="Menü öffnen" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav-links" aria-label="Hauptnavigation">
      <a href="/">Startseite</a>
      <a href="/depot-strategie/">Depot-Strategie</a>
      <a href="/hard-asset-guide/">Hard Asset Guide</a>
      <div class="dropdown">
        <button class="dropdown-btn" aria-haspopup="true">Themen ▾</button>
        <div class="dropdown-content">
          <a href="/shipping/">🚢 Shipping</a>
          <a href="/midstream/">🛢️ Pipelines / Midstream</a>
          <a href="/mining-aktien/">⛏️ Mining Aktien</a>
          <a href="/upstream-aktien/">🛢️ Upstream Aktien</a>
          <hr>
          <a href="/kategorien/high-yield-aktien.html">💰 High-Yield Aktien</a>
          <a href="/rohstoff-superzyklus-master.html">🌋 Rohstoff Superzyklus</a>
          <hr>
          <a href="/bestenlisten/beste-lng-aktien-2025.html">🔥 Beste LNG-Aktien 2026</a>
          <a href="/bestenlisten/beste-tanker-aktien-2025.html">🚢 Beste Tanker-Aktien 2026</a>
          <a href="/bestenlisten/top-5-high-yield-aktien-2025.html">💸 Top 5 High-Yield 2026</a>
        </div>
      </div>
      <div class="dropdown">
        <button class="dropdown-btn" aria-haspopup="true">Podcast ▾</button>
        <div class="dropdown-content">
          <a href="/podcast/">🎧 Alle Podcasts</a>
          <hr>
          <a href="/podcast/der-finanzfeuer-talk.html">🔥 Finanzfeuer Talk</a>
          <a href="/podcast/mein-weg-zur-dividendenstrategie-2025.html">💰 Dividenden-Journey</a>
          <a href="/podcast/timing-ist-alles-dividendenstrategie-podcast-2025.html">⏱️ Timing & Zyklen</a>
          <hr>
          <a href="/podcast/maritime-investments-schifffahrtsaktien-2025.html">🚢 Maritime / Shipping</a>
          <a href="/podcast/bdc-aktien-erklaert-2025.html">🏦 BDC Aktien</a>
          <a href="/podcast/mining-serie-high-dividend-ressourcen-2025-2028.html">⛏️ Mining Serie</a>
        </div>
      </div>
      <a href="/blog/">Blog</a>
      <a href="/investing-analysen.html">Investing.com</a>
      <a href="/rechner/" class="nav-highlight">Rechner</a>
    </nav>
  </div>
  <!-- Mobile Nav -->
  <nav class="nav-mobile" id="navMobile" aria-label="Mobile Navigation">
    <div class="mob-label">Navigation</div>
    <a href="/">🏠 Startseite</a>
    <a href="/depot-strategie/">📊 Depot-Strategie</a>
    <a href="/hard-asset-guide/">🧱 Hard Asset Guide</a>
    <a href="/blog/">📰 Blog</a>
    <a href="/rechner/">🧮 Alle Rechner</a>
    <a href="/investing-analysen.html">🔗 Investing.com</a>
    <a href="/toolbox.html">🧰 Toolbox</a>
    <a href="/glossar/">📗 Glossar</a>
    <div class="mob-label">Themen</div>
    <a href="/shipping/">🚢 Shipping</a>
    <a href="/midstream/">🛢️ Midstream / Pipelines</a>
    <a href="/mining-aktien/">⛏️ Mining Aktien</a>
    <a href="/upstream-aktien/">🛢️ Upstream Aktien</a>
    <a href="/kategorien/high-yield-aktien.html">💰 High-Yield Aktien</a>
    <a href="/rohstoff-superzyklus-master.html">🌋 Rohstoff Superzyklus</a>
    <div class="mob-label">Podcast</div>
    <a href="/podcast/">🎧 Alle Podcasts</a>
    <a href="/podcast/der-finanzfeuer-talk.html">🔥 Finanzfeuer Talk</a>
    <a href="/podcast/mining-serie-high-dividend-ressourcen-2025-2028.html">⛏️ Mining Serie</a>
  </nav>
</header>"""

# Pages to fix: list of (filepath, strategy)
# strategy: 'replace_header' = replace old <header>...</header>
#           'insert_after_body' = insert after <body>
TARGETS = [
    ('shipping/index.html', 'replace_header'),
    ('shipping/shipindex.html', 'replace_header'),
    ('rohstoff-superzyklus-master.html', 'insert_after_body'),
    ('rohstoffe/kupfer-superzyklus.html', 'replace_header'),
    ('rohstoffe/nickel-superzyklus.html', 'replace_header'),
    ('rohstoffe/uran-superzyklus.html', 'replace_header'),
    ('rohstoffe/zink-superzyklus.html', 'replace_header'),
    ('glossar/shipping-cluster.html', 'replace_header'),
    ('kategorien/rohstoff-superzyklus-2025-2030.html', 'replace_header'),
    ('blog/meine-toolbox-broker-tools-plattformen-2025.html', 'replace_header'),
]

# Pattern: matches a simple <header>...</header> that is NOT class="nav"
OLD_HEADER_PATTERN = re.compile(
    r'<header(?! class="nav")[^>]*>.*?</header>',
    re.DOTALL
)

for relpath, strategy in TARGETS:
    filepath = os.path.join(BASE, relpath)
    if not os.path.exists(filepath):
        print(f"⚠️  NOT FOUND: {relpath}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    if strategy == 'replace_header':
        # Check if it has a header.nav already
        if '<header class="nav">' in content:
            print(f"  ✅ Already has .nav header: {relpath}")
            continue
        # Replace old <header> with canonical nav
        new_content = OLD_HEADER_PATTERN.sub(CANONICAL_NAV_HTML, content, count=1)
        if new_content == content:
            print(f"  ⚠️  No old header found: {relpath}")
            continue

    elif strategy == 'insert_after_body':
        if '<header class="nav">' in content:
            print(f"  ✅ Already has .nav header: {relpath}")
            continue
        # Insert after <body>
        new_content = content.replace('<body>', '<body>\n\n' + CANONICAL_NAV_HTML + '\n', 1)
        if new_content == content:
            print(f"  ⚠️  No <body> found: {relpath}")
            continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  ✅ Fixed: {relpath}")

print("\n✅ Done!")
