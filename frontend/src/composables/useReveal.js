import { nextTick, onMounted, onUnmounted, ref } from "vue";

/**
 * MagicPost-style scroll reveal: fade + translateY when elements enter the viewport.
 * Adds `visibleClass` (default `is-in`) once; pairs with CSS on `rootClass` (default `reveal-on`).
 */
export function useScrollReveal(
  rootRef,
  selector = "[data-reveal]",
  options = {},
) {
  const {
    visibleClass = "is-in",
    rootClass = "reveal-on",
    threshold = 0.15,
    rootMargin = "0px 0px -60px 0px",
  } = options;

  const revealEnabled = ref(false);
  let observer = null;

  onMounted(async () => {
    await nextTick();
    const root = rootRef.value;
    if (!root) return;

    const elements = root.querySelectorAll(selector);
    if (!elements.length) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      elements.forEach((el) => el.classList.add(visibleClass));
      return;
    }

    if (!("IntersectionObserver" in window)) {
      elements.forEach((el) => el.classList.add(visibleClass));
      return;
    }

    revealEnabled.value = true;
    root.classList.add(rootClass);

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add(visibleClass);
          observer.unobserve(entry.target);
        });
      },
      { threshold, rootMargin },
    );

    elements.forEach((el) => observer.observe(el));
  });

  onUnmounted(() => {
    observer?.disconnect();
    rootRef.value?.classList.remove(rootClass);
  });

  return { revealEnabled };
}

/** @deprecated Use useScrollReveal */
export function useReveal(selector = ".reveal", options = {}) {
  const rootRef = ref(null);

  onMounted(async () => {
    await nextTick();
    const elements = document.querySelectorAll(selector);
    if (!elements.length) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      elements.forEach((el) => el.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12,
        rootMargin: "0px 0px -6% 0px",
        ...options,
      },
    );

    elements.forEach((el) => observer.observe(el));
  });

  return { rootRef };
}
