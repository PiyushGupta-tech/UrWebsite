<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const ASSET = "/images/figma-hyper-checkout/showcase";
const STAGE = { w: 1291, h: 638 };

/** Card stack — CSS nodes sit at each card mid-Y; fan viewBox matches this height. */
const CARD_H = 66;
const CARD_GAP = 16;
const CARD_STACK_H = CARD_H * 4 + CARD_GAP * 3; // 312
const CARD_MIDS = [0, 1, 2, 3].map((i) => i * (CARD_H + CARD_GAP) + CARD_H / 2);
/** Hub is lifted in CSS; fan paths must meet that visual centre. */
const HUB_LIFT = 10;
const HUB_ATTACH_Y = CARD_STACK_H / 2 - HUB_LIFT; // 146

/**
 * Absolutized Figma strokes (652:8034 / 652:8189) in each frame's space.
 * Remapped at runtime so endpoints snap to card nodes + hub.
 * Order: top → bottom.
 */
const LEFT_FIGMA = [
  {
    id: "652:8036",
    start: [8.087, 7.855],
    end: [79.137, 107.703],
    d: "M 8.0870 7.8550 C 8.0553 9.7863 28.2447 11.2770 34.2391 18.0374 C 40.2334 24.7978 48.9946 65.1303 56.9452 87.6632 C 64.8959 110.1960 74.8926 107.6740 74.8926 107.6740 L 79.1370 107.7031",
  },
  {
    id: "652:8041",
    start: [4.133, 89.479],
    end: [79.219, 119.102],
    d: "M 4.1330 89.4790 C 4.0764 90.0846 25.7264 90.0827 32.0807 92.0609 C 38.4350 94.0390 47.3668 106.4681 55.6365 113.3410 C 63.9062 120.2139 74.6642 119.1918 74.6642 119.1918 L 79.2190 119.1023",
  },
  {
    id: "652:8051",
    start: [14.4347, 172.8857],
    end: [78.9284, 135.7444],
    d: "M 14.4347 172.8857 C 14.3894 172.1443 32.9407 171.9033 38.3959 169.4080 C 43.8511 166.9127 51.5692 151.5831 58.6911 143.0689 C 65.8130 134.5546 75.0259 135.6860 75.0259 135.6860 L 78.9284 135.7444",
  },
  {
    id: "652:8046",
    start: [14.7306, 255.1543],
    end: [78.9674, 144.6417],
    d: "M 14.7306 255.1543 C 14.7063 253.0226 32.9004 251.2928 38.3163 243.8054 C 43.7322 236.3180 51.7150 191.7610 58.9282 166.8552 C 66.1414 141.9494 75.1430 144.6916 75.1430 144.6916 L 78.9674 144.6417",
  },
];

const RIGHT_FIGMA = [
  {
    id: "652:8190",
    start: [120.7215, 6.0503],
    end: [3.1715, 97.6785],
    d: "M 120.7215 6.0503 C 120.7919 7.8430 87.1448 8.9343 77.2122 15.1210 C 67.2796 21.3077 53.0392 58.6083 39.9884 79.4031 C 26.9376 100.1978 10.2477 97.7129 10.2477 97.7129 L 3.1715 97.6785",
  },
  {
    id: "652:8194",
    start: [124.1209, 78.1265],
    end: [7.5781, 109.6895],
    d: "M 124.1209 78.1265 C 124.2104 78.7794 90.5834 78.6728 80.7193 80.7741 C 70.8552 82.8753 57.0164 96.2272 44.1908 103.5943 C 31.3652 110.9613 14.6529 109.8079 14.6529 109.8079 L 7.5781 109.6895",
  },
  {
    id: "652:8203",
    start: [123.9519, 164.4585],
    end: [7.1716, 118.7271],
    d: "M 123.9519 164.4585 C 124.0370 163.5367 90.4052 163.3607 80.5250 160.2958 C 70.6447 157.2308 56.7112 138.2299 43.8324 127.6954 C 30.9537 117.1610 14.2467 118.6285 14.2467 118.6285 L 7.1716 118.7271",
  },
  {
    id: "652:8198",
    start: [124.95, 243.3604],
    end: [7.1057, 127.8844],
    d: "M 124.9500 243.3604 C 125.0148 241.1121 91.3619 239.5876 81.4092 231.7814 C 71.4566 223.9753 57.0989 177.1221 43.9823 150.9782 C 30.8657 124.8342 14.1823 127.8740 14.1823 127.8740 L 7.1057 127.8844",
  },
];

const FAN_DASH = [3.4, 10];
const FAN_STROKE = 1.37;

const leftFanEl = ref(null);
const rightFanEl = ref(null);
const leftFanW = ref(80);
const rightFanW = ref(110);
let fanObserver = null;

function parsePath(d) {
  const tokens = d.match(/[MLC]|[-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?/gi) || [];
  const cmds = [];
  let i = 0;
  while (i < tokens.length) {
    const cmd = tokens[i].toUpperCase();
    i += 1;
    const nums = [];
    while (i < tokens.length && !/^[MLC]$/i.test(tokens[i])) {
      nums.push(Number(tokens[i]));
      i += 1;
    }
    cmds.push({ cmd, nums });
  }
  return cmds;
}

function formatPath(cmds) {
  return cmds
    .map(({ cmd, nums }) => `${cmd}${nums.map((n) => n.toFixed(2)).join(" ")}`)
    .join("");
}

/** Map Figma curve onto layout endpoints while keeping relative shape. */
function remapPath(d, fromStart, fromEnd, toStart, toEnd) {
  const [x0, y0] = fromStart;
  const [x1, y1] = fromEnd;
  const [X0, Y0] = toStart;
  const [X1, Y1] = toEnd;
  const dx = x1 - x0 || 1e-6;
  const dy = y1 - y0 || 1e-6;
  const sx = (X1 - X0) / dx;
  const sy = (Y1 - Y0) / dy;
  const cmds = parsePath(d).map(({ cmd, nums }) => ({
    cmd,
    nums: nums.map((n, i) => {
      if (i % 2 === 0) return X0 + (n - x0) * sx;
      return Y0 + (n - y0) * sy;
    }),
  }));
  return formatPath(cmds);
}

/** Reverse cubic path so animateMotion can run hub → card on right wires. */
function reversePath(d) {
  const cmds = parsePath(d);
  const points = [];
  let cur = null;
  for (const { cmd, nums } of cmds) {
    if (cmd === "M") {
      cur = [nums[0], nums[1]];
      points.push({ type: "M", p: cur });
    } else if (cmd === "L") {
      const p = [nums[0], nums[1]];
      points.push({ type: "L", from: cur, to: p });
      cur = p;
    } else if (cmd === "C") {
      const c1 = [nums[0], nums[1]];
      const c2 = [nums[2], nums[3]];
      const p = [nums[4], nums[5]];
      points.push({ type: "C", from: cur, c1, c2, to: p });
      cur = p;
    }
  }
  const end = points[points.length - 1].to || points[points.length - 1].p;
  const out = [{ cmd: "M", nums: end }];
  for (let i = points.length - 1; i >= 1; i -= 1) {
    const seg = points[i];
    if (seg.type === "L") {
      out.push({ cmd: "L", nums: seg.from });
    } else if (seg.type === "C") {
      out.push({
        cmd: "C",
        nums: [...seg.c2, ...seg.c1, ...seg.from],
      });
    }
  }
  return formatPath(out);
}

function buildWires(figma, width, toHub) {
  /** Card ::after nodes hang ~5px off the card; fan margins pull ~2px over. */
  const nodeX = 3;
  return figma.map((wire, i) => {
    const cardY = CARD_MIDS[i];
    const d = toHub
      ? remapPath(wire.d, wire.start, wire.end, [nodeX, cardY], [width, HUB_ATTACH_Y])
      : reversePath(
          remapPath(
            wire.d,
            wire.start,
            wire.end,
            [width - nodeX, cardY],
            [0, HUB_ATTACH_Y],
          ),
        );
    return {
      id: wire.id,
      d,
      strokeWidth: FAN_STROKE,
      dash: FAN_DASH,
    };
  });
}

const leftWires = computed(() => buildWires(LEFT_FIGMA, leftFanW.value, true));
const rightWires = computed(() => buildWires(RIGHT_FIGMA, rightFanW.value, false));

function dashAttr(dash) {
  return dash.join(" ");
}

const features = [
  {
    title: "Auto-detects user context",
    body: "Device, location, behaviour",
    icon: `${ASSET}/icon-context.svg`,
  },
  {
    title: "Predicts best payment method",
    body: "Device, location, behaviour",
    icon: `${ASSET}/icon-predict.svg`,
  },
  {
    title: "Intelligent Routing",
    body: "To the best performing payment path",
    icon: `${ASSET}/icon-routing.svg`,
  },
  {
    title: "Real-time optimization",
    body: "For a seamless experience",
    icon: `${ASSET}/icon-optimize.svg`,
  },
];

const modes = ["UPI", "Cards", "Netbanking", "Wallets", "EMI"];

const apps = [
  { id: "gpay", label: "GPay", logo: `${ASSET}/logo-gpay.png` },
  { id: "phonepe", label: "PhonePe", logo: `${ASSET}/logo-phonepe.png` },
  { id: "paytm", label: "Paytm", logo: `${ASSET}/logo-paytm.png` },
  { id: "bhim", label: "BHIM", logo: `${ASSET}/logo-bhim.png` },
];

const providers = [
  { id: "razorpay", name: "Razorpay", rate: 98.7, logo: `${ASSET}/psp-razorpay.png` },
  { id: "payu", name: "PayU", rate: 94.3, logo: `${ASSET}/psp-payu.png` },
  { id: "cashfree", name: "Cashfree", rate: 95.4, logo: `${ASSET}/psp-cashfree.png` },
  { id: "unlimit", name: "Unlimit", rate: 94.1, logo: `${ASSET}/psp-unlimit.png` },
];

/** Winning rate always clears the chasing band, so there is a single clear leader. */
const LEAD_RATE = { min: 97.9, span: 1.3 }; // 97.9 – 99.2
const CHASE_RATE = { min: 93.2, span: 3.4 }; // 93.2 – 96.6

/** The phone body only ever shows the UPI panel, so the mode stays on UPI. */
const ACTIVE_MODE = modes.indexOf("UPI");
const activeApp = ref(0);
const liveProvider = ref(0);
/** Provider handed the winning rate for the current round. */
const leadProvider = ref(0);
const rates = ref(providers.map((p) => p.rate));
const displayRates = ref(providers.map((p) => p.rate));
const paused = ref(false);
const reduceMotion = ref(false);
let appTimer = null;
let routeTimer = null;
let rateFrame = null;

/** Card that blinks green — the one showing the highest success rate. */
const bestProvider = computed(() =>
  rates.value.reduce((best, rate, i) => (rate > rates.value[best] ? i : best), 0),
);

function formatRate(value) {
  return `${Number(value).toFixed(1)}%`;
}

function nextApp() {
  activeApp.value = (activeApp.value + 1) % apps.length;
}

/** Re-deal rates so a different provider leads, keeping the win unambiguous. */
function dealRates(lead) {
  return providers.map((_, i) => {
    const band = i === lead ? LEAD_RATE : CHASE_RATE;
    return Math.round((band.min + Math.random() * band.span) * 10) / 10;
  });
}

function nextRoute() {
  liveProvider.value = (liveProvider.value + 1) % providers.length;
  // A full pass through the cards hands the lead — and the green blink — onward.
  if (liveProvider.value === 0) {
    leadProvider.value = (leadProvider.value + 1) % providers.length;
    rates.value = dealRates(leadProvider.value);
    animateRates();
  }
}

function animateRates(fromZero = false) {
  if (rateFrame) cancelAnimationFrame(rateFrame);
  rateFrame = null;
  const target = rates.value;
  if (reduceMotion.value) {
    displayRates.value = [...target];
    return;
  }
  const from = fromZero ? target.map(() => 0) : [...displayRates.value];
  const duration = fromZero ? 1400 : 800;
  const start = performance.now();
  function tick(now) {
    const t = Math.min(1, (now - start) / duration);
    const eased = 1 - (1 - t) ** 3;
    displayRates.value = target.map((v, i) => from[i] + (v - from[i]) * eased);
    rateFrame = t < 1 ? requestAnimationFrame(tick) : null;
  }
  rateFrame = requestAnimationFrame(tick);
}

function startTimers() {
  stopTimers();
  if (reduceMotion.value || paused.value) return;
  appTimer = window.setInterval(nextApp, 2500);
  routeTimer = window.setInterval(nextRoute, 3000);
}

function stopTimers() {
  if (appTimer) clearInterval(appTimer);
  if (routeTimer) clearInterval(routeTimer);
  appTimer = routeTimer = null;
}

function onEnter() {
  paused.value = true;
  stopTimers();
}

function onLeave() {
  paused.value = false;
  startTimers();
}

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  animateRates(true);
  startTimers();

  if (typeof ResizeObserver !== "undefined") {
    fanObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = Math.round(entry.contentRect.width);
        if (w <= 0) continue;
        if (entry.target === leftFanEl.value) leftFanW.value = w;
        else if (entry.target === rightFanEl.value) rightFanW.value = w;
      }
    });
    if (leftFanEl.value) fanObserver.observe(leftFanEl.value);
    if (rightFanEl.value) fanObserver.observe(rightFanEl.value);
  }
});

onBeforeUnmount(() => {
  stopTimers();
  if (rateFrame) cancelAnimationFrame(rateFrame);
  rateFrame = null;
  if (fanObserver) fanObserver.disconnect();
  fanObserver = null;
});
</script>

<template>
  <div
    class="hc-stage"
    role="img"
    aria-label="Adaptive Hyper Checkout with smart routing and payment modes"
    :style="{ aspectRatio: `${STAGE.w} / ${STAGE.h}` }"
    @mouseenter="onEnter"
    @mouseleave="onLeave"
    @focusin="onEnter"
    @focusout="onLeave"
  >
    <!-- Left rail: CSS grid so fan fills card→hub gap -->
    <div class="hc-stage__rail hc-stage__rail--left">
      <p class="hc-stage__heading hc-stage__heading--left">smart checkout that adapts</p>
      <ul class="hc-stage__cards hc-stage__cards--left">
        <li
          v-for="(card, index) in features"
          :key="card.title"
          class="hc-stage__card"
          :style="{ '--delay': `${0.05 + index * 0.07}s` }"
        >
          <img :src="card.icon" alt="" width="16" height="16" decoding="async" />
          <div class="hc-stage__card-text">
            <p class="hc-stage__card-title">{{ card.title }}</p>
            <p class="hc-stage__card-body">{{ card.body }}</p>
          </div>
        </li>
      </ul>

      <svg
        ref="leftFanEl"
        class="hc-stage__fan hc-stage__fan--left"
        :viewBox="`0 0 ${leftFanW} ${CARD_STACK_H}`"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <path
          v-for="(wire, i) in leftWires"
          :key="`${wire.id}-stroke`"
          class="hc-stage__path"
          :d="wire.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="wire.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(wire.dash)"
          vector-effect="non-scaling-stroke"
        />
        <circle
          v-for="(wire, i) in leftWires"
          v-show="!reduceMotion"
          :key="`${wire.id}-dot`"
          class="hc-stage__flow-dot"
          r="3.2"
          vector-effect="non-scaling-stroke"
        >
          <animateMotion
            :dur="`${2.9 + i * 0.32}s`"
            :begin="`${i * 0.46}s`"
            repeatCount="indefinite"
            :path="wire.d"
          />
        </circle>
      </svg>

      <div class="hc-stage__hub-wrap hc-stage__hub-wrap--left">
        <div class="hc-stage__hub">
          <div class="hc-stage__hub-ring" />
          <div class="hc-stage__hub-core">
            <img :src="`${ASSET}/logo-r.svg`" alt="" width="24" height="29" decoding="async" />
          </div>
        </div>
      </div>

      <!-- Hub → phone bridge; shares a 1fr track with the fan so the hub centres -->
      <div class="hc-stage__bridge hc-stage__bridge--left" aria-hidden="true">
        <span class="hc-stage__bridge-track">
          <svg class="hc-stage__bridge-rule" viewBox="0 0 100 4" preserveAspectRatio="none">
            <line
              class="hc-stage__path"
              x1="0"
              y1="2"
              x2="100"
              y2="2"
              stroke="currentColor"
              stroke-linecap="round"
              vector-effect="non-scaling-stroke"
            />
          </svg>
          <span v-show="!reduceMotion" class="hc-stage__bridge-dot" />
        </span>
        <svg class="hc-stage__bridge-head" viewBox="0 0 10 14">
          <path
            d="M2.4 2.2 L7.8 7 L2.4 11.8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
    </div>

    <!-- Center phone -->
    <div class="hc-stage__phone">
      <header class="hc-stage__phone-head">
        <div class="hc-stage__brand">
          <span class="hc-stage__brand-mark">
            <img :src="`${ASSET}/brand-cart.svg`" alt="" width="13" height="13" decoding="async" />
          </span>
          <span class="hc-stage__brand-name">YourBrand</span>
        </div>
        <div class="hc-stage__secure">
          <img :src="`${ASSET}/shield.svg`" alt="" width="11" height="11" decoding="async" />
          <span>Secure Checkout</span>
        </div>
      </header>

      <div class="hc-stage__amount">
        <div>
          <p class="hc-stage__amount-label">Order Amount</p>
          <p class="hc-stage__amount-value">₹2,499.00</p>
        </div>
        <button type="button" class="hc-stage__details" tabindex="-1">
          View Details
          <img :src="`${ASSET}/chevron.svg`" alt="" width="13" height="13" decoding="async" />
        </button>
      </div>

      <div class="hc-stage__modes-wrap">
        <p class="hc-stage__section-label">Payment Mode</p>
        <div class="hc-stage__modes" role="tablist" aria-label="Payment modes">
          <button
            v-for="(mode, index) in modes"
            :key="mode"
            type="button"
            class="hc-stage__mode"
            :class="{ 'hc-stage__mode--active': index === ACTIVE_MODE }"
            role="tab"
            :aria-selected="index === ACTIVE_MODE"
            tabindex="-1"
          >
            {{ mode }}
          </button>
        </div>
      </div>

      <div class="hc-stage__upi">
        <div class="hc-stage__upi-card">
          <span class="hc-stage__badge">RECOMMENDED</span>
          <div class="hc-stage__upi-row">
            <span class="hc-stage__upi-icon">
              <img :src="`${ASSET}/logo-bhim.png`" alt="" width="23" height="23" decoding="async" />
            </span>
            <div>
              <p class="hc-stage__upi-title">Enter UPI ID</p>
              <p class="hc-stage__upi-sub">Instant payment · High success rate</p>
            </div>
          </div>
          <div class="hc-stage__upi-input-row">
            <div class="hc-stage__upi-input">
              <span>yourname@upi</span>
              <span class="hc-stage__caret" aria-hidden="true" />
            </div>
            <button type="button" class="hc-stage__verify" tabindex="-1">Verify</button>
          </div>
        </div>

        <div class="hc-stage__apps-block">
          <p class="hc-stage__section-label hc-stage__section-label--apps">Quick Pay via App</p>
          <div class="hc-stage__apps">
            <button
              v-for="(app, index) in apps"
              :key="app.id"
              type="button"
              class="hc-stage__app"
              :class="{ 'hc-stage__app--active': index === activeApp }"
              @click="activeApp = index"
            >
              <img :src="app.logo" :alt="app.label" width="30" height="30" decoding="async" />
              <span>{{ app.label }}</span>
            </button>
          </div>
        </div>

        <button type="button" class="hc-stage__pay" tabindex="-1">Pay ₹2,499.00</button>
      </div>

      <footer class="hc-stage__phone-foot">
        <img :src="`${ASSET}/shield-secure.svg`" alt="" width="11" height="11" decoding="async" />
        <p>Secured by <strong>Urbanrupee</strong></p>
      </footer>
    </div>

    <!-- Right rail: CSS grid so fan fills hub→card gap -->
    <div class="hc-stage__rail hc-stage__rail--right">
      <!-- Phone → hub bridge -->
      <div class="hc-stage__bridge hc-stage__bridge--right" aria-hidden="true">
        <span class="hc-stage__bridge-track">
          <svg class="hc-stage__bridge-rule" viewBox="0 0 100 4" preserveAspectRatio="none">
            <line
              class="hc-stage__path"
              x1="0"
              y1="2"
              x2="100"
              y2="2"
              stroke="currentColor"
              stroke-linecap="round"
              vector-effect="non-scaling-stroke"
            />
          </svg>
          <span v-show="!reduceMotion" class="hc-stage__bridge-dot hc-stage__bridge-dot--delayed" />
        </span>
        <svg class="hc-stage__bridge-head" viewBox="0 0 10 14">
          <path
            d="M2.4 2.2 L7.8 7 L2.4 11.8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>

      <div class="hc-stage__hub-wrap hc-stage__hub-wrap--right">
        <div class="hc-stage__hub">
          <div class="hc-stage__hub-ring" />
          <div class="hc-stage__hub-core">
            <img
              :src="`${ASSET}/check-outline.svg`"
              alt=""
              width="32"
              height="32"
              decoding="async"
            />
          </div>
        </div>
      </div>

      <svg
        ref="rightFanEl"
        class="hc-stage__fan hc-stage__fan--right"
        :viewBox="`0 0 ${rightFanW} ${CARD_STACK_H}`"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <path
          v-for="(wire, i) in rightWires"
          :key="`${wire.id}-stroke`"
          class="hc-stage__path"
          :class="{ 'hc-stage__path--best': i === bestProvider }"
          :d="wire.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="wire.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(wire.dash)"
          vector-effect="non-scaling-stroke"
        />
        <circle
          v-for="(wire, i) in rightWires"
          v-show="!reduceMotion"
          :key="`${wire.id}-dot`"
          class="hc-stage__flow-dot"
          :class="{ 'hc-stage__flow-dot--best': i === bestProvider }"
          r="3.2"
          vector-effect="non-scaling-stroke"
        >
          <animateMotion
            :dur="`${2.9 + i * 0.32}s`"
            :begin="`${i * 0.46}s`"
            repeatCount="indefinite"
            :path="wire.d"
          />
        </circle>
      </svg>

      <p class="hc-stage__heading hc-stage__heading--right">intelligent routing maximum success</p>
      <ul class="hc-stage__cards hc-stage__cards--psp">
        <li
          v-for="(psp, index) in providers"
          :key="psp.id"
          class="hc-stage__card hc-stage__card--psp"
          :class="{
            'hc-stage__card--live': index === liveProvider,
            'hc-stage__card--best': index === bestProvider,
          }"
          :style="{ '--delay': `${0.12 + index * 0.07}s` }"
        >
          <img
            class="hc-stage__psp-logo"
            :src="psp.logo"
            :alt="psp.name"
            width="20"
            height="20"
            decoding="async"
          />
          <div class="hc-stage__card-text">
            <p class="hc-stage__card-title">{{ psp.name }}</p>
            <p class="hc-stage__card-body">
              Success Rate:
              <span
                class="hc-stage__rate"
                :class="{ 'hc-stage__rate--best': index === bestProvider }"
              >{{ formatRate(displayRates[index]) }}</span>
            </p>
          </div>
          <span
            v-if="index === bestProvider"
            class="hc-stage__live-dot"
            aria-hidden="true"
          />
        </li>
      </ul>
      <p class="hc-stage__more">and more...</p>
    </div>
  </div>
</template>

<style scoped>
.hc-stage {
  --hc-teal: #097495;
  --hc-cyan: #38b7d3;
  --hc-green: #12b76a;
  /* Badge green reads on white surfaces (badge fill, card border, rate text). */
  --hc-badge-green: #2d6a4f;
  --hc-badge-green-rgb: 45, 106, 79;
  /* The dark badge green disappears against the teal stage, so anything that
     glows or draws on the background uses this brighter tint of the same hue. */
  --hc-green-bright: #3ddc97;
  --hc-green-bright-rgb: 61, 220, 151;
  /* Hub rise above the card-stack midpoint; mirrors HUB_LIFT in script. */
  --hc-hub-lift: 10px;
  --hc-ink: #252b37;
  position: relative;
  width: 100%;
  border-radius: 14.141px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: var(--hc-ink);
  user-select: none;
}

/* —— Side rails (CSS grid: heading / cards | fan | hub / more) —— */
.hc-stage__rail {
  --hc-stack: 312px;
  --hc-card-col: minmax(200px, 230px);
  /* Fixed label rows keep the card stack — and the hub — dead-centre of the stage,
     so the bridges can anchor to 50% without depending on heading line count. */
  --hc-label-row: 44px;
  position: absolute;
  top: 0;
  bottom: 0;
  display: grid;
  align-content: center;
  align-items: center;
  column-gap: 0;
  row-gap: 12px;
  grid-template-rows: var(--hc-label-row) var(--hc-stack) var(--hc-label-row);
  z-index: 2;
  min-width: 0;
}

/* Rails reach the phone edge, and the two 1fr tracks either side of the hub
   are equal — so each hub lands mid-way between its cards and the phone. */
.hc-stage__rail--left {
  left: 2.2%;
  width: 36.5%;
  grid-template-columns: var(--hc-card-col) minmax(48px, 1fr) auto minmax(48px, 1fr);
}

.hc-stage__rail--right {
  right: 2.2%;
  width: 36.5%;
  grid-template-columns: minmax(48px, 1fr) auto minmax(48px, 1fr) minmax(140px, 160px);
}

.hc-stage__heading {
  margin: 0;
  width: 100%;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.2;
  text-align: center;
  text-transform: capitalize;
  color: #ffffff;
}

.hc-stage__heading--left {
  grid-column: 1;
  grid-row: 1;
  align-self: end;
}

.hc-stage__heading--right {
  grid-column: 4;
  grid-row: 1;
  align-self: end;
}

.hc-stage__cards {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  height: var(--hc-stack);
  min-width: 0;
}

.hc-stage__cards--left {
  grid-column: 1;
  grid-row: 2;
}

.hc-stage__cards--psp {
  grid-column: 4;
  grid-row: 2;
}

.hc-stage__more {
  grid-column: 4;
  grid-row: 3;
  margin: 0;
  font-size: 10px;
  font-weight: 600;
  color: #ffffff;
  text-align: center;
  align-self: start;
  line-height: 1.2;
}

.hc-stage__card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  height: 66px;
  min-height: 66px;
  max-height: 66px;
  padding: 8px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2.5px 1.3px #e9eaeb;
  animation: hc-card-in 0.65s ease both;
  animation-delay: var(--delay, 0s);
}

/* Card-side connector nodes (hub join has none). */
.hc-stage__cards--left .hc-stage__card::after,
.hc-stage__cards--psp .hc-stage__card::after {
  content: "";
  position: absolute;
  top: 50%;
  width: 11px;
  height: 11px;
  border-radius: 50%;
  background: var(--hc-cyan);
  border: 1.5px solid #ffffff;
  box-shadow: 0 0 0 1px #80dbed;
  transform: translateY(-50%);
  z-index: 2;
  pointer-events: none;
}

.hc-stage__cards--left .hc-stage__card::after {
  right: -5px;
}

.hc-stage__cards--psp .hc-stage__card::after {
  left: -5px;
}

/* Node matches its wire, so the winning path reads green end to end. */
.hc-stage__cards--psp .hc-stage__card--best::after {
  background: var(--hc-green-bright);
  box-shadow: 0 0 0 1px rgba(var(--hc-green-bright-rgb), 0.9);
}

.hc-stage__card--psp {
  padding: 0 10px;
  border-radius: 9px;
  transition:
    transform 0.35s ease,
    box-shadow 0.35s ease;
}

.hc-stage__card--live {
  transform: translateX(-2px);
  box-shadow:
    0 4px 12px rgba(9, 116, 149, 0.18),
    0 2.5px 1.3px #e9eaeb;
}

/* Winner ring lives on ::before so the card's entry animation is untouched. */
.hc-stage__card--psp::before {
  content: "";
  position: absolute;
  inset: 0;
  border: 1.5px solid transparent;
  border-radius: inherit;
  pointer-events: none;
  transition: border-color 0.3s ease;
}

.hc-stage__card--best::before {
  border-color: var(--hc-badge-green);
  animation: hc-best-glow 2s ease-in-out infinite;
}

.hc-stage__card > img:first-child,
.hc-stage__psp-logo {
  display: block;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.hc-stage__psp-logo {
  width: 20px;
  height: 20px;
}

.hc-stage__card-text {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
  flex: 1;
}

.hc-stage__card-title {
  margin: 0;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: #252b37;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  overflow: hidden;
}

.hc-stage__card-body {
  margin: 0;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  font-size: 10px;
  font-weight: 500;
  line-height: normal;
  color: #535862;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.hc-stage__rate {
  font-weight: 700;
}

.hc-stage__rate--best {
  color: var(--hc-badge-green);
}

.hc-stage__live-dot {
  flex-shrink: 0;
  width: 7px;
  height: 7px;
  margin-left: auto;
  border-radius: 50%;
  background: var(--hc-badge-green);
  /* Static halo so the glow survives reduced-motion, where the pulse is off. */
  box-shadow: 0 0 5px 1.5px rgba(var(--hc-green-bright-rgb), 0.85);
  /* Same 2s period as the card ring, so dot and border pulse together. */
  animation: hc-dot-pulse 2s ease-in-out infinite;
}

.hc-stage__fan {
  width: 100%;
  height: var(--hc-stack);
  max-height: var(--hc-stack);
  overflow: visible;
  display: block;
  min-width: 0;
  align-self: stretch;
}

.hc-stage__fan--left {
  grid-column: 2;
  grid-row: 2;
  margin-left: -2px;
  margin-right: -6px;
}

.hc-stage__fan--right {
  grid-column: 3;
  grid-row: 2;
  margin-left: -6px;
  margin-right: -2px;
}

/* Short dashes on a thicker stroke so the round caps read as pills (bridges). */
.hc-stage__path {
  stroke: #ffffff;
  stroke-width: 2.6;
  stroke-dasharray: 3.4 10;
  animation: hc-wire-march 1.4s linear infinite;
  transition: stroke 0.4s ease;
}

/* Sparse dash so the march reads clearly on fan connectors. */
.hc-stage__fan .hc-stage__path {
  stroke-width: 1.37;
  stroke-dasharray: 3.4 10;
  animation: hc-fan-march 1.1s linear infinite;
}

/* Wire feeding the winning provider. */
.hc-stage__path--best {
  stroke: var(--hc-green-bright);
  filter: drop-shadow(0 0 3px rgba(var(--hc-green-bright-rgb), 0.85));
}

.hc-stage__flow-dot {
  fill: var(--hc-cyan);
  filter: drop-shadow(0 0 4px rgba(56, 183, 211, 0.95));
  transition: fill 0.4s ease;
}

.hc-stage__flow-dot--best {
  fill: var(--hc-green-bright);
  filter: drop-shadow(0 0 5px rgba(var(--hc-green-bright-rgb), 0.95));
}

.hc-stage__hub-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  height: var(--hc-stack);
  grid-row: 2;
}

.hc-stage__hub-wrap--left {
  grid-column: 3;
}

.hc-stage__hub-wrap--right {
  grid-column: 2;
}

/* —— Hub ↔ phone bridges —— */
.hc-stage__bridge {
  grid-row: 2;
  display: flex;
  align-items: center;
  gap: 2px;
  height: 14px;
  min-width: 0;
  /* Match the hub's rise off the card-stack midpoint. */
  transform: translateY(calc(-1 * var(--hc-hub-lift)));
  /* Track and arrowhead inherit white; only the travelling dot stays blue. */
  color: #ffffff;
  pointer-events: none;
}

.hc-stage__bridge--left {
  grid-column: 4;
}

.hc-stage__bridge--right {
  grid-column: 1;
}

.hc-stage__bridge-track {
  position: relative;
  flex: 1 1 auto;
  min-width: 0;
  height: 4px;
}

/* A flat horizontal line, so stretching it can't distort the round dash caps. */
.hc-stage__bridge-rule {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.hc-stage__bridge-dot {
  position: absolute;
  top: 50%;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #62e9fe;
  filter: drop-shadow(0 0 4px rgba(98, 233, 254, 0.95));
  animation: hc-bridge-dot 2.2s linear infinite;
}

.hc-stage__bridge-dot--delayed {
  animation-delay: 0.45s;
}

.hc-stage__bridge-head {
  flex: 0 0 auto;
  width: 10px;
  height: 14px;
  animation: hc-bridge-pulse 2.1s ease-in-out infinite;
}

.hc-stage__hub {
  position: relative;
  width: clamp(52px, 5.4vw, 70px);
  /* aspect-ratio + no shrink keeps the ring a true circle. */
  aspect-ratio: 1;
  height: auto;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  /* Raise visual hub so the fan join sits a little above centre */
  transform: translateY(calc(-1 * var(--hc-hub-lift)));
  z-index: 2;
}

.hc-stage__hub-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(238deg, #80dbed 7%, rgba(255, 255, 255, 0.87) 58%, #00b7db 93%);
  animation: hc-hub-pulse 3.1s ease-in-out infinite;
}

.hc-stage__hub-core {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  width: 74%;
  height: 74%;
  border-radius: 50%;
  background: #ffffff;
}

.hc-stage__hub-core img {
  display: block;
  width: 46%;
  height: auto;
}

.hc-stage__hub-wrap--right .hc-stage__hub-core img {
  width: 58%;
}

/* —— Phone —— */
.hc-stage__phone {
  position: absolute;
  left: calc(50% - 11.3%);
  top: 9.6%;
  width: 22.6%;
  height: 80.9%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border: 0.8px solid var(--hc-teal);
  border-radius: 19.6px;
  overflow: hidden;
  box-shadow: 0 18px 40px rgba(9, 29, 52, 0.18);
  z-index: 4;
  animation: hc-phone-in 0.8s ease both;
}

.hc-stage__phone-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 3.5% 4.8%;
  border-bottom: 0.8px solid #f3f4f6;
  flex-shrink: 0;
}

.hc-stage__brand {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.hc-stage__brand-mark {
  display: grid;
  place-items: center;
  width: clamp(18px, 1.95vw, 25px);
  height: clamp(18px, 1.95vw, 25px);
  border-radius: 9px;
  background: var(--hc-teal);
  flex-shrink: 0;
}

.hc-stage__brand-mark img {
  width: 52%;
  height: auto;
}

.hc-stage__brand-name {
  font-size: clamp(9px, 0.97vw, 12.6px);
  font-weight: 700;
  color: #1e2939;
  white-space: nowrap;
}

.hc-stage__secure {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 7px;
  border: 0.8px solid #2d6a4f;
  border-radius: 999px;
  background: rgba(45, 106, 79, 0.1);
  color: #2d6a4f;
  font-size: clamp(6px, 0.62vw, 8px);
  font-weight: 600;
  white-space: nowrap;
}

.hc-stage__amount {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 3.5% 4.8%;
  border-bottom: 0.8px solid #f3f4f6;
  flex-shrink: 0;
}

.hc-stage__amount-label {
  margin: 0;
  font-size: clamp(6px, 0.62vw, 8px);
  font-weight: 500;
  letter-spacing: 0.24px;
  text-transform: uppercase;
  color: #99a1af;
}

.hc-stage__amount-value {
  margin: 2px 0 0;
  font-size: clamp(14px, 1.55vw, 20px);
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1.35;
  color: #101828;
}

.hc-stage__details {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  border: 0;
  background: transparent;
  color: var(--hc-teal);
  font: inherit;
  font-size: clamp(9px, 0.93vw, 12px);
  font-weight: 500;
  cursor: default;
  white-space: nowrap;
}

.hc-stage__modes-wrap {
  padding: 3.5% 4.8% 1.5%;
  flex-shrink: 0;
}

.hc-stage__section-label {
  margin: 0;
  font-size: clamp(6px, 0.62vw, 8px);
  font-weight: 700;
  letter-spacing: 0.79px;
  text-transform: uppercase;
  color: #99a1af;
}

.hc-stage__section-label--apps {
  font-size: clamp(7px, 0.78vw, 10px);
  font-weight: 600;
  letter-spacing: 0.94px;
}

.hc-stage__modes {
  display: flex;
  gap: 3px;
  margin-top: 8px;
  overflow: hidden;
}

/* Sized so all five modes fit the phone width, as in the reference. */
.hc-stage__mode {
  flex: 0 0 auto;
  height: clamp(20px, 2.1vw, 27px);
  padding: 0 clamp(4px, 0.55vw, 6px);
  border: 0.8px solid #f3f4f6;
  border-radius: 9px;
  background: #f9fafb;
  color: #6a7282;
  font: inherit;
  font-size: clamp(6px, 0.62vw, 8px);
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  transition:
    background 0.25s ease,
    color 0.25s ease,
    border-color 0.25s ease;
}

.hc-stage__mode--active {
  background: var(--hc-teal);
  border-color: var(--hc-teal);
  color: #ffffff;
}

.hc-stage__upi {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  min-height: 0;
  padding: 2.5% 4.8% 3%;
}

.hc-stage__upi-card {
  position: relative;
  padding: 3.5% 4%;
  border: 1.6px solid var(--hc-teal);
  border-radius: 10px;
  background: rgba(9, 116, 149, 0.06);
  overflow: hidden;
  flex-shrink: 0;
}

.hc-stage__badge {
  position: absolute;
  top: 0;
  right: 0;
  padding: 3px 8px;
  border-radius: 0 0 0 6px;
  background: var(--hc-badge-green);
  color: #ffffff;
  font-size: clamp(6px, 0.62vw, 8px);
  font-weight: 700;
  letter-spacing: 0.2px;
  animation: hc-badge-pulse 2.4s ease-in-out infinite;
}

.hc-stage__upi-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hc-stage__upi-icon {
  display: grid;
  place-items: center;
  width: clamp(22px, 2.4vw, 31px);
  height: clamp(22px, 2.4vw, 31px);
  border-radius: 6px;
  background: #ffffff;
  border: 0.8px solid #dbeafe;
  box-shadow: 0 0.8px 1.2px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.hc-stage__upi-icon img {
  width: 72%;
  height: auto;
  object-fit: contain;
}

.hc-stage__upi-title {
  margin: 0;
  font-size: clamp(9px, 0.93vw, 12px);
  font-weight: 600;
  color: #1e2939;
}

.hc-stage__upi-sub {
  margin: 0;
  font-size: clamp(6px, 0.62vw, 8px);
  color: #99a1af;
}

.hc-stage__upi-input-row {
  display: flex;
  gap: 6px;
  margin-top: 10px;
}

.hc-stage__upi-input {
  position: relative;
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  min-width: 0;
  height: clamp(24px, 2.55vw, 33px);
  padding: 0 9px;
  border: 0.8px solid #bedbff;
  border-radius: 6px;
  background: #ffffff;
  font-size: clamp(9px, 0.93vw, 12px);
  color: #d1d5dc;
}

.hc-stage__caret {
  width: 1.5px;
  height: 55%;
  margin-left: 1px;
  background: var(--hc-teal);
  animation: hc-caret 1s steps(1) infinite;
}

.hc-stage__verify {
  flex-shrink: 0;
  min-width: clamp(48px, 4.9vw, 63px);
  height: clamp(24px, 2.55vw, 33px);
  border: 0;
  border-radius: 6px;
  background: var(--hc-teal);
  opacity: 0.6;
  color: #ffffff;
  font: inherit;
  font-size: clamp(9px, 0.93vw, 12px);
  font-weight: 700;
  cursor: default;
}

.hc-stage__apps-block {
  padding-top: 4%;
  flex-shrink: 0;
}

.hc-stage__apps {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 5px;
  margin-top: 8px;
}

.hc-stage__app {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 7%;
  border: 0.8px solid #f3f4f6;
  border-radius: 9px;
  background: #ffffff;
  color: #6a7282;
  font: inherit;
  font-size: clamp(7px, 0.78vw, 10px);
  font-weight: 500;
  cursor: pointer;
  transition:
    border-color 0.25s ease,
    box-shadow 0.25s ease,
    transform 0.25s ease;
}

.hc-stage__app img {
  display: block;
  width: 62%;
  max-width: 30px;
  height: auto;
  aspect-ratio: 1;
  object-fit: contain;
}

.hc-stage__app--active {
  border-color: var(--hc-teal);
  box-shadow: 0 0 0 1px rgba(9, 116, 149, 0.2);
  transform: translateY(-1px);
}

.hc-stage__pay {
  margin-top: auto;
  width: 100%;
  height: clamp(28px, 2.9vw, 38px);
  border: 0;
  border-radius: 9px;
  background: #e5e7eb;
  color: #99a1af;
  font: inherit;
  font-size: clamp(9px, 0.85vw, 11px);
  font-weight: 600;
  cursor: default;
  flex-shrink: 0;
}

.hc-stage__phone-foot {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 3% 4.8%;
  border-top: 0.8px solid #f3f4f6;
  background: #f9fafb;
  flex-shrink: 0;
}

.hc-stage__phone-foot p {
  margin: 0;
  font-size: clamp(7px, 0.78vw, 10px);
  color: #99a1af;
}

.hc-stage__phone-foot strong {
  font-weight: 700;
  color: #4a5565;
}

/* Offset must be a whole number of dash periods to loop seamlessly. */
@keyframes hc-wire-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes hc-fan-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes hc-card-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes hc-phone-in {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes hc-hub-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.92;
  }
  50% {
    transform: scale(1.07);
    opacity: 1;
  }
}

@keyframes hc-bridge-pulse {
  0%,
  100% {
    opacity: 0.72;
  }
  50% {
    opacity: 1;
  }
}

@keyframes hc-bridge-dot {
  from {
    left: 0;
    transform: translate(-50%, -50%);
    opacity: 0;
  }
  12%,
  88% {
    opacity: 1;
  }
  to {
    left: 100%;
    transform: translate(-50%, -50%);
    opacity: 0;
  }
}

/* Soft halo that breathes, plus a ring that rides outward and fades. */
@keyframes hc-dot-pulse {
  0%,
  100% {
    box-shadow:
      0 0 4px 1px rgba(var(--hc-green-bright-rgb), 0.6),
      0 0 0 0 rgba(var(--hc-green-bright-rgb), 0.6);
  }
  50% {
    box-shadow:
      0 0 8px 2.5px rgba(var(--hc-green-bright-rgb), 1),
      0 0 0 6px rgba(var(--hc-green-bright-rgb), 0);
  }
}

@keyframes hc-best-glow {
  0%,
  100% {
    border-color: rgba(var(--hc-badge-green-rgb), 0.4);
    box-shadow:
      0 0 4px 0 rgba(var(--hc-green-bright-rgb), 0.35),
      inset 0 0 0 0 rgba(var(--hc-green-bright-rgb), 0);
  }
  50% {
    border-color: var(--hc-badge-green);
    box-shadow:
      0 0 13px 3px rgba(var(--hc-green-bright-rgb), 0.95),
      inset 0 0 7px rgba(var(--hc-green-bright-rgb), 0.3);
  }
}

@keyframes hc-badge-pulse {
  0%,
  100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.12);
  }
}

@keyframes hc-caret {
  0%,
  49% {
    opacity: 1;
  }
  50%,
  100% {
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hc-stage__card,
  .hc-stage__phone,
  .hc-stage__hub-ring,
  .hc-stage__bridge-head,
  .hc-stage__bridge-dot,
  .hc-stage__path,
  .hc-stage__fan .hc-stage__path,
  .hc-stage__live-dot,
  .hc-stage__badge,
  .hc-stage__caret,
  .hc-stage__card--best::before {
    animation: none !important;
  }

  .hc-stage__card--live {
    transform: none;
  }

  .hc-stage__flow-dot {
    display: none;
  }
}

@media (max-width: 900px) {
  .hc-stage {
    aspect-ratio: auto !important;
    min-height: 0;
    padding: 28px 16px 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
  }

  .hc-stage__rail,
  .hc-stage__phone {
    position: static;
    width: 100%;
    height: auto;
    max-width: 360px;
  }

  .hc-stage__fan,
  .hc-stage__hub-wrap,
  .hc-stage__bridge {
    display: none;
  }

  .hc-stage__rail {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }

  .hc-stage__cards {
    height: auto;
  }

  .hc-stage__cards--left .hc-stage__card::after,
  .hc-stage__cards--psp .hc-stage__card::after {
    display: none;
  }

  .hc-stage__phone {
    order: -1;
    left: auto;
    height: auto;
    min-height: 480px;
  }

  .hc-stage__cards {
    width: 100%;
  }

  .hc-stage__card {
    height: auto;
    min-height: 66px;
    max-height: none;
    padding: 8px;
  }

  .hc-stage__card-title {
    font-size: 14px;
  }

  .hc-stage__card-body {
    font-size: 10px;
    white-space: normal;
  }
}
</style>
