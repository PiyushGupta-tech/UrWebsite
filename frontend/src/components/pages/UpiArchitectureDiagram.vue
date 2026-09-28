<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from "vue";

/** Asset root — Figma 296:2487 */
const ASSET = "/images/figma-upi/arch";
const ARTBOARD_W = 1291;
const ARTBOARD_H = 813;
/** Equal top/bottom inset around the diagram inside the viewport band */
const V_PAD = 24;
/** Bump fitted scale up 10% for presence while keeping uniform scaling */
const SCALE_BOOST = 1.1;

defineProps({
  ready: { type: Boolean, default: true },
  alt: {
    type: String,
    default:
      "Urbanrupee Seamless UPI Switch connecting payment initiation, UPI network, bank pipes, and settlement",
  },
});

const reduceMotion = ref(false);
const scalerRef = ref(null);
const scale = ref(1);
const offsetX = ref(0);
let resizeObserver = null;

function getNavOffset() {
  const page = document.querySelector(".page-view");
  if (page) {
    const raw = getComputedStyle(page).getPropertyValue("--page-nav-offset");
    const n = parseFloat(raw);
    if (Number.isFinite(n)) return n;
  }
  return 129;
}

function updateScale() {
  const el = scalerRef.value;
  if (!el || typeof window === "undefined") return;

  const widthScale = el.clientWidth / ARTBOARD_W;
  // Viewport band under navbar, minus equal vertical padding around the diagram
  const availH = Math.max(0, window.innerHeight - getNavOffset() - V_PAD * 2);
  const heightScale = availH > 0 ? availH / ARTBOARD_H : widthScale;

  // Uniform scale only — preserves aspect ratio / text readability (no Y-squash).
  // Container width stays full; diagram centers if height limits scale.
  scale.value = Math.min(widthScale, heightScale, 1) * SCALE_BOOST;
  offsetX.value = Math.max(0, (el.clientWidth - ARTBOARD_W * scale.value) / 2);
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  nextTick(updateScale);
  if (typeof ResizeObserver !== "undefined") {
    resizeObserver = new ResizeObserver(updateScale);
    if (scalerRef.value) resizeObserver.observe(scalerRef.value);
  }
  window.addEventListener("resize", updateScale, { passive: true });
});

onBeforeUnmount(() => {
  resizeObserver?.disconnect();
  window.removeEventListener("resize", updateScale);
});

const switchRows = [
  {
    id: "unified-upi-api",
    title: "Unified UPI API",
    body: "Intent • QR • Collect",
    icon: `${ASSET}/icon-api.svg`,
    nodeId: "296:2496",
  },
  {
    id: "routing-engine",
    title: "Routing Engine",
    body: "Smart Routing • Priority • Failover",
    icon: `${ASSET}/icon-routing.svg`,
    nodeId: "296:2507",
  },
  {
    id: "pipe-adapters",
    title: "Pipe Adapters",
    body: "Normalize Request & Response",
    icon: `${ASSET}/icon-adapters.svg`,
    nodeId: "296:2516",
  },
  {
    id: "lifecycle-ledger",
    title: "Lifecycle & Ledger",
    body: "Status • UTR • Webhooks • Refunds",
    icon: `${ASSET}/icon-ledger.svg`,
    nodeId: "296:2527",
  },
];

const pipes = [
  {
    id: "pipe-a",
    title: "Pipe A",
    body: "PSP / Bank",
    icon: `${ASSET}/icon-bank-a.svg`,
    nodeId: "296:2574",
  },
  {
    id: "pipe-b",
    title: "Pipe B",
    body: "PSP / Bank",
    icon: `${ASSET}/icon-bank-b.svg`,
    nodeId: "296:2583",
  },
  {
    id: "pipe-c",
    title: "Pipe C",
    body: "PSP / Bank",
    icon: `${ASSET}/icon-bank-c.svg`,
    nodeId: "296:2592",
  },
];

/** Shared path strings drive dashed strokes + traveling dots */
const flowPaths = [
  {
    id: "init",
    d: "M190 293 H308",
    arrow: true,
    dur: 2.4,
    begin: 0,
  },
  {
    id: "pipes",
    // Touch outer pipes frame top border (y=618)
    d: "M462.5 518 V618",
    arrow: false,
    dur: 2.1,
    begin: 0.35,
  },
  {
    id: "npci",
    // From pipes frame up, rounded corner, into NPCI left border (786.5) at card mid (289)
    d: "M690 618 V306 A17 17 0 0 1 707 289 H786.5",
    arrow: true,
    dur: 3.2,
    begin: 0.2,
  },
  {
    id: "auth",
    // Turn down mid-gap; arrow tips at auth-frame outer border (left=1113), not the inner card
    d: "M993.5 289 H1048 A17 17 0 0 1 1065 306 V351 A17 17 0 0 0 1082 368 H1113",
    arrow: true,
    dur: 2.6,
    begin: 0.55,
  },
  {
    id: "settle",
    d: "M1176 430 V505",
    arrow: true,
    dur: 1.9,
    begin: 0.8,
  },
];
</script>

<template>
  <div
    class="uad"
    :class="{ 'uad--ready': ready && !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <div ref="scalerRef" class="uad__scaler">
      <div
        class="uad__artboard"
        data-arch-part="stage"
        data-node-id="296:2487"
        :style="{
          transform: `scale(${scale})`,
          marginLeft: `${offsetX}px`,
          marginBottom: `${ARTBOARD_H * scale - ARTBOARD_H}px`,
        }"
      >
        <!-- Animated flow strokes + traveling dots -->
        <svg
          class="uad__flows"
          viewBox="0 0 1291 813"
          fill="none"
          aria-hidden="true"
          data-arch-part="connectors"
        >
          <defs>
            <marker
              id="uad-arrow"
              viewBox="0 0 10 10"
              refX="8"
              refY="5"
              markerWidth="7"
              markerHeight="7"
              orient="auto-start-reverse"
            >
              <path d="M1 1.5 L8.5 5 L1 8.5 Z" fill="#ffffff" />
            </marker>
          </defs>

          <path
            v-for="flow in flowPaths"
            :key="flow.id"
            class="uad__flow"
            :class="`uad__flow--${flow.id}`"
            :d="flow.d"
            :marker-end="flow.arrow ? 'url(#uad-arrow)' : undefined"
          />

          <circle
            v-for="flow in flowPaths"
            v-show="!reduceMotion"
            :key="`${flow.id}-dot`"
            class="uad__flow-dot"
            r="3.2"
          >
            <animateMotion
              :dur="`${flow.dur}s`"
              :begin="`${flow.begin}s`"
              repeatCount="indefinite"
              :path="flow.d"
            />
          </circle>
          <!-- Second staggered dots on longer routes -->
          <circle
            v-for="flow in flowPaths.filter((f) => f.id === 'npci' || f.id === 'auth')"
            v-show="!reduceMotion"
            :key="`${flow.id}-dot-b`"
            class="uad__flow-dot uad__flow-dot--soft"
            r="2.4"
          >
            <animateMotion
              :dur="`${flow.dur}s`"
              :begin="`${flow.begin + flow.dur * 0.5}s`"
              repeatCount="indefinite"
              :path="flow.d"
            />
          </circle>
        </svg>

        <!-- Payment Initiation — 315:1809 -->
        <section
          class="uad__part uad__initiation"
          data-arch-part="payment-initiation"
          data-node-id="315:1809"
        >
          <div class="uad__initiation-frame" data-node-id="296:2539">
            <article
              class="uad__mini-card"
              data-arch-part="merchant"
              data-node-id="296:2540"
            >
              <img
                :src="`${ASSET}/icon-merchant.svg`"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
              <div class="uad__mini-card-text">
                <p class="uad__mini-card-title">Merchant</p>
                <p class="uad__mini-card-body">Checkout / API</p>
              </div>
            </article>
            <article
              class="uad__mini-card"
              data-arch-part="customer"
              data-node-id="296:2549"
            >
              <img
                :src="`${ASSET}/icon-customer.svg`"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
              <div class="uad__mini-card-text">
                <p class="uad__mini-card-title">Customer</p>
                <p class="uad__mini-card-body">UPI Apps</p>
              </div>
            </article>
          </div>
          <p class="uad__col-label" data-arch-part="label-initiation" data-node-id="296:2492">
            Payment Initiation
          </p>
        </section>

        <!-- Urbanrupee Seamless UPI Switch — 315:1810 -->
        <section
          class="uad__part uad__switch"
          data-arch-part="switch"
          data-node-id="315:1810"
        >
          <p
            class="uad__switch-title"
            data-arch-part="switch-title"
            data-node-id="296:2651"
          >
            Urbanrupee Seamless UPI Switch
          </p>
          <div class="uad__switch-panel" data-node-id="296:2493">
            <div class="uad__switch-rows" data-node-id="296:2495">
              <article
                v-for="(row, i) in switchRows"
                :key="row.id"
                class="uad__switch-row"
                :data-arch-part="row.id"
                :data-node-id="row.nodeId"
                :style="{ '--d': `${i * 0.35}s` }"
              >
                <img
                  :src="row.icon"
                  alt=""
                  width="28"
                  height="28"
                  decoding="async"
                />
                <div class="uad__switch-row-text">
                  <p class="uad__switch-row-title">{{ row.title }}</p>
                  <p class="uad__switch-row-body">{{ row.body }}</p>
                </div>
              </article>
            </div>
            <div
              class="uad__switch-pill"
              data-arch-part="single-source"
              data-node-id="296:2537"
            >
              Single source of truth
            </div>
          </div>
        </section>

        <!-- NPCI — 296:2565 (no outer glow) -->
        <article
          class="uad__part uad__npci"
          data-arch-part="npci"
          data-node-id="296:2565"
        >
          <div class="uad__npci-inner" data-node-id="507:4988">
            <div class="uad__npci-logo" data-node-id="296:2566">
              <img
                :src="`${ASSET}/upi-wordmark-clear.png`"
                alt=""
                width="82"
                height="35"
                decoding="async"
              />
            </div>
            <p class="uad__npci-text" data-node-id="296:2570">NPCI</p>
          </div>
        </article>

        <!-- Bank Pipes — 296:2573 -->
        <section
          class="uad__part uad__pipes"
          data-arch-part="pipes"
          data-node-id="296:2573"
        >
          <article
            v-for="(pipe, i) in pipes"
            :key="pipe.id"
            class="uad__pipe-card"
            :data-arch-part="pipe.id"
            :data-node-id="pipe.nodeId"
            :style="{ '--d': `${i * 0.28}s` }"
          >
            <img
              :src="pipe.icon"
              alt=""
              width="32"
              height="32"
              decoding="async"
            />
            <div class="uad__mini-card-text">
              <p class="uad__mini-card-title">{{ pipe.title }}</p>
              <p class="uad__mini-card-body uad__mini-card-body--med">
                {{ pipe.body }}
              </p>
            </div>
          </article>
        </section>

        <!-- Authorization & Settlement — 296:2616 / 296:2623 -->
        <section
          class="uad__part uad__auth"
          data-arch-part="authorization"
          data-node-id="296:2616"
        >
          <div class="uad__auth-frame" data-node-id="296:2623">
            <article
              class="uad__mini-card uad__mini-card--auth"
              data-arch-part="issuer-bank"
              data-node-id="296:2624"
            >
              <img
                :src="`${ASSET}/icon-issuer.svg`"
                alt=""
                width="28"
                height="28"
                decoding="async"
              />
              <div class="uad__mini-card-text">
                <p class="uad__mini-card-title">Issuer Bank</p>
                <p class="uad__mini-card-body">Customer Bank</p>
              </div>
            </article>

            <div
              class="uad__auth-gap"
              data-arch-part="connector-issuer-settlement"
              data-node-id="296:2633"
              aria-hidden="true"
            />

            <article
              class="uad__mini-card uad__mini-card--auth"
              data-arch-part="settlement"
              data-node-id="296:2639"
            >
              <div class="uad__settle-icon">
                <img
                  :src="`${ASSET}/icon-settlement.svg`"
                  alt=""
                  width="19"
                  height="23"
                  decoding="async"
                />
              </div>
              <div class="uad__mini-card-text">
                <p class="uad__mini-card-title">Settlement</p>
                <p class="uad__mini-card-body">Real-time / T+ 1</p>
              </div>
            </article>
          </div>
          <p
            class="uad__col-label uad__col-label--auth"
            data-arch-part="label-authorization"
            data-node-id="296:2653"
          >
            Authorization &amp; Settlement
          </p>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.uad {
  width: 100%;
  max-width: 1291px;
  margin: 0 auto;
  padding-block: 24px;
  box-sizing: border-box;
}

.uad__scaler {
  width: 100%;
  overflow: visible;
}

.uad__artboard {
  position: relative;
  width: 1291px;
  height: 813px;
  transform-origin: top left;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  border-radius: 14.141px;
  overflow: hidden;
}

.uad__part {
  position: absolute;
  box-sizing: border-box;
  z-index: 2;
}

/* —— Payment Initiation —— */
.uad__initiation {
  left: 34px;
  top: 173px;
  width: 158px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.uad__initiation-frame {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  width: 125px;
  padding: 16px;
  box-sizing: border-box;
  border: 1px solid rgba(235, 235, 235, 0.5);
  border-radius: 12px;
}

.uad__mini-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 91px;
  height: 87px;
  padding: 14px;
  box-sizing: border-box;
  background: #ffffff;
  border: 0.5px solid #fafafa;
  border-radius: 6px;
  box-shadow: 0 3.4px 1.7px #e9eaeb;
}

.uad__mini-card img {
  display: block;
  flex-shrink: 0;
}

.uad__mini-card-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  width: 100%;
  text-align: center;
}

.uad__mini-card-title,
.uad__mini-card-body {
  margin: 0;
  width: 100%;
  color: #252b37;
  word-break: break-word;
}

.uad__mini-card-title {
  font-size: 12px;
  font-weight: 600;
  line-height: normal;
}

.uad__mini-card-body {
  font-size: 8px;
  font-weight: 600;
  line-height: normal;
}

.uad__mini-card-body--med {
  font-weight: 500;
}

.uad__col-label {
  margin: 0;
  width: 100%;
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  text-align: center;
  text-transform: capitalize;
  color: #ffffff;
}

.uad__col-label--auth {
  width: 166px;
  height: 44px;
  margin-top: 8px;
  margin-left: auto;
  margin-right: 0;
  line-height: normal;
}

/* —— Switch —— */
.uad__switch {
  left: 316px;
  top: 85px;
  width: 272px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
}

.uad__switch-title {
  margin: 0;
  width: 100%;
  height: 22px;
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  text-align: center;
  text-transform: capitalize;
  color: #ffffff;
}

.uad__switch-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 12px;
}

.uad__switch-rows {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.uad__switch-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4.1px 2px #e9eaeb;
}

.uad__switch-row img {
  display: block;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
}

.uad__switch-row-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.uad__switch-row-title,
.uad__switch-row-body {
  margin: 0;
  color: #252b37;
  word-break: break-word;
}

.uad__switch-row-title {
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
}

.uad__switch-row-body {
  font-size: 10px;
  font-weight: 500;
  line-height: normal;
}

.uad__switch-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 238px;
  height: 37px;
  border-radius: 15px;
  background: #097495;
  border: 0.6px solid #097495;
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  line-height: normal;
  text-align: center;
  white-space: nowrap;
}

/* —— NPCI (no bright outer glow) —— */
.uad__npci {
  left: 786.5px;
  top: 247px;
  width: 207px;
  padding: 24px 32px;
  box-sizing: border-box;
  border-radius: 8px;
  border: 0.7px solid #fafafa;
  background: linear-gradient(147deg, #097495 3.35%, #0292b8 100%);
  box-shadow: none;
  filter: none;
}

.uad__npci-inner {
  display: flex;
  align-items: center;
  gap: 2px;
  width: 100%;
}

.uad__npci-logo {
  position: relative;
  width: 82px;
  height: 35px;
  flex-shrink: 0;
  overflow: hidden;
}

.uad__npci-logo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: left center;
}

.uad__npci-text {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  line-height: normal;
  color: #ffffff;
  white-space: nowrap;
}

/* —— Pipes —— */
.uad__pipes {
  left: 387px;
  top: 618px;
  width: 406px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 16px;
  box-sizing: border-box;
  border: 1px solid rgba(235, 235, 235, 0.5);
  border-radius: 12px;
}

.uad__pipe-card {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 7px;
  min-width: 0;
  height: 98px;
  padding: 15px;
  box-sizing: border-box;
  background: #ffffff;
  border: 0.6px solid #fafafa;
  border-radius: 7px;
  box-shadow: 0 3.9px 1.9px #e9eaeb;
}

.uad__pipe-card img {
  display: block;
  width: 32px;
  height: 32px;
}

/* —— Authorization —— */
.uad__auth {
  left: 994px;
  top: 292px;
  width: 248px;
  height: 370px;
}

.uad__auth-frame {
  position: absolute;
  left: 119px;
  top: 12px;
  width: 129px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  box-sizing: border-box;
  border: 1px solid rgba(235, 235, 235, 0.5);
  border-radius: 12px;
}

.uad__mini-card--auth {
  width: 95px;
  height: 96px;
}

.uad__settle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  overflow: hidden;
}

.uad__settle-icon img {
  display: block;
  width: 19px;
  height: 23px;
}

.uad__auth-gap {
  width: 17px;
  height: 75px;
  flex-shrink: 0;
}

.uad__auth .uad__col-label--auth {
  position: absolute;
  left: 98px;
  top: 346px;
  width: 166px;
}

/* —— Animated connectors —— */
.uad__flows {
  position: absolute;
  inset: 0;
  width: 1291px;
  height: 813px;
  z-index: 1;
  pointer-events: none;
  overflow: visible;
}

.uad__flow {
  stroke: #ffffff;
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 3.4 10;
  opacity: 0.88;
  fill: none;
}

.uad__flow--auth {
  stroke-width: 1.75;
}

.uad__flow-dot {
  fill: #7ee8ff;
  filter: drop-shadow(0 0 4px rgba(126, 232, 255, 0.95));
}

.uad__flow-dot--soft {
  fill: #ffffff;
  opacity: 0.85;
  filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.75));
}

.uad--ready .uad__flow {
  animation: uad-dash 1.4s linear infinite;
}

.uad--ready .uad__flow--pipes {
  animation-delay: 0.15s;
}

.uad--ready .uad__flow--npci {
  animation-delay: 0.3s;
}

.uad--ready .uad__flow--auth {
  animation-delay: 0.45s;
}

.uad--ready .uad__flow--settle {
  animation-delay: 0.6s;
}

@keyframes uad-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

/* —— Subtle component motion —— */
.uad--ready .uad__mini-card {
  animation: uad-card-float 5.2s ease-in-out infinite;
}

.uad--ready .uad__initiation .uad__mini-card:nth-child(2) {
  animation-delay: 0.4s;
}

.uad--ready .uad__switch-row {
  animation: uad-card-float 5.6s ease-in-out infinite;
  animation-delay: var(--d, 0s);
}

.uad--ready .uad__pipe-card {
  animation: uad-card-float 5.4s ease-in-out infinite;
  animation-delay: var(--d, 0s);
}

.uad--ready .uad__mini-card--auth {
  animation: uad-card-float 5.5s ease-in-out infinite;
}

.uad--ready .uad__mini-card--auth[data-arch-part="settlement"] {
  animation-delay: 0.45s;
}

.uad--ready .uad__npci {
  animation: uad-npci-breathe 4.8s ease-in-out infinite;
}

.uad--ready .uad__switch-pill {
  animation: uad-pill-glow 3.6s ease-in-out infinite;
}

@keyframes uad-card-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

@keyframes uad-npci-breathe {
  0%,
  100% {
    transform: translateY(0);
    border-color: rgba(250, 250, 250, 0.85);
  }
  50% {
    transform: translateY(-2px);
    border-color: rgba(250, 250, 250, 1);
  }
}

@keyframes uad-pill-glow {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(9, 116, 149, 0);
  }
  50% {
    box-shadow: 0 0 0 3px rgba(9, 116, 149, 0.18);
  }
}

@media (prefers-reduced-motion: reduce) {
  .uad--ready .uad__flow,
  .uad--ready .uad__mini-card,
  .uad--ready .uad__switch-row,
  .uad--ready .uad__pipe-card,
  .uad--ready .uad__npci,
  .uad--ready .uad__switch-pill {
    animation: none;
  }

  .uad__flow-dot {
    display: none;
  }
}
</style>
