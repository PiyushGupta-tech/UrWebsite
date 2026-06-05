<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import BrandLogo from "./BrandLogo.vue";

const props = defineProps({
  dashboard: { type: Object, required: true },
  tilted: { type: Boolean, default: true },
  logoPlaceholder: { type: Boolean, default: false },
  themeBreathe: { type: Boolean, default: false },
});

const ROTATE_MS = props.dashboard.rotate_interval_ms || 5000;

const periods = computed(() => props.dashboard.periods || []);
const activePeriod = ref(props.dashboard.default_period || "This Month");
const chartView = ref("Line");
const activeNav = ref("In Ledger");
const isAnimating = ref(false);

let rotateTimer = null;
let animTimer = null;
let resumeTimer = null;
let userPaused = false;

const periodTitles = computed(() => props.dashboard.period_titles || {});

const periodSnapshots = computed(
  () => props.dashboard.period_snapshots || {},
);

const activeSnapshot = computed(
  () => periodSnapshots.value[activePeriod.value] || null,
);

const activeStats = computed(() => {
  if (activeSnapshot.value?.stats) return activeSnapshot.value.stats;
  return props.dashboard.stats || [];
});

const analyticsTitle = computed(
  () =>
    periodTitles.value[activePeriod.value] ||
    props.dashboard.title ||
    "Payin Analytics",
);

const statusDistribution = computed(() => {
  if (activeSnapshot.value?.status_distribution) {
    return activeSnapshot.value.status_distribution;
  }
  return props.dashboard.status_distribution || [];
});

/** Trend lines: success line tracks closer to total as success rate rises (70–78%). */
const chartPaths = {
  Today: {
    amt: "M0,95 L40,82 L80,88 L120,72 L160,78 L200,65 L240,70 L280,58 L320,62 L320,120 L0,120 Z",
    ok: "M0,100 L40,92 L80,96 L120,84 L160,88 L200,78 L240,82 L280,76 L320,78 L320,120 L0,120 Z",
    total: "0,96 40,84 80,90 120,74 160,80 200,68 240,72 280,60 320,64",
    success: "0,102 40,94 80,98 120,86 160,90 200,80 240,84 280,78 320,80",
    amount: "0,92 40,80 80,86 120,70 160,76 200,62 240,68 280,56 320,60",
  },
  Yesterday: {
    amt: "M0,92 L40,78 L80,86 L120,68 L160,74 L200,58 L240,64 L280,52 L320,56 L320,120 L0,120 Z",
    ok: "M0,98 L40,88 L80,92 L120,78 L160,82 L200,70 L240,74 L280,66 L320,68 L320,120 L0,120 Z",
    total: "0,94 40,80 80,88 120,70 160,76 200,60 240,66 280,54 320,58",
    success: "0,100 40,90 80,94 120,80 160,84 200,72 240,76 280,68 320,70",
    amount: "0,90 40,76 80,84 120,66 160,72 200,56 240,62 280,50 320,54",
  },
  "This Week": {
    amt: "M0,88 L40,70 L80,82 L120,48 L160,58 L200,38 L240,48 L280,28 L320,38 L320,120 L0,120 Z",
    ok: "M0,94 L40,82 L80,90 L120,62 L160,70 L200,52 L240,62 L280,46 L320,50 L320,120 L0,120 Z",
    total: "0,88 40,72 80,82 120,48 160,58 200,38 240,52 280,28 320,40",
    success: "0,94 40,80 80,88 120,60 160,68 200,50 240,60 280,44 320,48",
    amount: "0,85 40,68 80,80 120,42 160,52 200,32 240,48 280,22 320,38",
  },
  "This Month": {
    amt: "M0,90 L40,70 L80,85 L120,40 L160,55 L200,30 L240,50 L280,20 L320,35 L320,120 L0,120 Z",
    ok: "M0,93 L40,78 L80,88 L120,56 L160,66 L200,46 L240,60 L280,40 L320,48 L320,120 L0,120 Z",
    total: "0,88 40,72 80,82 120,48 160,58 200,38 240,52 280,28 320,40",
    success: "0,93 40,76 80,86 120,54 160,64 200,44 240,58 280,38 320,46",
    amount: "0,85 40,68 80,80 120,42 160,52 200,32 240,48 280,22 320,38",
  },
  "This Year": {
    amt: "M0,86 L40,62 L80,78 L120,32 L160,44 L200,22 L240,36 L280,14 L320,26 L320,120 L0,120 Z",
    ok: "M0,90 L40,74 L80,84 L120,50 L160,58 L200,40 L240,52 L280,36 L320,42 L320,120 L0,120 Z",
    total: "0,84 40,64 80,76 120,36 160,48 200,26 240,40 280,18 320,30",
    success: "0,89 40,72 80,82 120,48 160,56 200,38 240,48 280,34 320,40",
    amount: "0,82 40,60 80,74 120,30 160,42 200,20 240,34 280,12 320,24",
  },
  All: {
    amt: "M0,84 L40,58 L80,74 L120,28 L160,40 L200,18 L240,32 L280,10 L320,20 L320,120 L0,120 Z",
    ok: "M0,87 L40,70 L80,80 L120,46 L160,54 L200,36 L240,48 L280,32 L320,38 L320,120 L0,120 Z",
    total: "0,82 40,60 80,72 120,32 160,42 200,22 240,36 280,16 320,26",
    success: "0,86 40,68 80,78 120,44 160,52 200,34 240,44 280,30 320,36",
    amount: "0,80 40,56 80,70 120,26 160,38 200,16 240,30 280,8 320,18",
  },
};

const activeChart = computed(() => {
  const snap = activeSnapshot.value;
  if (snap?.chart) return snap.chart;
  return chartPaths[activePeriod.value] || chartPaths["This Month"];
});

const donutStyle = computed(() => {
  const items = statusDistribution.value;
  let acc = 0;
  const stops = items.map((item) => {
    const start = acc;
    acc += item.percent;
    return `${item.color} ${start}% ${acc}%`;
  });
  return { background: `conic-gradient(${stops.join(", ")})` };
});

function playPeriodTransition() {
  isAnimating.value = false;
  clearTimeout(animTimer);
  requestAnimationFrame(() => {
    isAnimating.value = true;
    animTimer = setTimeout(() => {
      isAnimating.value = false;
    }, 360);
  });
}

function nextPeriodIndex(current) {
  const list = periods.value;
  if (!list.length) return 0;
  return (list.indexOf(current) + 1) % list.length;
}

function setPeriod(period, { manual = false } = {}) {
  if (!periods.value.includes(period) || period === activePeriod.value) return;
  activePeriod.value = period;
  playPeriodTransition();
  if (manual) scheduleRotation();
}

function scheduleRotation() {
  clearInterval(rotateTimer);
  if (userPaused || periods.value.length < 2) return;
  rotateTimer = setInterval(() => {
    if (userPaused) return;
    setPeriod(periods.value[nextPeriodIndex(activePeriod.value)]);
  }, ROTATE_MS);
}

function selectPeriod(p) {
  setPeriod(p, { manual: true });
}

function onPointerEnter() {
  userPaused = true;
  clearInterval(rotateTimer);
}

function onPointerLeave() {
  userPaused = false;
  clearTimeout(resumeTimer);
  resumeTimer = setTimeout(scheduleRotation, 400);
}

function selectChart(v) {
  chartView.value = v;
}

function selectNav(label) {
  activeNav.value = label;
}

onMounted(() => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  scheduleRotation();
});

onUnmounted(() => {
  clearInterval(rotateTimer);
  clearTimeout(animTimer);
  clearTimeout(resumeTimer);
});

watch(
  () => props.dashboard.default_period,
  (p) => {
    if (p && periods.value.includes(p)) activePeriod.value = p;
  },
);
</script>

<template>
  <article
    class="dash"
    :class="{
      'dash--tilted': tilted,
      'dash--theme-breathe': themeBreathe,
    }"
    role="region"
    aria-label="Urbanrupee dashboard preview"
    @pointerenter="onPointerEnter"
    @pointerleave="onPointerLeave"
  >
    <div v-if="themeBreathe" class="dash__mesh" aria-hidden="true">
      <span class="dash__orb dash__orb--cyan" />
      <span class="dash__orb dash__orb--violet" />
      <span class="dash__orb dash__orb--pink" />
    </div>

    <header class="dash__bar">
      <div class="dash__bar-brand">
        <span v-if="logoPlaceholder" class="dash__logo-placeholder">your logo</span>
        <BrandLogo
          v-else
          variant="on-dark"
          alt="Urbanrupee"
          class="dash__brand-logo"
        />
      </div>
      <span class="dash__avatar" aria-hidden="true" />
    </header>

    <div class="dash__body">
      <aside class="dash__sidebar">
        <button type="button" class="dash__collapse" aria-label="Collapse menu">«</button>
        <nav class="dash__nav">
          <template v-for="(group, gi) in dashboard.sidebar" :key="gi">
            <p v-if="group.section" class="dash__nav-section">{{ group.section }}</p>
            <button
              v-for="item in group.items"
              :key="item.label"
              type="button"
              class="dash__nav-item"
              :class="{ 'dash__nav-item--active': activeNav === item.label }"
              @click="selectNav(item.label)"
            >
              <span class="dash__nav-dot" />
              {{ item.label }}
            </button>
          </template>
        </nav>
      </aside>

      <main class="dash__main">
        <div class="dash__analytics-bar">
          <p class="dash__analytics-title">{{ analyticsTitle }}</p>
          <div class="dash__periods" role="tablist" aria-label="Analytics period">
            <button
              v-for="p in periods"
              :key="p"
              type="button"
              role="tab"
              class="dash__period"
              :class="{ 'dash__period--active': activePeriod === p }"
              :aria-selected="activePeriod === p"
              @click="selectPeriod(p)"
            >
              {{ p }}
            </button>
          </div>
        </div>

        <div
          class="dash__metrics"
          :class="{ 'dash__metrics--animating': isAnimating }"
          aria-live="polite"
          aria-atomic="true"
        >
          <div class="dash__stats">
            <div
              v-for="stat in activeStats"
              :key="`${activePeriod}-${stat.label}`"
              class="dash__stat"
              :class="`dash__stat--${stat.variant}`"
            >
              <span class="dash__stat-label">{{ stat.label }}</span>
              <strong class="dash__stat-value">{{ stat.value }}</strong>
              <span class="dash__stat-sub">{{ stat.sub }}</span>
            </div>
          </div>

          <div class="dash__charts">
            <section class="dash__chart-card">
              <header class="dash__chart-head">
                <span>Transaction Trends</span>
                <div class="dash__chart-tabs">
                  <button
                    v-for="v in dashboard.chart_views"
                    :key="v"
                    type="button"
                    :class="{ active: chartView === v }"
                    @click="selectChart(v)"
                  >
                    {{ v }}
                  </button>
                </div>
              </header>
              <div class="dash__line-chart" :data-view="chartView">
                <svg
                  viewBox="0 0 320 120"
                  preserveAspectRatio="none"
                  aria-hidden="true"
                >
                  <defs>
                    <linearGradient id="dashAmtFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#f97316" stop-opacity="0.35" />
                      <stop offset="100%" stop-color="#f97316" stop-opacity="0" />
                    </linearGradient>
                    <linearGradient id="dashOkFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#22c55e" stop-opacity="0.3" />
                      <stop offset="100%" stop-color="#22c55e" stop-opacity="0" />
                    </linearGradient>
                  </defs>
                  <path fill="url(#dashAmtFill)" :d="activeChart.amt" />
                  <path fill="url(#dashOkFill)" :d="activeChart.ok" />
                  <polyline
                    fill="none"
                    stroke="#3b82f6"
                    stroke-width="2"
                    :points="activeChart.total"
                  />
                  <polyline
                    fill="none"
                    stroke="#22c55e"
                    stroke-width="2"
                    :points="activeChart.success"
                  />
                  <polyline
                    fill="none"
                    stroke="#f97316"
                    stroke-width="2"
                    :points="activeChart.amount"
                  />
                </svg>
                <div class="dash__chart-legend">
                  <span><i class="c-total" /> Total</span>
                  <span><i class="c-ok" /> Successful</span>
                  <span><i class="c-amt" /> Amount</span>
                </div>
              </div>
            </section>

            <section class="dash__chart-card dash__chart-card--donut">
              <header class="dash__chart-head">
                <span>Status Distribution</span>
              </header>
              <div class="dash__donut-wrap">
                <div class="dash__donut" :style="donutStyle">
                  <div class="dash__donut-hole" />
                </div>
                <ul class="dash__donut-legend">
                  <li v-for="item in statusDistribution" :key="item.label">
                    <span :style="{ background: item.color }" />
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  </article>
</template>

<style scoped>
.dash {
  --dash-sidebar: #1e293b;
  --dash-bar: #0f172a;
  --dash-bg: #f1f5f9;
  --dash-card: #ffffff;
  --dash-text: #0f172a;
  --dash-muted: #475569;

  position: relative;
  width: min(100%, 520px);
  min-height: 400px;
  border-radius: 14px;
  overflow: hidden;
  background: var(--dash-bg);
  border: 1px solid #e2e8f0;
  box-shadow:
    0 24px 48px rgba(15, 23, 42, 0.18),
    0 0 0 1px rgba(0, 0, 0, 0.04);
  font-size: 11px;
  color: var(--dash-text);
}

.dash--theme-breathe {
  border: 2px solid transparent;
  background-image:
    linear-gradient(#f1f5f9, #f1f5f9),
    linear-gradient(
      90deg,
      #22d3ee,
      #818cf8,
      #c084fc,
      #f472b6,
      #fb923c,
      #22d3ee
    );
  background-origin: border-box;
  background-clip: padding-box, border-box;
  background-size:
    100% 100%,
    320% 100%;
  animation: dash-border-flow 5s linear infinite;
  box-shadow:
    0 28px 56px rgba(15, 23, 42, 0.22),
    0 0 40px rgba(34, 211, 238, 0.12),
    0 0 64px rgba(244, 114, 182, 0.08);
}

.dash__mesh {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.dash__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(48px);
  opacity: 0.45;
  mix-blend-mode: multiply;
}

.dash__orb--cyan {
  width: 50%;
  height: 45%;
  background: #22d3ee;
  top: -12%;
  left: -10%;
  animation: dash-orb-a 10s ease-in-out infinite;
}

.dash__orb--violet {
  width: 45%;
  height: 48%;
  background: #a78bfa;
  bottom: -8%;
  right: -12%;
  animation: dash-orb-b 12s ease-in-out infinite;
}

.dash__orb--pink {
  width: 40%;
  height: 38%;
  background: #f472b6;
  top: 35%;
  left: 30%;
  animation: dash-orb-c 11s ease-in-out infinite;
}

.dash__logo-placeholder {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: rgba(255, 255, 255, 0.85);
  padding: 4px 10px;
  border: 1.5px solid transparent;
  border-radius: 6px;
  background:
    linear-gradient(#0f172a, #0f172a) padding-box,
    linear-gradient(90deg, #22d3ee, #a78bfa, #f472b6, #22d3ee) border-box;
  background-size:
    100% 100%,
    220% 100%;
  animation: dash-border-flow 4s linear infinite;
}

@keyframes dash-border-flow {
  0% {
    background-position:
      0 0,
      0% 50%;
  }

  100% {
    background-position:
      0 0,
      200% 50%;
  }
}

@keyframes dash-orb-a {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(24%, 20%);
  }
}

@keyframes dash-orb-b {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(-22%, -18%);
  }
}

@keyframes dash-orb-c {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(18%, -14%);
  }
}

.dash--theme-breathe .dash__bar {
  position: relative;
  z-index: 1;
  background: linear-gradient(
    120deg,
    #0f172a,
    #0e7490,
    #6366f1,
    #0f172a
  );
  background-size: 280% 280%;
  animation: dash-bar-flow 8s ease infinite;
}

.dash--theme-breathe .dash__body {
  position: relative;
  z-index: 1;
}

.dash--theme-breathe .dash__period--active {
  background: linear-gradient(90deg, #22d3ee, #a78bfa, #f472b6);
  background-size: 200% 100%;
  animation: dash-border-flow 3s linear infinite;
  color: #0f172a;
}

.dash--theme-breathe .dash__stat--cyan {
  box-shadow: 0 0 16px rgba(6, 182, 212, 0.35);
}

@keyframes dash-bar-flow {
  0%,
  100% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .dash--theme-breathe {
    animation: none;
  }

  .dash--theme-breathe .dash__orb,
  .dash--theme-breathe .dash__bar,
  .dash--theme-breathe .dash__period--active,
  .dash--theme-breathe .dash__logo-placeholder {
    animation: none;
  }
}

.dash--tilted {
  transform: rotate(-2.5deg);
  box-shadow: 0 28px 56px rgba(15, 23, 42, 0.22);
}

.dash__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: var(--dash-bar);
  color: #fff;
}

.dash__bar-brand {
  display: flex;
  align-items: center;
}

.dash__brand-logo :deep(.brand-logo--on-dark) {
  height: 12px;
  max-width: 66px;
}

.dash__avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #94a3b8, #cbd5e1);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.dash__body {
  display: flex;
  min-height: 340px;
}

.dash__sidebar {
  width: 118px;
  flex-shrink: 0;
  background: var(--dash-sidebar);
  color: #cbd5e1;
  padding: 8px 6px;
}

.dash__collapse {
  width: 100%;
  border: none;
  background: transparent;
  color: #94a3b8;
  text-align: left;
  padding: 4px 6px;
  cursor: pointer;
  font-size: 12px;
}

.dash__nav-section {
  margin: 10px 6px 4px;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #94a3b8;
}

.dash__nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  padding: 6px 8px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #e2e8f0;
  font-size: 9px;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: background 0.15s;
}

.dash__nav-item--active,
.dash__nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.dash__nav-dot {
  width: 6px;
  height: 6px;
  border-radius: 2px;
  background: currentColor;
  opacity: 0.5;
  flex-shrink: 0;
}

.dash__main {
  flex: 1;
  padding: 10px;
  min-width: 0;
}

.dash__analytics-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  background: #334155;
  border-radius: 8px;
  color: #fff;
  margin-bottom: 10px;
}

.dash__analytics-title {
  margin: 0;
  font-size: 11px;
  font-weight: 600;
}

.dash__periods {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.dash__period {
  padding: 4px 8px;
  border: none;
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  font-size: 8px;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.25s ease,
    color 0.25s ease,
    transform 0.2s ease;
}

.dash__period:hover {
  background: rgba(255, 255, 255, 0.18);
  color: #fff;
}

.dash__period--active {
  background: #fff;
  color: #0f172a;
}

.dash__metrics--animating {
  animation: dash-metrics-swap 0.36s ease forwards;
}

@keyframes dash-metrics-swap {
  0% {
    opacity: 1;
  }
  40% {
    opacity: 0.45;
  }
  100% {
    opacity: 1;
  }
}

.dash__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 10px;
}

.dash__stat {
  padding: 10px 8px;
  border-radius: 8px;
  color: #fff;
  min-height: 72px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.dash__stat--navy {
  background: linear-gradient(145deg, #1e3a5f, #0f2744);
}

.dash__stat--blue {
  background: linear-gradient(145deg, #2563eb, #1d4ed8);
}

.dash__stat--cyan {
  background: linear-gradient(145deg, #0891b2, #06b6d4);
}

.dash__stat-label {
  font-size: 8px;
  font-weight: 600;
  opacity: 0.9;
  margin-bottom: 4px;
}

.dash__stat-value {
  font-size: clamp(8px, 2.1vw, 11px);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  word-break: break-word;
}

.dash__stat-sub {
  margin-top: 4px;
  font-size: 7px;
  opacity: 0.85;
  background: rgba(0, 0, 0, 0.15);
  padding: 2px 6px;
  border-radius: var(--radius-pill);
  align-self: flex-start;
}

.dash__charts {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 8px;
}

.dash__chart-card {
  background: var(--dash-card);
  border-radius: 8px;
  padding: 8px;
  border: 1px solid #e2e8f0;
}

.dash__chart-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 9px;
  font-weight: 600;
}

.dash__chart-tabs {
  display: flex;
  gap: 2px;
}

.dash__chart-tabs button {
  padding: 3px 6px;
  border: none;
  border-radius: 4px;
  background: #f1f5f9;
  color: var(--dash-muted);
  font-size: 7px;
  font-weight: 600;
  cursor: pointer;
}

.dash__chart-tabs button.active {
  background: #3b82f6;
  color: #fff;
}

.dash__line-chart svg {
  width: 100%;
  height: 90px;
  display: block;
}

.dash__line-chart[data-view="Bar"] svg path,
.dash__line-chart[data-view="Bar"] svg polyline {
  opacity: 0.3;
}

.dash__chart-legend {
  display: flex;
  gap: 8px;
  margin-top: 4px;
  font-size: 7px;
  color: var(--dash-muted);
}

.dash__chart-legend i {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 2px;
  margin-right: 3px;
  vertical-align: middle;
}

.c-total {
  background: #3b82f6;
}

.c-ok {
  background: #22c55e;
}

.c-amt {
  background: #f97316;
}

.dash__donut-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.dash__donut {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  transition: background 0.36s ease;
}

.dash__donut-hole {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--dash-card);
}

.dash__donut-legend {
  list-style: none;
  margin: 0;
  padding: 0;
  width: 100%;
  font-size: 8px;
}

.dash__donut-legend li {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
  color: var(--dash-muted);
}

.dash__donut-legend span {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  flex-shrink: 0;
}

@media (max-width: 520px) {
  .dash__stats {
    grid-template-columns: 1fr;
  }

  .dash__charts {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .dash__metrics--animating {
    animation: none !important;
  }
}
</style>
