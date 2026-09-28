/** Apply page SEO to document head (title, description, keywords, OG/Twitter, canonical). */

function setMeta(attr, key, value) {
  if (!value) return;
  let el = document.querySelector(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement("meta");
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute("content", value);
}

function setOrRemoveMeta(attr, key, value) {
  if (value) {
    setMeta(attr, key, value);
    return;
  }
  document.querySelector(`meta[${attr}="${key}"]`)?.remove();
}

function setCanonical(href) {
  if (!href) return;
  let el = document.querySelector('link[rel="canonical"]');
  if (!el) {
    el = document.createElement("link");
    el.setAttribute("rel", "canonical");
    document.head.appendChild(el);
  }
  el.setAttribute("href", href);
}

const STRUCTURED_DATA_ID = "urbanrupee-structured-data";

function removeStructuredData() {
  const existing = document.getElementById(STRUCTURED_DATA_ID);
  if (existing) existing.remove();
}

export function applyStructuredData(graph) {
  removeStructuredData();
  if (!graph?.length) return;
  const script = document.createElement("script");
  script.id = STRUCTURED_DATA_ID;
  script.type = "application/ld+json";
  script.textContent = JSON.stringify({
    "@context": "https://schema.org",
    "@graph": graph,
  });
  document.head.appendChild(script);
}

export function applySeo(seo, structuredData) {
  if (!seo) return;
  if (seo.title) document.title = seo.title;
  setMeta("name", "description", seo.description);
  setOrRemoveMeta("name", "keywords", seo.keywords);
  setMeta("property", "og:title", seo.title);
  setMeta("property", "og:description", seo.description);
  setMeta("name", "twitter:title", seo.title);
  setMeta("name", "twitter:description", seo.description);
  if (seo.canonical) {
    setMeta("property", "og:url", seo.canonical);
    setCanonical(seo.canonical);
  }
  if (structuredData) {
    applyStructuredData(structuredData);
  }
}
