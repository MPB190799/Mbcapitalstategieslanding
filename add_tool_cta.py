#!/usr/bin/env python3
"""Add YOC-Rechner CTA block to blog articles that don't already link to the calculator tools."""

import os
import glob

BASE = '/home/user/Mbcapitalstategieslanding/blog'

TOOL_CTA = '''
<!-- Interner CTA: YOC-Rechner -->
<div class="cta-box" style="border-left:4px solid #d4af37;margin:28px 0;">
  <h3 style="margin:0 0 8px;color:#d4af37;">🧮 Deine persönliche Dividendenrendite berechnen</h3>
  <p style="margin:0 0 12px;color:#cfd6e6;">Wie stark arbeitet dein eingesetztes Kapital wirklich? Der <strong>Yield-on-Cost-Rechner</strong> zeigt dir deine persönliche Rendite auf den Einstandskurs – kostenlos & sofort.</p>
  <a href="/tools/yield-on-cost-rechner.html" style="display:inline-block;background:#d4af37;color:#0f1115;font-weight:700;padding:10px 22px;border-radius:6px;text-decoration:none;">Zum YOC-Rechner →</a>
  <a href="/rechner/" style="display:inline-block;margin-left:10px;color:#d4af37;font-weight:600;text-decoration:none;font-size:0.9em;">Alle Rechner →</a>
</div>'''

SKIP_PATTERNS = [
    'yield-on-cost-rechner',
    'dividendenrechner',
    'noindex',
    'tool-cta',
]

# Insert before disclaimer or cta-box or related-articles
INSERT_BEFORE = [
    '<div class="disclaimer"',
    '<div class="related-articles"',
    '<p class="sources-disclaimer"',
    '<div class="cta-box"',
]

def should_skip(content):
    for p in SKIP_PATTERNS:
        if p in content:
            return True
    return False

def add_cta(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if should_skip(content):
        return False

    # Find insertion point
    for marker in INSERT_BEFORE:
        idx = content.find(marker)
        if idx != -1:
            content = content[:idx] + TOOL_CTA + '\n' + content[idx:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

    return False

if __name__ == '__main__':
    files = glob.glob(os.path.join(BASE, '*.html'))
    added = 0
    skipped = 0
    not_found = 0

    for fp in sorted(files):
        result = add_cta(fp)
        if result is True:
            print(f'  [+] Added CTA to {os.path.basename(fp)}')
            added += 1
        elif result is False and not should_skip(open(fp).read()):
            print(f'  [?] No insertion point in {os.path.basename(fp)}')
            not_found += 1
        else:
            skipped += 1

    print(f'\nDone: {added} added, {skipped} skipped (already have link), {not_found} no insertion point found')
