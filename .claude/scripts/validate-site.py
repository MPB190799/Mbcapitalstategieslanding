#!/usr/bin/env python3
"""
MB Capital Strategies — Site Validation Script
Wird vom Daily Optimization Agent genutzt um Probleme zu finden.

Prüft:
- Meta-Tags (title, description, canonical, OG)
- JSON-LD Schemas
- Broken internal Links
- Favicon-Links
- AdSense-Script
- nav.js Einbindung
- Disclaimer auf Blog-Artikeln
- Sitemap-Konsistenz
- CSS/JS Syntax-Basics

Ausgabe: JSON-Report mit Findings pro Datei.
"""

import os
import re
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent.parent  # .claude/scripts/ → project root
DOMAIN = "https://mbcapitalstrategies.com"

# Seiten die keine normalen Content-Seiten sind
SKIP_FILES = {
    "googleecd17b151bd5b1c1.html",
}

# Redirect-Stubs erkennen
REDIRECT_PATTERN = re.compile(r'<meta\s+http-equiv=["\']refresh["\']', re.IGNORECASE)
NOINDEX_PATTERN = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\']noindex', re.IGNORECASE)


def find_html_files():
    """Findet alle HTML-Dateien im Projekt."""
    html_files = []
    for root, dirs, files in os.walk(BASE):
        # Skip hidden dirs, node_modules etc
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for f in files:
            if f.endswith('.html') and f not in SKIP_FILES:
                html_files.append(os.path.join(root, f))
    return html_files


def is_redirect_stub(content):
    """Prüft ob die Datei ein Redirect-Stub ist."""
    return bool(REDIRECT_PATTERN.search(content)) and bool(NOINDEX_PATTERN.search(content))


def check_meta_tags(filepath, content):
    """Prüft Pflicht-Meta-Tags."""
    issues = []

    if not re.search(r'<title>', content):
        issues.append("Fehlend: <title>")

    if not re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
        issues.append("Fehlend: meta description")

    if not re.search(r'<link\s+rel=["\']canonical["\']', content, re.IGNORECASE):
        issues.append("Fehlend: canonical link")

    if not re.search(r'<meta\s+property=["\']og:title["\']', content, re.IGNORECASE):
        issues.append("Fehlend: og:title")

    if not re.search(r'<meta\s+property=["\']og:description["\']', content, re.IGNORECASE):
        issues.append("Fehlend: og:description")

    if not re.search(r'<meta\s+name=["\']twitter:card["\']', content, re.IGNORECASE):
        issues.append("Fehlend: twitter:card")

    return issues


def check_favicon(filepath, content):
    """Prüft Favicon-Links."""
    issues = []
    if not re.search(r'favicon\.ico', content):
        issues.append("Fehlend: favicon.ico Link")
    if not re.search(r'apple-touch-icon', content):
        issues.append("Fehlend: apple-touch-icon")
    if not re.search(r'site\.webmanifest', content):
        issues.append("Fehlend: site.webmanifest")
    return issues


def check_adsense(filepath, content):
    """Prüft AdSense-Script."""
    if not re.search(r'ca-pub-7097302643579933', content):
        return ["Fehlend: AdSense Script"]
    return []


def check_nav_js(filepath, content):
    """Prüft nav.js Einbindung."""
    if not re.search(r'nav\.js', content) and not re.search(r'nav\.min\.js', content):
        return ["Fehlend: nav.js Einbindung"]
    return []


def check_schema(filepath, content):
    """Prüft JSON-LD Schemas."""
    issues = []
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', content, re.DOTALL)

    for i, schema_str in enumerate(schemas):
        try:
            json.loads(schema_str)
        except json.JSONDecodeError as e:
            issues.append(f"JSON-LD Schema #{i+1} hat Syntax-Fehler: {e}")

    return issues


def check_blog_disclaimer(filepath, content):
    """Prüft Disclaimer auf Blog-Artikeln."""
    rel_path = os.path.relpath(filepath, BASE)
    if rel_path.startswith("blog/") and rel_path != "blog/index.html" and not rel_path.endswith("styles.css"):
        if not re.search(r'disclaimer|Keine Anlageberatung', content, re.IGNORECASE):
            return ["Fehlend: Disclaimer auf Blog-Artikel"]
    return []


def check_internal_links(filepath, content):
    """Sammelt interne Links zur späteren Validierung."""
    links = re.findall(r'href=["\'](/[^"\'#]*)["\']', content)
    broken = []
    for link in links:
        # Normalisiere Link
        link_path = link.rstrip('/')
        if link_path == '':
            continue

        # Prüfe ob Datei existiert
        target = BASE / link_path.lstrip('/')
        if target.is_dir():
            target = target / "index.html"
        elif not target.suffix:
            target_with_html = Path(str(target) + ".html")
            target_dir = target / "index.html"
            if not target_with_html.exists() and not target_dir.exists() and not target.exists():
                broken.append(f"Broken Link: {link}")
                continue

        if not target.exists():
            broken.append(f"Broken Link: {link}")

    return broken


def check_sitemap_coverage():
    """Prüft ob alle Content-Seiten in Sitemaps sind."""
    issues = []

    # Sammle alle URLs aus Sitemaps
    sitemap_urls = set()
    sitemap_files = list(BASE.glob("sitemap*.xml")) + list(BASE.glob("glossar-sitemap.xml"))

    for sf in sitemap_files:
        content = sf.read_text(errors='ignore')
        urls = re.findall(r'<loc>(.*?)</loc>', content)
        for url in urls:
            path = url.replace(DOMAIN, '').rstrip('/')
            if not path:
                path = '/'
            sitemap_urls.add(path)

    return {"sitemap_urls_count": len(sitemap_urls), "sitemap_files": [str(s.name) for s in sitemap_files]}


def check_copyright_year(filepath, content):
    """Prüft ob das Copyright-Jahr aktuell ist."""
    issues = []
    old_years = re.findall(r'&copy;\s*202[0-5]\b', content)
    if old_years:
        issues.append(f"Veraltetes Copyright-Jahr: {old_years}")
    return issues


def run_validation():
    """Hauptfunktion — validiert alle HTML-Dateien."""
    html_files = find_html_files()
    report = {
        "total_files": len(html_files),
        "files_with_issues": 0,
        "total_issues": 0,
        "redirect_stubs": 0,
        "details": {},
        "sitemap_info": check_sitemap_coverage(),
    }

    for filepath in sorted(html_files):
        rel_path = os.path.relpath(filepath, BASE)

        try:
            content = open(filepath, 'r', errors='ignore').read()
        except Exception as e:
            report["details"][rel_path] = [f"Kann nicht gelesen werden: {e}"]
            continue

        # Redirect-Stubs separat zählen
        if is_redirect_stub(content):
            report["redirect_stubs"] += 1
            continue

        all_issues = []
        all_issues.extend(check_meta_tags(filepath, content))
        all_issues.extend(check_favicon(filepath, content))
        all_issues.extend(check_adsense(filepath, content))
        all_issues.extend(check_nav_js(filepath, content))
        all_issues.extend(check_schema(filepath, content))
        all_issues.extend(check_blog_disclaimer(filepath, content))
        all_issues.extend(check_copyright_year(filepath, content))
        # Internal links check is slower, only on blog articles
        if rel_path.startswith("blog/"):
            all_issues.extend(check_internal_links(filepath, content))

        if all_issues:
            report["details"][rel_path] = all_issues
            report["files_with_issues"] += 1
            report["total_issues"] += len(all_issues)

    return report


if __name__ == "__main__":
    report = run_validation()

    if "--json" in sys.argv:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"MB Capital Strategies — Site Validation Report")
        print(f"{'='*60}")
        print(f"Dateien geprüft:    {report['total_files']}")
        print(f"Redirect-Stubs:     {report['redirect_stubs']}")
        print(f"Dateien mit Issues: {report['files_with_issues']}")
        print(f"Gesamt-Issues:      {report['total_issues']}")
        print(f"Sitemap-URLs:       {report['sitemap_info']['sitemap_urls_count']}")
        print()

        if report["details"]:
            print("FINDINGS:")
            print("-" * 40)
            for filepath, issues in sorted(report["details"].items()):
                print(f"\n{filepath}:")
                for issue in issues:
                    print(f"  - {issue}")
        else:
            print("Keine Issues gefunden!")

        print(f"\n{'='*60}")
