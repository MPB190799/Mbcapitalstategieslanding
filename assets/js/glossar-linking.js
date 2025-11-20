document.addEventListener("DOMContentLoaded", async () => {

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
        ".blog-content",
        ".article-content",
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

    let html = target.innerHTML;

    // Bereits existierende Links schützen
    html = html.replace(/<a\b[^>]*>.*?<\/a>/gi, m =>
        m.replace(/</g, "§§LT§§").replace(/>/g, "§§GT§§")
    );

    // 3) Glossar-Begriffe verlinken
    for (const [term, anchor] of Object.entries(glossary)) {
        const safeTerm = term.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
        const regex = new RegExp(`\\b(${safeTerm})\\b`, "gi");

        html = html.replace(regex,
            `<a href="/glossar/#${anchor}" class="glossar-link">$1</a>`
        );
    }

    // Maskierung zurücksetzen
    html = html.replace(/§§LT§§/g, "<").replace(/§§GT§§/g, ">");

    // 4) Ausgabe
    target.innerHTML = html;

});

