// ===== MB Glossar – Auto-Linking in Blogartikeln =====

(async () => {
  const res = await fetch("/glossar/terms.json");
  const raw = await res.text();
  const clean = raw
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/,\s*}/g, "}");
  const terms = JSON.parse(clean);

  const root = document.querySelector(".blog-content, .article-content, article, main");
  if (!root) return;

  const escapeRegExp = (str) => str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const entries = Object.entries(terms)
    .sort((a, b) => b[0].length - a[0].length)
    .map(([name, slug]) => ({
      name,
      slug,
      regex: new RegExp(`\\b${escapeRegExp(name)}\\b`, "gi")
    }));

  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode(node) {
        const parent = node.parentNode;
        if (!parent) return NodeFilter.FILTER_REJECT;

        const tag = parent.nodeName;

        // ❌ NICHT verlinken in:
        if (["A", "BUTTON", "SCRIPT", "STYLE", "H1", "H2", "H3", "H4", "H5"].includes(tag)) {
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
  while ((node = walker.nextNode())) toReplace.push(node);

  for (const textNode of toReplace) {
    let text = textNode.nodeValue;
    let changed = false;

    for (const { name, slug, regex } of entries) {
      const url = `/glossar/?begriff=${slug}`;
      const linked = text.replace(regex, (match) =>
        `<a href="${url}" class="glossar-link">${match}</a>`
      );

      if (linked !== text) {
        text = linked;
        changed = true;
      }
    }

    if (changed) {
      const span = document.createElement("span");
      span.innerHTML = text;
      textNode.parentNode.replaceChild(span, textNode);
    }
  }

  // Optional: kleines Branding für Links
  const style = document.createElement("style");
  style.textContent = `
    .glossar-link {
      color: #d4af37;
      font-weight: 600;
      text-decoration: none;
      border-bottom: 1px dashed #d4af37;
    }
    .glossar-link:hover {
      text-decoration: underline;
    }
  `;
  document.head.appendChild(style);
})();
// ===== Glossar Link Tracking =====
document.addEventListener("click", function (e) {
  const link = e.target.closest("a.glossar-link");
  if (!link) return;

  const slug = new URL(link.href).searchParams.get("begriff");
  const from = window.location.pathname;

  // Optional: Google Analytics (gtag)
  if (window.gtag) {
    gtag("event", "glossar_click", {
      event_category: "Glossar",
      event_label: slug,
      value: 1,
      page_from: from
    });
  }

  // Optional: Log in Console (Debug)
  console.log(`Glossar Click → ${slug} (from ${from})`);
});
