<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const BASE = "/images/figma-about-v2";

/* Figma 1020:9263: 866 × 806 stage; x/y are tile centres, r is rotation in degrees.
   Each back tile travels with the white tile named in `pair`. */
const backTiles = [
  { x: 585.03, y: 695.03, r: -34.67, pair: "Jio" },
  { x: 329.48, y: 694.48, r: -16.17, pair: "Unlimit" },
  { x: 801.08, y: 348.04, r: 0, pair: "Airpay" },
  { x: 768.32, y: 570.28, r: -22.3, pair: "Razorpay" },
  { x: 117.8, y: 587.8, r: -8.28, pair: "Kotak" },
  { x: 84.09, y: 333.09, r: -0.83, pair: "PayU" },
  { x: 167.04, y: 137.04, r: 0, pair: "Easebuzz" },
  { x: 430.04, y: 74.04, r: 0, pair: "IDFC FIRST Bank" },
  { x: 695.04, y: 141.04, r: 0, pair: "Cashfree" },
];

/* logo boxes are in the tile's own 146 × 146 space, before the tile rotation */
const tiles = [
  {
    name: "Easebuzz",
    x: 185.04,
    y: 138.04,
    r: 0,
    logo: { src: "logo-easebuzz.png", left: 40.41, top: 45.15, w: 66.751, h: 54.693,
      crop: { w: 476.13, h: 307.09, left: 0, top: -107.09 } },
  },
  { name: "IDFC FIRST Bank", x: 443.04, y: 73.04, r: 0, idfc: true },
  {
    name: "Cashfree",
    x: 715.04,
    y: 138.04,
    r: 0,
    logo: { src: "logo-cashfree.png", left: 44.7, top: 44.66, w: 57.171, h: 57.171 },
  },
  {
    name: "PayU",
    x: 73.04,
    y: 341.04,
    r: 0,
    logo: { src: "logo-payu.png", left: 23.23, top: 43.97, w: 101.014, h: 58.023,
      crop: { w: 186.96, h: 169.98, left: -47.02, top: -34.2 } },
  },
  {
    name: "Airpay",
    x: 793.04,
    y: 341.04,
    r: 0,
    logo: { src: "logo-airpay.png", left: 26.37, top: 60.94, w: 93.796, h: 28.978 },
  },
  {
    name: "Kotak",
    x: 103.21,
    y: 590.21,
    r: -7.74,
    logo: { src: "logo-kotak.png", left: 17.29, top: 54.08, w: 109.983, h: 36.871, r: 7.74,
      crop: { w: 128.08, h: 382.05, left: -13.47, top: -142.74 } },
  },
  { name: "Razorpay", x: 755.84, y: 574.84, r: 39.68, tile: "tile-razorpay.svg" },
  {
    name: "Unlimit",
    x: 317.23,
    y: 698.23,
    r: -15.88,
    logo: { src: "logo-un.png", left: 39.81, top: 57.37, w: 66.542, h: 32.38, r: 21.89 },
  },
  {
    name: "Jio",
    x: 576.51,
    y: 704.51,
    r: -34.36,
    logo: { src: "logo-jio.png", left: 40.23, top: 39.5, w: 66.997, h: 66.997, r: 34.36 },
  },
];

const TILE = 146.072;
const ORBIT_CENTRE = { x: 433, y: 403 };
const ORBIT_SECONDS = 70;
const SAMPLES_PER_SEGMENT = 48;

function tileStyle(t) {
  return {
    left: `${t.x - TILE / 2}px`,
    top: `${t.y - TILE / 2}px`,
  };
}

function faceStyle(t) {
  return t.r ? { transform: `rotate(${t.r}deg)` } : undefined;
}

/* Closed Catmull-Rom loop through the white tile centres, ordered clockwise around the copy,
   so every tile travels through the others' Figma positions without leaving the stage. */
function buildOrbit() {
  const ring = [...tiles].sort(
    (a, b) =>
      Math.atan2(a.y - ORBIT_CENTRE.y, a.x - ORBIT_CENTRE.x) -
      Math.atan2(b.y - ORBIT_CENTRE.y, b.x - ORBIT_CENTRE.x),
  );
  const n = ring.length;
  const points = [];
  const starts = new Map();

  for (let i = 0; i < n; i += 1) {
    const p0 = ring[(i - 1 + n) % n];
    const p1 = ring[i];
    const p2 = ring[(i + 1) % n];
    const p3 = ring[(i + 2) % n];
    starts.set(p1.name, points.length);
    for (let s = 0; s < SAMPLES_PER_SEGMENT; s += 1) {
      const t = s / SAMPLES_PER_SEGMENT;
      const t2 = t * t;
      const t3 = t2 * t;
      points.push({
        x: 0.5 * (2 * p1.x + (p2.x - p0.x) * t + (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 + (3 * p1.x - p0.x - 3 * p2.x + p3.x) * t3),
        y: 0.5 * (2 * p1.y + (p2.y - p0.y) * t + (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 + (3 * p1.y - p0.y - 3 * p2.y + p3.y) * t3),
      });
    }
  }

  const lengths = [0];
  for (let i = 1; i <= points.length; i += 1) {
    const a = points[i - 1];
    const b = points[i % points.length];
    lengths.push(lengths[i - 1] + Math.hypot(b.x - a.x, b.y - a.y));
  }
  const total = lengths[points.length];
  const startFraction = new Map([...starts].map(([name, index]) => [name, lengths[index] / total]));

  function pointAt(fraction) {
    const target = (((fraction % 1) + 1) % 1) * total;
    let lo = 0;
    let hi = points.length;
    while (lo < hi - 1) {
      const mid = (lo + hi) >> 1;
      if (lengths[mid] <= target) lo = mid;
      else hi = mid;
    }
    const a = points[lo];
    const b = points[(lo + 1) % points.length];
    const span = lengths[lo + 1] - lengths[lo] || 1;
    const k = (target - lengths[lo]) / span;
    return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k };
  }

  return { startFraction, pointAt };
}

const orbit = buildOrbit();
const tileEls = new Map();
const backEls = new Map();
const root = ref(null);
let frame = 0;
let lastTime = 0;
let progress = 0;
let inView = false;
let observer = null;
let motionQuery = null;

function setTileEl(name, el, store) {
  if (el) store.set(name, el);
  else store.delete(name);
}

function render() {
  for (const t of tiles) {
    const p = orbit.pointAt(orbit.startFraction.get(t.name) + progress);
    const transform = `translate3d(${(p.x - t.x).toFixed(2)}px, ${(p.y - t.y).toFixed(2)}px, 0)`;
    const el = tileEls.get(t.name);
    if (el) el.style.transform = transform;
    const back = backEls.get(t.name);
    if (back) back.style.transform = transform;
  }
}

function tick(now) {
  const dt = lastTime ? Math.min((now - lastTime) / 1000, 0.1) : 0;
  lastTime = now;
  progress = (progress + dt / ORBIT_SECONDS) % 1;
  render();
  frame = requestAnimationFrame(tick);
}

function start() {
  if (frame || !inView || motionQuery?.matches) return;
  lastTime = 0;
  frame = requestAnimationFrame(tick);
}

function stop() {
  if (frame) cancelAnimationFrame(frame);
  frame = 0;
}

function onMotionChange() {
  if (motionQuery.matches) {
    stop();
    progress = 0;
    render();
  } else {
    start();
  }
}

onMounted(() => {
  motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  motionQuery.addEventListener("change", onMotionChange);
  if (typeof IntersectionObserver === "undefined") {
    inView = true;
    start();
    return;
  }
  observer = new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    if (inView) start();
    else stop();
  });
  observer.observe(root.value);
});

onBeforeUnmount(() => {
  stop();
  observer?.disconnect();
  motionQuery?.removeEventListener("change", onMotionChange);
});

function logoStyle(logo) {
  return {
    left: `${logo.left}px`,
    top: `${logo.top}px`,
    width: `${logo.w}px`,
    height: `${logo.h}px`,
    transform: logo.r ? `rotate(${logo.r}deg)` : undefined,
  };
}

function cropStyle(crop) {
  return {
    width: `${crop.w}%`,
    height: `${crop.h}%`,
    left: `${crop.left}%`,
    top: `${crop.top}%`,
  };
}
</script>

<template>
  <div ref="root" class="partners-graphic" role="img" aria-label="Urbanrupee banking and payment partners">
    <span
      v-for="(t, i) in backTiles"
      :key="`back-${i}`"
      :ref="(el) => setTileEl(t.pair, el, backEls)"
      class="partners-graphic__tile"
      :style="tileStyle(t)"
      aria-hidden="true"
    >
      <span class="partners-graphic__face" :style="faceStyle(t)">
        <img
          class="partners-graphic__shape"
          :src="`${BASE}/tile-back.svg`"
          alt=""
          width="168.237"
          height="187.806"
          decoding="async"
        />
      </span>
    </span>

    <span
      v-for="(t, i) in tiles"
      :key="t.name"
      :ref="(el) => setTileEl(t.name, el, tileEls)"
      class="partners-graphic__tile"
      :style="tileStyle(t)"
    >
      <span class="partners-graphic__bob" :style="{ '--bob-delay': `${i * -0.47}s` }">
        <span class="partners-graphic__face" :style="faceStyle(t)">
          <img
            class="partners-graphic__shape"
            :src="`${BASE}/${t.tile || 'tile.svg'}`"
            :alt="t.tile ? t.name : ''"
            width="168.237"
            height="187.806"
            decoding="async"
          />

          <span
            v-if="t.logo"
            class="partners-graphic__logo"
            :class="{ 'partners-graphic__logo--crop': t.logo.crop }"
            :style="logoStyle(t.logo)"
          >
            <img
              :src="`${BASE}/${t.logo.src}`"
              :alt="t.name"
              :style="t.logo.crop ? cropStyle(t.logo.crop) : undefined"
              loading="lazy"
              decoding="async"
            />
          </span>

          <span v-if="t.idfc" class="partners-graphic__idfc" :aria-label="t.name" role="img">
            <span class="partners-graphic__idfc-mark" aria-hidden="true">
              <span class="partners-graphic__idfc-bars">
                <i />
                <i />
                <i class="partners-graphic__idfc-bar--short" />
              </span>
            </span>
            <span class="partners-graphic__idfc-text" aria-hidden="true">
              <span>IDFC FIRST</span>
              <span>Bank</span>
            </span>
          </span>
        </span>
      </span>
    </span>
  </div>
</template>

<style scoped>
.partners-graphic {
  position: relative;
  width: 866px;
  height: 806px;
}

.partners-graphic__tile {
  position: absolute;
  width: 146.072px;
  height: 146.072px;
  will-change: transform;
}

.partners-graphic__bob,
.partners-graphic__face {
  position: absolute;
  inset: 0;
  display: block;
}

.partners-graphic__bob {
  animation: partners-bob 3.2s ease-in-out var(--bob-delay, 0s) infinite alternate;
}

@keyframes partners-bob {
  from {
    transform: translateY(-3px);
  }

  to {
    transform: translateY(3px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .partners-graphic__bob {
    animation: none;
  }
}

/* SVG carries its drop shadow, so it spills past the 146px tile (Figma inset -7.14% / -7.59% / -21.43%) */
.partners-graphic__shape {
  position: absolute;
  left: -11.087px;
  top: -10.434px;
  width: 168.237px;
  height: 187.806px;
  max-width: none;
  display: block;
}

.partners-graphic__logo {
  position: absolute;
  display: block;
}

.partners-graphic__logo img {
  display: block;
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
}

.partners-graphic__logo--crop {
  overflow: hidden;
}

.partners-graphic__logo--crop img {
  position: absolute;
  width: auto;
  height: auto;
}

.partners-graphic__idfc {
  position: absolute;
  left: 26.62px;
  top: 63.01px;
  width: 93.796px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 4.502px;
  padding: 4.502px;
  background: #000000;
  overflow: hidden;
}

.partners-graphic__idfc-mark {
  flex-shrink: 0;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24.012px;
  height: 24.762px;
  padding: 4.502px 3.752px;
  border: 1.501px solid #ffffff;
}

.partners-graphic__idfc-bars {
  display: flex;
  flex-direction: column;
  gap: 2.251px;
  width: 16.508px;
}

.partners-graphic__idfc-bars i {
  display: block;
  width: 100%;
  height: 3.752px;
  background: #ffffff;
}

.partners-graphic__idfc-bars .partners-graphic__idfc-bar--short {
  width: 4.502px;
}

.partners-graphic__idfc-text {
  display: flex;
  flex-direction: column;
  gap: 3.001px;
  width: 62.281px;
  font-family: "Inter", system-ui, sans-serif;
  font-size: 10.505px;
  font-weight: 600;
  line-height: 9.004px;
  letter-spacing: -0.3152px;
  color: #ffffff;
  white-space: nowrap;
}
</style>
