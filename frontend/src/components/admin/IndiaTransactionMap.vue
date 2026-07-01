<script setup>
import { computed } from "vue";
import IndiaMerchantMap from "@/components/IndiaMerchantMap.vue";
import { mapCitiesTodayToLocations } from "@/constants/indiaCityCoords";
import { formatInr } from "@/utils/adminFormat";

const props = defineProps({
  mapCities: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});

const cityGroups = computed(() => mapCitiesTodayToLocations(props.mapCities));

const mapData = computed(() => ({
  locations: cityGroups.value.map((group) => ({
    id: group.id,
    company: `${group.city} · ${group.txn_count} txn${group.txn_count === 1 ? "" : "s"} · ${formatInr(group.amount_with_fees)}`,
    x: group.x,
    y: group.y,
    lat: group.lat,
    lon: group.lon,
    state_id: group.state_id,
  })),
}));

const mapHint = computed(() =>
  cityGroups.value.length
    ? "Today's successful payouts by merchant city"
    : "No successful payouts with city data today",
);
</script>

<template>
  <article class="admin-card map-card">
    <h2 class="map-card__title">Live transaction map</h2>

    <div v-if="loading" class="map-card__body map-card__body--loading shimmer-block" />

    <IndiaMerchantMap
      v-else
      class="map-card__body map-card__map"
      variant="admin"
      compact
      :map="mapData"
      :hint="mapHint"
      aria-label="Map of India showing today's successful payout cities"
    />
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

.map-card__title {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 600;
  color: var(--ur-text);
  flex-shrink: 0;
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

.map-card__body :deep(.india-map__hint) {
  flex-shrink: 0;
}

.map-card__body--loading {
  border-radius: 10px;
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
    background-position: -200% 0;
  }
}
</style>
