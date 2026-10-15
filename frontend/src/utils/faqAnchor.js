/** Element id of an FAQ question; must match faq_anchor() in backend/website/knowledge.py. */
export function faqAnchor(question) {
  const slug = String(question || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
  return `faq-${slug}`;
}
