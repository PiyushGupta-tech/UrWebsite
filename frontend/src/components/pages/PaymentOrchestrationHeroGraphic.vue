<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from "vue";
import { LOGO_PATHS, PSP_LOGOS } from "@/constants/logos.js";
import { ORCHESTRATION_MODES } from "@/constants/orchestrationModes.js";

const emit = defineEmits(["story-change"]);

const props = defineProps({
  ready: { type: Boolean, default: false },
});

const partners = [
  { id: "airpay", name: "Airpay", logo: PSP_LOGOS.airpay },
  { id: "jio-payments", name: "Jio", logo: PSP_LOGOS.jioPayments },
  { id: "easebuzz", name: "Easebuzz", logo: PSP_LOGOS.easebuzz },
  { id: "cashfree", name: "Cashfree", logo: PSP_LOGOS.cashfree },
  { id: "unlimit", name: "Unlimit", logo: PSP_LOGOS.unlimit },
  { id: "payu", name: "PayU", logo: PSP_LOGOS.payu },
];

const modes = ORCHESTRATION_MODES;
const MODE_CYCLE_MS = 5000;
const modeIndex = ref(0);
const smartPartnerIndex = ref(0);
let modeCycleTimer = null;
let smartCycleTimer = null;

const mode = computed(() => modes[modeIndex.value] ?? modes[0]);

const selectedSmartPartner = computed(
  () => partners[smartPartnerIndex.value] ?? partners[0],
);

const activePartner = computed(() => {
  if (mode.value.id === "smart") {
    return selectedSmartPartner.value;
  }
  return partners.find((p) => p.id === mode.value.pickId) ?? partners[0];
});

const bestRatePartner = computed(() => {
  if (mode.value.id !== "smart" || !mode.value.rates) return null;
  let best = partners[0];
  let max = 0;
  for (const p of partners) {
    const r = mode.value.rates[p.id] ?? 0;
    if (r > max) {
      max = r;
      best = p;
    }
  }
  return best;
});

function partnerRate(id) {
  return mode.value.rates?.[id];
}

function partnerShare(id) {
  return mode.value.shares?.[id] ?? 0;
}

function isPartnerDown(id) {
  return mode.value.downId === id;
}

function isPartnerActive(id) {
  if (mode.value.id === "smart") {
    return selectedSmartPartner.value.id === id;
  }
  if (mode.value.id === "balance") {
    return (mode.value.shares?.[id] ?? 0) >= 18;
  }
  return mode.value.pickId === id;
}

function isPartnerRouteHot(id) {
  if (mode.value.id === "smart") return selectedSmartPartner.value.id === id;
  if (mode.value.id === "failover") return id === mode.value.pickId;
  if (mode.value.id === "balance") return (mode.value.shares?.[id] ?? 0) > 0;
  return false;
}

function syncSmartToBest() {
  const best = bestRatePartner.value;
  if (!best) return;
  const i = partners.findIndex((p) => p.id === best.id);
  if (i >= 0) smartPartnerIndex.value = i;
}

function selectSmartPartner(index) {
  smartPartnerIndex.value = index % partners.length;
  restartSmartCycle();
}

function onPartnerClick(index) {
  if (mode.value.id === "smart") {
    selectSmartPartner(index);
  }
}

function stopModeCycle() {
  if (modeCycleTimer) {
    clearInterval(modeCycleTimer);
    modeCycleTimer = null;
  }
}

function startModeCycle() {
  stopModeCycle();
  if (!props.ready) return;
  modeCycleTimer = setInterval(() => {
    if (!props.ready) return;
    modeIndex.value = (modeIndex.value + 1) % modes.length;
  }, MODE_CYCLE_MS);
}

function restartModeCycle() {
  stopModeCycle();
  startModeCycle();
}

function stopSmartCycle() {
  if (smartCycleTimer) {
    clearInterval(smartCycleTimer);
    smartCycleTimer = null;
  }
}

function startSmartCycle() {
  stopSmartCycle();
  if (mode.value.id !== "smart" || !props.ready) return;
  smartCycleTimer = setInterval(() => {
    if (mode.value.id !== "smart" || !props.ready) return;
    smartPartnerIndex.value = (smartPartnerIndex.value + 1) % partners.length;
  }, 2800);
}

function restartSmartCycle() {
  stopSmartCycle();
  startSmartCycle();
}

const providersWrapRef = ref(null);
const routingRef = ref(null);

const routingView = ref({ w: 464, h: 52, hubX: 232, busY: 30 });
const partnerRoutePaths = ref([]);
const routeBusPath = ref("");
const failoverPath = ref("");

const activeRoutePath = computed(
  () => partnerRoutePaths.value[smartPartnerIndex.value] ?? "",
);

function measureRoutes() {
  const routing = routingRef.value;
  const wrap = providersWrapRef.value;
  if (!routing || !wrap) return;

  const routingRect = routing.getBoundingClientRect();
  const w = Math.max(1, Math.round(routingRect.width));
  const h = Math.max(1, Math.round(routingRect.height));
  const hubX = w / 2;
  const hubY = 6;
  const busY = Math.round(h * 0.58);
  const endY = h;

  const tiles = wrap.querySelectorAll(".viz__partner");
  if (!tiles.length) return;

  const paths = [];
  let x0 = 0;
  let xLast = w;

  tiles.forEach((tile, i) => {
    const tr = tile.getBoundingClientRect();
    const x = Math.round(tr.left + tr.width / 2 - routingRect.left);
    if (i === 0) x0 = x;
    if (i === tiles.length - 1) xLast = x;
    paths.push(`M${hubX},${hubY} L${hubX},${busY} L${x},${busY} L${x},${endY}`);
  });

  partnerRoutePaths.value = paths;
  routeBusPath.value = `M${x0},${busY} L${xLast},${busY}`;
  routingView.value = { w, h, hubX, busY };

  // Failover orange follows the same hub → bus → branch tree as the blue routes,
  // landing on the down PG (not a freehand curve).
  const downIndex = partners.findIndex((p) => p.id === mode.value.downId);
  failoverPath.value =
    downIndex >= 0 && paths[downIndex] ? paths[downIndex] : "";
}

let resizeObserver = null;

function scheduleMeasureRoutes() {
  requestAnimationFrame(measureRoutes);
}

function selectMode(i) {
  modeIndex.value = i;
  restartModeCycle();
}

watch(
  mode,
  (m) => {
    emit("story-change", m.id);
    if (m.id === "smart") {
      syncSmartToBest();
      startSmartCycle();
    } else {
      stopSmartCycle();
    }
  },
  { immediate: true },
);

watch(
  () => props.ready,
  (ready) => {
    if (ready) {
      startModeCycle();
      if (mode.value.id === "smart") startSmartCycle();
    } else {
      stopModeCycle();
      stopSmartCycle();
    }
    nextTick(scheduleMeasureRoutes);
  },
  { immediate: true },
);

watch(mode, () => nextTick(scheduleMeasureRoutes));

watch(smartPartnerIndex, () => nextTick(scheduleMeasureRoutes));

onMounted(() => {
  if (props.ready) {
    startModeCycle();
    if (mode.value.id === "smart") startSmartCycle();
  }
  resizeObserver = new ResizeObserver(scheduleMeasureRoutes);
  if (providersWrapRef.value) resizeObserver.observe(providersWrapRef.value);
  nextTick(scheduleMeasureRoutes);
});

onUnmounted(() => {
  stopModeCycle();
  stopSmartCycle();
  resizeObserver?.disconnect();
  resizeObserver = null;
});
</script>

<template>
  <div
    class="viz"
    :class="[`viz--${mode.id}`, { 'viz--ready': ready }]"
    role="group"
    :aria-label="`${mode.section}: payment orchestration`"
  >
    <div class="viz__card">
      <div class="viz__modes" role="tablist">
        <button
          v-for="(m, i) in modes"
          :key="m.id"
          type="button"
          role="tab"
          class="viz__mode"
          :class="{ 'viz__mode--on': modeIndex === i }"
          :aria-selected="modeIndex === i"
          @click="selectMode(i)"
        >
          <span v-if="m.id === 'smart'" class="viz__mode-glyph" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2" />
              <rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2" />
              <rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2" />
              <rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2" />
            </svg>
          </span>
          <span v-else-if="m.id === 'failover'" class="viz__mode-glyph" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3v18M8 7l4-4 4 4M8 17l4 4 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
          </span>
          <span v-else class="viz__mode-glyph" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="4" y="12" width="4" height="8" rx="1" fill="currentColor" />
              <rect x="10" y="8" width="4" height="12" rx="1" fill="currentColor" opacity="0.7" />
              <rect x="16" y="4" width="4" height="16" rx="1" fill="currentColor" opacity="0.45" />
            </svg>
          </span>
          <span class="viz__mode-label">{{ m.title }}</span>
        </button>
      </div>

      <p class="viz__section">{{ mode.section }}</p>

      <div class="viz__pipeline">
        <svg
          class="viz__flow-svg"
          viewBox="0 0 480 72"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <defs>
            <linearGradient id="vizFlow" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#22d3ee" />
              <stop offset="100%" stop-color="#06b6d4" />
            </linearGradient>
          </defs>
          <path
            class="viz__flow-path"
            d="M48,36 H168 M192,36 H312 M336,36 H432"
            fill="none"
            stroke="url(#vizFlow)"
            stroke-width="3"
            stroke-linecap="round"
            stroke-dasharray="3.4 10"
          />
          <circle v-if="ready" r="5" fill="#fbbf24" stroke="#fff" stroke-width="2">
            <animateMotion dur="2.2s" repeatCount="indefinite" path="M48,36 H432" />
          </circle>
        </svg>

        <div class="viz__node viz__node--shop">
          <div class="viz__bubble viz__bubble--shop">
            <svg class="viz__glyph" viewBox="0 0 64 64" fill="none" aria-hidden="true">
              <rect x="14" y="22" width="36" height="28" rx="6" fill="#fff" stroke="#ea580c" stroke-width="2.5" />
              <path d="M12 22 L32 10 L52 22" stroke="#ea580c" stroke-width="2.5" stroke-linejoin="round" />
              <circle cx="44" cy="18" r="8" fill="#22c55e" />
              <path d="M41 18 L43 20 L47 15" stroke="#fff" stroke-width="2" stroke-linecap="round" />
            </svg>
          </div>
          <span class="viz__tag">Store</span>
        </div>

        <div class="viz__chevron" aria-hidden="true">›</div>

        <div class="viz__node viz__node--hub">
          <div class="viz__bubble viz__bubble--hub">
            <span class="viz__hub-ring" aria-hidden="true" />
            <img src="/images/figma-home/hero-diagram/logo.svg" alt="" class="viz__hub-logo" />
            <span
              v-if="mode.id === 'smart'"
              class="viz__hub-badge"
              aria-hidden="true"
            >Pick best</span>
            <span
              v-else-if="mode.id === 'failover'"
              class="viz__hub-badge viz__hub-badge--alert"
              aria-hidden="true"
            >Switch</span>
            <span
              v-else
              class="viz__hub-badge viz__hub-badge--split"
              aria-hidden="true"
            >Split</span>
          </div>
          <span class="viz__tag viz__tag--hub">Urbanrupee</span>
        </div>

        <div class="viz__chevron" aria-hidden="true">›</div>

        <div class="viz__node viz__node--psp">
          <div class="viz__bubble viz__bubble--psp viz__bubble--psp-hot">
            <img
              :key="activePartner.id"
              :src="activePartner.logo"
              :alt="activePartner.name"
              class="viz__psp-hero"
            />
            <span v-if="mode.id === 'failover'" class="viz__swap" aria-hidden="true">
              <svg viewBox="0 0 28 28" fill="none">
                <path d="M8 14h12M18 10l4 4-4 4" stroke="#fff" stroke-width="2.5" stroke-linecap="round" />
              </svg>
            </span>
          </div>
          <span class="viz__tag">{{ activePartner.name }}</span>
        </div>

        <div class="viz__chevron" aria-hidden="true">›</div>

        <div class="viz__node viz__node--done">
          <div class="viz__bubble viz__bubble--done">
            <svg class="viz__glyph" viewBox="0 0 64 64" fill="none" aria-hidden="true">
              <circle cx="32" cy="32" r="26" fill="#dcfce7" stroke="#16a34a" stroke-width="3" />
              <path d="M20 32 L28 40 L44 22" stroke="#16a34a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </div>
          <span class="viz__tag">Done</span>
        </div>
      </div>

      <div ref="providersWrapRef" class="viz__providers-wrap">
        <div ref="routingRef" class="viz__routing" aria-hidden="true">
          <svg
            class="viz__routing-svg"
            :viewBox="`0 0 ${routingView.w} ${routingView.h}`"
            preserveAspectRatio="none"
          >
            <defs>
              <linearGradient id="routeHot" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#22d3ee" />
                <stop offset="100%" stop-color="#06b6d4" />
              </linearGradient>
            </defs>
            <path
              v-if="routeBusPath"
              class="viz__route viz__route--bus"
              :d="routeBusPath"
              fill="none"
            />
            <path
              v-for="(p, i) in partners"
              :key="`route-${p.id}`"
              :d="partnerRoutePaths[i] || ''"
              class="viz__route"
              :class="{
                'viz__route--hot': isPartnerRouteHot(p.id),
                'viz__route--off': isPartnerDown(p.id),
                'viz__route--share': mode.id === 'balance',
              }"
              fill="none"
              stroke-width="1.8"
              vector-effect="non-scaling-stroke"
              stroke-linecap="round"
            />
            <path
              v-if="mode.id === 'failover' && ready && failoverPath"
              class="viz__route viz__route--redirect"
              :d="failoverPath"
              fill="none"
              stroke-width="2.2"
              vector-effect="non-scaling-stroke"
            />
            <circle
              v-if="ready && mode.id === 'smart' && activeRoutePath"
              r="2.2"
              fill="#22d3ee"
              stroke="#fff"
              stroke-width="1.2"
              vector-effect="non-scaling-stroke"
            >
              <animateMotion
                :key="`smart-route-${smartPartnerIndex}`"
                dur="1.8s"
                repeatCount="indefinite"
                :path="activeRoutePath"
              />
            </circle>
            <circle
              v-if="ready && mode.id === 'failover' && failoverPath"
              r="2.2"
              fill="#f97316"
              vector-effect="non-scaling-stroke"
            >
              <animateMotion
                dur="1.4s"
                repeatCount="indefinite"
                :path="failoverPath"
              />
            </circle>
          </svg>
          <div class="viz__routing-hub">
            <img src="/logos/favicon.svg" alt="" width="20" height="20" />
          </div>
        </div>

        <ul class="viz__partners" aria-label="Payment providers">
          <li
            v-for="(p, i) in partners"
          :key="p.id"
          class="viz__partner"
          :class="{
            'viz__partner--on': isPartnerActive(p.id),
            'viz__partner--off': isPartnerDown(p.id),
            'viz__partner--failover': mode.id === 'failover' && isPartnerDown(p.id),
            'viz__partner--route': isPartnerRouteHot(p.id),
            'viz__partner--pick': mode.id === 'smart',
          }"
          :title="p.name"
          :role="mode.id === 'smart' ? 'button' : undefined"
          :tabindex="mode.id === 'smart' ? 0 : undefined"
          @click="onPartnerClick(i)"
          @keydown.enter.prevent="onPartnerClick(i)"
          @keydown.space.prevent="onPartnerClick(i)"
        >
          <img :src="p.logo" :alt="p.name" loading="lazy" />
          <!-- Fixed-height metric slot so smart / failover / balance keep the same card height. -->
          <span class="viz__metric">
            <span
              v-if="mode.id === 'smart' && partnerRate(p.id)"
              class="viz__rate"
            >{{ partnerRate(p.id) }}%</span>
            <span
              v-else-if="mode.id === 'balance'"
              class="viz__share"
              :style="{ '--share': `${partnerShare(p.id)}%` }"
            >
              <span class="viz__share-bar" />
              <span class="viz__share-num">{{ partnerShare(p.id) }}%</span>
            </span>
          </span>
          <span v-if="isPartnerDown(p.id)" class="viz__status viz__status--off">
            <svg viewBox="0 0 12 12" aria-hidden="true">
              <path d="M2 2l8 8M10 2L2 10" stroke="currentColor" stroke-width="2" />
            </svg>
          </span>
          <span
            v-else-if="mode.id === 'smart' && bestRatePartner?.id === p.id"
            class="viz__status viz__status--best"
          >Best</span>
          <span
            v-else-if="mode.id === 'failover' && p.id === mode.pickId"
            class="viz__status viz__status--on"
            aria-hidden="true"
          />
          <span
            v-else-if="mode.id === 'balance' && partnerShare(p.id) >= 20"
            class="viz__status viz__status--on"
            aria-hidden="true"
          />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.viz {
  width: 100%;
  max-width: 520px;
  margin-inline: auto;
}

.viz__card {
  /* Tallest mode is load-balance (share bars); lock height so mode switches don't jump. */
  min-height: 390px;
  padding: 14px 12px 12px;
  border-radius: 18px;
  background: linear-gradient(165deg, #f0f9ff 0%, #fff 55%, #ecfeff 100%);
  border: 1px solid #bae6fd;
  box-shadow: 0 16px 40px rgba(6, 182, 212, 0.14);
  box-sizing: border-box;
}

.viz__modes {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}

.viz__mode {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 4px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  color: #64748b;
  transition:
    border-color 0.2s,
    background 0.2s,
    color 0.2s,
    transform 0.2s;
}

.viz__mode--on {
  border-color: #06b6d4;
  background: #ecfeff;
  color: #0e7490;
  transform: translateY(-2px);
}

.viz__mode-glyph {
  width: 22px;
  height: 22px;
  display: block;
}

.viz__mode-glyph svg {
  width: 100%;
  height: 100%;
}

.viz__mode-label {
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.viz__section {
  margin: 0 0 10px;
  font-size: 11px;
  font-weight: 800;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #0891b2;
}

.viz__pipeline {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1.15fr auto 1fr;
  align-items: center;
  gap: 2px 0;
  padding: 8px 0 0;
  min-height: 118px;
}

.viz__flow-svg {
  position: absolute;
  left: 4%;
  right: 4%;
  top: 38%;
  height: 28px;
  width: 92%;
  pointer-events: none;
  z-index: 0;
}

.viz--ready .viz__flow-path {
  animation: viz-dash 2s linear infinite;
}

@keyframes viz-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

.viz__node {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.viz__chevron {
  z-index: 1;
  font-size: 22px;
  font-weight: 800;
  color: #22d3ee;
  line-height: 1;
  opacity: 0.85;
}

.viz__bubble {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: #fff;
  border: 2px solid #e2e8f0;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  position: relative;
}

.viz__bubble--shop {
  border-color: #fdba74;
  background: linear-gradient(145deg, #fff7ed, #fff);
}

.viz__bubble--hub {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border-color: #38bdf8;
  background: linear-gradient(145deg, #ecfeff, #fff);
  flex-direction: column;
  gap: 0;
}

.viz__hub-ring {
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px dashed rgba(6, 182, 212, 0.45);
}

.viz--ready .viz__hub-ring {
  animation: viz-ring 3s ease-in-out infinite;
}

@keyframes viz-ring {
  50% {
    transform: scale(1.06);
    border-color: rgba(34, 211, 238, 0.7);
  }
}

.viz__hub-logo {
  width: 34px;
  height: 34px;
  object-fit: contain;
  position: relative;
  z-index: 1;
}

.viz__hub-badge {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 7px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #fff;
  background: #0891b2;
  padding: 2px 7px;
  border-radius: 999px;
  border: 2px solid #fff;
  white-space: nowrap;
  z-index: 2;
}

.viz__hub-badge--alert {
  background: #f97316;
}

.viz__hub-badge--split {
  background: #6366f1;
}

.viz__bubble--psp {
  width: 88px;
  height: 88px;
  border-radius: 20px;
}

.viz__bubble--psp-hot {
  border-color: #06b6d4;
  box-shadow:
    0 0 0 3px rgba(6, 182, 212, 0.2),
    0 12px 28px rgba(6, 182, 212, 0.28);
}

.viz__psp-hero {
  max-width: 72px;
  max-height: 40px;
  object-fit: contain;
  transition: opacity 0.25s ease;
}

.viz--story-smart .viz__psp-hero {
  animation: viz-psp-in 0.35s ease;
}

@keyframes viz-psp-in {
  from {
    opacity: 0.4;
    transform: scale(0.92);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.viz__swap {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f97316;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 4px 10px rgba(249, 115, 22, 0.45);
}

.viz__swap svg {
  width: 16px;
  height: 16px;
}

.viz__bubble--done {
  border-color: #86efac;
  background: linear-gradient(145deg, #f0fdf4, #fff);
}

.viz__glyph {
  width: 56px;
  height: 56px;
}

.viz__tag {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  white-space: nowrap;
  line-height: 1.2;
  min-height: 12px;
}

.viz__tag--hub {
  color: #0891b2;
}

.viz__providers-wrap {
  margin-top: 12px;
  padding: 0 8px;
}

.viz__routing {
  position: relative;
  height: 52px;
  margin-bottom: 4px;
}

.viz__routing-svg {
  width: 100%;
  height: 100%;
  display: block;
  overflow: visible;
}

.viz__routing-hub {
  position: absolute;
  left: 50%;
  top: -5px;
  transform: translateX(-50%);
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 2px solid #38bdf8;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
  z-index: 2;
}

.viz__routing-hub img {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

.viz__route {
  stroke: #cbd5e1;
  stroke-dasharray: 3.4 10;
  opacity: 0.5;
  transition:
    stroke 0.35s,
    opacity 0.35s,
    stroke-width 0.35s;
}

.viz__route--bus {
  opacity: 0.65;
}

.viz__route--hot {
  stroke: url(#routeHot);
  stroke-width: 2.5;
  stroke-dasharray: none;
  opacity: 1;
}

.viz--ready .viz__route--hot {
  animation: viz-route-pulse 1.8s ease-in-out infinite;
}

@keyframes viz-route-pulse {
  50% {
    stroke-width: 3;
    opacity: 0.85;
  }
}

.viz__route--off {
  stroke: #fca5a5;
  opacity: 0.35;
  stroke-dasharray: 3.4 10;
}

.viz--story-balance .viz__route--share {
  stroke: #93c5fd;
  opacity: 0.65;
  stroke-dasharray: none;
}

.viz--story-balance .viz__route--hot {
  stroke: #6366f1;
}

.viz__route--redirect {
  stroke: #f97316;
  opacity: 1;
  stroke-dasharray: 3.4 10;
}

.viz--ready .viz__route--redirect {
  animation: viz-dash 1.2s linear infinite;
}

.viz__partners {
  list-style: none;
  margin: 0;
  padding: 8px 0 10px;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 6px;
  /* Matches load-balance (tallest) so smart/failover don't collapse the row. */
  min-height: 82px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-sizing: border-box;
}

.viz__partner {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 65px;
  padding: 8px 4px 6px;
  border-radius: 10px;
  border: 2px solid #f1f5f9;
  background: #f8fafc;
  opacity: 0.55;
  box-sizing: border-box;
  transition:
    opacity 0.25s,
    border-color 0.25s,
    transform 0.25s,
    box-shadow 0.25s,
    gap 0.55s cubic-bezier(0.6, 0.6, 0, 1);
}

.viz__partner--pick {
  cursor: pointer;
}

.viz__partner--pick:focus-visible {
  outline: 2px solid #06b6d4;
  outline-offset: 2px;
}

.viz__partner img {
  display: block;
  max-width: 100%;
  max-height: 22px;
  object-fit: contain;
}

.viz__metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  /* Reserve load-balance share (bar + label) so failover/smart don't shrink the row. */
  height: 20px;
  overflow: hidden;
  opacity: 1;
  transition:
    height 0.55s cubic-bezier(0.6, 0.6, 0, 1),
    opacity 0.35s ease;
}

/* Failover: collapse metrics so logos center; reverse animates back for other modes. */
.viz--failover .viz__partner {
  gap: 0;
}

.viz--failover .viz__metric {
  height: 0;
  opacity: 0;
  pointer-events: none;
}

.viz__partner--route {
  opacity: 0.85;
}

.viz__partner--on {
  opacity: 1;
  border-color: #06b6d4;
  background: #fff;
  transform: scale(1.04);
  box-shadow: 0 4px 14px rgba(6, 182, 212, 0.18);
}

.viz--story-balance .viz__partner--on {
  border-color: #818cf8;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.18);
}

.viz__partner--off {
  opacity: 0.35;
  filter: grayscale(1);
  border-color: #fecaca;
  background: #fef2f2;
}

/* Failover target: full-color logo + orange border (not greyscale). */
.viz__partner--failover {
  opacity: 1;
  filter: none;
  border-color: #f97316;
  background: #fff;
  box-shadow: 0 4px 14px rgba(249, 115, 22, 0.18);
}

.viz--failover .viz__partner--failover .viz__status--off {
  background: #f97316;
}

.viz__rate {
  font-size: 9px;
  font-weight: 800;
  color: #0891b2;
  line-height: 1;
}

.viz--story-smart .viz__partner--on .viz__rate {
  color: #0f766e;
}

.viz__share {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.viz__share-bar {
  display: block;
  width: 100%;
  height: 4px;
  border-radius: 4px;
  background: #e2e8f0;
  position: relative;
  overflow: hidden;
}

.viz__share-bar::after {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--share, 0%);
  background: linear-gradient(90deg, #818cf8, #6366f1);
  border-radius: 4px;
  transition: width 0.4s ease;
}

.viz__share-num {
  font-size: 8px;
  font-weight: 800;
  line-height: 1;
  color: #6366f1;
}

.viz__status {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  border: 2px solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 7px;
  font-weight: 800;
  text-transform: uppercase;
}

.viz__status--off {
  background: #ef4444;
  color: #fff;
  width: 16px;
  padding: 0;
}

.viz__status--off svg {
  width: 8px;
  height: 8px;
}

.viz__status--on {
  background: #22c55e;
  width: 10px;
  min-width: 10px;
  padding: 0;
}

.viz__status--best {
  background: #0891b2;
  color: #fff;
}

@media (max-width: 480px) {
  .viz__pipeline {
    min-height: 100px;
  }

  .viz__bubble {
    width: 58px;
    height: 58px;
  }

  .viz__bubble--hub {
    width: 64px;
    height: 64px;
  }

  .viz__hub-logo {
    width: 30px;
    height: 30px;
  }

  .viz__bubble--psp {
    width: 72px;
    height: 72px;
  }

  .viz__glyph {
    width: 44px;
    height: 44px;
  }

  .viz__partners {
    grid-template-columns: repeat(3, 1fr);
    min-height: 0;
  }

  .viz__partner {
    min-height: 0;
  }

  .viz__card {
    min-height: 0;
  }

  .viz__chevron {
    font-size: 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .viz--ready .viz__flow-path,
  .viz--ready .viz__hub-ring,
  .viz--ready .viz__route--hot,
  .viz--ready .viz__route--redirect {
    animation: none;
  }
}
</style>
