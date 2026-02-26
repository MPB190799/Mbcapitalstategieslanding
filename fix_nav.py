#!/usr/bin/env python3
"""
fix_nav.py – Vereinheitlicht die Navigation auf ALLEN HTML-Seiten.

Änderungen:
1. Ersetzt Sektoren/Themen-Dropdown (+ optionalen Podcast-Dropdown) durch kanonische Versionen
2. Setzt mobiles Nav-Label "Sektoren" → "Themen" + aktualisiert mobile Links
3. Behebt Homepage-Duplikat (Upstream Aktien × 2) + /blog/index.html → /blog/
"""

import os, re

BASE = '/home/user/Mbcapitalstategieslanding'

# ─────────────────────────────────────────────────────────────────────────────
# KANONISCHER NAV-BLOCK (Desktop): Themen + Podcast
# Indent: 6 Spaces für <div class="dropdown">, 8 für Inhalte, 10 für Links
# ─────────────────────────────────────────────────────────────────────────────
CANONICAL_NAV = """\
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
      </div>"""

# ─────────────────────────────────────────────────────────────────────────────
# REGEX: Desktop-Dropdown (Sektoren oder Themen) + optionaler Podcast
# Matcht den kompletten Block mit 6-Space-Indent
# ─────────────────────────────────────────────────────────────────────────────
DROPDOWN_PATTERN = re.compile(
    r'      <div class="dropdown">\n'
    r'        <button[^>]*>(?:Sektoren|Themen) ▾</button>\n'
    r'        <div class="dropdown-content">.*?</div>\n'
    r'      </div>'
    r'(?:\n      <div class="dropdown">\n'
    r'        <button[^>]*>Podcast ▾</button>\n'
    r'        <div class="dropdown-content">.*?</div>\n'
    r'      </div>)?',
    re.DOTALL
)

# ─────────────────────────────────────────────────────────────────────────────
# REGEX: Mobile-Nav Sektoren-Sektion
# ─────────────────────────────────────────────────────────────────────────────
MOB_SEKTOREN_PATTERN = re.compile(
    r'( +)<div class="mob-label">Sektoren</div>\n'
    r'(.*?)'
    r'(?=\1<div class="mob-label">)',
    re.DOTALL
)

def get_mob_canonical(indent):
    i = indent
    return (
        f'{i}<div class="mob-label">Themen</div>\n'
        f'{i}<a href="/shipping/">🚢 Shipping</a>\n'
        f'{i}<a href="/midstream/">🛢️ Midstream / Pipelines</a>\n'
        f'{i}<a href="/mining-aktien/">⛏️ Mining Aktien</a>\n'
        f'{i}<a href="/upstream-aktien/">🛢️ Upstream Aktien</a>\n'
        f'{i}<a href="/kategorien/high-yield-aktien.html">💰 High-Yield Aktien</a>\n'
        f'{i}<a href="/rohstoff-superzyklus-master.html">🌋 Rohstoff Superzyklus</a>\n'
    )

# ─────────────────────────────────────────────────────────────────────────────
# CONTENT PAGES: Desktop + Mobile Nav fixen
# ─────────────────────────────────────────────────────────────────────────────
def fix_content_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. Desktop-Nav: Sektoren/Themen + Podcast → kanonisch
    content = DROPDOWN_PATTERN.sub(CANONICAL_NAV, content, count=1)

    # 2. Mobile-Nav: Sektoren-Sektion → kanonisch
    def mob_repl(m):
        return get_mob_canonical(m.group(1))
    content = MOB_SEKTOREN_PATTERN.sub(mob_repl, content, count=1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ─────────────────────────────────────────────────────────────────────────────
# HOMEPAGE: Nur Duplikat + /blog/index.html fixen
# ─────────────────────────────────────────────────────────────────────────────
def fix_homepage(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Duplikat Upstream entfernen: zwei aufeinanderfolgende gleiche Links
    content = re.sub(
        r'(<a href="/upstream-aktien/">[^\n]+</a>)\n[ \t]+<a href="/upstream-aktien/">[^\n]+</a>',
        r'\1',
        content
    )

    # /blog/index.html → /blog/ (Desktop + Mobile)
    content = content.replace(
        '<a href="/blog/index.html">Blog</a>',
        '<a href="/blog/">Blog</a>'
    )
    content = content.replace(
        '<a href="/blog/index.html">📰 Blog</a>',
        '<a href="/blog/">📰 Blog</a>'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Homepage fixed: {os.path.basename(filepath)}")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
homepage = os.path.join(BASE, 'index.html')
fix_homepage(homepage)

fixed_count = 0
skipped = []

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for filename in files:
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(root, filename)
        if filepath == homepage:
            continue
        if fix_content_page(filepath):
            fixed_count += 1
            print(f"  ✅ {os.path.relpath(filepath, BASE)}")
        else:
            skipped.append(os.path.relpath(filepath, BASE))

print(f"\n{'='*60}")
print(f"✅ Content-Seiten aktualisiert: {fixed_count}")
if skipped:
    print(f"⏭  Keine Änderung nötig ({len(skipped)} Seiten):")
    for s in skipped[:10]:
        print(f"     {s}")
    if len(skipped) > 10:
        print(f"     ... und {len(skipped)-10} weitere")
