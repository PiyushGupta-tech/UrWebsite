<script setup>
import { onMounted, ref } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Business connected to UPI, cards, bank transfer, and wallets",
  },
});

/**
 * Figma 391:15401 — Multi Channel Disbursement.
 * Exact wire geometry: Figma-exported stroke paths + absoluteTransform
 * matrices (same pattern as CollectionsSmarterDiagram). Marching dashes only.
 */
const ASSET = "/images/figma-payouts/control/multichannel";
const ART_W = 800;
const ART_H = 269;

const METHODS = [
  { label: "UPI", icon: "phone.svg" },
  { label: "Cards", icon: "credit-card.svg" },
  { label: "Bank Transfer", icon: "bank.svg" },
  { label: "Wallets", icon: "wallet.svg" },
];

/** Sitewide connector dash (Collections / Payouts platform / Hyper Checkout). */
const DASH = [3.4, 10];

/**
 * matrix = CSS matrix(a,b,c,d,e,f) from Figma absoluteTransform
 * relative to artboard 391:15401. d = exact Figma SVG stroke export
 * for each Line node (curved centerline as shown in the design).
 */
const WIRES = [
  {
    id: "left",
    // 391:15441 Line 605
    matrix: [-0.999504, 0.031505, -0.01251, -0.999922, 219.498535, 160.326172],
    d: "M0.76811 1.10294L20.1525 0.773112C30.4091 0.598594 40.2117 4.99599 46.9015 12.7726C54.098 23.4748 65.8796 30.2021 78.754 30.9604L84.3048 31.2873",
    sw: 1.53621,
  },
  {
    id: "fan-upi",
    // 391:15427
    matrix: [-0.999802, 0.019921, 0.019788, 0.999804, 575.547852, 65.960938],
    d: "M0.566617 1.76867L63.5747 0.576568C81.1137 0.244735 97.7766 8.22625 108.511 22.1009L118.428 34.9192C136.711 65.1523 168.614 84.5436 203.87 86.8525L213.985 87.515",
    sw: 1.13323,
  },
  {
    id: "fan-cards",
    // 391:15433
    matrix: [-0.999833, 0.018302, 0.021539, 0.999768, 581.379883, 123.177734],
    d: "M0.567465 1.90246L72.9984 0.576773C84.6209 0.364046 96.0176 3.8015 105.584 10.4053L109.296 12.9678C114.687 16.6889 120.693 19.4276 127.037 21.0576L150.148 26.9955C150.148 26.9955 159.569 28.6732 165.792 29.3452C171.642 29.9769 180.185 30.3712 180.185 30.3712L218.256 32.3696",
    sw: 1.13493,
  },
  {
    id: "fan-bank",
    // 391:15436
    matrix: [-0.999833, -0.018302, 0.021539, -0.999768, 576.450195, 188.556641],
    d: "M0.566616 1.70941L73.5881 0.57333C82.5453 0.433972 91.4032 2.46544 99.4045 6.49411L120.062 16.8953C138.568 23.7774 158.184 27.1862 177.927 26.9504L213.403 26.5269",
    sw: 1.13323,
  },
  {
    id: "fan-wallets",
    // 391:15430
    matrix: [-0.999833, -0.018302, 0.021539, -0.999768, 583.250977, 244.472656],
    d: "M0.566617 1.76617L66.4272 0.575698C83.5168 0.266792 99.7951 7.85134 110.552 21.1347L121.095 34.1544C139.643 63.4583 172.039 81.0721 206.718 80.7081L221.703 80.5508",
    sw: 1.13323,
  },
];

const HUBS = [
  { cx: 134.305, cy: 131.704, r: 3.04 },
  { cx: 366.543, cy: 157.889, r: 3.095 },
  { cx: 583.118, cy: 68.118, r: 4.588 },
  { cx: 583.118, cy: 124.118, r: 4.588 },
  { cx: 583.118, cy: 186.118, r: 4.588 },
  { cx: 583.118, cy: 244.118, r: 4.588 },
];

function matrixAttr(m) {
  return `matrix(${m.join(" ")})`;
}

function dashAttr(dash) {
  return dash.join(" ");
}

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});
</script>

<template>
  <div
    class="po-mc"
    :class="{ 'po-mc--static': reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div class="po-mc__business">
      <div class="po-mc__business-icon">
        <img :src="`${ASSET}/building.svg`" alt="" width="27" height="27" />
      </div>
      <p class="po-mc__business-label">Your Business</p>
    </div>

    <div class="po-mc__hub">
      <img :src="`${ASSET}/logo.svg`" alt="" width="47" height="58" />
    </div>

    <div class="po-mc__methods">
      <div
        v-for="m in METHODS"
        :key="m.label"
        class="po-mc__method"
      >
        <img :src="`${ASSET}/${m.icon}`" alt="" width="18" height="18" />
        <span>{{ m.label }}</span>
      </div>
    </div>

    <svg
      class="po-mc__wires"
      :viewBox="`0 0 ${ART_W} ${ART_H}`"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <linearGradient
          id="po-mc-wire-grad"
          x1="0%"
          y1="0%"
          x2="100%"
          y2="0%"
        >
          <stop stop-color="#0292B8" />
          <stop offset="1" stop-color="#134E66" />
        </linearGradient>
      </defs>

      <g
        v-for="w in WIRES"
        :key="w.id"
        :transform="matrixAttr(w.matrix)"
      >
        <path
          class="po-mc__stroke"
          :d="w.d"
          stroke="url(#po-mc-wire-grad)"
          :stroke-width="w.sw"
          :stroke-dasharray="dashAttr(DASH)"
          stroke-linecap="round"
          stroke-linejoin="round"
          fill="none"
        />
      </g>

      <circle
        v-for="(h, i) in HUBS"
        :key="`h-${i}`"
        :cx="h.cx"
        :cy="h.cy"
        :r="h.r"
        fill="#38B7D3"
      />
    </svg>
  </div>
</template>

<style scoped>
.po-mc {
  --po-mc-ink: #252b37;
  position: relative;
  width: 100%;
  max-width: 800px;
  aspect-ratio: 800 / 269;
  container-type: inline-size;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  overflow: visible;
}

.po-mc__business {
  position: absolute;
  left: 0;
  top: calc(70.68 / 269 * 100%);
  width: calc(130.564 / 800 * 100%);
  aspect-ratio: 1;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(8px, 2cqi, 15.7px);
  padding: clamp(12px, 2.9cqi, 23.56px);
  border-radius: clamp(10px, 2cqi, 15.7px);
  background: #fff;
  box-shadow:
    0 0.98px 0.98px rgba(0, 0, 0, 0.1),
    0 0.98px 1.47px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.po-mc__business-icon {
  width: clamp(36px, 6.9cqi, 54.97px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: rgba(9, 116, 149, 0.1);
  display: grid;
  place-items: center;
}

.po-mc__business-icon img {
  width: 50%;
  height: auto;
  display: block;
}

.po-mc__business-label {
  margin: 0;
  font-size: clamp(11px, 1.75cqi, 14px);
  font-weight: 600;
  color: var(--po-mc-ink);
  white-space: nowrap;
}

.po-mc__hub {
  position: absolute;
  left: calc(223.82 / 800 * 100%);
  top: calc(90.31 / 269 * 100%);
  width: calc(137.436 / 800 * 100%);
  aspect-ratio: 1;
  z-index: 2;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: linear-gradient(180deg, #0292b8 38.44%, #00b7db 100%);
  box-shadow: 0 7.85px 11.78px rgba(2, 146, 184, 0.25);
}

.po-mc__hub img {
  width: 34%;
  height: auto;
  display: block;
}

.po-mc__methods {
  position: absolute;
  left: calc(587 / 800 * 100%);
  top: calc(16 / 269 * 100%);
  width: calc(172 / 800 * 100%);
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 3cqi, 23.95px);
  padding: clamp(10px, 2.5cqi, 20px) clamp(8px, 2cqi, 16px);
  border-radius: clamp(8px, 1.5cqi, 12px);
  background: #fff;
  border: 0.75px solid #e9eaeb;
  box-sizing: border-box;
}

.po-mc__method {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1cqi, 8px);
  width: 100%;
  height: clamp(28px, 4.9cqi, 39px);
  padding: clamp(6px, 1.5cqi, 12px) clamp(8px, 2cqi, 16px);
  border-radius: 4px;
  background: #fff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 3px 3.7px #e9eaeb;
  box-sizing: border-box;
}

.po-mc__method img {
  width: clamp(14px, 2.25cqi, 18px);
  height: auto;
  display: block;
  flex-shrink: 0;
}

.po-mc__method span {
  font-size: clamp(10px, 1.5cqi, 12px);
  font-weight: 600;
  color: var(--po-mc-ink);
  white-space: nowrap;
}

.po-mc__wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  pointer-events: none;
  overflow: visible;
  z-index: 1;
}

.po-mc__stroke {
  /* Path local origin is at the destination end; positive offset = flow out */
  animation: po-mc-dash 1.1s linear infinite;
}

.po-mc--static .po-mc__stroke {
  animation: none;
}

@keyframes po-mc-dash {
  to {
    stroke-dashoffset: 13.4;
  }
}

@media (prefers-reduced-motion: reduce) {
  .po-mc__stroke {
    animation: none;
  }
}
</style>
