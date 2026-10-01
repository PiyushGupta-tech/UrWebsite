<script setup>
import { useRateCycle } from "@/composables/useRateCycle.js";

/* Figma 990:8307 — Intelligent Routing card; the donut draws in step with the uptime count-up. */
const { rateLabel, rateOpacity, chartOffset, chartOpacity } = useRateCycle(99.99);

const ASSET = "/images/figma-home/hero-v2";

const PSPS = [
  { name: "PSP 1", status: "ok", note: "120ms" },
  { name: "PSP 2", status: "down", note: "Failover" },
  { name: "PSP 3", status: "down", note: "Failover" },
];
</script>

<template>
  <div class="hg-routing">
    <div class="hg-routing__body">
      <p class="hg-routing__title">Intelligent Routing</p>
      <div class="hg-routing__row">
        <!-- Figma's segment path as a stroked arc: r 28.206 / width 9.954 spans its 23.23–33.18 ring, sweeping 334.24° clockwise from 12 o'clock. -->
        <svg class="hg-routing__donut" viewBox="0 0 73 73" fill="none" aria-hidden="true">
          <path
            pathLength="1"
            d="M36.5 8.294A28.206 28.206 0 1 1 24.241 11.098"
            stroke="#0066cc"
            stroke-width="9.954"
            :style="{
              strokeDasharray: 1,
              strokeDashoffset: chartOffset,
              opacity: chartOpacity,
            }"
          />
        </svg>
        <div class="hg-routing__list">
          <div v-for="psp in PSPS" :key="psp.name" class="hg-routing__psp">
            <span class="hg-routing__psp-name">
              <span>{{ psp.name }}</span>
              <span v-if="psp.status === 'ok'" class="hg-routing__ok">
                <img :src="`${ASSET}/check-sm.svg`" alt="" width="6" height="6" />
              </span>
              <img v-else class="hg-routing__down" :src="`${ASSET}/danger.svg`" alt="" width="12" height="12" />
            </span>
            <span>{{ psp.note }}</span>
          </div>
        </div>
      </div>
    </div>
    <span class="hg-routing__value" :style="{ opacity: rateOpacity }">{{ rateLabel }}</span>
  </div>
</template>

<style scoped>
.hg-routing {
  left: 216px;
  top: 8px;
  width: 254px;
  overflow: hidden;
  box-sizing: border-box;
  padding: 12px 20px;
  border: 0.552px solid #e2e8f0;
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 8.838px 22.095px rgba(13, 23, 48, 0.06);
  line-height: normal;
  color: #252b37;
}

.hg-routing *,
.hg-routing *::before,
.hg-routing *::after {
  box-sizing: border-box;
}

.hg-routing img {
  display: block;
  max-width: none;
}

.hg-routing__body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.hg-routing__title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.hg-routing__row {
  display: flex;
  align-items: center;
  gap: 24px;
}

.hg-routing__donut {
  display: block;
  flex-shrink: 0;
  width: 73px;
  height: 73px;
}

.hg-routing__list {
  display: flex;
  flex-direction: column;
  gap: 7px;
  flex-shrink: 0;
  width: 112px;
  padding: 6px;
  border-radius: 4px;
  background: #ffffff;
  filter: drop-shadow(0 1px 7px rgba(0, 0, 0, 0.08)) drop-shadow(0 1px 7px rgba(0, 0, 0, 0.08));
}

.hg-routing__psp {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 14px;
  font-size: 10px;
  font-weight: 500;
  white-space: nowrap;
}

.hg-routing__psp-name {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
  flex-shrink: 0;
  width: 53px;
}

.hg-routing__ok {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 12px;
  height: 12px;
  border-radius: 46.199px;
  background: #097495;
}

.hg-routing__ok img {
  width: 6px;
  height: 6px;
}

.hg-routing__down {
  flex-shrink: 0;
  width: 12px;
  height: 12px;
}

/*
 * Figma offsets are from the outer edge; absolute children start inside the 0.552px border.
 * Centred rather than left-aligned like Figma, so the count-up stays put as digits grow.
 */
.hg-routing__value {
  position: absolute;
  left: 33.898px;
  top: 67.898px;
  width: 44px;
  height: 16px;
  font-size: 12px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  text-align: center;
  white-space: nowrap;
}
</style>
