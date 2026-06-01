<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import {
  parseStatValue,
  formatStatValue,
  animateStatValues,
} from "@/composables/useCountUp.js";

const props = defineProps({
  stats: { type: Array, required: true },
});

const sectionRef = ref(null);
const hasAnimated = ref(false);
let cancelAnimation = null;
let observer = null;

const parsedStats = computed(() => props.stats.map((s) => parseStatValue(s.value)));

const displays = ref(
  parsedStats.value.map((p) => formatStatValue(p, 0)),
);

function setFinalValues() {
  displays.value = props.stats.map((s) => s.value);
}

function runCountUp() {
  if (hasAnimated.value) return;
  hasAnimated.value = true;

  cancelAnimation?.();
  cancelAnimation = animateStatValues(parsedStats.value, {
    duration: 1800,
    onFrame: (values) => {
      displays.value = values;
    },
    onComplete: setFinalValues,
  });
}

onMounted(() => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setFinalValues();
    return;
  }

  observer = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return;
      runCountUp();
      observer?.disconnect();
    },
    { threshold: 0.25, rootMargin: "0px 0px -8% 0px" },
  );

  if (sectionRef.value) observer.observe(sectionRef.value);
});

onUnmounted(() => {
  observer?.disconnect();
  cancelAnimation?.();
});
</script>

<template>
  <section ref="sectionRef" class="stats section--tight">
    <div class="container stats__grid">
      <div v-for="(stat, i) in stats" :key="stat.label" class="stats__item">
        <span class="stats__value">{{ displays[i] }}</span>
        <span class="stats__label">{{ stat.label }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.stats {
  background: var(--btn-primary-gradient);
  color: #fff;
}

.stats__grid {
  display: grid;
  gap: 32px;
  text-align: center;
}

.stats__value {
  display: block;
  font-size: clamp(40px, 6vw, 56px);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.stats__label {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  opacity: 0.75;
}

@media (min-width: 640px) {
  .stats__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
