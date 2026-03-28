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

    // Track linked anchors to avoid duplicate links for same concept
    const linkedAnchors = new Set();
    // Track linked term strings to skip substrings of already-linked terms
    const linkedTerms = [];

    for (const textNode of textNodes) {
        const text = textNode.textContent;
        if (!text.trim()) continue;

        // Find all matches in this text node, longest terms first
        const matches = [];
        for (const [term, anchor] of sortedTerms) {
            if (linkedAnchors.has(anchor)) continue;
            const safeTerm = term.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
            const regex = new RegExp(`\\b(${safeTerm})\\b`, "gi");
            const match = regex.exec(text);
            if (match) {
                // Check if this match overlaps with an already-found longer match
                const start = match.index;
                const end = start + match[0].length;
                const overlaps = matches.some(m => !(end <= m.start || start >= m.end));
                if (!overlaps) {
                    matches.push({ start, end, text: match[1], anchor, term });
                }
            }
        }

        if (matches.length === 0) continue;

        // Sort matches by position in text
        matches.sort((a, b) => a.start - b.start);

        // Build replacement
        const fragment = document.createDocumentFragment();
        let lastIndex = 0;

        for (const m of matches) {
            if (m.start > lastIndex) {
                fragment.appendChild(document.createTextNode(text.slice(lastIndex, m.start)));
            }
            const link = document.createElement('a');
            link.href = `/glossar/#${m.anchor}`;
            link.className = 'glossar-link';
            link.textContent = m.text;
            fragment.appendChild(link);
            lastIndex = m.end;
            linkedAnchors.add(m.anchor);
            linkedTerms.push(m.term.toLowerCase());
        }

        if (lastIndex < text.length) {
            fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
        }

        textNode.parentNode.replaceChild(fragment, textNode);
    }

});

