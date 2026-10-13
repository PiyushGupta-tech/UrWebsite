import { onBeforeUnmount, ref, watch } from "vue";

/**
 * Track position for a one-card-at-a-time slider whose last card is followed by a
 * clone of the first, so wrapping slides one card instead of rewinding the row.
 * `slide` runs 0..count (count = the clone); `snapping` disables the transition while
 * the track jumps between the clone and the real first card.
 */
export function useLoopSlider(activeIndex, count, durationMs = 450) {
  const slide = ref(activeIndex.value);
  const snapping = ref(false);
  let snapTimer = null;

  function clearSnapTimer() {
    if (snapTimer) clearTimeout(snapTimer);
    snapTimer = null;
  }

  function snapTo(index, then) {
    snapping.value = true;
    slide.value = index;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        snapping.value = false;
        then?.();
      });
    });
  }

  function settleClone() {
    clearSnapTimer();
    if (slide.value === count.value) snapTo(0);
  }

  watch(activeIndex, (next, prev) => {
    clearSnapTimer();
    const total = count.value;
    if (total > 2 && prev === total - 1 && next === 0) {
      slide.value = total;
      // transitionend never fires without a transition (reduced motion, desktop layout).
      snapTimer = setTimeout(settleClone, durationMs + 100);
    } else if (total > 2 && prev === 0 && next === total - 1) {
      snapTo(total, () => {
        slide.value = activeIndex.value;
      });
    } else if (slide.value === total) {
      // Still parked on the clone: jump to the real first card before moving on.
      snapTo(0, () => {
        slide.value = activeIndex.value;
      });
    } else {
      slide.value = next;
    }
  });

  function onTrackTransitionEnd(event) {
    if (event.target !== event.currentTarget || event.propertyName !== "transform") return;
    settleClone();
  }

  onBeforeUnmount(clearSnapTimer);

  return { slide, snapping, onTrackTransitionEnd };
}
