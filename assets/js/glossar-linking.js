document.addEventListener("DOMContentLoaded", () => {

    // 🔥 1. Begriffe aus deinem Glossar
    const terms = {
        "Dividende": "dividende",
        "Dividendenrendite": "dividendenrendite",
        "Yield on Cost": "yield-on-cost",
        "Ausschüttungsquote": "payout-ratio",
        "BDC": "bdc",
        "Cashflow": "cashflow",
        "Free Cashflow": "free-cashflow",
        "Diversifikation": "diversifikation",
        "Ex-Dividenden-Tag": "ex-dividenden-tag",
        "Hard Assets": "hard-assets",
        "LNG": "lng",
        "Midstream": "midstream",
        "Pipeline": "midstream",
        "NAV": "nav",
        "REIT": "reit",
        "Margin of Safety": "margin-of-safety",
        "Rohstoffzyklus": "rohstoffzyklus",
        "Shipping-Zyklus": "shipping-zyklus",
        "Value Trap": "value-trap",
        "Withholding Tax": "withholding-tax",
        "Quellensteuer": "withholding-tax",
        "Toolbox": "toolbox"
    };

    // 🔥 2. Wo soll verlinkt werden?
    const contentSelectors = [
        ".blog-content",
        ".article-content",
        "main",
        ".post",
        ".content"
    ];

    let targetElement = null;

    for (const sel of contentSelectors) {
        const el = document.querySelector(sel);
        if (el) {
            targetElement = el;
            break;
        }
    }

    if (!targetElement) return;

    let html = targetElement.innerHTML;

    // 🔥 3. Begriffe einmal verlinken
    for (const [word, anchor] of Object.entries(terms)) {

        const regex = new RegExp(`\\b(${word})\\b`, "i");

        html = html.replace(regex, `<a href="/glossar/#${anchor}" class="glossar-link">$1</a>`);
    }

    targetElement.innerHTML = html;

});
