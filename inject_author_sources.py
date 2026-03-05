import os, glob

AUTHOR_BOX = '''
<!-- AUTHOR BOX -->
<div class="author-box" style="max-width:860px;margin:40px auto 0;">
  <img src="/marco.jpg" alt="Marco Bozem" class="author-img">
  <div class="author-info">
    <span class="author-label">Autor</span>
    <strong class="author-name">Marco Bozem</strong>
    <p class="author-bio">Unabh&auml;ngiger Investor &amp; Finanz-Analyst mit Fokus auf Hard Assets, Rohstoffe und Cashflow-Strategien. Gr&uuml;nder von MB Capital Strategies.</p>
    <div class="author-links">
      <a href="/ueber-marco-bozem/">&Uuml;ber Marco</a>
      <a href="https://www.youtube.com/@mbcapitalstrategies" target="_blank" rel="noopener">YouTube</a>
      <a href="https://www.linkedin.com/in/marco-bozem/" target="_blank" rel="noopener">LinkedIn</a>
    </div>
  </div>
</div>

<!-- SOURCES BOX -->
<div class="sources-box" style="max-width:860px;margin:16px auto 0;">
  <h4>Datenquellen &amp; Referenzen</h4>
  <ul>
    <li>Fundamentaldaten &amp; Kennzahlen: <a href="https://www.investing.com/pro/" target="_blank" rel="noopener sponsored">InvestingPro</a></li>
    <li>Offizielle Gesch&auml;ftsberichte: Investor Relations des Unternehmens</li>
    <li>Marktpreise &amp; Charts: Yahoo Finance</li>
    <li>Nachrichten &amp; Meldungen: Reuters, Bloomberg</li>
  </ul>
  <p class="sources-disclaimer">Keine Anlageberatung. Alle Angaben ohne Gew&auml;hr. Bitte eigene Due Diligence durchf&uuml;hren.</p>
</div>

'''

ANCHOR = '<!-- ======================== MB CAPITAL INSIDER NEWSLETTER ======================== -->'
ANCHOR_ALT = '<!-- ======================== MB CAPITAL NEWSLETTER ======================== -->'

blog_dir = '/home/user/Mbcapitalstategieslanding/blog'
files = glob.glob(os.path.join(blog_dir, '*.html'))

updated = 0
skipped_already = 0
skipped_no_anchor = 0

for fpath in sorted(files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'author-box' in content:
        skipped_already += 1
        continue

    anchor = None
    if ANCHOR in content:
        anchor = ANCHOR
    elif ANCHOR_ALT in content:
        anchor = ANCHOR_ALT

    if not anchor:
        skipped_no_anchor += 1
        print(f"  NO ANCHOR: {os.path.basename(fpath)}")
        continue

    new_content = content.replace(anchor, AUTHOR_BOX + anchor, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    updated += 1

print(f"Updated:          {updated}")
print(f"Already had box:  {skipped_already}")
print(f"No anchor found:  {skipped_no_anchor}")
