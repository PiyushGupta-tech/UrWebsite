<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from "vue";

const ASSET = "/images/figma-collections/smarter";

defineProps({
  ready: { type: Boolean, default: true },
});

const reduceMotion = ref(false);
const scalerRef = ref(null);
const scale = ref(1);
let resizeObserver = null;

function updateScale() {
  const el = scalerRef.value;
  if (!el) return;
  scale.value = Math.min(el.clientWidth / 1291, 1);
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  nextTick(updateScale);
  if (typeof ResizeObserver !== "undefined") {
    resizeObserver = new ResizeObserver(updateScale);
    if (scalerRef.value) resizeObserver.observe(scalerRef.value);
  } else {
    window.addEventListener("resize", updateScale);
  }
});

onBeforeUnmount(() => {
  resizeObserver?.disconnect();
  window.removeEventListener("resize", updateScale);
});

const customers = [
  {
    title: "Retail Customers",
    body: "One-time payments",
    icon: `${ASSET}/profile.svg`,
    w: 24,
  },
  {
    title: "Business Customers",
    body: "Invoice payments",
    icon: `${ASSET}/business.svg`,
    w: 24,
  },
  {
    title: "Subscribers",
    body: "Recurrings payments",
    icon: `${ASSET}/couple.svg`,
    w: 28,
  },
  {
    title: "B2B Partners",
    body: "Bulk Collections",
    icon: `${ASSET}/people-team.svg`,
    w: 26,
  },
];

const features = [
  { label: "Secure & Compliant", icon: `${ASSET}/shield.svg` },
  { label: "Real-time processing", icon: `${ASSET}/time.svg` },
  { label: "Reconcillation", icon: `${ASSET}/reconcile.svg` },
  { label: "High Availability", icon: `${ASSET}/availability.svg` },
];

const businessChecks = [
  "Receive payments",
  "Track in real-time",
  "Automate reconciliation",
  "Access detailed reports",
  "Scale effortlessly",
];

const methods = [
  { label: "Netbanking", icon: `${ASSET}/building.svg`, w: 20, h: 20, chip: 125 },
  { label: "UPI", icon: `${ASSET}/upi.svg`, w: 16, h: 23, chip: 82 },
  { label: "Cards", icon: `${ASSET}/cards.svg`, w: 20, h: 20, chip: 96 },
  { label: "Wallets", icon: `${ASSET}/wallet.svg`, w: 18, h: 18, chip: 104 },
];

/**
 * Animated connectors — exact Figma strokes.
 * Left fan 466:37720 @ (310, 159.88); right fork 466:37836 @ (822, 261).
 */
const LEFT_FAN = {
  x: 310,
  y: 159.88174438476562,
  w: 168.40603637695312,
  h: 239.23651123046875,
  strokeWidth: 1.37341964245,
  dash: [3.4, 10],
  /** Top → bottom */
  wires: [
    {
      id: "466:37733",
      matrix: [
        0.999723613262, -0.0235103741288, 0.0167667362839, 0.999859452248, 11.37890625,
        4.6015625,
      ],
      d: "M 0.00028893828857690096 0 C -0.12888483225833625 1.837087869644165 43.09036636352539 3.7681546211242676 55.72230911254883 10.353615760803223 C 68.35425186157227 16.939076900482178 85.85188674926758 55.5427303314209 102.17642211914062 77.18728637695312 C 118.50095748901367 98.83184242248535 140.00416564941406 96.68557739257812 140.00416564941406 96.68557739257812 L 149.09913635253906 96.82103729248047",
    },
    {
      id: "466:37727",
      matrix: [
        0.999723613262, -0.0235103741288, 0.0167667362839, 0.999859452248, 11, 79.2265625,
      ],
      d: "M 0.000309460939451924 0 C -0.13290497926315648 0.7470762512126294 42.77955358242141 0.5514684563419876 57.46536063082776 4.210436007258696 C 72.1511676792341 7.869403558175405 88.53741720239591 22.587194647288158 105.37259936790765 31.389242112312107 C 122.20778153341939 40.19128957733606 144.38362930287272 39.31848171060508 144.38362930287272 39.31848171060508 L 153.7631072998047 39.373565673828125",
    },
    {
      id: "466:37738",
      matrix: [
        0.999723613262, -0.0235103741288, -0.0167667362839, -0.999859452248, 14.48046875,
        157.064453125,
      ],
      d: "M 0.0003052728421166825 0 C -0.13110633040749892 0.5380553334227276 42.20060252803542 0.3971755122331593 56.68766118855893 3.0324178608324805 C 71.17471984908244 5.667660209431801 87.33921175697373 16.267629349552635 103.94655770728822 22.606993537212535 C 120.55390365760272 28.946357724872435 142.42963201768612 28.317750052455345 142.42963201768612 28.317750052455345 L 151.6821746826172 28.357421875",
    },
    {
      id: "466:37722",
      matrix: [
        0.999723613262, 0.0235103741288, 0.0167667362839, -0.999859452248, 14, 232.97265625,
      ],
      d: "M 0.0002922335252025084 0 C -0.13035472009554577 1.8637708977447613 43.58179891968654 3.8228846742967493 56.35780574847236 10.503997762718559 C 69.13381257725817 17.18511085114037 86.83101032286721 56.34948295962266 103.34172082856051 78.30841659196166 C 119.85243133425381 100.26735022430066 141.6008733745496 98.08990194071293 141.6008733745496 98.08990194071293 L 150.79957580566406 98.22732543945312",
    },
  ],
  /** Outer source nodes (ring) + hub-side join dots */
  sources: [
    { cx: 7.238, cy: 6 },
    { cx: 6.238, cy: 80 },
    { cx: 8.238, cy: 156 },
    { cx: 7.238, cy: 233.001 },
  ],
  joins: [
    { cx: 171.301, cy: 98 },
    { cx: 171.302, cy: 114 },
    { cx: 171.301, cy: 125 },
    { cx: 171.301, cy: 146.406 },
  ],
};

const RIGHT_FAN = {
  x: 822,
  y: 261,
  w: 147,
  h: 90,
  strokeWidth: 1.05808460712,
  dash: [3.4, 10],
  /** Top branch then bottom — Figma path runs card→hub; reverse motion for flow */
  wires: [
    {
      id: "466:37838",
      matrix: [
        -0.999866187572, -0.016357216984, -0.024098807946, 0.999709546566, 147, 2.38671875,
      ],
      d: "M 0.00028281229322946725 0 C -0.12615225194039592 0.8518299082950612 42.17677423541813 1.7472361324103867 54.540899134653905 4.800815191701221 C 66.90502403388967 7.854394250992056 84.03168846843835 25.75432841888238 100.01011490033865 35.790581709302174 C 115.98854133223895 45.82683499972197 137.035833727654 44.83164418760241 137.035833727654 44.83164418760241 L 145.93797302246094 44.89445114135742",
    },
    {
      id: "466:37837",
      matrix: [
        -0.999866187572, 0.016357216984, -0.024098807946, -0.999709546566, 147, 87.150390625,
      ],
      d: "M 0.00028281226803383554 0 C -0.1261522439116181 0.85182995558051 42.17677164374403 1.747236017849696 54.54089640473347 4.800815126499955 C 66.90502116572291 7.854394235150213 84.03168522105696 25.754329395846362 100.01011086629866 35.79058271310549 C 115.98853651154036 45.826836030364625 137.03583067143387 44.83164426849857 137.03583067143387 44.83164426849857 L 145.93797302246094 44.89445114135742",
    },
  ],
};

function matrixAttr(m) {
  return `matrix(${m.join(" ")})`;
}

function dashAttr(dash) {
  return dash.join(" ");
}

/** Static endpoint assets that aren't part of the animated stroke frames */
const connectors = [
  {
    id: "right-dot-top",
    src: `${ASSET}/wire-right-dot.svg`,
    left: 969,
    top: 257,
    width: 12,
    height: 12,
  },
  {
    id: "right-dot-bot",
    src: `${ASSET}/wire-right-dot.svg`,
    left: 968,
    top: 343,
    width: 12,
    height: 12,
  },
  {
    id: "right-hub",
    src: `${ASSET}/wire-right-hub.svg`,
    left: 814,
    top: 301,
    width: 8,
    height: 8,
  },
  {
    id: "down",
    src: `${ASSET}/wire-down.svg`,
    left: 639,
    top: 427,
    width: 12,
    height: 64,
  },
];
</script>

<template>
  <div
    class="csd"
    :class="{ 'csd--ready': ready && !reduceMotion }"
    role="img"
    aria-label="Collections platform connecting customers, Urbanrupee, merchants, and payment methods"
  >
    <div ref="scalerRef" class="csd__scaler">
      <div
        class="csd__artboard"
        :style="{
          transform: `scale(${scale})`,
          marginBottom: `${813 * scale - 813}px`,
        }"
      >
        <div class="csd__wires" aria-hidden="true">
          <!-- Left fan — exact Figma 466:37720 -->
          <svg
            class="csd__fan csd__fan--left"
            :viewBox="`0 0 ${LEFT_FAN.w} ${LEFT_FAN.h}`"
            fill="none"
            :style="{
              left: `${LEFT_FAN.x}px`,
              top: `${LEFT_FAN.y}px`,
              width: `${LEFT_FAN.w}px`,
              height: `${LEFT_FAN.h}px`,
            }"
          >
            <g
              v-for="(wire, i) in LEFT_FAN.wires"
              :key="wire.id"
              :transform="matrixAttr(wire.matrix)"
            >
              <path
                class="csd__dash"
                :d="wire.d"
                fill="none"
                stroke="#ffffff"
                :stroke-width="LEFT_FAN.strokeWidth"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="dashAttr(LEFT_FAN.dash)"
              />
              <circle
                v-show="ready && !reduceMotion"
                class="csd__flow-dot"
                r="2.4"
              >
                <animateMotion
                  :dur="`${2.8 + i * 0.28}s`"
                  :begin="`${i * 0.4}s`"
                  repeatCount="indefinite"
                  :path="wire.d"
                />
              </circle>
            </g>
            <g class="csd__nodes">
              <g v-for="(n, i) in LEFT_FAN.sources" :key="`ls-${i}`">
                <circle
                  :cx="n.cx"
                  :cy="n.cy"
                  r="6"
                  fill="#80DBED"
                  stroke="#ffffff"
                  stroke-width="1.5"
                />
                <circle :cx="n.cx" :cy="n.cy" r="4.2" fill="#38B7D3" />
              </g>
              <circle
                v-for="(n, i) in LEFT_FAN.joins"
                :key="`lj-${i}`"
                :cx="n.cx"
                :cy="n.cy"
                r="4"
                fill="#80DBED"
              />
            </g>
          </svg>

          <!-- Right fork — exact Figma 466:37836 -->
          <svg
            class="csd__fan csd__fan--right"
            :viewBox="`0 0 ${RIGHT_FAN.w} ${RIGHT_FAN.h}`"
            fill="none"
            :style="{
              left: `${RIGHT_FAN.x}px`,
              top: `${RIGHT_FAN.y}px`,
              width: `${RIGHT_FAN.w}px`,
              height: `${RIGHT_FAN.h}px`,
            }"
          >
            <g
              v-for="(wire, i) in RIGHT_FAN.wires"
              :key="wire.id"
              :transform="matrixAttr(wire.matrix)"
            >
              <path
                class="csd__dash csd__dash--rtl"
                :d="wire.d"
                fill="none"
                stroke="#ffffff"
                :stroke-width="RIGHT_FAN.strokeWidth"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="dashAttr(RIGHT_FAN.dash)"
              />
              <circle
                v-show="ready && !reduceMotion"
                class="csd__flow-dot"
                r="2.2"
              >
                <!-- Path runs card→hub; reverse so the dot travels hub→business -->
                <animateMotion
                  :dur="`${2.8 + i * 0.28}s`"
                  :begin="`${0.2 + i * 0.4}s`"
                  repeatCount="indefinite"
                  calcMode="linear"
                  keyPoints="1;0"
                  keyTimes="0;1"
                  :path="wire.d"
                />
              </circle>
            </g>
          </svg>

          <img
            v-for="conn in connectors"
            :key="conn.id"
            class="csd__wire"
            :class="`csd__wire--${conn.id}`"
            :src="conn.src"
            alt=""
            decoding="async"
            :style="{
              left: `${conn.left}px`,
              top: `${conn.top}px`,
              width: `${conn.width}px`,
              height: `${conn.height}px`,
            }"
          />
        </div>

        <!-- YOUR CUSTOMERS — Figma 370:2403 @ 66,90 -->
        <section class="csd__customers">
          <div class="csd__tab">YOUR CUSTOMERS</div>
          <div class="csd__customers-body">
            <div class="csd__customers-list">
              <article
                v-for="item in customers"
                :key="item.title"
                class="csd__row"
              >
                <img :src="item.icon" alt="" :width="item.w" :height="item.w" />
                <div>
                  <p class="csd__row-title">{{ item.title }}</p>
                  <p class="csd__row-body">{{ item.body }}</p>
                </div>
              </article>
            </div>
            <p class="csd__more">and more...</p>
          </div>
        </section>

        <!-- HUB — Figma 330:2651 -->
        <section class="csd__hub">
          <div class="csd__logo">
            <img
              class="csd__logo-u"
              :src="`${ASSET}/logo-mark.svg`"
              alt=""
              width="31"
              height="37"
            />
            <img
              class="csd__logo-arrow"
              :src="`${ASSET}/logo-arrow.svg`"
              alt=""
              width="17"
              height="22"
            />
            <p class="csd__logo-text">
              <span class="csd__logo-teal">rban</span><span>rupee</span>
            </p>
          </div>
          <p class="csd__hub-title">Collections Platform</p>
          <div class="csd__features">
            <article
              v-for="(feat, i) in features"
              :key="feat.label"
              class="csd__feature"
              :style="{ '--d': `${i * 0.4}s` }"
            >
              <img :src="feat.icon" alt="" width="24" height="24" />
              <p>{{ feat.label }}</p>
            </article>
          </div>
        </section>

        <!-- YOUR BUSINESS — Figma 466:37633 @ 981,138 -->
        <section class="csd__business">
          <div class="csd__tab">YOUR BUSINESS</div>
          <div class="csd__business-body">
            <div class="csd__business-head">
              <img :src="`${ASSET}/shop.svg`" alt="" width="72" height="72" />
              <p class="csd__business-title">Merchant / Enterprise</p>
            </div>
            <ul class="csd__checks">
              <li v-for="c in businessChecks" :key="c">
                <span class="csd__check" aria-hidden="true">
                  <img :src="`${ASSET}/check.svg`" alt="" width="6" height="5" />
                </span>
                {{ c }}
              </li>
            </ul>
          </div>
        </section>

        <!-- PAYMENT METHODS — Figma 466:37783 -->
        <section class="csd__methods">
          <div class="csd__tab csd__tab--methods">PAYMENT METHODS</div>
          <div class="csd__methods-grid">
            <article
              v-for="m in methods"
              :key="m.label"
              class="csd__method"
              :style="{ width: `${m.chip}px` }"
            >
              <img :src="m.icon" alt="" :width="m.w" :height="m.h" />
              <p>{{ m.label }}</p>
            </article>
          </div>
          <p class="csd__more">and more...</p>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.csd {
  width: 100%;
  max-width: 1291px;
  margin: 0 auto;
}

.csd__scaler {
  width: 100%;
  overflow: hidden;
  border-radius: 14px;
}

.csd__artboard {
  position: relative;
  width: 1291px;
  height: 813px;
  transform-origin: top left;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.csd__wires {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.csd__fan {
  position: absolute;
  display: block;
  overflow: visible;
}

.csd--ready .csd__dash {
  animation: csd-dash-march 1.1s linear infinite;
}

.csd--ready .csd__dash--rtl {
  animation-name: csd-dash-march-rtl;
}

.csd__flow-dot {
  fill: #80dbed;
  filter: drop-shadow(0 0 3px rgba(128, 219, 237, 0.95));
}

.csd__wire {
  position: absolute;
  display: block;
  max-width: none;
  object-fit: fill;
  transform-origin: center center;
}

.csd--ready .csd__wire--down {
  animation: csd-wire-flow 1.35s ease-in-out infinite;
  animation-delay: 0.45s;
}

.csd--ready .csd__wire--right-dot-top,
.csd--ready .csd__wire--right-dot-bot,
.csd--ready .csd__wire--right-hub {
  animation: csd-wire-flow 1.35s ease-in-out infinite;
  animation-delay: 0.2s;
}

@keyframes csd-dash-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes csd-dash-march-rtl {
  to {
    stroke-dashoffset: 13.4;
  }
}

@keyframes csd-wire-flow {
  0%,
  100% {
    opacity: 0.78;
    filter: brightness(0.96);
  }
  50% {
    opacity: 1;
    filter: brightness(1.18);
  }
}

.csd__tab {
  position: absolute;
  top: 0;
  left: 50%;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 182px;
  height: 43px;
  transform: translateX(-50%);
  border-radius: 7px;
  background: #097495;
  border: 1px solid #097495;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
}

.csd__customers {
  position: absolute;
  left: 66px;
  top: 90px;
  width: 243px;
  z-index: 2;
}

.csd__customers-body {
  margin-top: 23px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  padding: 28px 20px;
  background: #fff;
  border: 0.879px solid #e9eaeb;
  border-radius: 14px;
  box-sizing: border-box;
  min-height: 356px;
}

.csd__customers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.csd__row {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  height: 62px;
  padding: 12px;
  box-sizing: border-box;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 3.2px 1.6px #e9eaeb;
}

.csd__row img {
  flex-shrink: 0;
  object-fit: contain;
}

.csd__row-title,
.csd__row-body,
.csd__more,
.csd__hub-title,
.csd__business-title,
.csd__feature p,
.csd__method p,
.csd__logo-text,
.csd__checks {
  margin: 0;
}

.csd__row-title {
  font-size: 14px;
  font-weight: 600;
  color: #252b37;
}

.csd__row-body {
  font-size: 10px;
  font-weight: 500;
  line-height: 16px;
  color: #535862;
}

.csd__more {
  font-size: 12px;
  font-weight: 600;
  color: #252b37;
  text-align: center;
}

.csd__hub {
  position: absolute;
  left: 479px;
  top: 137px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  width: 330px;
  padding: 24px 40px;
  box-sizing: border-box;
  background: #fff;
  border: 0.515px solid #097495;
  border-radius: 12.7px;
  box-shadow:
    -3.7px -3.7px 2.2px rgba(9, 116, 149, 0.06),
    3.7px 3.7px 2.2px rgba(9, 116, 149, 0.06);
}

.csd__logo {
  display: flex;
  align-items: center;
  gap: 2px;
  width: 200px;
}

.csd__logo-u {
  width: 30.5px;
  height: 36.7px;
  object-fit: contain;
}

.csd__logo-arrow {
  width: 17px;
  height: 22px;
  object-fit: contain;
}

.csd__logo-text {
  font-size: 28px;
  font-weight: 800;
  line-height: 31px;
  color: #141414;
  white-space: nowrap;
}

.csd__logo-teal {
  color: #097495;
}

.csd__hub-title {
  width: 100%;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  text-transform: capitalize;
  color: #252b37;
}

.csd__features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 13px;
  width: 100%;
}

.csd__feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 62px;
  height: auto;
  padding: 10px 16px;
  box-sizing: border-box;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 1.9px 0.95px #e9eaeb;
  overflow: hidden;
}

.csd__feature img {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  object-fit: contain;
}

.csd__feature p {
  width: 100%;
  font-size: 10px;
  font-weight: 500;
  line-height: 1.2;
  text-align: center;
  color: #252b37;
}

.csd--ready .csd__feature {
  animation: csd-feat-float 4.8s ease-in-out infinite;
  animation-delay: var(--d, 0s);
}

@keyframes csd-feat-float {
  0%,
  100% {
    transform: translateY(0);
    box-shadow: 0 1.9px 0.95px #e9eaeb;
  }
  50% {
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(9, 116, 149, 0.12);
  }
}

.csd__business {
  position: absolute;
  left: 981px;
  top: 138px;
  width: 231px;
  z-index: 2;
}

.csd__business .csd__tab {
  top: -29px;
}

.csd__business-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  height: 312px;
  padding: 16px;
  box-sizing: border-box;
  background: #fff;
  border: 0.879px solid #e9eaeb;
  border-radius: 14px;
}

.csd__business-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.csd__business-title {
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  text-transform: capitalize;
  color: #252b37;
}

.csd__checks {
  list-style: none;
  padding: 10px 20px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  min-height: 148px;
  box-sizing: border-box;
  background: #fff;
  border-radius: 10.3px;
  box-shadow: 0 3.2px 1.6px #e9eaeb;
}

.csd__checks li {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #535862;
}

.csd__check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  flex-shrink: 0;
  border-radius: 8px;
  background: #215a02;
}

.csd__methods {
  position: absolute;
  left: 508px;
  top: 529px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 283px;
  height: 165px;
  padding: 20px 24px;
  box-sizing: border-box;
  background: #fff;
  border: 0.8px solid #e9eaeb;
  border-radius: 12px;
}

.csd__tab--methods {
  top: -32px;
}

.csd__methods-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 26px;
  justify-content: center;
  width: 100%;
}

.csd__method {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 42px;
  padding: 12px 16px;
  box-sizing: border-box;
  background: #fff;
  border: 1.1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 3.2px 4px #e9eaeb;
}

.csd__method img {
  flex-shrink: 0;
  object-fit: contain;
}

.csd__method p {
  font-size: 12px;
  font-weight: 600;
  color: #252b37;
  white-space: nowrap;
}

@media (max-width: 900px) {
  .csd__artboard {
    width: 100%;
    height: auto;
    transform: none !important;
    margin-bottom: 0 !important;
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 28px 16px 24px;
    box-sizing: border-box;
  }

  .csd__wires {
    display: none;
  }

  .csd__customers,
  .csd__hub,
  .csd__business,
  .csd__methods {
    position: relative;
    left: auto;
    top: auto;
    width: 100%;
  }

  .csd__hub {
    order: -1;
  }

  .csd__tab--methods {
    position: relative;
    top: 0;
    transform: none;
    margin: 0 auto 8px;
  }

  .csd__customers-body,
  .csd__business-body {
    margin-top: 12px;
    height: auto;
    min-height: 0;
  }

  .csd__methods {
    height: auto;
  }

  .csd__method {
    width: 125px !important;
  }

  .csd__methods-grid {
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .csd__wire,
  .csd__dash,
  .csd__feature {
    animation: none !important;
  }
}
</style>
