const STORAGE_KEY = "ur:scroll-positions";

/** Only restore on the first paint of a full page load / refresh — not after in-app navigations. */
let allowRestore = true;
let restoreRaf = 0;

function storagePath(path) {
  return path || `${window.location.pathname}${window.location.search}${window.location.hash}`;
}

function readAll() {
  try {
    return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeAll(all) {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(all));
  } catch {
    /* quota / private mode */
  }
}

export function getSavedScroll(path) {
  if (typeof window === "undefined") return null;
  const y = readAll()[storagePath(path)];
  return Number.isFinite(y) ? y : null;
}

export function saveScroll(path, y = window.scrollY) {
  if (typeof window === "undefined") return;
  const all = readAll();
  all[storagePath(path)] = Math.max(0, Math.round(y));
  writeAll(all);
}

export function disableScrollRestore() {
  allowRestore = false;
  if (restoreRaf) {
    cancelAnimationFrame(restoreRaf);
    restoreRaf = 0;
  }
}

export function restoreScrollInstant(y) {
  if (!Number.isFinite(y) || y <= 0) return;
  const maxScroll = Math.max(
    0,
    document.documentElement.scrollHeight - window.innerHeight,
  );
  window.scrollTo({ top: Math.min(y, maxScroll), left: 0, behavior: "instant" });
}

/**
 * Restore saved scroll after async layout settles.
 * Retries until the document is tall enough (or attempts run out) to avoid a mid-page hitch.
 */
export function scheduleScrollRestore(path) {
  if (typeof window === "undefined" || !allowRestore) return;

  const targetPath = storagePath(path);
  const y = getSavedScroll(targetPath);
  if (y == null || y < 1) return;

  if (restoreRaf) cancelAnimationFrame(restoreRaf);

  let attempts = 0;
  const maxAttempts = 90;

  const tick = () => {
    if (!allowRestore) {
      restoreRaf = 0;
      return;
    }
    // Path changed before restore finished (client nav) — abort.
    if (storagePath() !== targetPath) {
      restoreRaf = 0;
      return;
    }

    attempts += 1;
    const maxScroll = Math.max(
      0,
      document.documentElement.scrollHeight - window.innerHeight,
    );

    if (maxScroll >= y - 8 || attempts >= maxAttempts) {
      restoreScrollInstant(y);
      restoreRaf = 0;
      return;
    }

    restoreRaf = requestAnimationFrame(tick);
  };

  restoreRaf = requestAnimationFrame(tick);
}

export function initScrollRestoration(router) {
  if (typeof window === "undefined") return;

  history.scrollRestoration = "manual";

  let scrollTicking = false;
  const onScroll = () => {
    if (scrollTicking) return;
    scrollTicking = true;
    requestAnimationFrame(() => {
      scrollTicking = false;
      saveScroll();
    });
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("pagehide", () => saveScroll());

  router.afterEach((to, from) => {
    // Client-side route changes should start at top; refresh/initial keep restore enabled.
    if (from.matched.length) {
      disableScrollRestore();
      saveScroll(to.fullPath, 0);
    }
  });
}
