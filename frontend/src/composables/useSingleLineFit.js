import { nextTick, onBeforeUnmount, onMounted, watch } from "vue";

/* Headroom so sub-pixel rounding never tips a fitted label back onto two lines. */
const SAFETY = 0.98;
/* clientWidth is rounded, so a label that exactly fills its box can read ~0.5px over. */
const TOLERANCE_PX = 1;

/**
 * Keeps a group of labels on one line by shrinking them all by one shared factor.
 *
 * Writes the factor to `--fit-scale` on the root element. Labels matched by
 * `selector` must use `white-space: nowrap`, fill their box's width, and size
 * their font with `calc(<base size> * var(--fit-scale, 1))`.
 */
export function useSingleLineFit(rootRef, selector, { watchSource, minScale = 0.6 } = {}) {
  let resizeObserver = null;
  let frame = 0;

  function fit() {
    frame = 0;
    const root = rootRef.value;
    if (!root) return;

    root.style.setProperty("--fit-scale", "1");
    const range = document.createRange();
    let scale = 1;
    root.querySelectorAll(selector).forEach((label) => {
      range.selectNodeContents(label);
      const natural = range.getBoundingClientRect().width;
      const available = label.clientWidth;
      if (natural > 0 && available > 0 && natural > available + TOLERANCE_PX) {
        scale = Math.min(scale, (available * SAFETY) / natural);
      }
    });
    root.style.setProperty("--fit-scale", Math.max(minScale, scale).toFixed(3));
  }

  function schedule() {
    if (!frame && typeof requestAnimationFrame !== "undefined") {
      frame = requestAnimationFrame(fit);
    }
  }

  onMounted(() => {
    if (typeof ResizeObserver !== "undefined") {
      resizeObserver = new ResizeObserver(schedule);
      if (rootRef.value) resizeObserver.observe(rootRef.value);
    }
    schedule();
    /* A web font swapping in changes text width without resizing the root. */
    document.fonts?.ready.then(schedule);
    document.fonts?.addEventListener?.("loadingdone", schedule);
  });

  /* The root can mount late (v-if), so follow it rather than reading it once. */
  watch(
    rootRef,
    (el, prev) => {
      if (prev) resizeObserver?.unobserve(prev);
      if (el) resizeObserver?.observe(el);
      schedule();
    },
    { flush: "post" },
  );

  if (watchSource) {
    watch(watchSource, () => nextTick(schedule));
  }

  onBeforeUnmount(() => {
    document.fonts?.removeEventListener?.("loadingdone", schedule);
    resizeObserver?.disconnect();
    if (frame) cancelAnimationFrame(frame);
  });
}
