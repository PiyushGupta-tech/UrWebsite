import { computed, onBeforeUnmount, onMounted, ref } from "vue";

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

/**
 * Looping "count up + draw chart" cycle used by rate cards.
 * Timeline per cycle: draw/count → hold → fade out → blank → fade in at 0.
 * chartOffset runs 1 → 0 for a pathLength="1" dash reveal.
 */
export function useRateCycle(
  target,
  { cycleMs = 3000, drawRatio = 0.55, decimals = 2, prefix = "" } = {},
) {
  const displayRate = ref(0);
  const rateOpacity = ref(1);
  const chartOffset = ref(1);
  const chartOpacity = ref(1);
  let rafId = 0;
  let cycleStart = 0;

  const rateLabel = computed(() => `${prefix}${displayRate.value.toFixed(decimals)}%`);

  function setFinal() {
    displayRate.value = target;
    rateOpacity.value = 1;
    chartOffset.value = 0;
    chartOpacity.value = 1;
  }

  function tick(now) {
    if (!cycleStart) cycleStart = now;
    const t = ((now - cycleStart) % cycleMs) / cycleMs;

    if (t < drawRatio) {
      const p = easeInOut(t / drawRatio);
      displayRate.value = target * p;
      chartOffset.value = 1 - p;
      rateOpacity.value = 1;
      chartOpacity.value = 1;
    } else if (t < 0.72) {
      setFinal();
    } else if (t < 0.88) {
      displayRate.value = target;
      chartOffset.value = 0;
      const fade = 1 - (t - 0.72) / (0.88 - 0.72);
      rateOpacity.value = fade;
      chartOpacity.value = fade;
    } else if (t < 0.89) {
      displayRate.value = 0;
      chartOffset.value = 1;
      rateOpacity.value = 0;
      chartOpacity.value = 0;
    } else {
      displayRate.value = 0;
      chartOffset.value = 1;
      const show = (t - 0.89) / (1 - 0.89);
      rateOpacity.value = show;
      chartOpacity.value = show;
    }

    rafId = window.requestAnimationFrame(tick);
  }

  function stop() {
    if (rafId) {
      window.cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  function start() {
    stop();
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) {
      setFinal();
      return;
    }
    cycleStart = 0;
    rafId = window.requestAnimationFrame(tick);
  }

  onMounted(start);
  onBeforeUnmount(stop);

  return { rateLabel, rateOpacity, chartOffset, chartOpacity };
}
