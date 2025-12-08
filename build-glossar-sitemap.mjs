import { readFileSync, writeFileSync } from "fs";

const raw = readFileSync("./glossar/terms.json", "utf8");

// Kommentare entfernen + zu gültigem JSON machen
const clean = raw
  .replace(/\/\*[\s\S]*?\*\*/g, "")
  .replace(/\/\*[\s\S]*?\*\//g, "")
  .replace(/,\s*}/g, "}");

const terms = JSON.parse(clean);

// Slugs sammeln und doppelte entfernen
const base = "https://mbcapitalstrategies.com/glossar/?begriff=";
const urls = Array.from(new Set(Object.values(terms).map((s) => base + s)));

const lines = [];
lines.push(`<?xml version="1.0" encoding="UTF-8"?>`);
lines.push(`<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`);
for (const u of urls.sort()) {
  lines.push(`  <url><loc>${u}</loc></url>`);
}
lines.push(`</urlset>`);

writeFileSync("./glossar-sitemap.xml", lines.join("\n"), "utf8");
console.log("✅ glossar-sitemap.xml erzeugt. URLs:", urls.length);
