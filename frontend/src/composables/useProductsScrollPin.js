import { onMounted, onUnmounted, ref } from "vue";

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

const STICKY_TOP = 120;
/** Graphic transition only in the last fraction of each copy step scroll. */
const TRANSITION_FRACTION = 0.2;

/**
 * Juspay-style products pin: text scrolls per step; graphic holds until the
 * last lines of the current step, then the next graphic slides up.
 */
export function useProductsScrollPin(rootRef, itemCountRef) {
  const progress = ref(0);
  const activeIndex = ref(0);
  const stepProgress = ref(0);
  const isPinned = ref(false);
  const reducedMotion = ref(false);
  let frame = 0;
  let stepHeight = 0;

  function measure() {
    const root = rootRef.value;
    if (!root) return;

    const count = Math.max(itemCountRef.value, 1);
    const copyStep = root.querySelector(".home-products__copy-step");
    stepHeight =
      copyStep?.offsetHeight || Math.max(window.innerHeight - STICKY_TOP, 1);

    const rect = root.getBoundingClientRect();
    const viewport = window.innerHeight;
    const scrollRange = root.offsetHeight - (viewport - STICKY_TOP);

    if (scrollRange <= 0) {
      progress.value = 0;
      activeIndex.value = 0;
      stepProgress.value = 0;
      isPinned.value = false;
      return;
    }

    const scrolled = clamp(STICKY_TOP - rect.top, 0, scrollRange);
    const scaled = scrolled / stepHeight;
    const currentStep = Math.min(Math.floor(scaled), count - 1);
    const withinStep = scaled - currentStep;

    progress.value = scrolled / scrollRange;
    stepProgress.value = withinStep;
    isPinned.value = rect.top <= STICKY_TOP && rect.bottom > viewport;
    activeIndex.value = currentStep;
  }

  function scheduleMeasure() {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(measure);
  }

  onMounted(() => {
    reducedMotion.value = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    measure();
    window.addEventListener("scroll", scheduleMeasure, { passive: true });
    window.addEventListener("resize", scheduleMeasure);
  });

  onUnmounted(() => {
    cancelAnimationFrame(frame);
    window.removeEventListener("scroll", scheduleMeasure);
    window.removeEventListener("resize", scheduleMeasure);
  });

  function transitionT(withinStep) {
    const start = 1 - TRANSITION_FRACTION;
    if (withinStep <= start) return 0;
    return clamp((withinStep - start) / TRANSITION_FRACTION, 0, 1);
  }

  function slideOffset(index, count = 3) {
    if (reducedMotion.value) {
      return index === activeIndex.value ? 0 : 100;
    }

    const currentStep = activeIndex.value;
    const t = transitionT(stepProgress.value);

    if (index < currentStep) return -100;
    if (index > currentStep + 1) return 100;

    if (index === currentStep) {
      return currentStep >= count - 1 ? 0 : -t * 100;
    }

    if (index === currentStep + 1) {
      return (1 - t) * 100;
    }

    return 100;
  }

  function slideStyle(index, count = 3) {
    return {
      transform: `translate3d(0, ${slideOffset(index, count)}%, 0)`,
    };
  }

  function copyStyle(index, count = 3) {
    if (reducedMotion.value) {
      return {
        opacity: index === activeIndex.value ? 1 : 0.35,
        transform: "none",
      };
    }

    const currentStep = activeIndex.value;
    const t = transitionT(stepProgress.value);

    if (index === currentStep) {
      return {
        opacity: 1,
        transform: "none",
      };
    }

    if (index === currentStep + 1 && t > 0) {
      return {
        opacity: 0.35 + 0.65 * t,
        transform: `translate3d(0, ${(1 - t) * 24}px, 0)`,
      };
    }

    return {
      opacity: index < currentStep ? 0.18 : 0.35,
      transform: "none",
    };
  }

  return {
    progress,
    activeIndex,
    stepProgress,
    isPinned,
    reducedMotion,
    slideStyle,
    copyStyle,
    measure,
  };
}
