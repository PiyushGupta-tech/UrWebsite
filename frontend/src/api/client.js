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

function parseSseBlock(block) {
  let event = "message";
  const dataLines = [];
  for (const line of block.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
  }
  if (!dataLines.length) return null;
  try {
    return { event, data: JSON.parse(dataLines.join("\n")) };
  } catch {
    return null;
  }
}

/**
 * Send a chat message and receive the reply as server-sent events.
 * onEvent(name, data) fires for "meta", "delta", and "done".
 */
export async function streamChat({ message, conversationId, pagePath, language, signal, onEvent }) {
  const res = await fetch(`${API_BASE}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify({
      message,
      conversation_id: conversationId || undefined,
      page_path: pagePath || undefined,
      language: language || undefined,
    }),
    signal,
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const err = new Error(data.detail || `API error: ${res.status}`);
    err.status = res.status;
    err.code = data.code || "";
    throw err;
  }

  const emitBlocks = (text) => {
    const blocks = text.split("\n\n");
    const rest = blocks.pop();
    for (const block of blocks) {
      const parsed = parseSseBlock(block);
      if (parsed) onEvent(parsed.event, parsed.data);
    }
    return rest;
  };

  if (!res.body?.getReader) {
    emitBlocks(`${await res.text()}\n\n`);
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer = emitBlocks(buffer + decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n"));
  }
  emitBlocks(`${buffer}${decoder.decode()}\n\n`);
}

export async function submitChatLead(payload) {
  const res = await fetch(`${API_BASE}/chat/lead/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || `API error: ${res.status}`);
    err.status = res.status;
    err.fieldErrors = data.errors || {};
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
    err.fieldErrors = data.errors || {};
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

export function fetchAdminChats({ filter = "all", page = 1 } = {}) {
  const params = new URLSearchParams({ filter, page: String(page) });
  return adminFetch(`/admin/chats/?${params}`);
}

export function fetchAdminChat(id) {
  return adminFetch(`/admin/chats/${encodeURIComponent(id)}/`);
}
