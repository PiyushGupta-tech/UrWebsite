<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import {
  animateStatValues,
  formatStatValue,
  parseStatValue,
} from "@/composables/useCountUp.js";

const props = defineProps({
  items: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: "Performance metrics" },
  /** When false, cards stay hidden until set true (hero entrance). */
  ready: { type: Boolean, default: true },
  /** Count-up duration in ms when the strip enters view. */
  duration: { type: Number, default: 1800 },
});

const rootRef = ref(null);
const displays = ref([]);
let observer = null;
let cancelAnimation = null;
let hasAnimated = false;

const parsed = computed(() =>
  props.items.map((stat) => parseStatValue(stat.value)),
);

function setFinalValues() {
  displays.value = props.items.map((stat) => stat.value);
}

function resetValues() {
  displays.value = parsed.value.map((p) => formatStatValue(p, 0));
}

function runCountUp() {
  cancelAnimation?.();
  if (!parsed.value.length) return;
  cancelAnimation = animateStatValues(parsed.value, {
    duration: props.duration,
    onFrame: (values) => {
      displays.value = values;
    },
    onComplete: setFinalValues,
  });
}

function prefersReducedMotion() {
  return (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
}

function setupObserver() {
  observer?.disconnect();
  observer = null;
  cancelAnimation?.();
  cancelAnimation = null;
  hasAnimated = false;

  if (!props.items.length) {
    displays.value = [];
    return;
  }

  if (prefersReducedMotion()) {
    setFinalValues();
    hasAnimated = true;
    return;
  }

  resetValues();

  if (typeof IntersectionObserver === "undefined") {
    setFinalValues();
    return;
  }

  observer = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting || hasAnimated) return;
      hasAnimated = true;
      runCountUp();
      observer?.disconnect();
      observer = null;
    },
    { threshold: 0.25, rootMargin: "0px 0px -8% 0px" },
  );

  if (rootRef.value) observer.observe(rootRef.value);
}

onMounted(() => {
  nextTick(setupObserver);
});

onBeforeUnmount(() => {
  observer?.disconnect();
  cancelAnimation?.();
});

watch(
  () => props.items.map((s) => `${s.label}:${s.value}`).join("|"),
  async () => {
    await nextTick();
    setupObserver();
  },
);
</script>

<template>
  <div
    v-if="items.length"
    ref="rootRef"
    class="ur-metrics"
    :class="{ 'ur-metrics--ready': ready }"
    :aria-label="ariaLabel"
  >
    <article
      v-for="(stat, index) in items"
      :key="stat.label"
      class="ur-metrics__card"
    >
      <p class="ur-metrics__value">
        {{ displays[index] ?? stat.value }}
      </p>
      <p class="ur-metrics__label">{{ stat.label }}</p>
    </article>
  </div>
</template>

<style scoped>
/* Shared metric strip — Collections Figma card treatment + count-up */
.ur-metrics {
  display: flex;
  align-items: stretch;
  gap: 52px;
  width: 100%;
  max-width: 1208px;
  margin-inline: auto;
  box-sizing: border-box;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.6s ease 0.12s,
    transform 0.6s ease 0.12s;
}

.ur-metrics--ready {
  opacity: 1;
  transform: none;
}

.ur-metrics__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex: 1 1 0;
  min-width: 0;
  height: 174px;
  padding: 20px 16px;
  box-sizing: border-box;
  background: #ffffff;
  border: 1px solid #e9eaeb;
  border-radius: 14.141px;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.1),
    0 1px 2px -1px rgba(0, 0, 0, 0.1);
}

.ur-metrics__value {
  margin: 0;
  min-height: 72px;
  font-size: 64px;
  font-weight: 600;
  line-height: 72px;
  letter-spacing: -1.92px;
  text-align: center;
  color: #181d27;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.ur-metrics__label {
  margin: 0;
  max-width: 185px;
  font-size: 20px;
  font-weight: 600;
  line-height: 32px;
  letter-spacing: -0.6px;
  text-align: center;
  color: #414651;
}

@media (max-width: 1100px) {
  .ur-metrics {
    gap: 20px;
  }

  .ur-metrics__value {
    font-size: 48px;
    line-height: 56px;
    min-height: 56px;
  }

  .ur-metrics__label {
    font-size: 16px;
    line-height: 24px;
  }
}

@media (max-width: 768px) {
  .ur-metrics {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  .ur-metrics__card {
    height: auto;
    min-height: 140px;
  }

  .ur-metrics__value {
    font-size: 40px;
    line-height: 48px;
    min-height: 48px;
  }

  .ur-metrics__label {
    font-size: 15px;
    line-height: 22px;
  }
}
</style>
