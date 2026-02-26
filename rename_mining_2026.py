#!/usr/bin/env python3
"""
rename_mining_2026.py – Benennt 9 Mining-Analyse-Artikel von -2025 auf -2026 um.

Schritte pro Artikel:
1. Liest alte -2025.html
2. Erstellt neue -2026.html (aktualisiert canonical, title, Schema-URLs, dateModified)
3. Ersetzt alte -2025.html durch Meta-Refresh-Redirect → neue URL
4. Aktualisiert blog/index.html, sitemap-blog.xml + alle internen Querverweise
"""

import os, re, shutil

BASE = '/home/user/Mbcapitalstategieslanding'

# Nur die 9 Mining-Artikel (keine Pipeline-Artikel)
MINING_SLUGS = [
    'thungela-resources-analyse',
    'whitehaven-coal-analyse',
    'yancoal-australia-analyse',
    'bhp-analyse',
    'fortescue-analyse',
    'rio-tinto-analyse',
    'vale-analyse',
    'glencore-analyse',
    'kazatomprom-analyse',
]

def transform_for_2026(content, old_slug, new_slug):
    """Aktualisiert URLs, canonical, title und Schema in der kopierten Datei."""
    # 1. Dateinamen-Slug überall ersetzen (canonical, breadcrumb, BlogPosting item, href etc.)
    content = content.replace(old_slug + '.html', new_slug + '.html')

    # 2. Titel-Tag: "Analyse 2025" → "Analyse 2026" (nur Titel-Tag, nicht Fließtext)
    content = re.sub(
        r'(<title>[^<]*?)\b2025\b([^<]*?</title>)',
        lambda m: m.group(0).replace('2025', '2026'),
        content
    )

    # 3. breadcrumb "name" field: "… 2025 …" → "… 2026 …"
    content = re.sub(
        r'("name":\s*"[^"]*?)2025([^"]*?")',
        r'\g<1>2026\2',
        content
    )

    # 4. dateModified aktualisieren
    content = re.sub(
        r'"dateModified":\s*"[^"]*"',
        '"dateModified": "2026-02-26"',
        content
    )

    return content


def make_redirect_page(old_url_path, new_url_path):
    """Erstellt eine einfache Meta-Refresh-Redirect-Seite."""
    new_full_url = 'https://mbcapitalstrategies.com' + new_url_path
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url={new_full_url}">
  <link rel="canonical" href="{new_full_url}">
  <title>Weitergeleitet…</title>
</head>
<body>
  <p>Diese Seite wurde verschoben. <a href="{new_full_url}">Klicke hier, falls du nicht automatisch weitergeleitet wirst.</a></p>
</body>
</html>
"""


results = []

for base_slug in MINING_SLUGS:
    old_filename = base_slug + '-2025.html'
    new_filename = base_slug + '-2026.html'
    old_filepath = os.path.join(BASE, 'blog', old_filename)
    new_filepath = os.path.join(BASE, 'blog', new_filename)

    if not os.path.exists(old_filepath):
        print(f"⚠️  NOT FOUND: blog/{old_filename}")
        continue

    # Prüfe ob neue Datei bereits existiert
    if os.path.exists(new_filepath):
        print(f"  ⚠️  Already exists: blog/{new_filename} – überschreibe")

    # 1. Lese alte Datei
    with open(old_filepath, 'r', encoding='utf-8') as f:
        old_content = f.read()

    old_slug_full = base_slug + '-2025'
    new_slug_full = base_slug + '-2026'

    # 2. Erstelle neue Datei mit aktualisierten URLs/Titeln
    new_content = transform_for_2026(old_content, old_slug_full, new_slug_full)

    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  ✅ Created: blog/{new_filename}")

    # 3. Ersetze alte Datei durch Redirect
    redirect_html = make_redirect_page(
        '/blog/' + old_filename,
        '/blog/' + new_filename
    )
    with open(old_filepath, 'w', encoding='utf-8') as f:
        f.write(redirect_html)
    print(f"  ↩️  Redirect: blog/{old_filename} → {new_filename}")

    results.append((old_filename, new_filename))


# ─── Aktualisiere blog/index.html ─────────────────────────────────────────────
blog_index = os.path.join(BASE, 'blog', 'index.html')
with open(blog_index, 'r', encoding='utf-8') as f:
    idx = f.read()

original_idx = idx
for old_fn, new_fn in results:
    idx = idx.replace(old_fn, new_fn)

if idx != original_idx:
    with open(blog_index, 'w', encoding='utf-8') as f:
        f.write(idx)
    print(f"\n  ✅ blog/index.html aktualisiert")
else:
    print(f"\n  ⏭  blog/index.html – keine Änderung nötig")


# ─── Aktualisiere sitemap-blog.xml ────────────────────────────────────────────
sitemap = os.path.join(BASE, 'sitemap-blog.xml')
with open(sitemap, 'r', encoding='utf-8') as f:
    sm = f.read()

original_sm = sm
for old_fn, new_fn in results:
    sm = sm.replace(old_fn, new_fn)

if sm != original_sm:
    with open(sitemap, 'w', encoding='utf-8') as f:
        f.write(sm)
    print(f"  ✅ sitemap-blog.xml aktualisiert")
else:
    print(f"  ⏭  sitemap-blog.xml – keine Änderung nötig")


# ─── Aktualisiere Querverweise in anderen Blog-Artikeln ───────────────────────
blog_dir = os.path.join(BASE, 'blog')
for fn in os.listdir(blog_dir):
    if not fn.endswith('.html'):
        continue
    fp = os.path.join(blog_dir, fn)
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    for old_fn, new_fn in results:
        c = c.replace(old_fn, new_fn)
    if c != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"  ✅ Querverweise in blog/{fn} aktualisiert")


# ─── Aktualisiere mining-aktien/index.html falls vorhanden ───────────────────
mining_hub = os.path.join(BASE, 'mining-aktien', 'index.html')
if os.path.exists(mining_hub):
    with open(mining_hub, 'r', encoding='utf-8') as f:
        mh = f.read()
    orig = mh
    for old_fn, new_fn in results:
        mh = mh.replace(old_fn, new_fn)
    if mh != orig:
        with open(mining_hub, 'w', encoding='utf-8') as f:
            f.write(mh)
        print(f"  ✅ mining-aktien/index.html aktualisiert")


print(f"\n✅ Done! {len(results)} Artikel umbenannt.")
