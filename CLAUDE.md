# CLAUDE.md — MB Capital Strategies

## Project Overview

**MB Capital Strategies** (`mbcapitalstrategies.com`) is a German-language static website focused on dividend investing in hard assets (energy, shipping, mining, pipelines). It is authored by Marco Bozem and hosted on **GitHub Pages** with a custom domain via `CNAME`.

This is **not** a JavaScript/Node.js application — it is a **static HTML site** with ~122 hand-authored HTML pages, inline CSS/JS, and a handful of utility scripts for batch operations.

## Tech Stack

| Layer | Technology |
|---|---|
| Hosting | GitHub Pages (custom domain: `mbcapitalstrategies.com`) |
| Language | Static HTML, inline CSS, vanilla JavaScript |
| Font | Montserrat (Google Fonts, weights 400–800) |
| Monetization | Google AdSense (`ca-pub-7097302643579933`) |
| Analytics | Google Consent Mode v2 (DSGVO/GDPR compliant) |
| Structured Data | JSON-LD (Schema.org: FAQPage, BreadcrumbList, BlogPosting, WebApplication, Organization, WebSite) |
| Build Scripts | Python 3 (batch HTML transformations), Node.js/ESM (sitemap generation) |

**There is no build step, bundler, or framework.** Pages are served as-is from the repository root.

## Repository Structure

```
/                           # Root = GitHub Pages document root
├── index.html              # Homepage (~1570 lines, self-contained with inline <style>)
├── CNAME                   # Custom domain: mbcapitalstrategies.com
├── robots.txt              # Crawl directives + sitemap references
├── ads.txt                 # AdSense publisher verification (pub-7097302643579933)
├── site.webmanifest        # PWA manifest (icons, theme #0f1115)
│
├── blog/                   # 69 article pages + index (stock analyses, market news, guides)
│   ├── index.html          # Blog listing page with 8-category filter (Mining, Shipping, Midstream, BDC, Dividenden, Upstream, Rechner)
│   └── styles.css          # Shared stylesheet for blog + most content pages (1206 lines, 20 CSS custom properties)
│
├── tools/                  # Interactive financial calculators (8 tools)
│   ├── dividendenrechner.html
│   ├── yield-on-cost-rechner.html
│   ├── dividenden-snowball-rechner.html
│   ├── dividend-snowball-yoc-pro.html
│   ├── dividenden-reinvest-rechner.html
│   ├── dividenden-wachstumsrechner.html
│   ├── finanzielle-freiheit-rechner.html
│   └── shipping-cashflow-rechner.html
│
├── rechner/                # Calculator index page
│   └── index.html
│
├── podcast/                # Podcast pages (7 episodes + index)
│   ├── index.html
│   ├── styles.css          # Podcast-specific styles (121 lines, shares design tokens)
│   ├── der-finanzfeuer-talk.html
│   ├── mein-weg-zur-dividendenstrategie-2025.html
│   ├── timing-ist-alles-dividendenstrategie-podcast-2025.html
│   ├── maritime-investments-schifffahrtsaktien-2025.html
│   ├── bdc-aktien-erklaert-2025.html
│   ├── mining-serie-high-dividend-ressourcen-2025-2028.html
│   └── pipeline-aktien-analyse-2025.html
│
├── glossar/                # Financial glossary system (211 terms → 137 unique anchors)
│   ├── index.html          # Glossary page with search/filter + dynamic SEO via ?begriff= param
│   ├── terms.json          # Term→slug mapping (used for auto-linking)
│   ├── glossar.js          # Glossary page logic (search, filter, Schema.org, URL params)
│   ├── autolink-glossar.js # Client-side glossary term auto-linker
│   ├── shipping-cluster.html  # Shipping terminology hub
│   ├── aisc-mining.html    # Mining cost definitions (AISC)
│   └── tce-rate.html       # Shipping TCE rate glossary
│
├── assets/
│   └── js/
│       ├── nav.js          # Shared nav injection + cookie consent + scroll effects + article schema (v3, 484 lines)
│       └── glossar-linking.js  # Auto-links glossary terms in article content
│
├── shipping/               # Shipping sector hub (index.html)
├── shipping-aktien/        # Shipping stocks index (index.html)
├── midstream/              # Pipeline/midstream sector hub (index.html)
├── mining-aktien/          # Mining stocks index (index.html, lists 22 analyses)
├── upstream-aktien/        # Upstream oil & gas stocks index (index.html, lists 12 analyses)
├── rohstoffe/              # Commodity deep-dives
│   ├── kupfer-superzyklus.html
│   ├── nickel-superzyklus.html
│   ├── uran-superzyklus.html
│   └── zink-superzyklus.html
├── kategorien/             # Category pages
│   ├── high-yield-aktien.html
│   ├── mining-aktien.html
│   └── rohstoff-superzyklus-2025-2030.html
├── bestenlisten/           # "Best of" annual lists — 2026 pages + 2025 redirect stubs
│   ├── beste-lng-aktien-2026.html
│   ├── beste-tanker-aktien-2026.html
│   ├── top-5-high-yield-aktien-2026.html
│   ├── beste-lng-aktien-2025.html          # redirect stub → 2026
│   ├── beste-tanker-aktien-2025.html       # redirect stub → 2026
│   └── top-5-high-yield-aktien-2025.html   # redirect stub → 2026
├── dividendenstrategie/    # Dividend strategy guide
│   ├── index.html          # Main dividend strategy page
│   ├── abgeltungssteuer.html  # Capital gains tax guide (Abgeltungssteuer)
│   └── bdc-aktien/         # BDC stocks sub-section
│       └── index.html
├── depot-strategie/        # Portfolio strategy with embedded Parqet widgets (index.html)
├── hard-asset-guide/       # Hard asset investing guide (index.html)
├── ueber-marco-bozem/      # About the author (index.html)
│
├── sitemap.xml             # Master sitemap index (9 sub-sitemaps)
├── sitemap-main.xml        # Core pages sitemap (27 URLs)
├── sitemap-blog.xml        # Blog articles sitemap (84 URLs)
├── sitemap-tools.xml       # Calculator tools sitemap (9 URLs)
├── sitemap-video.xml       # Video sitemap (23 YouTube embeds)
├── sitemap-kategorien.xml  # Category pages (5 URLs)
├── sitemap-bestenlisten.xml # Best-of lists (3 URLs)
├── sitemap-investing.xml   # Investing.com hub (1 URL)
├── sitemap-travel.xml      # Travel content (1 URL)
├── glossar-sitemap.xml     # Auto-generated glossary sitemap (137 URLs)
│
├── datenschutz.html        # Privacy policy (DSGVO)
├── impressum.html          # Legal notice (German law requirement)
├── toolbox.html            # Recommended brokers & tools (with affiliate links)
├── blogindex.html          # Alternative blog listing
├── investing-analysen.html # Investing.com analyses hub
├── rohstoff-superzyklus-master.html  # Commodity supercycle master page
├── googleecd17b151bd5b1c1.html      # Google Search Console verification
│
├── add_nav.py              # Adds canonical nav to pages missing it (10 target pages)
├── fix_nav.py              # Standardizes nav dropdowns across ALL HTML pages
├── add_faq_schema.py       # Injects FAQPage JSON-LD into 10 mining/upstream articles
├── rename_mining_2026.py   # Renames articles from -2025 to -2026 with redirect stubs
├── build-glossar-sitemap.mjs  # Node.js ESM script to generate glossar-sitemap.xml
│
├── Logo.png                # Brand logo (used in nav, schema, everywhere)
├── marco.jpg               # Author photo (used in author bio injection)
├── background.jpg          # Homepage background image
├── BannermitMarco.jpg      # Author banner image
├── favicon.ico             # Standard favicon
├── favicon-16x16.png       # 16px favicon
├── favicon-32x32.png       # 32px favicon
├── apple-touch-icon.png    # Apple touch icon (180px)
├── android-chrome-*.png    # Android PWA icons (192px, 512px)
└── *.jpg, *.jpeg           # Infographic charts (commodity demand, supply gaps, etc.)
```

## Blog Content Inventory

The 69 blog articles break down by sector:

| Category | Count | Examples |
|---|---|---|
| Mining | 22 analyses + 9 redirect stubs | BHP, Rio Tinto, Vale, Barrick Gold, Glencore, Kazatomprom |
| Upstream Oil & Gas | 12 analyses | Equinor, Petrobras, Devon Energy, ENI, OMV, Repsol |
| Shipping & Tanker | 8 articles | Green Shipping 2026, Hidden Champions, LNG/Tanker picks |
| Midstream / Pipeline | 5 articles | Pembina, TC Energy, Enbridge, ONEOK, Pipeline Finale |
| BDC & High-Yield | 5 articles | Newtek vs Hercules, Crescent vs Blue Owl, 10% Yield picks |
| Market News & Macro | 4 articles | Rohstoff-Superzyklus, Container & Kupfer News, Debitum check |
| Tools & Resources | 2 articles | Toolbox/Broker review, Shipping Cashflow Rechner |
| Tax Guide | 1 article | Quellensteuer Kanada & Australien |

**Redirect stubs** (9 files): Mining articles renamed from `-2025.html` to `-2026.html`. Old URLs use `<meta http-equiv="refresh">` + `<meta name="robots" content="noindex, follow">` + canonical pointing to new URL.

**Blog index filters** (`blog/index.html`): 8 category buttons filter articles via `data-category` attributes on `.post` cards using vanilla JS.

## Design System

### CSS Custom Properties (`/blog/styles.css`)

```css
/* Color Palette */
--gold: #d4af37;                              /* Primary accent / brand gold */
--gold-strong: #e0bd55;                       /* Bright gold for gradients */
--gold-dim: rgba(212,175,55,0.12);            /* Subtle gold backgrounds */
--gold-border: rgba(212,175,55,0.22);         /* Border color */
--bg: #0f1115;                                /* Dark background */
--bg-soft: #151821;                           /* Slightly lighter background */
--bg-card: #1a1f2b;                           /* Card background */
--glass: rgba(21,24,33,0.75);                 /* Glassmorphism background */
--text: #f5f6fa;                              /* Primary text (near-white) */
--text-soft: #cfd6e6;                         /* Secondary text */
--text-muted: #9aa6c0;                        /* Muted text */

/* Layout */
--radius: 16px;                               /* Standard border radius */
--radius-sm: 10px;                            /* Small element radius */
--transition: 0.28s cubic-bezier(0.4,0,0.2,1);  /* Easing function */

/* Shadows */
--shadow-card: 0 4px 20px rgba(0,0,0,0.3);
--shadow-hover: 0 12px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(212,175,55,0.18);
--shadow-gold: 0 0 30px rgba(212,175,55,0.15);  /* Gold glow effect */
```

### Visual Style

- **Dark theme** with gold (#d4af37) accents throughout
- **Glassmorphism** cards with `backdrop-filter: blur()` and semi-transparent backgrounds
- **Montserrat** font family (400–800 weights via Google Fonts)
- Gradient gold headings using `-webkit-background-clip: text`
- Hover effects: `translateY(-6px)` lift with gold border glow
- Reading progress bar on article pages (gold gradient, fixed top)
- Scroll reveal animations via IntersectionObserver (`.reveal` → `.visible`, threshold 8%)

### Key CSS Classes

| Class | Purpose |
|---|---|
| `.nav`, `.nav-inner`, `.nav-links` | Main sticky navigation bar |
| `.nav-hamburger`, `.nav-mobile` | Mobile navigation (breakpoint: 700px) |
| `.dropdown`, `.dropdown-btn`, `.dropdown-content` | Dropdown menus in nav |
| `.container`, `.page-wrapper` | Content wrapper (max-width: 960px) |
| `.page-header` | Centered page title section with gold gradient |
| `.article-hero`, `.article-hero .inner` | Full-width article header with gradient background |
| `.article-body` | Article content wrapper (max-width: 860px) |
| `.article-meta` | Article metadata line (date, author, category) |
| `.post`, `.card` | Glassmorphism content cards |
| `.posts`, `.grid` | Card grid layouts |
| `.btn`, `.btn-secondary` | Gold pill buttons |
| `.info-box` | Blue-gold info callout (border-left: 4px solid #d4af37) |
| `.risk-box` | Red risk callout (border-left: 4px solid #ff6b6b) |
| `.success-box` | Green success callout |
| `.key-takeaway` | Highlighted takeaway with star icon |
| `.metrics-grid`, `.metric-card` | Financial metrics display grid |
| `.metric-value`, `.metric-label` | Metric card content elements |
| `.table-wrapper`, `.data-table` | Styled data tables |
| `.cta-box` | Call-to-action box with gold top border |
| `.related-articles` | Related content links section |
| `.breadcrumbs` | Navigation breadcrumbs (max-width: 900px) |
| `.author-box`, `.author-info` | Author bio card |
| `.disclaimer` | Legal disclaimer box |
| `.reveal` | Scroll-triggered fade-in animation |
| `.section-label` | Uppercase gold pill label |
| `.section-label-grid` | Section labels in blog index grid |
| `.filter-bar`, `.filter-btn` | Blog category filter UI |
| `.video-wrapper` | Responsive 16:9 YouTube embed container |
| `.site-footer`, `.footer-inner`, `.footer-bottom` | Page footer |
| `.reading-progress` | Reading progress bar (injected by nav.js) |

## Stylesheets

There are **two main CSS sources** — pages use one or the other:

1. **`/blog/styles.css`** — The shared design system stylesheet (1206 lines, 20 CSS custom properties). Used by blog articles, tools, rechner, podcast pages, and most content pages. Referenced as `<link rel="stylesheet" href="/blog/styles.css?v=2">`.

2. **Inline `<style>` blocks** — The homepage (`index.html`) and some older pages embed their own styles directly. These share the same design tokens but may have page-specific additions.

Some pages include **both** the shared stylesheet and additional inline `<style>` overrides (e.g., `.info-box`, `.risk-box`, `.breadcrumbs` styling).

**`/podcast/styles.css`** (121 lines) — Podcast-specific styles extending the shared design system.

## Navigation

### Shared Navigation (`/assets/js/nav.js` — v3)

All pages should include:
```html
<script src="/assets/js/nav.js" defer></script>
```

This script (484 lines) is the **single source of truth** for navigation across all 100+ pages. It provides:

- **Nav HTML injection** — replaces `<nav class="nav">` or `<header class="nav">` elements with the canonical navigation HTML at runtime. A nav change in `nav.js` propagates to every page automatically.
- **Hamburger menu** toggle for mobile (< 700px)
- **Dropdown menus** (hover on desktop, click on mobile)
- **Scroll reveal** animation (IntersectionObserver on `.reveal` elements, threshold 0.08, rootMargin `0px 0px -40px 0px`)
- **Reading progress bar** (on pages with `.article-body`, `article`, or `.article-hero`)
- **Active nav link** highlighting based on current URL path
- **Author bio injection** on `/blog/*` article pages (auto-inserts Marco Bozem bio with links to YouTube and LinkedIn)
- **Article schema injection** — auto-generates `BlogPosting` JSON-LD for blog articles that lack one (fixes E-E-A-T for legacy articles)
- **Cookie consent banner** (DSGVO-compliant, Google Consent Mode v2, stored in `localStorage` as `mbcs_consent_v1`)

### nav.js Boot Order

```
DOMContentLoaded →
  1. injectNav()           — creates nav DOM (must run first)
  2. setupHamburger()      — mobile menu toggle
  3. setupDropdowns()      — dropdown hover/click
  4. setupScrollReveal()   — IntersectionObserver on .reveal
  5. setupReadingProgress() — progress bar for articles
  6. setupActiveNav()      — highlight current page link
  7. setupAuthorBio()      — inject author card on blog articles
  8. injectArticleSchema() — inject BlogPosting JSON-LD if missing
  9. setupCookieBanner()   — only if no prior consent stored
```

### nav.js Page Detection Logic

Blog article detection (for author bio + schema injection):
```javascript
path.startsWith('/blog/') &&
path !== '/blog/' &&
!path.endsWith('index.html') &&
!path.endsWith('alle-finanzrechner.html') &&
!path.endsWith('meine-toolbox-broker-tools-plattformen-2025.html') &&
!path.endsWith('wise-airalo-vietnam-erfahrungen.html')
```

### Canonical Navigation HTML

The canonical nav is defined in **three places** (keep them in sync):
1. **`/assets/js/nav.js`** `injectNav()` function — the runtime source of truth
2. **`add_nav.py`** `CANONICAL_NAV_HTML` constant — for batch-adding nav to new pages
3. **`fix_nav.py`** `CANONICAL_NAV` constant — for batch-fixing nav across all pages

### Desktop Nav Links

- **Startseite** → `/`
- **Depot** → `/depot-strategie/`
- **Hard Asset Guide** → `/hard-asset-guide/`
- **Themen** dropdown:
  - Shipping Aktien → `/shipping-aktien/`
  - Pipelines / Midstream → `/midstream/`
  - Mining Aktien → `/mining-aktien/`
  - Upstream Aktien → `/upstream-aktien/`
  - Dividendenstrategie → `/dividendenstrategie/`
  - (separator)
  - High-Yield & BDC → `/kategorien/high-yield-aktien.html`
  - Rohstoff Superzyklus → `/rohstoff-superzyklus-master.html`
  - (separator)
  - Beste LNG-Aktien 2026 → `/bestenlisten/beste-lng-aktien-2026.html`
  - Beste Tanker-Aktien 2026 → `/bestenlisten/beste-tanker-aktien-2026.html`
  - Top 5 High-Yield 2026 → `/bestenlisten/top-5-high-yield-aktien-2026.html`
- **Podcast** dropdown:
  - Alle Podcasts → `/podcast/`
  - (separator)
  - Finanzfeuer Talk → `/podcast/der-finanzfeuer-talk.html`
  - Dividenden-Journey → `/podcast/mein-weg-zur-dividendenstrategie-2025.html`
  - Timing & Zyklen → `/podcast/timing-ist-alles-dividendenstrategie-podcast-2025.html`
  - (separator)
  - Maritime / Shipping → `/podcast/maritime-investments-schifffahrtsaktien-2025.html`
  - BDC Aktien → `/podcast/bdc-aktien-erklaert-2025.html`
  - Mining Serie → `/podcast/mining-serie-high-dividend-ressourcen-2025-2028.html`
- **Blog** → `/blog/`
- **Investing.com** → `/investing-analysen.html`
- **Rechner** (highlighted gold) → `/rechner/`

### Mobile Nav Links (< 700px)

Navigation section (8 links): Startseite, Depot-Strategie, Hard Asset Guide, Blog, Alle Rechner, Investing.com, Toolbox, Glossar

Themen section (6 links): Shipping, Midstream, Mining, Upstream, High-Yield, Rohstoff Superzyklus

Podcast section (3 links): Finanzfeuer Talk, Dividenden-Journey, Timing & Zyklen

When adding new pages, they only need a stub `<nav class="nav"></nav>` element — `nav.js` injects the full HTML at runtime. For pages that must work without JS, use the `CANONICAL_NAV_HTML` from `add_nav.py`.

### Cookie Consent Banner

- **Consent key**: `mbcs_consent_v1` in `localStorage`
- **States**: `null` (first visit, shows banner), `'granted'` (ads + analytics on), `'denied'` (essential only)
- **Google Consent Mode v2**: Sets `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`
- **Banner buttons**: "Alle akzeptieren" (gold primary) / "Nur notwendige" (outline secondary)
- **Banner CSS**: Injected dynamically by nav.js (fixed bottom, glassmorphism, z-index 9999)
- **Privacy link**: Points to `/datenschutz.html`

## SEO Conventions

### Every page should include:

1. **`<title>`** — Descriptive, includes "| MB Capital Strategies" suffix
2. **`<meta name="description">`** — Unique, keyword-rich description
3. **`<link rel="canonical">`** — Absolute URL to `https://mbcapitalstrategies.com/...`
4. **Open Graph tags** (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`)
5. **Twitter Card tags** (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`)
6. **`<meta name="author" content="Marco Bozem">`**
7. **Favicon links** — Standard set:
   ```html
   <link rel="icon" type="image/x-icon" href="/favicon.ico">
   <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
   <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
   <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
   <link rel="manifest" href="/site.webmanifest">
   <meta name="theme-color" content="#0f1115">
   ```

### Structured Data (JSON-LD)

- **Blog articles**: `BreadcrumbList` + `BlogPosting` (auto-injected by `nav.js` if missing) + optional `FAQPage`
- **Tool pages**: `WebApplication` (with `applicationCategory: "FinanceApplication"`, `price: "0"`) + `FAQPage`
- **Homepage**: `FAQPage` + `WebSite` + `Organization`
- **Hub/index pages**: `BreadcrumbList`

Note: `nav.js` automatically injects `BlogPosting` schema for `/blog/*` article pages that don't already include one. The injected schema includes author (`Marco Bozem`), publisher (`MB Capital Strategies`), `sameAs` links (YouTube, LinkedIn), and date extraction from meta tags or URL patterns. This ensures E-E-A-T compliance for legacy articles without manual edits.

### Author Bio Auto-Injection

`nav.js` automatically inserts an `.author-box` card on blog article pages with:
- Photo: `/marco.jpg` (62x62)
- Name: Marco Bozem (links to `/ueber-marco-bozem/`)
- Bio text: "Unabhängiger Investor & Gründer von MB Capital Strategies..."
- Links: Über Marco, YouTube (`@mbcapitalstrategies`), LinkedIn

Insertion point (in priority order): `.breadcrumbs` → `.breadcrumb` → `section.container` → `.page-wrapper` → `.container h1` → `nav.nav`

### Sitemaps

The site uses a **sitemap index** pattern (`sitemap.xml` → 9 sub-sitemaps):

| Sitemap | URLs | Content |
|---|---|---|
| `sitemap-main.xml` | 27 | Core pages (hub pages, legal, about) |
| `sitemap-blog.xml` | 84 | Blog articles (all sectors) |
| `sitemap-tools.xml` | 9 | Calculator tools |
| `sitemap-video.xml` | 23 | YouTube video embeds with full video schema |
| `sitemap-kategorien.xml` | 5 | Category hub pages |
| `sitemap-bestenlisten.xml` | 3 | Annual best-of lists (2026 editions only) |
| `sitemap-investing.xml` | 1 | Investing.com analyses hub |
| `sitemap-travel.xml` | 1 | Travel content |
| `glossar-sitemap.xml` | 137 | Glossary terms (auto-generated from `terms.json`) |

**When adding new pages**, update the relevant sub-sitemap XML file. Do NOT include redirect stubs (`noindex` pages) in sitemaps.

## Utility Scripts

### Python Scripts (batch HTML transformations)

These scripts are **one-off or maintenance tools** — they modify HTML files in-place:

| Script | Purpose | Targets |
|---|---|---|
| `add_nav.py` | Adds canonical nav to pages missing it or replaces old `<header>` navs | 10 specific pages (shipping, rohstoffe, glossar, kategorien, blog) |
| `fix_nav.py` | Standardizes nav dropdowns (Themen + Podcast) across ALL pages | Every `.html` file in repo (recursive walk) |
| `add_faq_schema.py` | Injects FAQPage JSON-LD (5 Q&As each) into mining + upstream articles | 10 blog articles (Thungela, Whitehaven, Yancoal, BHP, Fortescue, Rio Tinto, Vale, Glencore, Kazatomprom) |
| `rename_mining_2026.py` | Renames articles from `-2025` to `-2026` with redirect stubs | 9 mining slugs + updates blog/index.html, sitemap-blog.xml, cross-references |

These scripts use hardcoded `BASE` paths. Current values:
- `add_nav.py`: `BASE = '/home/user/Mbcapitalstategieslanding'`
- `fix_nav.py`: `BASE = '/home/user/Mbcapitalstategieslanding'`
- `add_faq_schema.py`: `BASE = '/home/user/Mbcapitalstategieslanding/blog'`
- `rename_mining_2026.py`: `BASE = '/home/user/Mbcapitalstategieslanding'`

Update the `BASE` variable if running in a different environment.

#### `fix_nav.py` — Details

- Regex-replaces "Sektoren" or "Themen" dropdown blocks with canonical version
- Updates mobile nav labels "Sektoren" → "Themen"
- **Homepage special handling**: Removes duplicate "Upstream Aktien" links, updates `/blog/index.html` → `/blog/` references
- Processes homepage separately, then walks all other HTML files

#### `rename_mining_2026.py` — Redirect Stub Pattern

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url=https://mbcapitalstrategies.com/blog/[new-slug].html">
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="https://mbcapitalstrategies.com/blog/[new-slug].html">
  <title>Weitergeleitet…</title>
</head>
<body>
  <p>Diese Seite wurde verschoben. <a href="...">Klicke hier, falls du nicht automatisch weitergeleitet wirst.</a></p>
</body>
</html>
```

### Node.js Script

| Script | Purpose |
|---|---|
| `build-glossar-sitemap.mjs` | Reads `glossar/terms.json`, deduplicates slugs, generates `glossar-sitemap.xml` with URLs like `https://mbcapitalstrategies.com/glossar/?begriff=<slug>` |

Run with: `node build-glossar-sitemap.mjs`

## Glossary System

The glossary (`/glossar/`) consists of:

1. **`terms.json`** — Maps 211 German/English financial terms to 137 unique URL-safe anchors. Categories:
   - Core financial (15): Dividende, Cashflow, EBITDA, KGV, ROE, NAV, REIT...
   - Valuation & ratios (20+): KBV, KUV, PEG, Forward KGV, EV/EBITDA, Debt-to-Equity...
   - Shipping general (22): VLCC, Panamax, Suezmax, Capesize, Bulk Carrier, Baltic Dry Index...
   - Shipping 2026 regulations (34+): ETS Maritime, FuelEU, CII, EEXI, Dual Fuel, Retrofit, Rotor-Sail...
   - Mining & resources (17+): AISC, Ore Grade, Uranium, Yellowcake, Eisenerz, Kupfer...
   - Dividends (6+): DPS, DRIP, Dividend Coverage, Sonderdividende...
   - Midstream & MLPs (4+): MLP, K-1, Distributable Cash Flow, Pipeline...
   - Oil & Gas (4+): Upstream, Downstream, NGL, Throughput...
   - Macro & advanced (15+): DCF, WACC, Beta, Commodity Supercycle, Value Trap, Margin of Safety...

2. **`glossar.js`** — Powers the glossary index page with search/filter and dynamic SEO (title, description, Schema.org based on URL `?begriff=` parameter). Auto-opens and highlights term from URL param.

3. **`autolink-glossar.js`** / **`assets/js/glossar-linking.js`** — Client-side scripts that auto-link glossary terms found in article text. Fetches `/glossar/terms.json`, protects existing `<a>` tags, then replaces term matches with links to `/glossar/?begriff=anchor` or `/glossar/#anchor`. Uses word boundaries and case-insensitive matching.

4. **Specialized glossary pages**:
   - `shipping-cluster.html` — Shipping terminology hub
   - `aisc-mining.html` — Mining cost definitions (All-In Sustaining Costs)
   - `tce-rate.html` — Shipping Time Charter Equivalent rates

When adding new financial terms, add them to `terms.json` and regenerate the sitemap with `node build-glossar-sitemap.mjs`.

## Page Patterns

### Blog Article Template

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <!-- Favicons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0f1115">

  <!-- AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7097302643579933" crossorigin="anonymous"></script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="canonical" href="https://mbcapitalstrategies.com/blog/[slug].html">
  <title>[Company] – [Subtitle] | MB Capital Strategies</title>
  <meta name="description" content="[SEO description]">
  <meta name="author" content="Marco Bozem">

  <!-- Open Graph + Twitter -->
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="...">
  <meta property="og:url" content="...">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="stylesheet" href="/blog/styles.css?v=2">

  <!-- JSON-LD: BlogPosting -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "[Title]",
    "description": "[Description]",
    "author": { "@type": "Person", "name": "Marco Bozem", "url": "https://mbcapitalstrategies.com/ueber-marco-bozem/" },
    "publisher": { "@type": "Organization", "name": "MB Capital Strategies", "logo": { "@type": "ImageObject", "url": "https://mbcapitalstrategies.com/Logo.png" } },
    "mainEntityOfPage": "https://mbcapitalstrategies.com/blog/[slug].html",
    "datePublished": "[ISO date]",
    "dateModified": "[ISO date]",
    "image": { "@type": "ImageObject", "url": "...", "width": 1200, "height": 630 }
  }
  </script>

  <!-- JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Startseite", "item": "https://mbcapitalstrategies.com/" },
      { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://mbcapitalstrategies.com/blog/" },
      { "@type": "ListItem", "position": 3, "name": "[Title]", "item": "https://mbcapitalstrategies.com/blog/[slug].html" }
    ]
  }
  </script>

  <!-- JSON-LD: FAQPage (optional, 5 Q&As) -->

  <!-- Inline <style> overrides (if needed) -->
</head>
<body>
  <nav class="nav"></nav>  <!-- nav.js injects full nav HTML here -->

  <nav class="breadcrumbs">
    <a href="/">Startseite</a> ›
    <a href="/blog/">Blog</a> ›
    <span>[Current Article]</span>
  </nav>

  <!-- Author bio is auto-injected by nav.js after breadcrumbs -->

  <section class="article-hero">
    <div class="inner">
      <h1>[Title]</h1>
      <div class="article-meta">
        <span>Published: [Date]</span>
        <span>Marco Bozem</span>
        <span>[Category]</span>
      </div>
    </div>
  </section>

  <article class="article-body">
    <!-- Content sections with h2/h3, paragraphs, tables -->
    <div class="info-box"><strong>Info:</strong> [Key information]</div>
    <div class="risk-box"><strong>Risiko:</strong> [Risk factors]</div>
    <div class="key-takeaway"><p>[Key insight]</p></div>
    <div class="metrics-grid">
      <div class="metric-card">
        <span class="metric-value">10%</span>
        <span class="metric-label">Dividendenrendite</span>
      </div>
    </div>
    <div class="video-wrapper">
      <iframe src="https://www.youtube.com/embed/[id]" ...></iframe>
    </div>

    <div class="cta-box">
      <h3>[Call to Action]</h3>
      <a href="[link]" class="btn">Action Button</a>
    </div>
    <div class="related-articles">
      <h3>Verwandte Artikel</h3>
      <ul><li><a href="...">Title</a></li></ul>
    </div>
    <div class="disclaimer">
      <strong>Disclaimer:</strong> Keine Anlageberatung. Alle Angaben ohne Gewähr.
    </div>
  </article>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-col"><h4>Section</h4><a href="...">Link</a></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 MB Capital Strategies &middot; Marco Bozem</span>
    </div>
  </footer>

  <script src="/assets/js/nav.js" defer></script>
  <script src="/assets/js/glossar-linking.js" defer></script>
</body>
</html>
```

### Tool Page Template

Tool pages (calculators) include:
- `WebApplication` JSON-LD schema (with `applicationCategory: "FinanceApplication"`, `price: "0"`)
- `FAQPage` JSON-LD with tool-specific questions
- Interactive JavaScript calculator (inline `<script>`)
- SEO-optimized text content below the calculator
- Same nav, favicon, AdSense setup as blog articles

### Section Hub Template (e.g., `/shipping-aktien/index.html`)

Hub pages list articles for a sector with card grids (`.posts` / `.grid`), use the shared design system, and typically include:
- `BreadcrumbList` JSON-LD
- Card grid of related articles
- Sector overview text
- CTA box linking to related tools or guides

### Homepage (`index.html`)

Self-contained (~1570 lines) with ALL styles inline. Features:
- Hero section with background image
- Sector cards (Shipping, Mining, Midstream, Upstream, Dividendenstrategie)
- Featured articles grid
- YouTube embed
- Tool/calculator showcase
- Newsletter/CTA sections
- Own inline nav (NOT from nav.js — must be updated manually)

## Content Conventions

- **Language**: All content is in **German** (`lang="de"`)
- **Disclaimer**: Every analysis article must include a legal disclaimer: "Keine Anlageberatung. Alle Angaben ohne Gewähr."
- **Author**: Marco Bozem — all articles attributed to him
- **Date format**: German format in display, ISO 8601 in Schema.org (`datePublished`, `dateModified`)
- **URLs**: Use lowercase, hyphenated slugs. Year suffix pattern: `aktie-analyse-2026.html`. When renaming year suffixes (e.g., 2025→2026), keep the old file as a `<meta http-equiv="refresh">` redirect stub with `<meta name="robots" content="noindex, follow">`
- **Images**: Root-level JPEGs/PNGs for charts and infographics. Use `loading="lazy"` for below-fold images
- **YouTube embeds**: Wrapped in `.video-wrapper` for responsive 16:9 aspect ratio
- **AdSense**: Include on all public pages: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7097302643579933" crossorigin="anonymous"></script>`
- **Affiliate links**: Broker/tool recommendations in `toolbox.html` and some articles contain affiliate links with disclosure

## Development Workflow

1. **No build step required** — edit HTML/CSS/JS files directly
2. **Test locally** — open HTML files in a browser or use a local server (`python -m http.server`)
3. **Maintain nav consistency** — use `fix_nav.py` or `add_nav.py` after adding new pages
4. **Update sitemaps** — manually edit the relevant `sitemap-*.xml` when adding/removing pages
5. **Regenerate glossary sitemap** — run `node build-glossar-sitemap.mjs` after editing `terms.json`
6. **Deployment** — push to `main` branch; GitHub Pages auto-deploys

## Common Tasks

### Adding a New Blog Article
1. Create `blog/<slug>.html` following the blog article template above
2. Include favicon links, AdSense script, meta tags (title, description, author, canonical, OG, Twitter)
3. Add `<link rel="stylesheet" href="/blog/styles.css?v=2">`
4. Add JSON-LD `BreadcrumbList` schema (3 items: Startseite → Blog → Article)
5. Add JSON-LD `BlogPosting` schema (or rely on nav.js auto-injection for legacy articles)
6. Optionally add `FAQPage` schema (5 relevant Q&As for E-E-A-T)
7. Add stub `<nav class="nav"></nav>` (nav.js injects full nav at runtime)
8. Add breadcrumbs, article-hero, article-body, disclaimer, footer
9. Include `<script src="/assets/js/nav.js" defer></script>` and optionally `<script src="/assets/js/glossar-linking.js" defer></script>`
10. Add entry to `sitemap-blog.xml` with appropriate priority and changefreq
11. Add card entry to `blog/index.html` (with correct `data-category`) and relevant sector hub pages

### Adding a New Calculator Tool
1. Create `tools/<name>.html` following tool page template
2. Add `WebApplication` + `FAQPage` JSON-LD schemas
3. Include interactive JS calculator in inline `<script>`
4. Add entry to `sitemap-tools.xml`
5. Add card to `rechner/index.html`

### Renaming Articles (Year Updates, e.g., 2025→2026)
1. Copy old file to new filename (e.g., `xyz-2025.html` → `xyz-2026.html`)
2. Update title, canonical URL, breadcrumb name, dateModified in new file
3. Replace old file content with redirect stub (meta refresh + noindex + canonical to new URL)
4. Update `blog/index.html` card links
5. Update `sitemap-blog.xml` (replace old URL, keep only new)
6. Update cross-references in other blog articles and hub pages
7. Use `rename_mining_2026.py` as a reference for automating this process

### Updating Navigation Site-Wide
1. Update the nav HTML in **all three sources**: `injectNav()` in `/assets/js/nav.js`, `CANONICAL_NAV_HTML` in `add_nav.py`, and `CANONICAL_NAV` in `fix_nav.py`
2. Since `nav.js` injects the nav at runtime, most pages update automatically after step 1
3. Run `python3 fix_nav.py` to update the static HTML nav in all pages (for no-JS fallback and initial render)
4. Manually verify the homepage (`index.html`) as it has its own inline nav that must be updated separately

### Adding Glossary Terms
1. Add term → slug mapping to `glossar/terms.json`
2. Run `node build-glossar-sitemap.mjs` to regenerate `glossar-sitemap.xml`
3. Terms are automatically linked in articles via `glossar-linking.js`

## Social & External Links

| Platform | URL |
|---|---|
| YouTube | `https://www.youtube.com/@mbcapitalstrategies` |
| LinkedIn | `https://www.linkedin.com/in/marco-bozem-182173295` |
| Website | `https://mbcapitalstrategies.com` |
| Author Page | `/ueber-marco-bozem/` |

## Important Notes

- **No package.json or npm dependencies** — the only Node.js usage is `build-glossar-sitemap.mjs` (runs with bare Node.js, uses only `fs` built-in)
- **No test suite** — this is a content site; verify changes by visual inspection in the browser
- **GitHub Pages deployment** — the repository root IS the site root; every file is publicly accessible
- **DSGVO compliance** — cookie consent banner is mandatory; do not add tracking without consent flow
- **Inline styles on homepage** — `index.html` is self-contained (~1570 lines) with all styles inline; changes to the design system in `blog/styles.css` do NOT automatically affect it
- **Homepage nav is separate** — `index.html` has its own inline nav that is NOT replaced by `nav.js`. Must be updated manually when nav changes.
- **Python scripts use hardcoded paths** — update `BASE` variable if running outside the expected environment
- **AdSense publisher ID** — `ca-pub-7097302643579933` (referenced in `ads.txt` and all page headers)
- **robots.txt** — Disallows `/admin/`, `/draft/`, `/tmp/`, `/private/`. Allows all CSS/JS for mobile-friendly testing. Lists all 10 sitemaps.
- **Redirect stubs** must include `<meta name="robots" content="noindex, follow">` to prevent indexing of old URLs
- **Blog article exclusions** — `nav.js` explicitly excludes `alle-finanzrechner.html`, `meine-toolbox-broker-tools-plattformen-2025.html`, and `wise-airalo-vietnam-erfahrungen.html` from author bio and schema injection
