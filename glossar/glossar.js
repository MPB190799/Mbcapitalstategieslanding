// ===== MB Glossar – Auto-Open + Dynamic SEO =====

// Helper: terms.json laden (mit Support für /* Kommentare */)
async function loadGlossarTerms() {
  const res = await fetch("/glossar/terms.json");
  const raw = await res.text();

  const clean = raw
    .replace(/\/\*[\s\S]*?\*\//g, "") // Kommentare entfernen
    .replace(/,\s*}/g, "}");          // letztes Komma vor } entfernen

  return JSON.parse(clean);
}

// URL-Parameter auslesen
const params = new URLSearchParams(window.location.search);
const slug = params.get("begriff");

// ---------- 1) Auto-Open + Scroll ----------
(function autoOpenGlossarTerm() {
  if (!slug) return;
  const el = document.getElementById(slug.toLowerCase());
  if (!el) return;

  // Akkordeon öffnen
  el.setAttribute("open", "open");

  // Sanft hinscrollen
  setTimeout(() => {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 200);

  // kleines Highlight
  el.style.boxShadow = "0 0 18px rgba(212,175,55,.75)";
  setTimeout(() => { el.style.boxShadow = ""; }, 1800);
})();

// ---------- 2) Dynamic SEO (Title + Description + Schema.org) ----------
(async function dynamicSeoForGlossar() {
  if (!slug) return;

  const terms = await loadGlossarTerms();

  let matchedName = null;
  for (const [name, key] of Object.entries(terms)) {
    if (String(key).toLowerCase() === slug.toLowerCase()) {
      matchedName = name;
      break;
    }
  }
  if (!matchedName) return;

  // Title dynamisch setzen
  document.title = `${matchedName} – Glossar | MB Capital Strategies`;

  // Meta Description anpassen oder neu anlegen
  let meta = document.querySelector('meta[name="description"]');
  if (!meta) {
    meta = document.createElement("meta");
    meta.name = "description";
    document.head.appendChild(meta);
  }
  meta.content = `${matchedName} einfach erklärt – Glossar für Hard-Asset- & Cashflow-Investoren.`;

  // DefinedTerm Schema.org einfügen
  const ld = {
    "@context": "https://schema.org",
    "@type": "DefinedTerm",
    "name": matchedName,
    "url": window.location.href,
    "inDefinedTermSet": "https://mbcapitalstrategies.com/glossar/"
  };

  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(ld);
  document.head.appendChild(script);
})();

