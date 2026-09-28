<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import MetricCards from "@/components/MetricCards.vue";
import WlConfigureStepGraphic from "./WlConfigureStepGraphic.vue";
import WlLaunchStepGraphic from "./WlLaunchStepGraphic.vue";
import WlBrandStepGraphic from "./WlBrandStepGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  dashboard: { type: Object, default: null },
  relatedLinks: { type: Array, default: () => [] },
});

/**
 * Platform callout wires — Figma 31:2866 (right). Left is this path mirrored.
 * Shared dash animation (synced, no stagger).
 */
const PLATFORM_WIRE_TOP =
  "M11.0022 87.9832L61.4376 87.9834C65.8559 87.9835 69.4376 84.4017 69.4376 79.9834L69.4374 14.5932C69.4373 10.2465 72.9081 6.6951 77.2537 6.59532L111.059 5.81917L154.662 5.81934";
const PLATFORM_WIRE_BOTTOM =
  "M10.6873 88L61.5388 90.0343C65.8158 90.2054 69.2003 93.7127 69.219 97.993L69.5157 165.888C69.5345 170.182 72.9401 173.696 77.2316 173.848L108.509 174.959L151.986 175.115";
const platformWires = [PLATFORM_WIRE_TOP, PLATFORM_WIRE_BOTTOM];

/** Right wire group local size (Figma 31:2866 / 31:2852). */
const PLATFORM_WIRE_W = 170;

/**
 * Stage is Figma 31:1509 (1291×693).
 * Inner frame 266:384 at (62,70); callouts at y=123 → absolute y=193.
 * Left 266:382: badges 131px + 12px gap + wires at x=143.
 * Right 31:2864 at x=857; badges at local x=182.
 */
const PLATFORM_STAGE = { w: 1291, h: 693 };

const platformBadges = [
  { label: "Your Services", x: 62, y: 193, w: 131, delay: "0s", side: "left" },
  { label: "Quick Deployment", x: 62, y: 358, w: 131, delay: "0.85s", side: "left" },
  { label: "Your Brand Logo", x: 1101, y: 193, w: 128, delay: "1.7s", side: "right" },
  { label: "Your Choice of Colors", x: 1101, y: 358, w: 128, delay: "2.55s", side: "right" },
];

/** Wire group origins in stage space (ports sit after the 12px gap on both sides). */
const PLATFORM_LEFT_WIRE = { x: 205, y: 221 };
const PLATFORM_RIGHT_WIRE = { x: 919, y: 221 };

/** Figma 274:2360 — left column (offset): cards 0,2; right column: cards 1,3 */
const benefitsLeft = computed(() => {
  const cards = props.page?.benefits?.cards || [];
  return [cards[0], cards[2]].filter(Boolean);
});
const benefitsRight = computed(() => {
  const cards = props.page?.benefits?.cards || [];
  return [cards[1], cards[3]].filter(Boolean);
});

const stepsFlowRef = ref(null);
const stepsSectionRef = ref(null);
const numRefs = ref([]);
const connectorPaths = ref([]);
const connectorDots = ref([]);
const svgSize = ref({ w: 0, h: 0 });
/** 0–1 scroll progress through the steps flow (drives cyan progress stroke). */
const wireProgress = ref(0);
let resizeObserver = null;
let scrollRaf = 0;
let reduceMotion = false;

function setNumRef(el, index) {
  if (el) numRefs.value[index] = el;
}

function clamp01(n) {
  return Math.min(1, Math.max(0, n));
}

function updateWireProgress() {
  const flow = stepsFlowRef.value;
  const nums = (props.page?.steps?.items || [])
    .map((_, i) => numRefs.value[i])
    .filter(Boolean);

  if (!flow || nums.length < 2 || connectorPaths.value.length === 0 || window.innerWidth <= 700) {
    wireProgress.value = 0;
    return;
  }

  if (reduceMotion) {
    wireProgress.value = 1;
    return;
  }

  const vh = window.innerHeight || 1;
  // Viewport scrub line — path fills as this line sweeps 01 → 03
  const anchor = vh * 0.42;
  const first = nums[0].getBoundingClientRect();
  const last = nums[nums.length - 1].getBoundingClientRect();
  // Path starts under 01 and ends above 03 (matches connector geometry)
  const startY = first.bottom + 28;
  const endY = last.top - 28;
  const span = endY - startY;

  if (span <= 1) {
    wireProgress.value = last.bottom < anchor ? 1 : 0;
    return;
  }

  let p = (anchor - startY) / span;
  // Ensure full completion once the last step has moved above the scrub line
  if (last.top < anchor) p = 1;
  // Or once the whole flow has left the upper viewport
  if (flow.getBoundingClientRect().bottom < vh * 0.2) p = 1;

  wireProgress.value = clamp01(p);
}

function onScroll() {
  if (scrollRaf) return;
  scrollRaf = requestAnimationFrame(() => {
    scrollRaf = 0;
    updateWireProgress();
  });
}

function onResize() {
  updateConnectors();
  updateWireProgress();
}

/** Local 0–1 draw amount for connector segment `index`. */
function segmentProgress(index) {
  const count = connectorPaths.value.length || 1;
  const start = index / count;
  const end = (index + 1) / count;
  const p = wireProgress.value;
  if (p <= start) return 0;
  if (p >= end - 0.001) return 1;
  return (p - start) / (end - start);
}

function progressDash(index) {
  const drawn = segmentProgress(index) * 100;
  // Keep a large trailing gap so the undrawn remainder stays hidden (avoids "100 0" SVG quirk)
  return `${drawn} 100`;
}

function isDotLit(index) {
  const count = connectorDots.value.length;
  if (wireProgress.value >= 0.99) return true;
  if (count <= 1) return wireProgress.value > 0.02;
  const threshold = index / (count - 1);
  return wireProgress.value >= threshold - 0.02;
}

function updateConnectors() {
  const flow = stepsFlowRef.value;
  const nums = (props.page?.steps?.items || [])
    .map((_, i) => numRefs.value[i])
    .filter(Boolean);

  if (!flow || nums.length < 2 || window.innerWidth <= 700) {
    connectorPaths.value = [];
    connectorDots.value = [];
    wireProgress.value = 0;
    return;
  }

  const flowBox = flow.getBoundingClientRect();
  svgSize.value = { w: flow.clientWidth, h: flow.clientHeight };

  const centers = nums.map((el) => {
    const r = el.getBoundingClientRect();
    const row = el.closest(".wl-steps__row");
    const rowBox = row?.getBoundingClientRect();
    return {
      x: r.left - flowBox.left + r.width / 2,
      top: r.top - flowBox.top,
      bottom: r.bottom - flowBox.top,
      rowBottom: rowBox ? rowBox.bottom - flowBox.top : r.bottom - flowBox.top,
      rowTop: rowBox ? rowBox.top - flowBox.top : r.top - flowBox.top,
    };
  });

  const paths = [];
  const dots = [];

  for (let i = 0; i < centers.length - 1; i += 1) {
    const a = centers[i];
    const b = centers[i + 1];
    // Clear gap between number and connector node (Figma)
    const startY = a.bottom + 28;
    const endY = Math.max(b.top - 28, startY + 40);
    // Keep the horizontal run in the gap between rows (Figma stair)
    const midY = a.rowBottom + (b.rowTop - a.rowBottom) / 2;

    paths.push(`M ${a.x} ${startY} V ${midY} H ${b.x} V ${endY}`);

    // Dot under the start number and above the end number of each segment
    dots.push({ x: a.x, y: startY });
    dots.push({ x: b.x, y: endY });
  }

  connectorPaths.value = paths;
  connectorDots.value = dots;
}

onMounted(async () => {
  reduceMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  await nextTick();
  updateConnectors();
  updateWireProgress();
  // Recalc after step visuals load (row heights change)
  requestAnimationFrame(() => {
    updateConnectors();
    updateWireProgress();
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onResize, { passive: true });
  window.addEventListener("load", onResize, { passive: true });

  if (typeof ResizeObserver !== "undefined" && stepsFlowRef.value) {
    resizeObserver = new ResizeObserver(() => {
      updateConnectors();
      updateWireProgress();
    });
    resizeObserver.observe(stepsFlowRef.value);
    stepsFlowRef.value.querySelectorAll("img").forEach((img) => {
      if (!img.complete) {
        img.addEventListener(
          "load",
          () => {
            updateConnectors();
            updateWireProgress();
          },
          { once: true },
        );
      }
    });
  }
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
  window.removeEventListener("resize", onResize);
  window.removeEventListener("load", onResize);
  resizeObserver?.disconnect();
  if (scrollRaf) cancelAnimationFrame(scrollRaf);
});

watch(
  () => props.page?.steps?.items,
  async () => {
    await nextTick();
    updateConnectors();
    updateWireProgress();
  },
  { deep: true },
);
</script>

<template>
  <main class="wl-page">
    <!-- Hero — Figma 31:1343 (1440×865) -->
    <section class="wl-hero">
      <div class="wl-hero__bg" aria-hidden="true">
        <img
          class="wl-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="wl-hero__inner">
        <div class="wl-hero__copy">
          <p v-if="page.eyebrow" class="wl-hero__eyebrow">{{ page.eyebrow }}</p>
          <h1 class="wl-hero__title">{{ page.title }}</h1>
          <p class="wl-hero__intro">{{ page.intro }}</p>
          <RouterLink to="/contact" class="wl-hero__cta">
            <span>{{ page.cta_label || "Talk to Expert" }}</span>
            <img
              src="/images/figma-contact/nav-arrow.svg"
              alt=""
              width="18"
              height="18"
              decoding="async"
            />
          </RouterLink>
        </div>

        <MetricCards
          v-if="page.metrics?.length"
          class="wl-hero__metrics"
          :items="page.metrics"
          aria-label="White label platform highlights"
        />
      </div>
    </section>

    <!-- Platform — Figma 31:1504 / 31:1509 -->
    <section v-if="page.platform" class="wl-platform">
      <div class="wl-platform__head">
        <h2 class="wl-platform__title">{{ page.platform.title }}</h2>
        <p class="wl-platform__body">{{ page.platform.body }}</p>
      </div>
      <div class="wl-platform__visual">
        <div class="wl-platform__stage" aria-hidden="true">
          <img
            class="wl-platform__bg"
            src="/images/figma-white-label/platform-visual.png"
            alt=""
            :width="PLATFORM_STAGE.w"
            :height="PLATFORM_STAGE.h"
            decoding="async"
          />

          <!-- Full-height gradient masks — erase PNG badge art so glass nodes match -->
          <div class="wl-platform__left-mask" />
          <div class="wl-platform__right-mask" />

          <div
            v-for="badge in platformBadges"
            :key="badge.label"
            class="wl-platform__badge"
            :class="`wl-platform__badge--${badge.side}`"
            :style="{
              left: `${(badge.x / PLATFORM_STAGE.w) * 100}%`,
              top: `${(badge.y / PLATFORM_STAGE.h) * 100}%`,
              width: `${(badge.w / PLATFORM_STAGE.w) * 100}%`,
              animationDelay: badge.delay,
            }"
          >
            <span>{{ badge.label }}</span>
          </div>

          <svg
            class="wl-platform__wires"
            :viewBox="`0 0 ${PLATFORM_STAGE.w} ${PLATFORM_STAGE.h}`"
            preserveAspectRatio="xMidYMid meet"
          >
            <!-- Left: PNG wires erased by solid left-mask; animated strokes only -->
            <g
              :transform="`translate(${PLATFORM_LEFT_WIRE.x} ${PLATFORM_LEFT_WIRE.y}) translate(${PLATFORM_WIRE_W} 0) scale(-1 1)`"
            >
              <path
                v-for="(d, i) in platformWires"
                :key="`left-wire-${i}`"
                :d="d"
                class="wl-platform__wire"
              />
              <circle class="wl-platform__hub" cx="5.608" cy="88.608" r="5.5" />
              <circle class="wl-platform__port-ring" cx="162.647" cy="7.647" r="7.65" />
              <circle class="wl-platform__port" cx="162.647" cy="7.647" r="4.5" />
              <circle class="wl-platform__port-ring" cx="159.647" cy="173.647" r="7.65" />
              <circle class="wl-platform__port" cx="159.647" cy="173.647" r="4.5" />
            </g>

            <!-- Right: cover PNG wires then redraw animated strokes -->
            <g
              :transform="`translate(${PLATFORM_RIGHT_WIRE.x} ${PLATFORM_RIGHT_WIRE.y})`"
            >
              <path
                v-for="(d, i) in platformWires"
                :key="`right-cover-${i}`"
                :d="d"
                class="wl-platform__wire-cover"
              />
              <path
                v-for="(d, i) in platformWires"
                :key="`right-wire-${i}`"
                :d="d"
                class="wl-platform__wire"
              />
              <circle class="wl-platform__hub" cx="5.608" cy="88.608" r="5.5" />
              <circle class="wl-platform__port-ring" cx="162.647" cy="7.647" r="7.65" />
              <circle class="wl-platform__port" cx="162.647" cy="7.647" r="4.5" />
              <circle class="wl-platform__port-ring" cx="159.647" cy="173.647" r="7.65" />
              <circle class="wl-platform__port" cx="159.647" cy="173.647" r="4.5" />
            </g>
          </svg>
        </div>
        <span class="visually-hidden">White-label payment dashboard under your brand</span>
      </div>
    </section>

    <!-- Steps — Figma 31:2880 -->
    <section
      v-if="page.steps"
      ref="stepsSectionRef"
      class="wl-steps"
    >
      <div class="wl-steps__head">
        <h2 class="wl-steps__title">{{ page.steps.title }}</h2>
        <p class="wl-steps__body">{{ page.steps.body }}</p>
      </div>

      <div ref="stepsFlowRef" class="wl-steps__flow">
        <svg
          v-if="connectorPaths.length"
          class="wl-steps__wires"
          :viewBox="`0 0 ${svgSize.w} ${svgSize.h}`"
          :width="svgSize.w"
          :height="svgSize.h"
          aria-hidden="true"
        >
          <defs>
            <filter
              id="wl-wire-progress-glow"
              x="-50%"
              y="-50%"
              width="200%"
              height="200%"
            >
              <feGaussianBlur stdDeviation="3.2" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <path
            v-for="(d, i) in connectorPaths"
            :key="`path-${i}`"
            :d="d"
            class="wl-steps__wire"
            pathLength="100"
          />
          <path
            v-for="(d, i) in connectorPaths"
            :key="`progress-${i}`"
            :d="d"
            class="wl-steps__wire-progress"
            pathLength="100"
            :stroke-dasharray="progressDash(i)"
          />
          <circle
            v-for="(dot, i) in connectorDots"
            :key="`dot-${i}`"
            :cx="dot.x"
            :cy="dot.y"
            r="3"
            class="wl-steps__wire-dot"
            :class="{ 'wl-steps__wire-dot--lit': isDotLit(i) }"
          />
        </svg>

        <div
          v-for="(step, index) in page.steps.items || []"
          :key="step.title"
          class="wl-steps__row"
          :class="{ 'wl-steps__row--reverse': index % 2 === 1 }"
        >
          <div class="wl-steps__copy">
            <p
              :ref="(el) => setNumRef(el, index)"
              class="wl-steps__num"
            >
              {{ step.number }}
            </p>
            <div class="wl-steps__text">
              <h3 class="wl-steps__name">{{ step.title }}</h3>
              <p class="wl-steps__desc">{{ step.body }}</p>
            </div>
          </div>
          <div class="wl-steps__visual">
            <WlConfigureStepGraphic
              v-if="step.title === 'Configure Your Platform'"
              :alt="step.title"
            />
            <WlLaunchStepGraphic
              v-else-if="step.title === 'Launch Under Your Brand'"
              :alt="step.title"
            />
            <WlBrandStepGraphic
              v-else-if="step.title === 'Customize Your Brand'"
              :alt="step.title"
            />
            <img
              v-else
              :src="step.image"
              :alt="step.title"
              :width="step.image_width || 498"
              :height="step.image_height || 269"
              decoding="async"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits — Figma 274:2360 -->
    <section v-if="page.benefits" class="wl-benefits">
      <div class="wl-benefits__copy">
        <h2 class="wl-benefits__title">{{ page.benefits.title }}</h2>
        <p class="wl-benefits__body">{{ page.benefits.body }}</p>
      </div>
      <div class="wl-benefits__cards" aria-label="Benefits">
        <div class="wl-benefits__col wl-benefits__col--offset">
          <article
            v-for="card in benefitsLeft"
            :key="card.title"
            class="wl-benefits__card"
          >
            <div
              class="wl-benefits__icon"
              :class="{ 'wl-benefits__icon--framed': !card.icon_framed }"
            >
              <img
                :src="card.icon"
                alt=""
                :width="card.icon_framed ? 53 : 26"
                :height="card.icon_framed ? 55 : 26"
                decoding="async"
              />
            </div>
            <div class="wl-benefits__card-text">
              <h3 class="wl-benefits__card-title">{{ card.title }}</h3>
              <p class="wl-benefits__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
        <div class="wl-benefits__col">
          <article
            v-for="card in benefitsRight"
            :key="card.title"
            class="wl-benefits__card"
          >
            <div
              class="wl-benefits__icon"
              :class="{ 'wl-benefits__icon--framed': !card.icon_framed }"
            >
              <img
                :src="card.icon"
                alt=""
                :width="card.icon_framed ? 53 : 26"
                :height="card.icon_framed ? 55 : 26"
                decoding="async"
              />
            </div>
            <div class="wl-benefits__card-text">
              <h3 class="wl-benefits__card-title">{{ card.title }}</h3>
              <p class="wl-benefits__card-body">{{ card.body }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.wl-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

/* —— Hero (1440×865 design) —— */
.wl-hero {
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  /* Pull under fixed nav so bg fills first viewport like Figma */
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.wl-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.wl-hero__bg-img {
  position: absolute;
  left: 50%;
  top: 0;
  width: 100%;
  min-width: 100%;
  height: 100%;
  min-height: 100%;
  transform: translateX(-50%);
  display: block;
  object-fit: cover;
  object-position: center top;
}

.wl-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  min-height: 0;
  padding: 80px 56px 100px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.wl-hero__copy {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  width: min(809px, 100%);
  text-align: center;
}

.wl-hero__eyebrow {
  margin: 0;
  padding: 8px 16px;
  border: 1px solid #0292b8;
  border-radius: 29px;
  font-size: 12px;
  font-weight: 700;
  line-height: 20px;
  letter-spacing: 1.7836px;
  text-transform: uppercase;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.wl-hero__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -1.26px;
  color: #252b37;
}

.wl-hero__intro {
  margin: 0;
  max-width: 669px;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.45;
  letter-spacing: 0.56px;
  color: #535862;
}

.wl-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 0 16px;
  margin-top: 22px;
  border-radius: 8px;
  background: #097495;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  transition: opacity 0.15s ease;
}

.wl-hero__cta:hover {
  opacity: 0.92;
  color: #ffffff;
}

/* Cards styled by shared MetricCards; keep them above the hero background. */
.wl-hero__metrics {
  position: relative;
  z-index: 1;
}

/* —— Platform —— */
.wl-platform {
  max-width: 1291px;
  margin: 0 auto;
  padding: 0 56px 100px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.wl-platform__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: min(732px, 100%);
  text-align: center;
}

.wl-platform__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.wl-platform__body {
  margin: 0;
  max-width: 588px;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.wl-platform__visual {
  position: relative;
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
}

.wl-platform__stage {
  position: relative;
  width: 100%;
  aspect-ratio: 1291 / 693;
}

.wl-platform__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

/* Full-height gradient masks match stage teal so no floating “box” edge */
.wl-platform__left-mask,
.wl-platform__right-mask {
  position: absolute;
  z-index: 1;
  top: 0;
  height: 100%;
  background: linear-gradient(
    180deg,
    #0291b7 0%,
    #038baf 10%,
    #0487ab 15%,
    #0681a3 25%,
    #077d9f 30%,
    #087697 40%,
    #097393 45%,
    #0a6f8e 50%,
    #0c6986 60%,
    #0d627e 70%,
    #0f5b76 80%,
    #11546e 90%,
    #124e66 100%
  );
  pointer-events: none;
}

.wl-platform__left-mask {
  left: 0;
  /* Solid through the left wire junction (≈306) up to the dashboard edge — no feather,
     or the PNG dashes show through under the animated stroke. */
  width: calc(328 / 1291 * 100%);
}

.wl-platform__right-mask {
  right: 0;
  width: calc(200 / 1291 * 100%);
  -webkit-mask-image: linear-gradient(90deg, transparent 0%, #000 12%, #000 100%);
  mask-image: linear-gradient(90deg, transparent 0%, #000 12%, #000 100%);
}

.wl-platform__wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

.wl-platform__badge {
  position: absolute;
  z-index: 3;
  height: calc(75 / 693 * 100%);
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 20px;
  /* Match home glass pills (Figma 89:2110) + frosted rim on dark stage */
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background:
    linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.16) 0%,
      rgba(255, 255, 255, 0.04) 100%
    ),
    rgba(9, 116, 149, 0.22);
  backdrop-filter: blur(14px) saturate(1.15);
  -webkit-backdrop-filter: blur(14px) saturate(1.15);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.45),
    inset 0 -1px 0 rgba(255, 255, 255, 0.06),
    0 6px 18px rgba(0, 0, 0, 0.16);
  transform-origin: center center;
  animation: wl-platform-breathe 3.6s ease-in-out infinite;
  overflow: visible;
}

.wl-platform__badge span {
  font-size: clamp(10px, 1.2vw, 16px);
  font-weight: 600;
  line-height: 1.2;
  color: #ffffff;
  text-align: center;
  text-transform: capitalize;
}

.wl-platform__wire-cover {
  fill: none;
  stroke: #097393;
  stroke-width: 5;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.wl-platform__wire {
  fill: none;
  stroke: rgba(255, 255, 255, 0.92);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 3.4 10;
  animation: wl-platform-dash 0.85s linear infinite;
}

.wl-platform__hub {
  fill: #38b7d3;
}

.wl-platform__port-ring {
  fill: #ffffff;
}

.wl-platform__port {
  fill: #38b7d3;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@keyframes wl-platform-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes wl-platform-breathe {
  0%,
  100% {
    opacity: 0.9;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.02);
  }
}

@media (prefers-reduced-motion: reduce) {
  .wl-platform__wire,
  .wl-platform__badge {
    animation: none;
  }

  .wl-platform__badge {
    opacity: 1;
    transform: none;
  }
}

/* —— Steps —— */
.wl-steps {
  max-width: 964px;
  margin: 0 auto;
  padding: 0 56px;
  box-sizing: border-box;
}

.wl-steps__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  max-width: 936px;
  margin-inline: auto;
  margin-bottom: 56px;
  text-align: center;
}

.wl-steps__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.wl-steps__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.wl-steps__flow {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 88px;
}

.wl-steps__wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: visible;
}

.wl-steps__wire {
  fill: none;
  stroke: #252b37;
  stroke-width: 1;
  stroke-dasharray: 3.4 10;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.wl-steps__wire-progress {
  fill: none;
  stroke: #06b6d4;
  stroke-width: 2.5;
  stroke-dashoffset: 0;
  stroke-linecap: round;
  stroke-linejoin: round;
  filter: url(#wl-wire-progress-glow);
  opacity: 0.95;
}

.wl-steps__wire-dot {
  fill: #252b37;
  transition: fill 0.2s ease, filter 0.2s ease;
}

.wl-steps__wire-dot--lit {
  fill: #06b6d4;
  filter: drop-shadow(0 0 5px rgba(6, 182, 212, 0.9));
}

@media (prefers-reduced-motion: reduce) {
  .wl-steps__wire-progress {
    filter: none;
  }
}

.wl-steps__row {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 64px;
  align-items: center;
}

.wl-steps__row--reverse {
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
}

.wl-steps__row--reverse .wl-steps__copy {
  order: 2;
}

.wl-steps__row--reverse .wl-steps__visual {
  order: 1;
}

.wl-steps__copy {
  display: flex;
  gap: 7px;
  align-items: flex-start;
}

.wl-steps__num {
  margin: 0;
  flex: 0 0 auto;
  min-width: 36px;
  padding: 0;
  font-size: 24px;
  font-weight: 500;
  letter-spacing: -0.24px;
  line-height: 1.2;
  color: #252b37;
  background: none;
  border-radius: 0;
  text-align: left;
}

.wl-steps__text {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 358px;
}

.wl-steps__name {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
  letter-spacing: -0.24px;
  color: #252b37;
}

.wl-steps__desc {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  color: #535862;
}

.wl-steps__visual {
  overflow: visible;
}

.wl-steps__visual img,
.wl-steps__visual :deep(.wl-cfg),
.wl-steps__visual :deep(.wl-launch),
.wl-steps__visual :deep(.wl-brand) {
  display: block;
  width: 100%;
  max-width: 498px;
  aspect-ratio: 498 / 280;
  height: auto;
  margin-inline: auto;
}

/* —— Benefits — Figma 31:3148 (1291×467) —— */
.wl-benefits {
  max-width: 1291px;
  margin: 80px auto 0;
  padding: 0 56px 40px;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 544px) minmax(0, 610px);
  gap: 86px;
  align-items: center;
}

.wl-benefits__copy {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 544px;
}

.wl-benefits__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.wl-benefits__body {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.wl-benefits__cards {
  position: relative;
  width: 100%;
  max-width: 610px;
  height: 467px;
  justify-self: end;
}

.wl-benefits__col {
  position: absolute;
  top: 0;
  width: 287px;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.wl-benefits__col--offset {
  left: 0;
  top: 73px;
}

.wl-benefits__col:not(.wl-benefits__col--offset) {
  left: 323px;
  top: 0;
}

.wl-benefits__card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  min-height: 179px;
  padding: 20px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 14.141px;
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.25s ease;
}

.wl-benefits__card:hover {
  box-shadow:
    0 0.904px 0.904px 0 rgba(0, 0, 0, 0.05),
    0 1.807px 2.711px 0 rgba(0, 0, 0, 0.04),
    0 3.614px 5.422px 0 rgba(34, 42, 53, 0.04),
    0 21.686px 61.444px 0 rgba(47, 48, 55, 0.05);
}

.wl-benefits__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 52.568px;
  height: 54.568px;
}

.wl-benefits__icon--framed {
  padding: 13.284px;
  box-sizing: border-box;
  background: rgba(9, 116, 149, 0.1);
  border-radius: 6.642px;
}

.wl-benefits__icon img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.wl-benefits__icon--framed img {
  width: 26px;
  height: 26px;
}

.wl-benefits__card-text {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.wl-benefits__card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0.48px;
  color: #252b37;
}

.wl-benefits__card-body {
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: #535862;
}

/* —— Tablet —— */
@media (max-width: 1200px) {
  .wl-hero__inner {
    padding: 64px 40px 100px;
    gap: 40px;
    min-height: 0;
  }

  .wl-hero__title,
  .wl-platform__title,
  .wl-steps__title,
  .wl-benefits__title {
    font-size: 32px;
    line-height: 1.25;
    letter-spacing: -0.8px;
  }

  .wl-platform,
  .wl-steps,
  .wl-benefits {
    padding-left: 40px;
    padding-right: 40px;
  }

  .wl-benefits {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .wl-benefits__cards {
    height: auto;
    max-width: none;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    justify-self: stretch;
  }

  .wl-benefits__col {
    position: static;
    width: auto;
    gap: 24px;
  }

  .wl-benefits__col--offset {
    top: auto;
  }
}

/* —— Phone —— */
@media (max-width: 700px) {
  .wl-hero__inner {
    padding: 40px 19px 100px;
    gap: 32px;
  }

  .wl-hero__title,
  .wl-platform__title,
  .wl-steps__title,
  .wl-benefits__title {
    font-size: 28px;
    letter-spacing: -0.6px;
  }

  .wl-hero__cta {
    width: 100%;
    max-width: 280px;
  }

  .wl-platform,
  .wl-steps,
  .wl-benefits {
    padding-left: 19px;
    padding-right: 19px;
  }

  .wl-platform {
    padding-bottom: 100px;
    margin-top: 0;
  }

  .wl-steps {
    margin-top: 0;
  }

  .wl-benefits {
    margin-top: 56px;
  }

  .wl-steps__row,
  .wl-steps__row--reverse {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .wl-steps__row--reverse .wl-steps__copy,
  .wl-steps__row--reverse .wl-steps__visual {
    order: initial;
  }

  .wl-steps__flow {
    gap: 40px;
  }

  .wl-steps__wires {
    display: none;
  }

  .wl-steps__name,
  .wl-steps__num {
    font-size: 20px;
  }

  .wl-benefits__cards {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .wl-benefits__card {
    min-height: 0;
  }
}
</style>
