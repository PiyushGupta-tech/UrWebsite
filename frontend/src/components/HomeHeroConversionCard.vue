<script setup>
import { useRateCycle } from "@/composables/useRateCycle.js";

/* Figma 990:8295 — Higher conversion card; count-up + draw matches Custom Checkout's rate card. */
const { rateLabel, rateOpacity, chartOffset, chartOpacity } = useRateCycle(32, {
  decimals: 0,
  prefix: "+",
});
</script>

<template>
  <div class="hg-conv">
    <div class="hg-conv__body">
      <div class="hg-conv__head">
        <span class="hg-conv__status">
          <img
            src="/images/figma-home/hero-v2/check.svg"
            alt=""
            width="10.0446"
            height="10.2784"
          />
        </span>
        <span class="hg-conv__text">
          <span class="hg-conv__label">Higher conversion</span>
          <span class="hg-conv__value" :style="{ opacity: rateOpacity }">{{ rateLabel }}</span>
        </span>
      </div>
      <div class="hg-conv__spark">
        <!-- The path starts at the arrowhead, so the reveal runs end → start -->
        <svg viewBox="0 0 142.785 38.7847" preserveAspectRatio="none" fill="none" aria-hidden="true">
          <path
            pathLength="1"
            d="M141.892 12.1827V0.892308H128.513M141.892 0.892308L123.928 12.8752L106.921 26.3465C101.204 30.8748 92.7774 29.0824 89.3985 22.6193L88.6252 21.1401C84.6021 13.4448 73.5884 13.4448 69.5653 21.1401L68.8065 22.5914C65.6675 28.5956 57.4751 29.5693 53.0163 24.468C49.2545 20.1642 42.5941 20.0638 38.7043 24.2523L35.3907 27.8203C31.3997 32.1177 25.0537 33.2706 19.8062 30.6514C14.0342 27.7704 7.02573 29.478 3.22583 34.691L0.89237 37.8923"
            stroke="#097495"
            stroke-width="1.78462"
            stroke-linecap="round"
            :style="{
              strokeDasharray: 1,
              strokeDashoffset: -chartOffset,
              opacity: chartOpacity,
            }"
          />
        </svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hg-conv {
  left: 218px;
  top: 160px;
  width: 176px;
  height: 110px;
  overflow: hidden;
  box-sizing: border-box;
  border: 0.552px solid #e2e8f0;
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 8.838px 22.095px rgba(13, 23, 48, 0.06);
}

.hg-conv__body {
  position: absolute;
  left: 16.45px;
  top: 14.45px;
  display: flex;
  flex-direction: column;
  width: 145px;
}

.hg-conv__head {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  width: 133px;
}

.hg-conv__status {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 21.524px;
  height: 22.025px;
  border-radius: 46.199px;
  background: #097495;
}

.hg-conv__status img {
  display: block;
  width: 10.045px;
  height: 10.278px;
}

.hg-conv__text {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 104px;
  font-weight: 600;
  line-height: normal;
  color: #252b37;
}

.hg-conv__label {
  font-size: 12px;
  white-space: nowrap;
}

.hg-conv__value {
  font-size: 15.467px;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.hg-conv__spark {
  position: relative;
  width: 141px;
  height: 37px;
}

.hg-conv__spark svg {
  position: absolute;
  left: -0.63%;
  top: -2.41%;
  display: block;
  width: 101.26%;
  height: 104.82%;
  overflow: visible;
}
</style>
