import { onMounted, onUnmounted, ref } from "vue";

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

const STICKY_TOP = 120;
/** Graphic transition in the last fraction of each (now longer) copy step. */
const TRANSITION_FRACTION = 0.28;

function easeInOutCubic(t) {
  return t < 0.5
    ? 4 * t * t * t
    : 1 - ((-2 * t + 2) ** 3) / 2;
}

/**
 * Juspay-style products pin: left copy steps scroll naturally; right media
 * stays sticky and slides to the next graphic near the end of each step.
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
    const scrollRange = Math.max(root.offsetHeight - (viewport - STICKY_TOP), 1);

    const scrolled = clamp(STICKY_TOP - rect.top, 0, scrollRange);
    const scaled = scrolled / stepHeight;
    const currentStep = Math.min(Math.floor(scaled), count - 1);
    const withinStep = clamp(scaled - currentStep, 0, 1);

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
    const raw = clamp((withinStep - start) / TRANSITION_FRACTION, 0, 1);
    return easeInOutCubic(raw);
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
    const offset = slideOffset(index, count);
    const distance = Math.min(Math.abs(offset), 100);
    const visibility = 1 - distance / 100;

    return {
      transform: `translate3d(0, ${offset}%, 0) scale(${0.985 + visibility * 0.015})`,
      opacity: 0.22 + visibility * 0.78,
      zIndex: index + 1,
    };
  }

  return {
    progress,
    activeIndex,
    stepProgress,
    isPinned,
    reducedMotion,
    slideStyle,
    measure,
  };
}
