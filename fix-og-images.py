#!/usr/bin/env python3
"""
Fix OG-Images: Replace marco.jpg with thematic og-images for all blog/tool/page files.
Mapping logic based on filename keywords.
"""
import os
import re

BASE = r"C:/Users/marco/OneDrive/Website Deutsch und Englisch/DE-Seite"

# Keyword -> OG-Image mapping (order matters: first match wins)
MAPPING = [
    # Shipping / Tanker / LNG / Maritime
    (["shipping", "tanker", "lng", "maritime", "schifffahrt", "vessel", "vlcc", "aframax",
      "frontline", "torm", "scorpio", "golar", "flex-lng", "cool-company", "cmb",
      "golden-ocean", "star-bulk", "mpc-container", "avance", "bw-lpg", "hidden-champion"],
     "https://mbcapitalstrategies.com/assets/og-shipping.jpg"),
    # Mining / Gold / Copper / Coal
    (["mining", "gold", "kupfer", "copper", "coal", "barrick", "newmont", "bhp", "rio-tinto",
      "anglogold", "b2gold", "fresnillo", "jiangxi", "central-asia", "thungela", "whitehaven",
      "exxaro", "yancoal", "suncoke", "south32", "valterra", "kazatomprom", "angloamerican",
      "gerdau", "rohstoff", "superzyklus", "uran"],
     "https://mbcapitalstrategies.com/assets/og-mining.jpg"),
    # Energy / Upstream / Oil & Gas
    (["energie", "energy", "upstream", "petrobras", "repsol", "equinor", "aker-bp", "coterra",
      "devon", "chevron", "conocophillips", "apa-aktie", "ecopetrol", "omv", "cardinal",
      "dno", "energean", "harbour", "inplay", "petrotal", "total-gabon", "woodside",
      "var-energi", "aker", "oelreserven", "markt-news"],
     "https://mbcapitalstrategies.com/assets/og-energy.jpg"),
    # Dividends / Yield / BDC / Finance
    (["dividenden", "dividende", "dividend", "yield", "rechner", "bdc", "finanzielle-freiheit",
      "snowball", "reinvest", "cashflow", "debitum", "finanzfeuer", "depot-update",
      "quellensteuer", "abgeltungssteuer", "krypto", "pipeline-serie", "broker", "toolbox",
      "meine-toolbox", "mein-weg", "kredit", "parqet", "newtek", "hercules", "wochenrueckblick",
      "marktbericht", "weekly", "finanzfeuer-talk"],
     "https://mbcapitalstrategies.com/assets/og-dividenden.jpg"),
]

DEFAULT_OG = "https://mbcapitalstrategies.com/assets/og-default.jpg"
PATTERN = re.compile(r'(<meta\s+property="og:image"\s+content=")[^"]*(")', re.IGNORECASE)
TWITTER_PATTERN = re.compile(r'(<meta\s+name="twitter:image"\s+content=")[^"]*(")', re.IGNORECASE)

def get_og_image(filename):
    fn = filename.lower()
    for keywords, img in MAPPING:
        if any(kw in fn for kw in keywords):
            return img
    return DEFAULT_OG

def process_file(filepath):
    filename = os.path.basename(filepath)
    new_img = get_og_image(filename)

    # Skip if already using a correct og-image (not marco.jpg)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Only process files that still use marco.jpg as og:image
    if 'marco.jpg' not in content:
        return False

    # Replace og:image
    new_content = PATTERN.sub(r'\g<1>' + new_img + r'\g<2>', content)
    # Replace twitter:image if it also uses marco.jpg
    new_content = TWITTER_PATTERN.sub(r'\g<1>' + new_img + r'\g<2>', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    dirs_to_scan = [
        os.path.join(BASE, "blog"),
        os.path.join(BASE, "tools"),
        os.path.join(BASE, "bestenlisten"),
        os.path.join(BASE, "podcast"),
        os.path.join(BASE, "rohstoffe"),
        os.path.join(BASE, "shipping"),
        os.path.join(BASE, "midstream"),
        os.path.join(BASE, "dividendenstrategie"),
        os.path.join(BASE, "depot-strategie"),
        BASE,  # root files
    ]

    changed = []
    for d in dirs_to_scan:
        if not os.path.exists(d):
            continue
        for fname in os.listdir(d):
            if fname.endswith('.html'):
                fpath = os.path.join(d, fname)
                if process_file(fpath):
                    changed.append(fpath.replace(BASE, ''))

    print(f"Fixed {len(changed)} files:")
    for f in sorted(changed):
        print(f"  {f}")

if __name__ == "__main__":
    main()
