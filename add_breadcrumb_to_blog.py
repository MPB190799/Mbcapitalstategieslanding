#!/usr/bin/env python3
"""
Adds BreadcrumbList JSON-LD schema to blog articles that don't have one.
"""

import os
import re
import json

BLOG_DIR = "/home/user/Mbcapitalstategieslanding/blog"
BASE_URL = "https://mbcapitalstrategies.com"

SKIP_FILES = {"styles.css", "styles.min.css", "index.html"}

# Map slug keywords to category breadcrumb
def get_category(slug, title):
    t = (slug + " " + title).lower()

    if any(k in t for k in ["pipeline", "pembina", "tc-energy", "enbridge", "oneok", "midstream"]):
        return ("Midstream & Pipelines", f"{BASE_URL}/midstream/")
    if any(k in t for k in ["bdc", "newtek", "hercules", "crescent", "blue-owl", "debitum"]):
        return ("BDC & Dividendenaktien", f"{BASE_URL}/blog/")
    if any(k in t for k in ["shipping", "tanker", "lng", "carrier", "schifffahrt", "avance", "bw-lpg"]):
        return ("Shipping Aktien", f"{BASE_URL}/shipping-aktien/")
    if any(k in t for k in ["mining", "gold", "kupfer", "barrick", "bhp", "rio-tinto", "glencore",
                              "angloamerican", "fortescue", "vale", "fresnillo", "central-asia",
                              "exxaro", "thungela", "yancoal", "whitehaven", "valterra", "gerdau",
                              "jiangxi", "b2gold", "indo-tambangraya", "suncoke"]):
        return ("Mining Aktien", f"{BASE_URL}/mining-aktien/")
    if any(k in t for k in ["energie", "energy", "upstream", "eni", "equinor", "petrobras",
                              "woodside", "panoro", "ecopetrol", "cardinal", "devon", "apa",
                              "aker", "coterra", "repsol", "omv", "kazatomprom", "uran"]):
        return ("Upstream Aktien", f"{BASE_URL}/upstream-aktien/")
    if any(k in t for k in ["rechner", "calculator", "toolbox", "tool", "finanzrechner", "snowball"]):
        return ("Tools & Rechner", f"{BASE_URL}/tools/")
    if any(k in t for k in ["rohstoff", "superzyklus", "dividenden", "dividende", "cashflow",
                              "markt-news", "news"]):
        return ("Blog", f"{BASE_URL}/blog/")

    return ("Blog", f"{BASE_URL}/blog/")


def build_breadcrumb(title, slug, category_name, category_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Startseite",
                "item": f"{BASE_URL}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": category_name,
                "item": category_url
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": f"{BASE_URL}/blog/{slug}.html"
            }
        ]
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if '"BreadcrumbList"' in content:
        return False, "already has breadcrumb"

    if "</head>" not in content:
        return False, "no </head>"

    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""
    # Clean title from site name suffix
    title = re.sub(r'\s*[|–—]\s*MB Capital Strategies.*$', '', title).strip()

    slug = os.path.basename(filepath).replace(".html", "")
    category_name, category_url = get_category(slug, title)

    breadcrumb_json = build_breadcrumb(title, slug, category_name, category_url)
    schema_block = f'\n  <script type="application/ld+json">\n{breadcrumb_json}\n  </script>'

    new_content = content.replace("</head>", schema_block + "\n</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"{category_name}"


def main():
    processed = 0
    skipped = 0

    for filename in sorted(os.listdir(BLOG_DIR)):
        if not filename.endswith(".html"):
            continue
        if filename in SKIP_FILES:
            continue

        filepath = os.path.join(BLOG_DIR, filename)
        try:
            success, msg = process_file(filepath)
            if success:
                print(f"  OK  {filename}: {msg}")
                processed += 1
            else:
                print(f" SKIP {filename}: {msg}")
                skipped += 1
        except Exception as e:
            print(f"  ERR {filename}: {e}")

    print(f"\nDone: {processed} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
