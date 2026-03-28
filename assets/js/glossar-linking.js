document.addEventListener("DOMContentLoaded", async () => {

    // Nicht auf Glossar-Seiten selbst ausführen
    if (window.location.pathname.startsWith('/glossar/')) return;

    // 1) JSON laden
    let glossary = {};
    try {
        const res = await fetch("/glossar/terms.json");
        glossary = await res.json();
    } catch (e) {
        console.error("Glossar konnte nicht geladen werden:", e);
        return;
    }

    // 2) Zielbereich suchen
    const selectors = [
        ".article-body",
        ".container",
        "main",
        ".post",
        ".content"
    ];

    let target = null;
    for (const s of selectors) {
        const el = document.querySelector(s);
        if (el) { target = el; break; }
    }
    if (!target) return;

    // 3) Glossar-Begriffe verlinken (nur in TextNodes, nie in <a> Tags)
    const walker = document.createTreeWalker(target, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
            // Skip text inside <a>, <script>, <style>, <code>, <pre> tags
            let parent = node.parentElement;
            while (parent && parent !== target) {
                const tag = parent.tagName.toLowerCase();
                if (tag === 'a' || tag === 'script' || tag === 'style' || tag === 'code' || tag === 'pre' || tag === 'button') {
                    return NodeFilter.FILTER_REJECT;
                }
                parent = parent.parentElement;
            }
            return NodeFilter.FILTER_ACCEPT;
        }
    });

    // Collect text nodes first (modifying during walk causes issues)
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) textNodes.push(node);

    // Sort terms by length (longest first) to avoid partial matches
    const sortedTerms = Object.entries(glossary).sort((a, b) => b[0].length - a[0].length);

    // Track linked terms to avoid duplicate links
    const linked = new Set();

    for (const textNode of textNodes) {
        let text = textNode.textContent;
        const parts = [];
        let lastIndex = 0;
        let modified = false;

        for (const [term, anchor] of sortedTerms) {
            if (linked.has(anchor)) continue;
            const safeTerm = term.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
            const regex = new RegExp(`\\b(${safeTerm})\\b`, "gi");
            let match;

            while ((match = regex.exec(text)) !== null) {
                if (match.index > lastIndex) {
                    parts.push(document.createTextNode(text.slice(lastIndex, match.index)));
                }
                const link = document.createElement('a');
                link.href = `/glossar/#${anchor}`;
                link.className = 'glossar-link';
                link.textContent = match[1];
                parts.push(link);
                lastIndex = match.index + match[0].length;
                linked.add(anchor);
                modified = true;
                break; // Only link first occurrence per term
            }
        }

        if (modified && parts.length > 0) {
            if (lastIndex < text.length) {
                parts.push(document.createTextNode(text.slice(lastIndex)));
            }
            const fragment = document.createDocumentFragment();
            parts.forEach(p => fragment.appendChild(p));
            textNode.parentNode.replaceChild(fragment, textNode);
        }
    }

});

