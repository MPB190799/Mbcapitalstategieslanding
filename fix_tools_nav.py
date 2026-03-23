#!/usr/bin/env python3
"""Fix navigation and footer in all tool pages (except shipping-cashflow-rechner.html which is already correct)."""

import re
import os

BASE = '/home/user/Mbcapitalstategieslanding/tools'

TOOLS = [
    'dividend-snowball-yoc-pro.html',
    'dividenden-reinvest-rechner.html',
    'dividenden-snowball-rechner.html',
    'dividenden-wachstumsrechner.html',
    'dividendenrechner.html',
    'finanzielle-freiheit-rechner.html',
    'yield-on-cost-rechner.html',
]

FOOTER_HTML = '''
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-col">
      <h4>MB Capital Strategies</h4>
      <a href="/">Startseite</a>
      <a href="/ueber-marco-bozem/">Über Marco Bozem</a>
      <a href="/depot-strategie/">Depot-Strategie</a>
      <a href="/hard-asset-guide/">Hard Asset Guide</a>
    </div>
    <div class="footer-col">
      <h4>Sektoren</h4>
      <a href="/shipping-aktien/">Shipping Aktien</a>
      <a href="/mining-aktien/">Mining Aktien</a>
      <a href="/midstream/">Midstream</a>
      <a href="/dividendenstrategie/">Dividendenstrategie</a>
    </div>
    <div class="footer-col">
      <h4>Content & Tools</h4>
      <a href="/blog/">Blog</a>
      <a href="/podcast/">Podcast</a>
      <a href="/rechner/">Finanzrechner</a>
      <a href="/glossar/">Glossar</a>
    </div>
    <div class="footer-col">
      <h4>Rechtliches</h4>
      <a href="/impressum.html">Impressum</a>
      <a href="/datenschutz.html">Datenschutz</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 MB Capital Strategies · Marco Bozem</span>
    <span>Keine Anlageberatung · Alle Angaben ohne Gewähr</span>
  </div>
</footer>'''

def fix_tool(filename):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Add blog/styles.css if missing
    if '/blog/styles.css' not in content:
        content = content.replace(
            '</head>',
            '  <link rel="stylesheet" href="/blog/styles.css?v=3">\n</head>'
        )
        changed = True
        print(f'  [+] Added blog/styles.css to {filename}')

    # 2. Replace mini nav block with empty stub
    # Match <nav class="nav"> ... </nav> block
    nav_pattern = re.compile(
        r'<nav class="nav">.*?</nav>',
        re.DOTALL
    )
    match = nav_pattern.search(content)
    if match:
        old_nav = match.group(0)
        # Only replace if it's the mini-nav (doesn't have nav-brand/dropdown structure)
        if 'nav-brand' not in old_nav and 'dropdown' not in old_nav:
            content = content.replace(old_nav, '<nav class="nav"></nav>', 1)
            changed = True
            print(f'  [+] Replaced mini-nav with stub in {filename}')

    # 3. Add footer if missing
    if 'site-footer' not in content:
        content = content.replace(
            '<script src="/assets/js/nav.js"',
            FOOTER_HTML + '\n<script src="/assets/js/nav.js"'
        )
        changed = True
        print(f'  [+] Added site-footer to {filename}')

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  => Saved {filename}')
    else:
        print(f'  => No changes needed for {filename}')

if __name__ == '__main__':
    for tool in TOOLS:
        print(f'\nProcessing {tool}...')
        fix_tool(tool)
    print('\nDone.')
