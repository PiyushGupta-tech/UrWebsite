<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps({
  path: { type: Object, required: true },
  ariaLabel: { type: String, default: "UPI transaction path" },
  /** Radians added to a badge's resting angle on phones, keyed by icon id (positive = clockwise). */
  phoneHomeOffsets: { type: Object, default: () => ({}) },
});

const PHONE_QUERY = "(max-width: 767px)";

/** Full Figma artboard — orbits live in this space */
const DESIGN_W = 1048;
/** Crop away faded top/bottom arcs that only add empty gap */
const CROP_TOP = 180;
const CROP_BOTTOM = 790;
const STAGE_W = DESIGN_W;
const STAGE_H = CROP_BOTTOM - CROP_TOP; // 610

const BADGE = 40;
const BADGE_HALF = BADGE / 2;
/** Slide distance along each badge’s visible arc (px in design space) */
const ARC_TRAVEL_PX = 52;

const ORBITS = {
  outer: { cx: 515.5, cy: 515.5, r: 515 },
  inner: { cx: 513.5, cy: 509.5, r: 405 },
};

const TIMING = {
  bank: { speed: 0.42, phase: 0.2 },
  trend: { speed: 0.36, phase: 1.5 },
  pod: { speed: 0.48, phase: 2.6 },
  route: { speed: 0.4, phase: 0.95 },
};

const reduceMotion = ref(false);
const isPhone = ref(false);
const badgePos = ref({});
let raf = 0;
let motion = [];
let phoneMql = null;

const icons = computed(() => props.path?.icons || []);

function parsePx(v) {
  return parseFloat(String(v));
}

function inCrop(x, y) {
  return (
    x >= 0 &&
    y >= CROP_TOP &&
    // Allow a few px past the right edge so edge badges (route) keep arc travel;
    // overflow:hidden on the stage clips any overhang.
    x <= STAGE_W - BADGE + 12 &&
    y <= CROP_BOTTOM - BADGE
  );
}

/** Shrink amplitude until both arc extremes keep the badge inside the crop */
function fitAmplitude(home, cx, cy, r, desiredAmp) {
  let amp = desiredAmp;
  for (let i = 0; i < 24; i += 1) {
    const a1 = home + amp;
    const a2 = home - amp;
    const x1 = cx + r * Math.cos(a1) - BADGE_HALF;
    const y1 = cy + r * Math.sin(a1) - BADGE_HALF;
    const x2 = cx + r * Math.cos(a2) - BADGE_HALF;
    const y2 = cy + r * Math.sin(a2) - BADGE_HALF;
    if (inCrop(x1, y1) && inCrop(x2, y2)) return amp;
    amp *= 0.85;
  }
  return Math.max(amp, 0.01);
}

function toStageStyle(x, y) {
  return {
    left: `${(x / STAGE_W) * 100}%`,
    top: `${((y - CROP_TOP) / STAGE_H) * 100}%`,
  };
}

function buildMotion(list) {
  return list.map((icon, i) => {
    const bx = parsePx(icon.left) + BADGE_HALF;
    const by = parsePx(icon.top) + BADGE_HALF;

    let key = "outer";
    let best = Infinity;
    for (const [k, o] of Object.entries(ORBITS)) {
      const err = Math.abs(Math.hypot(bx - o.cx, by - o.cy) - o.r);
      if (err < best) {
        best = err;
        key = k;
      }
    }

    const o = ORBITS[key];
    const offset = isPhone.value ? Number(props.phoneHomeOffsets?.[icon.id]) || 0 : 0;
    const home = Math.atan2(by - o.cy, bx - o.cx) + offset;
    const t = TIMING[icon.id] || { speed: 0.4 + i * 0.04, phase: i };
    const desiredAmp = ARC_TRAVEL_PX / o.r;

    return {
      id: icon.id,
      cx: o.cx,
      cy: o.cy,
      r: o.r,
      home,
      shifted: offset !== 0,
      amp: fitAmplitude(home, o.cx, o.cy, o.r, desiredAmp),
      speed: t.speed,
      phase: t.phase,
    };
  });
}

function restStyle(m) {
  return toStageStyle(
    m.cx + m.r * Math.cos(m.home) - BADGE_HALF,
    m.cy + m.r * Math.sin(m.home) - BADGE_HALF,
  );
}

function badgeStyle(icon) {
  const live = badgePos.value[icon.id];
  if (live) return { left: live.left, top: live.top };
  return toStageStyle(parsePx(icon.left), parsePx(icon.top));
}

function tick(now) {
  if (reduceMotion.value || !motion.length) return;
  const t = now / 1000;
  const next = {};
  for (const m of motion) {
    const angle = m.home + Math.sin(t * m.speed + m.phase) * m.amp;
    let x = m.cx + m.r * Math.cos(angle) - BADGE_HALF;
    let y = m.cy + m.r * Math.sin(angle) - BADGE_HALF;
    x = Math.min(STAGE_W - BADGE, Math.max(0, x));
    y = Math.min(CROP_BOTTOM - BADGE, Math.max(CROP_TOP, y));
    next[m.id] = toStageStyle(x, y);
  }
  badgePos.value = next;
  raf = requestAnimationFrame(tick);
}

function startMotion() {
  if (raf) cancelAnimationFrame(raf);
  motion = buildMotion(icons.value);
  if (!reduceMotion.value && motion.length) {
    raf = requestAnimationFrame(tick);
  } else {
    // Static badges rest at their data position unless a phone offset moved them.
    badgePos.value = Object.fromEntries(
      motion.filter((m) => m.shifted).map((m) => [m.id, restStyle(m)]),
    );
  }
}

function onPhoneChange(e) {
  isPhone.value = e.matches;
  startMotion();
}

watch(icons, startMotion, { deep: true });

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (typeof window !== "undefined") {
    phoneMql = window.matchMedia(PHONE_QUERY);
    isPhone.value = phoneMql.matches;
    phoneMql.addEventListener("change", onPhoneChange);
  }
  startMotion();
});

onBeforeUnmount(() => {
  if (raf) cancelAnimationFrame(raf);
  phoneMql?.removeEventListener("change", onPhoneChange);
});
</script>

<template>
  <section class="upi-path" :aria-label="ariaLabel">
    <div class="upi-path__stage">
      <!-- viewBox crops faded top/bottom arcs; side paths stay full-width -->
      <svg
        class="upi-path__orbits"
        :viewBox="`0 ${CROP_TOP} ${STAGE_W} ${STAGE_H}`"
        fill="none"
        aria-hidden="true"
        preserveAspectRatio="xMidYMid meet"
      >
        <defs>
          <linearGradient
            id="upiPathOrbitGrad"
            x1="524"
            y1="0"
            x2="524"
            y2="1031"
            gradientUnits="userSpaceOnUse"
          >
            <stop offset="0.24" stop-color="#EEEEEE" stop-opacity="0.2" />
            <stop offset="0.48" stop-color="#097495" stop-opacity="1" />
            <stop offset="0.71" stop-color="#EEEEEE" stop-opacity="0.2" />
          </linearGradient>
          <clipPath :id="'upiPathOrbitClip'">
            <rect
              :x="0"
              :y="CROP_TOP"
              :width="STAGE_W"
              :height="STAGE_H"
            />
          </clipPath>
        </defs>
        <g clip-path="url(#upiPathOrbitClip)">
          <circle
            cx="515.5"
            cy="515.5"
            r="515"
            stroke="url(#upiPathOrbitGrad)"
            stroke-width="1.5"
            vector-effect="non-scaling-stroke"
          />
          <circle
            cx="513.5"
            cy="509.5"
            r="405"
            stroke="url(#upiPathOrbitGrad)"
            stroke-width="1.5"
            vector-effect="non-scaling-stroke"
          />
        </g>
      </svg>

      <div
        v-for="icon in icons"
        :key="icon.id"
        class="upi-path__badge"
        :class="{ 'upi-path__badge--motion': !reduceMotion }"
        :style="badgeStyle(icon)"
      >
        <img
          :src="icon.src"
          alt=""
          :width="icon.width || 22"
          :height="icon.height || 22"
          decoding="async"
        />
      </div>

      <div class="upi-path__copy">
        <h2 class="upi-path__title">{{ path.title }}</h2>
        <!-- Phone copy comes first so adjacent-paragraph spacing never counts a hidden paragraph. -->
        <p
          v-for="(para, i) in path.phone_body || []"
          :key="`phone-${i}`"
          class="upi-path__body upi-path__body--phone"
        >
          {{ para }}
        </p>
        <p
          v-for="(para, i) in path.body || []"
          :key="i"
          class="upi-path__body"
          :class="{ 'upi-path__body--full': path.phone_body?.length }"
        >
          {{ para }}
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.upi-path {
  max-width: 1440px;
  margin: 48px auto 0;
  padding: 0 196px;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
}

.upi-path__stage {
  position: relative;
  width: min(1048px, 100%);
  /* Cropped mid-band with a little breathing room above/below */
  aspect-ratio: 1048 / 610;
  height: auto;
  overflow: hidden;
}

.upi-path__orbits {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  display: block;
}

.upi-path__badge {
  position: absolute;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(40 / 1048 * 100%);
  aspect-ratio: 1;
  box-sizing: border-box;
  border-radius: 9999px;
  border: 2px solid #ffffff;
  background: #097495;
  box-shadow:
    0 1px 1px rgba(0, 0, 0, 0.05),
    0 4px 6px rgba(34, 42, 53, 0.04),
    0 24px 68px rgba(47, 48, 55, 0.05),
    0 2px 3px rgba(0, 0, 0, 0.04),
    0 0 0 1px rgba(19, 19, 22, 0.05);
  will-change: left, top;
}

.upi-path__badge--motion::after {
  content: "";
  position: absolute;
  inset: -40%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(9, 116, 149, 0.2) 0%,
    rgba(9, 116, 149, 0) 70%
  );
  pointer-events: none;
  z-index: -1;
}

.upi-path__badge img {
  display: block;
  width: 50%;
  height: 50%;
  object-fit: contain;
}

.upi-path__copy {
  position: absolute;
  z-index: 1;
  left: 50%;
  /* Figma copy top 353 → (353 - 180) / 610 */
  top: 28.4%;
  width: min(609px, 90%);
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  text-align: center;
  pointer-events: none;
}

.upi-path__title {
  margin: 0;
  font-size: clamp(28px, 4vw, 42px);
  font-weight: 700;
  line-height: 1.33;
  text-transform: capitalize;
  color: #1e2a3b;
}

.upi-path__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 21px;
  color: #475569;
}

.upi-path__body--phone {
  display: none;
}

@media (max-width: 767px) {
  .upi-path__body--phone {
    display: block;
  }

  .upi-path__body--full {
    display: none;
  }
}

@media (max-width: 1200px) {
  .upi-path {
    padding-left: 48px;
    padding-right: 48px;
  }
}

@media (max-width: 900px) {
  .upi-path {
    padding-left: 24px;
    padding-right: 24px;
  }

  .upi-path__title {
    font-size: 28px;
  }

  .upi-path__copy {
    top: 22%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .upi-path__badge--motion::after {
    display: none;
  }
}
</style>
