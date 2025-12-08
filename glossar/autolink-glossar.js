(async () => {
  const res = await fetch("/glossar/terms.json");
  const terms = await res.json();

  // Ziel: nur Content verlinken, keine Überschriften, keine Links überschreiben
  const content = document.querySelector(".blog-content");
  if (!content) return;

  let html = content.innerHTML;

  for (const [name, slug] of Object.entries(terms)) {
    const regex = new RegExp(`\\b${name}\\b`, "gi");
    const url = `/glossar/?begriff=${slug}`;

    html = html.replace(regex, `<a href="${url}" class="gl-link">${name}</a>`);
  }

  content.innerHTML = html;
})();
