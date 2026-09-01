const API_BASE = import.meta.env.VITE_API_BASE || "/api";

function getCsrfToken() {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

async function adminFetch(path, options = {}) {
  const headers = {
    Accept: "application/json",
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.method && options.method !== "GET" ? { "X-CSRFToken": getCsrfToken() } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    ...options,
    headers,
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(
      data.detail
        || (res.status === 403 ? "Session expired. Refresh the page and try again." : `API error: ${res.status}`),
    );
    err.status = res.status;
    throw err;
  }
  return data;
}

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

export function fetchAdminMe() {
  return adminFetch("/admin/me/");
}

export function adminLogin(username, password) {
  return adminFetch("/admin/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function adminLogout() {
  return adminFetch("/admin/logout/", { method: "POST" });
}

export function fetchPayoutDashboard() {
  return adminFetch("/admin/payout-dashboard/");
}

export function fetchPayinDashboard() {
  return adminFetch("/admin/payin-dashboard/");
}
