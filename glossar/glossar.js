// --- Auto-Open + Scroll ---
const url = new URLSearchParams(window.location.search);
const openId = url.get("begriff");

if (openId) {
  const el = document.getElementById(openId.toLowerCase());
  if (el) {
    el.setAttribute("open", "open");

    setTimeout(() => {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 200);

    // Highlight-Effekt
    el.style.boxShadow = "0 0 18px rgba(212,175,55,.75)";
    setTimeout(() => { el.style.boxShadow = ""; }, 1800);
  }
}

// --- Dynamic SEO ---
(async () => {
  const slug = openId;
  if (!slug) return;

  const res = await fetch("/glossar/terms.json");
  const terms = await res.json();

  let matchedName = null;
  for (const [name, key] of Object.entries(terms)) {
    if (key.toLowerCase() === slug.toLowerCase()) {
      matchedName = name;
      break;
    }
  }
  if (!matchedName) return;

  // Title
  document.title = `${matchedName} – Glossar | MB Capital Strategies`;

  // Meta-Description
  let meta = document.querySelector('meta[name="description"]');
  if (!meta) {
    meta = document.createElement("meta");
    meta.name = "description";
    document.head.appendChild(meta);
  }
  meta.content = `${matchedName} erklärt – Glossar für Hard Asset & Cashflow Investoren.`;

  // JSON-LD Schema
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
