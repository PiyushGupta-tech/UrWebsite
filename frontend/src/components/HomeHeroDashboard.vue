<script setup>
/* Figma 990:8530 — white-label dashboard. */
const ASSET = "/images/figma-home/hero-v2";

const STATS = [
  { label: "Total Transactions", value: "24,780", delta: "↑ 12.5%" },
  { label: "Success Rate", value: "98.6%", delta: "↑ 8.2%" },
  { label: "Total Revenue", value: "₹12.6M", delta: "↑ 15.3%" },
];

const BARS = [
  { day: "Mon", height: 22.367 },
  { day: "Tue", height: 30.755 },
  { day: "Wed", height: 16.776 },
  { day: "Thu", height: 25.163 },
  { day: "Fri", height: 33.551 },
  { day: "Sat", height: 27.959 },
  { day: "Sun", height: 19.571 },
];
</script>

<template>
  <div class="hg-dash">
    <div class="hg-dash__header">
      <span class="hg-dash__logo">
        <img :src="`${ASSET}/dash-logo.svg`" alt="" width="8.947" height="8.947" />
        <span>YOUR LOGO&nbsp;&nbsp;I&nbsp;&nbsp;YOUR COLORS</span>
      </span>
      <span class="hg-dash__user">
        <img :src="`${ASSET}/dash-avatar.png`" alt="" width="8.947" height="8.947" />
        <span>Admin</span>
      </span>
    </div>

    <div class="hg-dash__body">
      <div class="hg-dash__toolbar">
        <span class="hg-dash__heading">Metrics</span>
        <span class="hg-dash__range">
          <span>Last 30 Days</span>
          <img :src="`${ASSET}/chevron-down.svg`" alt="" width="12" height="12" />
        </span>
      </div>

      <div class="hg-dash__content">
        <div class="hg-dash__stats">
          <div v-for="stat in STATS" :key="stat.label" class="hg-dash__stat">
            <span class="hg-dash__stat-label">{{ stat.label }}</span>
            <span class="hg-dash__stat-value">{{ stat.value }}</span>
            <span class="hg-dash__stat-delta">{{ stat.delta }}</span>
          </div>
        </div>

        <div class="hg-dash__chart">
          <span class="hg-dash__chart-title">Transaction Overview</span>
          <div class="hg-dash__bars">
            <div v-for="(bar, i) in BARS" :key="bar.day" class="hg-dash__bar-col">
              <span
                class="hg-dash__bar"
                :style="{ height: `${bar.height}px`, animationDelay: `${i * 0.15}s` }"
              />
              <span class="hg-dash__day">{{ bar.day }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <img class="hg-dash__cursor" :src="`${ASSET}/cursor.svg`" alt="" width="8" height="8" />
  </div>
</template>

<style scoped>
.hg-dash {
  left: 714px;
  top: 0;
  width: 295px;
  height: 167px;
  overflow: hidden;
  border-radius: 8.947px;
  background: #ffffff;
  box-shadow: 0 1px 2px -1px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.1);
  line-height: normal;
  color: #252b37;
}

.hg-dash,
.hg-dash *,
.hg-dash *::before,
.hg-dash *::after {
  box-sizing: border-box;
}

.hg-dash img {
  display: block;
  max-width: none;
}

.hg-dash__header {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 21px;
  padding: 5.592px 8.947px;
  background: #097495;
  color: #ffffff;
  font-weight: 600;
  white-space: nowrap;
}

.hg-dash__logo {
  display: flex;
  align-items: center;
  gap: 4.473px;
  font-size: 8px;
}

.hg-dash__user {
  display: flex;
  align-items: center;
  gap: 3.355px;
  font-size: 5.592px;
}

.hg-dash__logo img,
.hg-dash__user img {
  width: 8.947px;
  height: 8.947px;
}

.hg-dash__body {
  position: absolute;
  left: 8px;
  top: 26px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 9px;
  width: 278px;
}

.hg-dash__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  font-weight: 600;
  white-space: nowrap;
}

.hg-dash__heading {
  font-size: 8px;
}

.hg-dash__range {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 66px;
  height: 20px;
  padding: 4px 8px;
  border: 0.8px solid #e2e8f0;
  border-radius: 2px;
  font-size: 6px;
  color: #535862;
}

.hg-dash__range img {
  width: 12px;
  height: 12px;
}

.hg-dash__content {
  display: flex;
  flex-direction: column;
  gap: 9px;
  width: 100%;
}

.hg-dash__stats {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  height: 42.894px;
  white-space: nowrap;
}

.hg-dash__stat {
  display: flex;
  flex-shrink: 0;
  flex-direction: column;
  gap: 2.237px;
  width: 86.673px;
  padding: 6.71px;
  border: 0.559px solid #e5e7eb;
  border-radius: 4.473px;
  background: #fafbfa;
}

.hg-dash__stat-label {
  font-size: 5.033px;
  font-weight: 600;
  color: #535862;
  text-transform: uppercase;
}

.hg-dash__stat-value {
  font-size: 7.829px;
  font-weight: 700;
}

.hg-dash__stat-delta {
  font-size: 5.033px;
  font-weight: 600;
  color: #2d6a4f;
}

.hg-dash__chart {
  display: flex;
  flex-direction: column;
  gap: 12.861px;
  width: 100%;
}

.hg-dash__chart-title {
  font-size: 6.151px;
  font-weight: 600;
  white-space: nowrap;
}

.hg-dash__bars {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 17.894px;
  height: 33.551px;
  padding: 0 8.947px;
}

.hg-dash__bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 3.355px;
}

.hg-dash__bar {
  width: 7.829px;
  border-radius: 1.678px 1.678px 0 0;
  background: #097495;
}

.hg-dash__day {
  font-size: 6px;
  font-weight: 600;
  color: #535862;
  white-space: nowrap;
}

.hg-dash__cursor {
  position: absolute;
  left: 272px;
  top: 43px;
  width: 8px;
  height: 8px;
}

@media (prefers-reduced-motion: no-preference) {
  .hg-dash__bar {
    transform-origin: center bottom;
    animation: hg-dash-bar-grow 2.4s ease-in-out infinite;
  }
}

/* Vertical take on the hero's hg-bar-grow skeleton bars. */
@keyframes hg-dash-bar-grow {
  0%,
  100% {
    transform: scaleY(0.55);
  }
  50% {
    transform: scaleY(1);
  }
}
</style>
