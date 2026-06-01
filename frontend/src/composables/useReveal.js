import { nextTick, onMounted, onUnmounted } from "vue";

/**
 * Adds .is-visible when elements matching selector enter the viewport.
 */
export function useReveal(selector = ".reveal", options = {}) {
  let observer = null;

  onMounted(async () => {
    await nextTick();
    const elements = document.querySelectorAll(selector);
    if (!elements.length) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      elements.forEach((el) => el.classList.add("is-visible"));
      return;
    }

    observer = new IntersectionObserver(
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

  onUnmounted(() => {
    observer?.disconnect();
  });
}
