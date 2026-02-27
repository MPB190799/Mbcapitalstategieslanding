# CLAUDE.md — MB Capital Strategies

## Project Overview

**MB Capital Strategies** (`mbcapitalstrategies.com`) is a German-language static website focused on dividend investing in hard assets (energy, shipping, mining, pipelines). It is authored by Marco Bozem and hosted on **GitHub Pages** with a custom domain via `CNAME`.

This is **not** a JavaScript/Node.js application — it is a **static HTML site** with ~115 hand-authored HTML pages, inline CSS/JS, and a handful of utility scripts for batch operations.

## Tech Stack

| Layer | Technology |
|---|---|
| Hosting | GitHub Pages (custom domain: `mbcapitalstrategies.com`) |
| Language | Static HTML, inline CSS, vanilla JavaScript |
| Font | Montserrat (Google Fonts) |
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
├── ads.txt                 # AdSense publisher verification
├── site.webmanifest        # PWA manifest (icons, theme)
│
├── blog/                   # ~70 article pages (stock analyses, market news, guides)
│   ├── index.html          # Blog listing page
│   └── styles.css          # Shared stylesheet for blog + most content pages
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
│   ├── styles.css          # Podcast-specific styles (shares design tokens)
│   └── *.html
│
├── glossar/                # Financial glossary system
│   ├── index.html          # Glossary page with search
│   ├── terms.json          # Term→slug mapping (used for auto-linking)
│   ├── glossar.js          # Glossary page logic
│   ├── autolink-glossar.js # Client-side glossary term auto-linker
│   └── shipping-cluster.html
│
├── assets/
│   └── js/
│       ├── nav.js          # Shared navigation + cookie consent + scroll effects
│       └── glossar-linking.js  # Auto-links glossary terms in article content
│
├── shipping/               # Shipping sector hub
├── shipping-aktien/        # Shipping stocks index
├── midstream/              # Pipeline/midstream sector hub
├── mining-aktien/          # Mining stocks index
├── upstream-aktien/        # Upstream oil & gas stocks index
├── rohstoffe/              # Commodity deep-dives (copper, nickel, uranium, zinc)
├── kategorien/             # Category pages (high-yield, mining, commodity supercycle)
├── bestenlisten/           # "Best of" lists (LNG, tanker, high-yield)
├── dividendenstrategie/    # Dividend strategy guide
├── depot-strategie/        # Portfolio strategy with embedded Parqet widgets
├── hard-asset-guide/       # Hard asset investing guide
├── ueber-marco-bozem/      # About the author
│
├── sitemap.xml             # Master sitemap index
├── sitemap-main.xml        # Core pages sitemap
├── sitemap-blog.xml        # Blog articles sitemap
├── sitemap-tools.xml       # Calculator tools sitemap
├── sitemap-video.xml       # Video sitemap
├── sitemap-*.xml           # Additional sub-sitemaps
├── glossar-sitemap.xml     # Auto-generated glossary sitemap
│
├── datenschutz.html        # Privacy policy (DSGVO)
├── impressum.html          # Legal notice (German law requirement)
├── toolbox.html            # Recommended brokers & tools
├── blogindex.html          # Alternative blog listing
├── investing-analysen.html # Investing.com analyses hub
├── rohstoff-superzyklus-master.html  # Commodity supercycle master page
│
├── *.py                    # Python batch-processing scripts (see below)
├── build-glossar-sitemap.mjs  # Node.js ESM script to generate glossar-sitemap.xml
│
└── *.jpg, *.jpeg, *.png    # Root-level images (background, charts, author photo, favicons)
```

## Design System

### Color Palette (CSS Custom Properties)

```css
--gold: #d4af37;           /* Primary accent / brand gold */
--gold-strong: #e0bd55;    /* Bright gold for gradients */
--gold-dim: rgba(212,175,55,0.15);  /* Subtle gold backgrounds */
--bg: #0f1115;             /* Dark background */
--bg-soft: #151821;        /* Slightly lighter background */
--bg-card: #1a1f2b;        /* Card background */
--text: #f5f6fa;           /* Primary text (near-white) */
--text-2 / --text-soft: #cfd6e6;  /* Secondary text */
--text-muted / --muted: #9aa6c0;  /* Muted text */
--radius: 16px;            /* Card border radius */
--radius-sm: 10px;         /* Small element radius */
```

### Visual Style

- **Dark theme** with gold (#d4af37) accents throughout
- **Glassmorphism** cards with `backdrop-filter: blur()` and semi-transparent backgrounds
- **Montserrat** font family (400–800 weights)
- Gradient gold headings using `-webkit-background-clip: text`
- Hover effects: `translateY(-6px)` lift with gold border glow
- Reading progress bar on article pages (gold gradient, fixed top)
- Scroll reveal animations via IntersectionObserver (`.reveal` → `.visible`)

### Key CSS Classes

| Class | Purpose |
|---|---|
| `.nav`, `.nav-inner`, `.nav-links` | Main sticky navigation bar |
| `.nav-hamburger`, `.nav-mobile` | Mobile navigation (breakpoint: 700px) |
| `.dropdown`, `.dropdown-btn`, `.dropdown-content` | Dropdown menus in nav |
| `.container`, `.page-wrapper` | Content wrapper (max-width: 960px) |
| `.page-header` | Centered page title section with gold gradient |
| `.article-hero` | Full-width article header with gradient background |
| `.article-body` | Article content wrapper (max-width: 860px) |
| `.post`, `.card` | Glassmorphism content cards |
| `.btn`, `.btn-secondary` | Gold pill buttons |
| `.info-box`, `.risk-box`, `.success-box` | Colored info callout boxes |
| `.key-takeaway` | Highlighted takeaway with star icon |
| `.metrics-grid`, `.metric-card` | Financial metrics display grid |
| `.table-wrapper`, `.data-table` | Styled data tables |
| `.cta-box` | Call-to-action box with gold top border |
| `.related-articles` | Related content links grid |
| `.breadcrumbs` | Navigation breadcrumbs |
| `.author-box` | Author bio card |
| `.disclaimer` | Legal disclaimer box |
| `.reveal` | Scroll-triggered fade-in animation |
| `.section-label` | Uppercase gold pill label |
| `.filter-bar`, `.filter-btn` | Blog category filter UI |

## Stylesheets

There are **two main CSS sources** — pages use one or the other:

1. **`/blog/styles.css`** — The shared design system stylesheet (~1200 lines). Used by blog articles, tools, rechner, podcast pages, and most content pages. Referenced as `<link rel="stylesheet" href="/blog/styles.css?v=2">`.

2. **Inline `<style>` blocks** — The homepage (`index.html`) and some older pages embed their own styles directly. These share the same design tokens but may have page-specific additions.

Some pages include **both** the shared stylesheet and additional inline `<style>` overrides.

## Navigation

### Shared Navigation (`/assets/js/nav.js`)

All pages should include:
```html
<script src="/assets/js/nav.js" defer></script>
```

This script provides:
- **Hamburger menu** toggle for mobile (< 700px)
- **Dropdown menus** (hover on desktop, click on mobile)
- **Scroll reveal** animation (IntersectionObserver on `.reveal` elements)
- **Reading progress bar** (on pages with `.article-body`, `article`, or `.article-hero`)
- **Active nav link** highlighting based on current URL path
- **Author bio injection** on `/blog/*` article pages (auto-inserts Marco Bozem bio)
- **Cookie consent banner** (DSGVO-compliant, Google Consent Mode v2, stored in `localStorage` as `mbcs_consent_v1`)

### Canonical Navigation HTML

The standard nav structure is defined in `add_nav.py` and `fix_nav.py`. It includes:
- Brand logo + name linking to `/`
- Desktop links: Startseite, Depot-Strategie, Hard Asset Guide, Themen (dropdown), Podcast (dropdown), Blog, Investing.com, Rechner (highlighted)
- Mobile nav with categorized sections (Navigation, Themen, Podcast)

When adding or modifying pages, **always use the canonical nav HTML** from `add_nav.py` (the `CANONICAL_NAV_HTML` constant) to maintain consistency.

## SEO Conventions

### Every page should include:

1. **`<title>`** — Descriptive, includes "| MB Capital Strategies" suffix
2. **`<meta name="description">`** — Unique, keyword-rich description
3. **`<link rel="canonical">`** — Absolute URL to `https://mbcapitalstrategies.com/...`
4. **Open Graph tags** (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`)
5. **Twitter Card tags** (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`)
6. **`<meta name="author" content="Marco Bozem">`**
7. **Favicon links** — Standard set (ico, png 16/32, apple-touch-icon, webmanifest)

### Structured Data (JSON-LD)

- **Blog articles**: `BreadcrumbList` + optional `BlogPosting` + optional `FAQPage`
- **Tool pages**: `WebApplication` (with `applicationCategory: "FinanceApplication"`, `price: "0"`) + `FAQPage`
- **Homepage**: `FAQPage` + `WebSite` + `Organization`
- **Hub/index pages**: `BreadcrumbList`

### Sitemaps

The site uses a **sitemap index** pattern:
- `sitemap.xml` — Master index referencing all sub-sitemaps
- `sitemap-main.xml` — Core pages
- `sitemap-blog.xml` — Blog articles
- `sitemap-tools.xml` — Calculator tools
- `sitemap-video.xml` — YouTube video embeds
- `sitemap-kategorien.xml`, `sitemap-bestenlisten.xml`, `sitemap-investing.xml`, `sitemap-travel.xml`
- `glossar-sitemap.xml` — Auto-generated from `terms.json` via `build-glossar-sitemap.mjs`

**When adding new pages**, update the relevant sub-sitemap XML file.

## Utility Scripts

### Python Scripts (batch HTML transformations)

These scripts are **one-off or maintenance tools** — they modify HTML files in-place:

| Script | Purpose |
|---|---|
| `add_nav.py` | Adds canonical nav to pages missing it or replaces old `<header>` navs |
| `fix_nav.py` | Standardizes nav dropdowns (Themen + Podcast) across all pages |
| `add_faq_schema.py` | Injects FAQPage JSON-LD schema into blog articles |
| `rename_mining_2026.py` | Renames mining analysis articles from `-2025` to `-2026` URLs with redirects |

These scripts use hardcoded `BASE = '/home/user/Mbcapitalstategieslanding'` paths. Update the `BASE` variable if running in a different environment.

### Node.js Script

| Script | Purpose |
|---|---|
| `build-glossar-sitemap.mjs` | Reads `glossar/terms.json` and generates `glossar-sitemap.xml` |

Run with: `node build-glossar-sitemap.mjs`

## Glossary System

The glossary (`/glossar/`) consists of:

1. **`terms.json`** — Maps German financial terms to URL-safe anchors (e.g., `"Dividendenrendite": "dividendenrendite"`)
2. **`glossar.js`** — Powers the glossary index page with search/filter
3. **`autolink-glossar.js`** / **`assets/js/glossar-linking.js`** — Client-side scripts that auto-link glossary terms found in article text, creating links to `/glossar/#anchor` or `/glossar/?begriff=anchor`

When adding new financial terms, add them to `terms.json` and regenerate the sitemap.

## Page Patterns

### Blog Article Template

Blog articles follow this structure:
```
<!DOCTYPE html>
<html lang="de">
<head>
  <!-- meta, title, canonical, OG/Twitter, author -->
  <link rel="stylesheet" href="/blog/styles.css?v=2">
  <!-- AdSense script -->
  <!-- JSON-LD: BreadcrumbList -->
  <!-- JSON-LD: FAQPage (optional) -->
  <!-- Inline <style> overrides (if needed) -->
</head>
<body>
  <!-- Canonical Nav (header.nav) -->
  <nav class="breadcrumbs">...</nav>
  <!-- Author bio is auto-injected by nav.js -->
  <section class="article-hero">...</section>
  <article class="article-body">
    <!-- Content: h2/h3 headings, paragraphs, tables, info-boxes, metrics-grid -->
    <div class="cta-box">...</div>
    <div class="related-articles">...</div>
    <div class="disclaimer">...</div>
  </article>
  <footer class="site-footer">...</footer>
  <script src="/assets/js/nav.js" defer></script>
  <script src="/assets/js/glossar-linking.js" defer></script>
</body>
</html>
```

### Tool Page Template

Tool pages (calculators) include:
- `WebApplication` JSON-LD schema
- `FAQPage` JSON-LD with tool-specific questions
- Interactive JavaScript calculator (inline `<script>`)
- SEO-optimized text content below the calculator

### Section Hub Template (e.g., `/shipping/index.html`)

Hub pages list articles for a sector with card grids (`.posts` / `.grid`) and use the shared design system.

## Content Conventions

- **Language**: All content is in **German** (lang="de")
- **Disclaimer**: Every analysis article must include a legal disclaimer that content is for informational purposes only and does not constitute investment advice
- **Author**: Marco Bozem — all articles attributed to him
- **Date format**: German format in display, ISO 8601 in Schema.org (`datePublished`, `dateModified`)
- **URLs**: Use lowercase, hyphenated slugs. Year suffix pattern: `aktie-analyse-2026.html`
- **Images**: Root-level JPEGs/PNGs for charts and infographics. Use `loading="lazy"` for below-fold images
- **YouTube embeds**: Wrapped in `.video-wrapper` for responsive 16:9 aspect ratio
- **AdSense**: Include on all public pages: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7097302643579933" crossorigin="anonymous"></script>`

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
2. Include canonical nav HTML, breadcrumbs, article-hero, article-body
3. Add JSON-LD `BreadcrumbList` schema
4. Optionally add `FAQPage` schema (5 relevant Q&As)
5. Link `<link rel="stylesheet" href="/blog/styles.css?v=2">`
6. Include `<script src="/assets/js/nav.js" defer></script>` and optionally glossar-linking
7. Add entry to `sitemap-blog.xml`
8. Add card entry to `blog/index.html` and relevant sector hub pages

### Adding a New Calculator Tool
1. Create `tools/<name>.html` following tool page template
2. Add `WebApplication` + `FAQPage` JSON-LD schemas
3. Include interactive JS calculator in inline `<script>`
4. Add entry to `sitemap-tools.xml`
5. Add card to `rechner/index.html`

### Updating Navigation Site-Wide
1. Update the `CANONICAL_NAV_HTML` in `add_nav.py` and `CANONICAL_NAV` in `fix_nav.py`
2. Run `python3 fix_nav.py` to propagate changes to all pages
3. Manually verify the homepage (`index.html`) as it has its own inline nav

## Important Notes

- **No package.json or npm dependencies** — the only Node.js usage is `build-glossar-sitemap.mjs` (runs with bare Node.js, uses only `fs` built-in)
- **No test suite** — this is a content site; verify changes by visual inspection in the browser
- **GitHub Pages deployment** — the repository root IS the site root; every file is publicly accessible
- **DSGVO compliance** — cookie consent banner is mandatory; do not add tracking without consent flow
- **Inline styles on homepage** — `index.html` is self-contained (~1570 lines) with all styles inline; changes to the design system in `blog/styles.css` do NOT automatically affect it
- **Python scripts use hardcoded paths** — update `BASE` variable if running outside the expected environment
- **AdSense publisher ID** — `ca-pub-7097302643579933` (referenced in `ads.txt` and all page headers)
