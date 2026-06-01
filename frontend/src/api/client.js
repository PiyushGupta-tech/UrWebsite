const API_BASE = import.meta.env.VITE_API_BASE || "/api";

async function getJson(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const err = new Error(`API error: ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

export function fetchSite() {
  return getJson("/site/");
}

export function fetchHomepage() {
  return getJson("/homepage/");
}

export function fetchPage(slug) {
  return getJson(`/pages/${slug}/`);
}

export async function submitChat(message) {
  const res = await fetch(`${API_BASE}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || `API error: ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}

export async function submitContactForm(payload) {
  const res = await fetch(`${API_BASE}/contact/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || `API error: ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}
