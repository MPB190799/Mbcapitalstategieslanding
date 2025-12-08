// ===== MB Glossar – Auto-Open + Dynamic SEO =====

// Helper: terms.json laden (mit Support für /* Kommentare */)
async function loadGlossarTerms() {
  const res = await fetch("/glossar/terms.json");
  const raw = await res.text();

  const clean = raw
    .replace(/\/\*[\s\S]*?\*\//g, "")  // Kommentare entfernen
    .replace(/,\s*}/g, "}");           // trailing commas entfernen

  return JSON.parse(clean);
}

// URL-Parameter auslesen
const params = new URLSearchParams(window.location.search);
const slug = params.get("begriff")?.toLowerCase();

// ---------- 1) Auto-Open + Scroll ----------
(function autoOpenGlossarTerm() {
  if (!slug) return;

  const el = document.getElementById(slug);
  if (!el) return;

  el.open = true;

  // sanfter Scroll
  setTimeout(() => {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 180);

  // kleines visuelles Highlight
  el.style.boxShadow = "0 0 18px rgba(212,175,55,.75)";
  setTimeout(() => { el.style.boxShadow = ""; }, 1800);
})();

// ---------- 2) Dynamic SEO (Title + Description + Schema.org) ----------
(async function dynamicSeoForGlossar() {
  if (!slug) return;

  const terms = await loadGlossarTerms();

  // Reverse Lookup: slug → name
  const matchedName = Object.keys(terms).find(
    (name) => String(terms[name]).toLowerCase() === slug
  );

  if (!matchedName) return;

  // 2a: Title setzen
  document.title = `${matchedName} – Glossar | MB Capital Strategies`;

  // 2b: Meta Description setzen
  let meta = document.querySelector('meta[name="description"]');
  if (!meta) {
    meta = document.createElement("meta");
    meta.name = "description";
    document.head.appendChild(meta);
  }
  meta.content = `${matchedName} – Bedeutung, Definition und Anwendung im Hard-Asset- & Cashflow-Investing.`;

  // 2c: JSON-LD DefinedTerm einfügen
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
