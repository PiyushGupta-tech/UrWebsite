<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import IndiaMerchantMap from "@/components/IndiaMerchantMap.vue";
import {
  mergeMapCityLayers,
  buildCityMerchantLookup,
  extendMerchantLookupFromTransactions,
  resolveMerchantName,
} from "@/constants/indiaCityCoords";
import { formatInr } from "@/utils/adminFormat";

const props = defineProps({
  payoutCities: { type: Array, default: () => [] },
  payinCities: { type: Array, default: () => [] },
  payoutProviders: { type: Array, default: () => [] },
  payinProviders: { type: Array, default: () => [] },
  payoutTransactions: { type: Array, default: () => [] },
  payinTransactions: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});

const mapCardRef = ref(null);
const isFullscreen = ref(false);

const cityGroups = computed(() =>
  mergeMapCityLayers(props.payoutCities, props.payinCities),
);

const payoutMerchantLookup = computed(() =>
  extendMerchantLookupFromTransactions(
    buildCityMerchantLookup(props.payoutProviders, "payout"),
    props.payoutTransactions,
    "payout",
  ),
);

const payinMerchantLookup = computed(() =>
  extendMerchantLookupFromTransactions(
    buildCityMerchantLookup(props.payinProviders, "payin"),
    props.payinTransactions,
    "payin",
  ),
);

function mapPopupLabel(group) {
  const lookup =
    group.kind === "payin" ? payinMerchantLookup.value : payoutMerchantLookup.value;
  const merchant = resolveMerchantName(group, group.kind, lookup);
  const txns = `${group.txn_count} txn${group.txn_count === 1 ? "" : "s"}`;
  const amount = formatInr(group.amount_with_fees);

  if (merchant) {
    return `${merchant} · ${txns} · ${amount}`;
  }

  return `${txns} · ${amount}`;
}

const mapData = computed(() => ({
  locations: cityGroups.value.map((group) => ({
    id: group.id,
    kind: group.kind,
    company: mapPopupLabel(group),
    x: group.x,
    y: group.y,
    lat: group.lat,
    lon: group.lon,
    state_id: group.state_id,
  })),
}));

const mapHint = computed(() => {
  const payoutCount = props.payoutCities.length;
  const payinCount = props.payinCities.length;
  if (!payoutCount && !payinCount) {
    return "No successful payin or payout city data today";
  }
  return "Today's successful transactions by merchant city";
});

function onFullscreenChange() {
  isFullscreen.value = document.fullscreenElement === mapCardRef.value;
}

async function toggleFullscreen() {
  const el = mapCardRef.value;
  if (!el) return;

  try {
    if (document.fullscreenElement === el) {
      await document.exitFullscreen();
    } else {
      await el.requestFullscreen();
    }
  } catch {
    /* unsupported or denied */
  }
}

onMounted(() => {
  document.addEventListener("fullscreenchange", onFullscreenChange);
});

onUnmounted(() => {
  document.removeEventListener("fullscreenchange", onFullscreenChange);
  if (document.fullscreenElement === mapCardRef.value) {
    document.exitFullscreen().catch(() => {});
  }
});
</script>

<template>
  <article
    ref="mapCardRef"
    class="admin-card map-card"
    :class="{ 'map-card--fullscreen': isFullscreen }"
  >
    <h2 v-if="!isFullscreen" class="map-card__title">Live transaction map</h2>

    <div v-if="loading" class="map-card__body map-card__body--loading shimmer-block" />

    <div v-else class="map-card__wrap">
      <IndiaMerchantMap
        class="map-card__body map-card__map"
        variant="admin"
        compact
        :map="mapData"
        hint=""
        aria-label="Map of India showing today's successful payin and payout cities"
      />
    </div>

    <footer v-if="!loading" class="map-card__footer">
      <ul class="map-legend" aria-label="Map marker legend">
        <li class="map-legend__item">
          <span class="map-legend__dot map-legend__dot--payout" aria-hidden="true" />
          <span>Payout</span>
        </li>
        <li class="map-legend__item">
          <span class="map-legend__dot map-legend__dot--payin" aria-hidden="true" />
          <span>Payin</span>
        </li>
      </ul>

      <p class="map-card__hint">{{ mapHint }}</p>

      <button
        type="button"
        class="map-fullscreen-btn"
        :aria-label="isFullscreen ? 'Exit full screen map' : 'Full screen map'"
        :title="isFullscreen ? 'Exit full screen' : 'Full screen'"
        @click="toggleFullscreen"
      >
        <svg
          v-if="!isFullscreen"
          class="map-fullscreen-btn__icon"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            fill="currentColor"
            d="M3 9V3h6v2H5v4H3zm12-4h6v6h-2V5h-4V3zM3 15v6h6v-2H5v-4H3zm16 4h-4v2h6v-6h-2v4z"
          />
        </svg>
        <svg v-else class="map-fullscreen-btn__icon" viewBox="0 0 24 24" aria-hidden="true">
          <path
            fill="currentColor"
            d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"
          />
        </svg>
        <span class="map-fullscreen-btn__label">{{ isFullscreen ? "Exit" : "Full screen" }}</span>
      </button>
    </footer>
  </article>
</template>

<style scoped>
.map-card {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  min-height: 0;
  width: 100%;
  overflow: hidden;
}

.map-card--fullscreen,
.map-card:fullscreen {
  background: #000;
  border-color: #000;
}

.map-card:fullscreen {
  display: flex;
  flex-direction: column;
  padding: clamp(8px, 1.5vh, 16px);
  box-sizing: border-box;
}

.map-card:fullscreen .map-card__wrap {
  flex: 1 1 auto;
  min-height: 0;
}

.map-card:fullscreen .map-card__body :deep(.india-map),
.map-card:fullscreen .map-card__body :deep(.india-map__frame),
.map-card:fullscreen .map-card__body :deep(.india-map__map-wrap),
.map-card:fullscreen .map-card__body :deep(.india-map__svg) {
  height: 100%;
  min-height: 0;
}

.map-card__title {
  margin: 0 0 clamp(4px, 0.6vh, 6px);
  font-size: clamp(10px, 1.1vh, 12px);
  font-weight: 600;
  color: var(--ur-text);
  flex-shrink: 0;
}

.map-card__wrap {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.map-card__body {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.map-card__body :deep(.india-map) {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.map-card__body :deep(.india-map__frame) {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.map-card__body :deep(.india-map__map-wrap) {
  flex: 1 1 auto;
  min-height: 0;
  height: 100%;
  display: flex;
  align-items: stretch;
}

.map-card__body :deep(.india-map__svg) {
  flex: 1 1 auto;
  width: 100%;
  height: 100%;
  min-height: 0;
}

.map-card__footer {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: clamp(8px, 1vw, 12px);
  flex-shrink: 0;
  margin-top: clamp(4px, 0.6vh, 6px);
  min-height: clamp(32px, 4vh, 36px);
}

.map-card__hint {
  margin: 0;
  font-size: clamp(9px, 1vh, 11px);
  color: var(--ur-muted, #737373);
  text-align: center;
  line-height: 1.3;
}

.map-legend {
  margin: 0;
  padding: clamp(4px, 0.8vh, 6px) clamp(8px, 1vw, 10px);
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: clamp(3px, 0.5vh, 5px);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.72);
  border: 1px solid var(--ur-card-border, #1f1f1f);
}

.map-legend__item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: clamp(9px, 1vh, 11px);
  font-weight: 600;
  color: var(--ur-text, #f5f5f5);
  line-height: 1;
}

.map-legend__dot {
  flex-shrink: 0;
  width: clamp(8px, 1vh, 10px);
  height: clamp(8px, 1vh, 10px);
  border-radius: 50%;
  box-shadow: 0 0 6px currentColor;
}

.map-legend__dot--payout {
  background: #ff9f0a;
  color: rgba(255, 159, 10, 0.95);
  border: 1px solid #ff6b00;
}

.map-legend__dot--payin {
  background: #32ff7e;
  color: rgba(0, 255, 136, 0.95);
  border: 1px solid #00ff88;
  box-shadow: 0 0 8px rgba(0, 255, 136, 0.75);
}

.map-fullscreen-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: clamp(32px, 4vh, 36px);
  padding: 0 clamp(10px, 1.2vw, 12px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 8px;
  background: transparent;
  color: var(--ur-text, #f5f5f5);
  font-family: inherit;
  font-size: clamp(10px, 1.1vh, 12px);
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  box-shadow: none;
  backdrop-filter: none;
}

.map-fullscreen-btn:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.32);
  color: #fff;
}

.map-fullscreen-btn:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.35);
  outline-offset: 2px;
}

.map-fullscreen-btn__icon {
  flex-shrink: 0;
  width: clamp(14px, 1.6vh, 16px);
  height: clamp(14px, 1.6vh, 16px);
}

.map-fullscreen-btn__label {
  letter-spacing: 0.02em;
}

.map-card__body--loading {
  border-radius: 10px;
  flex: 1 1 auto;
  min-height: 0;
}

.shimmer-block {
  background: linear-gradient(
    90deg,
    var(--ur-card-bg) 25%,
    var(--ur-shimmer-mid) 50%,
    var(--ur-card-bg) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -100% 0;
  }
}
</style>
