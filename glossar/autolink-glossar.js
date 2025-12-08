// ===== MB Glossar – Auto-Linking in Blogartikeln =====

(async () => {
  // terms.json laden (mit Kommentar-Strip, wie in glossar.js)
  const res = await fetch("/glossar/terms.json");
  const raw = await res.text();
  const clean = raw
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/,\s*}/g, "}");
  const terms = JSON.parse(clean);

  // Content-Wrapper suchen
  const root = document.querySelector(".blog-content");
  if (!root) return;

  // Begriffe nach Länge sortieren (lange zuerst, damit "Yield on Cost" vor "Yield" matcht)
  const entries = Object.entries(terms).sort(
    (a, b) => b[0].length - a[0].length
  );

  const escapeRegExp = (str) =>
    str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const patterns = entries.map(([name, slug]) => ({
    name,
    slug,
    regex: new RegExp(`\\b${escapeRegExp(name)}\\b`, "gi"),
  }));

  // Nur Textknoten verarbeiten, keine Links etc.
  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode(node) {
        const parent = node.parentNode;
        if (!parent) return NodeFilter.FILTER_REJECT;
        // Nichts in Links / Buttons / Headings / explizit ausgeschlossenen Bereichen linken
        const tag = parent.nodeName;
        if (["A", "BUTTON", "SCRIPT", "STYLE"].includes(tag)) {
          return NodeFilter.FILTER_REJECT;
        }
        if (parent.closest && parent.closest("[data-no-glossar]")) {
          return NodeFilter.FILTER_REJECT;
        }
        if (!node.nodeValue || !node.nodeValue.trim()) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    },
    false
  );

  const toReplace = [];
  let node;
  while ((node = walker.nextNode())) {
    toReplace.push(node);
  }

  for (const textNode of toReplace) {
    let text = textNode.nodeValue;
    let changed = false;

    for (const { name, slug, regex } of patterns) {
      const url = `/glossar/?begriff=${slug}`;
      const replacement = (match) =>
        `<a href="${url}" class="glossar-link">${match}</a>`;
      const newText = text.replace(regex, replacement);
      if (newText !== text) {
        text = newText;
        changed = true;
      }
    }

    if (changed) {
      const span = document.createElement("span");
      span.innerHTML = text;
      textNode.parentNode.replaceChild(span, textNode);
    }
  }
})();
