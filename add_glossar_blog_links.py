#!/usr/bin/env python3
"""
Adds relevant blog article links to glossar pages in their <section class="related"> section.
Skips files that already have 2+ blog links in their related section.
"""

import os
import re

GLOSSAR_DIR = "/home/user/Mbcapitalstategieslanding/glossar"
BASE_URL = "https://mbcapitalstrategies.com"

# Mapping: glossar slug → list of (url, anchor_text)
BLOG_LINKS = {
    "bdc": [
        ("/blog/bdc-dividendenaktien-2025-newtek-vs-hercules.html", "Analyse: Newtek vs. Hercules Capital – BDC Duell 2025"),
        ("/blog/bdc-duell-2025-crescent-vs-blue-owl.html", "Analyse: Crescent Capital vs. Blue Owl – BDC Duell 2025"),
        ("/blog/debitum-investments-realitaetscheck-2026.html", "Debitum Investments Realitätscheck 2026"),
    ],
    "mlp": [
        ("/blog/pipeline-serie-teil1-pembina-pipeline-analyse-2025.html", "Pipeline-Serie Teil 1: Pembina Pipeline Analyse"),
        ("/blog/pipeline-serie-teil2-tc-energy-analyse-2025.html", "Pipeline-Serie Teil 2: TC Energy Analyse"),
        ("/blog/pipeline-serie-teil3-enbridge-analyse-2025.html", "Pipeline-Serie Teil 3: Enbridge Analyse"),
        ("/blog/oneok.html", "ONEOK Analyse – Midstream Champion"),
    ],
    "midstream": [
        ("/blog/pipeline-serie-teil1-pembina-pipeline-analyse-2025.html", "Pipeline-Serie Teil 1: Pembina Pipeline Analyse"),
        ("/blog/pipeline-serie-teil2-tc-energy-analyse-2025.html", "Pipeline-Serie Teil 2: TC Energy Analyse"),
        ("/blog/pipeline-serie-teil3-enbridge-analyse-2025.html", "Pipeline-Serie Teil 3: Enbridge Analyse"),
        ("/blog/pipeline-serie-finale-vergleich-2025.html", "Pipeline-Serie Finale: Der große Vergleich"),
    ],
    "shipping-cluster": [
        ("/blog/shipping-3-aktien-10prozent-2025.html", "3 Shipping-Aktien mit 10 % Dividende 2025"),
        ("/blog/shipping-6-aktien-depot-2025.html", "6 Shipping-Aktien für das Depot 2025"),
        ("/blog/green-shipping-2026-groesste-transformation-der-schifffahrt-seit-50-jahren.html", "Green Shipping 2026 – Die Transformation"),
        ("/bestenlisten/beste-tanker-aktien-2026.html", "Bestenliste: Beste Tanker-Aktien 2026"),
    ],
    "time-charter": [
        ("/blog/shipping-3-aktien-lng-tanker-2025.html", "3 LNG-Tanker Aktien 2025 mit planbarem Cashflow"),
        ("/bestenlisten/beste-lng-aktien-2026.html", "Bestenliste: Beste LNG-Aktien 2026"),
        ("/blog/shipping-cashflow-rechner.html", "Shipping-Cashflow-Rechner erklärt"),
    ],
    "tce-rate": [
        ("/blog/shipping-cashflow-rechner.html", "Shipping-Cashflow-Rechner: TCE berechnen"),
        ("/blog/shipping-tanker-mixedfleet-2025.html", "Tanker Mixed-Fleet Analyse 2025"),
        ("/bestenlisten/beste-tanker-aktien-2026.html", "Bestenliste: Beste Tanker-Aktien 2026"),
    ],
    "dayrate": [
        ("/blog/shipping-3-aktien-10prozent-2025.html", "3 Shipping-Aktien mit 10 % Dividende 2025"),
        ("/blog/hidden-champions-shipping-2025.html", "Hidden Champions im Shipping 2025"),
        ("/bestenlisten/beste-tanker-aktien-2026.html", "Bestenliste: Beste Tanker-Aktien 2026"),
    ],
    "baltic-dry-index": [
        ("/blog/markt-news-container-kupfer-februar-2026.html", "Markt-News: Container & Kupfer Februar 2026"),
        ("/blog/shipping-6-aktien-depot-2025.html", "6 Shipping-Aktien für das Depot 2025"),
        ("/blog/green-shipping-2026-groesste-transformation-der-schifffahrt-seit-50-jahren.html", "Green Shipping 2026"),
    ],
    "superzyklus": [
        ("/blog/rohstoff-superzyklus-2025.html", "Rohstoff-Superzyklus 2025 – Analyse"),
        ("/blog/mining-aktien-ueberblick-2026.html", "Mining Aktien Überblick 2026"),
        ("/rohstoff-superzyklus-master.html", "Rohstoff-Superzyklus Master-Guide"),
        ("/blog/dividendenaktien-10prozent-2025.html", "Dividendenaktien mit 10 % – Rohstoff-Picks 2025"),
    ],
    "aisc-mining": [
        ("/blog/barrick-gold-analyse-2026.html", "Barrick Gold Analyse 2026 – AISC & Cashflow"),
        ("/blog/bhp-analyse-2025.html", "BHP Analyse 2025 – Rohstoffgigant"),
        ("/blog/glencore-analyse-2025.html", "Glencore Analyse 2025 – Diversifizierter Riese"),
        ("/blog/mining-aktien-ueberblick-2026.html", "Mining Aktien Überblick 2026"),
    ],
    "hard-assets": [
        ("/rohstoff-superzyklus-master.html", "Rohstoff-Superzyklus Master-Guide"),
        ("/blog/dividendenaktien-10prozent-2025.html", "Hard Asset Dividendenaktien mit 10 %"),
        ("/blog/shipping-6-aktien-depot-2025.html", "6 Shipping Hard Assets für das Depot"),
        ("/bestenlisten/top-5-high-yield-aktien-2026.html", "Top 5 High-Yield Hard Assets 2026"),
    ],
    "upstream": [
        ("/blog/eni-analyse-2026.html", "ENI Analyse 2026 – LNG & Upstream"),
        ("/blog/equinor-analyse-2026.html", "Equinor Analyse 2026 – Norwegens Energieriese"),
        ("/blog/petrobras-analyse-2026.html", "Petrobras Analyse 2026 – 18 % FCF-Yield"),
        ("/blog/woodside-energy-analyse-2026.html", "Woodside Energy Analyse 2026 – LNG & Dividende"),
    ],
    "yield-on-cost": [
        ("/tools/yield-on-cost-rechner.html", "Yield-on-Cost-Rechner (kostenlos)"),
        ("/tools/dividend-snowball-yoc-pro.html", "Dividend Snowball & YoC PRO Rechner"),
        ("/blog/dividendenaktien-5-stabil-2025.html", "5 stabile Dividendenaktien mit YoC-Potenzial 2025"),
    ],
    "free-cashflow": [
        ("/blog/petrobras-analyse-2026.html", "Petrobras Analyse – 18 % FCF-Yield"),
        ("/blog/cardinal-energy-analyse-2026.html", "Cardinal Energy Analyse 2026 – FCF & Dividende"),
        ("/tools/dividendenrechner.html", "Kostenloser Dividenden- & Cashflow-Rechner"),
    ],
    "dividend-yield": [
        ("/tools/dividendenrechner.html", "Dividendenrechner – Rendite berechnen"),
        ("/blog/dividendenaktien-10prozent-2025.html", "Dividendenaktien mit 10 % Rendite 2025"),
        ("/bestenlisten/top-5-high-yield-aktien-2026.html", "Top 5 High-Yield Aktien 2026"),
    ],
    "payout-ratio": [
        ("/blog/dividendenaktien-5-stabil-2025.html", "5 stabile Dividendenaktien mit gesunder Ausschüttungsquote"),
        ("/tools/dividendenrechner.html", "Dividendenrechner mit Payout-Ratio-Analyse"),
        ("/bestenlisten/top-5-high-yield-aktien-2026.html", "Top 5 High-Yield Aktien 2026"),
    ],
    "cashflow-cover": [
        ("/blog/shipping-cashflow-rechner.html", "Shipping-Cashflow-Rechner – Coverage simulieren"),
        ("/blog/bdc-dividendenaktien-2025-newtek-vs-hercules.html", "BDC Dividend Coverage Analyse 2025"),
        ("/tools/dividenden-snowball-rechner.html", "Dividend Snowball Rechner"),
    ],
    "special-dividend": [
        ("/blog/thungela-resources-analyse-2025.html", "Thungela Resources – Sonderdividenden Analyse"),
        ("/blog/shipping-3-aktien-10prozent-2025.html", "Shipping-Aktien mit Sonderdividenden 2025"),
        ("/blog/vale-analyse-2025.html", "Vale Analyse – Sonderdividenden & Cashflow"),
    ],
    "dividend-cut": [
        ("/blog/dividendenaktien-5-stabil-2025.html", "5 stabile Dividendenaktien ohne Cut-Risiko"),
        ("/blog/pipeline-serie-finale-vergleich-2025.html", "Pipeline-Vergleich: Cut-Resistenz analysiert"),
    ],
    "ebitda": [
        ("/blog/bhp-analyse-2025.html", "BHP Analyse – EBITDA & Rohstoff-Cashflow"),
        ("/blog/mining-aktien-ueberblick-2026.html", "Mining Aktien Überblick 2026 – EBITDA-Vergleich"),
    ],
    "debt-ebitda": [
        ("/blog/pipeline-serie-finale-vergleich-2025.html", "Pipeline-Vergleich – Verschuldung & EBITDA"),
        ("/blog/bhp-analyse-2025.html", "BHP Analyse – Bilanz & Verschuldungsgrad"),
    ],
    "capex": [
        ("/blog/mining-aktien-ueberblick-2026.html", "Mining Aktien Überblick – Capex & Investitionen 2026"),
        ("/blog/rohstoff-superzyklus-2025.html", "Rohstoff-Superzyklus – Capex-Lücke erklärt"),
        ("/blog/woodside-energy-analyse-2026.html", "Woodside Energy – Capex & Wachstumsprojekte"),
    ],
}


def process_glossar_file(slug, links):
    filepath = os.path.join(GLOSSAR_DIR, f"{slug}.html")
    if not os.path.exists(filepath):
        return False, f"file not found: {slug}.html"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already has blog links in related section
    blog_count = len(re.findall(r'href="/blog/', content))
    if blog_count >= 2:
        return False, f"already has {blog_count} blog links"

    # Find the related section
    if '<section class="related">' not in content:
        return False, "no related section found"

    # Build new list items
    new_items = "\n".join(
        f'      <li><a href="{url}">{text}</a></li>'
        for url, text in links
    )

    # Find the closing ul in the related section and insert before it
    # We'll look for the pattern inside the related section
    # Find start of related section
    rel_start = content.find('<section class="related">')
    rel_end = content.find('</section>', rel_start)

    if rel_start == -1 or rel_end == -1:
        return False, "related section malformed"

    related_block = content[rel_start:rel_end]

    # Find the last </ul> in the related block
    ul_close_pos = related_block.rfind('</ul>')
    if ul_close_pos == -1:
        return False, "no </ul> in related section"

    # Insert new items before </ul>
    new_related = (
        related_block[:ul_close_pos]
        + new_items + "\n    </ul>"
        + related_block[ul_close_pos + len('</ul>'):]
    )

    new_content = content[:rel_start] + new_related + content[rel_end:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"added {len(links)} blog links"


def main():
    updated = 0
    skipped = 0
    for slug, links in BLOG_LINKS.items():
        try:
            ok, msg = process_glossar_file(slug, links)
            if ok:
                print(f"  OK  {slug}: {msg}")
                updated += 1
            else:
                print(f" SKIP {slug}: {msg}")
                skipped += 1
        except Exception as e:
            print(f"  ERR {slug}: {e}")

    print(f"\nDone: {updated} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
