<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import {
  animateStatValues,
  formatStatValue,
  parseStatValue,
} from "@/composables/useCountUp.js";
import CollectionsSmarterDiagram from "./CollectionsSmarterDiagram.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const heroReady = ref(false);
const statsRef = ref(null);
const statDisplays = ref([]);
let statsObserver = null;
let cancelStatAnimation = null;

const EXP_GAP = 24;
const EXP_SIDE_SCALE = 0.8;
const EXP_SIDE_OPACITY = 0.7;
const EXP_AUTOSCROLL_MS = 4000;
const EXP_RESUME_MS = 6000;

const smarterReady = ref(false);
const smarterRef = ref(null);
let smarterObserver = null;
const experienceIndex = ref(0);
/** Absolute track position (supports cloned slides for seamless looping). */
const experienceTrackIndex = ref(0);
const expTrackInstant = ref(false);
const expSectionRef = ref(null);
const expViewportRef = ref(null);
const expTrackRef = ref(null);
const expViewportWidth = ref(0);
const expSlideWidth = ref(850);
let expResizeObserver = null;
let expAutoTimer = 0;
let expResumeTimer = 0;
let expHoverPaused = false;
let expUserPaused = false;
let expReduceMotion = false;
let expInView = true;
let expVisibilityHandler = null;
let expIntersectObserver = null;

const pageStats = computed(() => props.page?.stats || []);
const parsedStats = computed(() => pageStats.value.map((stat) => parseStatValue(stat.value)));
const journeyCards = computed(() => props.page?.journey?.cards || []);
const experienceCards = computed(() => props.page?.experiences?.cards || []);
const flowSteps = computed(() => props.page?.flow?.steps || []);

/** Figma flow visuals — SVG exports under /images/figma-collections/flow/ */
const FLOW_VISUAL = {
  api: {
    kind: "single",
    src: "/images/figma-collections/flow/step01-api.svg",
    width: 397,
    height: 213,
  },
  initiate: {
    kind: "single",
    src: "/images/figma-collections/flow/step02-phone.svg",
    width: 216,
    height: 245,
  },
  pay: {
    kind: "single",
    src: "/images/figma-collections/flow/step03-methods.svg",
    width: 310,
    height: 270,
  },
  notify: {
    kind: "single",
    src: "/images/figma-collections/flow/step04-status.svg",
    width: 342,
    height: 207,
  },
  settle: {
    kind: "single",
    src: "/images/figma-collections/flow/step05-settlement.svg",
    width: 359,
    height: 218,
  },
};

const FLOW_WIRE_BREAKPOINT = 1100;

const flowListRef = ref(null);
const flowNumRefs = ref([]);
const flowConnectorPaths = ref([]);
const flowConnectorDots = ref([]);
const flowSvgSize = ref({ w: 0, h: 0 });
/** 0–1 scroll progress through the flow (drives cyan progress stroke). */
const flowWireProgress = ref(0);
let flowResizeObserver = null;
let flowScrollRaf = 0;
let flowReduceMotion = false;

function flowVisual(step) {
  return FLOW_VISUAL[step?.visual] || null;
}

function setFlowNumRef(el, index) {
  if (el) flowNumRefs.value[index] = el;
}

function clamp01(n) {
  return Math.min(1, Math.max(0, n));
}

function updateFlowWireProgress() {
  const flow = flowListRef.value;
  const nums = flowSteps.value.map((_, i) => flowNumRefs.value[i]).filter(Boolean);

  if (
    !flow ||
    nums.length < 2 ||
    flowConnectorPaths.value.length === 0 ||
    window.innerWidth <= FLOW_WIRE_BREAKPOINT
  ) {
    flowWireProgress.value = 0;
    return;
  }

  if (flowReduceMotion) {
    flowWireProgress.value = 1;
    return;
  }

  const vh = window.innerHeight || 1;
  const anchor = vh * 0.42;
  const first = nums[0].getBoundingClientRect();
  const last = nums[nums.length - 1].getBoundingClientRect();
  const startY = first.bottom + 28;
  const endY = last.top - 28;
  const span = endY - startY;

  if (span <= 1) {
    flowWireProgress.value = last.bottom < anchor ? 1 : 0;
    return;
  }

  let p = (anchor - startY) / span;
  if (last.top < anchor) p = 1;
  if (flow.getBoundingClientRect().bottom < vh * 0.2) p = 1;

  flowWireProgress.value = clamp01(p);
}

function updateFlowConnectors() {
  const flow = flowListRef.value;
  const nums = flowSteps.value.map((_, i) => flowNumRefs.value[i]).filter(Boolean);

  if (!flow || nums.length < 2 || window.innerWidth <= FLOW_WIRE_BREAKPOINT) {
    flowConnectorPaths.value = [];
    flowConnectorDots.value = [];
    flowWireProgress.value = 0;
    return;
  }

  const flowBox = flow.getBoundingClientRect();
  flowSvgSize.value = { w: flow.clientWidth, h: flow.clientHeight };

  const centers = nums.map((el) => {
    const r = el.getBoundingClientRect();
    const row = el.closest(".col-flow__row");
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
    const startY = a.bottom + 28;
    const endY = Math.max(b.top - 28, startY + 40);
    const midY = a.rowBottom + (b.rowTop - a.rowBottom) / 2;

    paths.push(`M ${a.x} ${startY} V ${midY} H ${b.x} V ${endY}`);
    dots.push({ x: a.x, y: startY });
    dots.push({ x: b.x, y: endY });
  }

  flowConnectorPaths.value = paths;
  flowConnectorDots.value = dots;
}

function flowSegmentProgress(index) {
  const count = flowConnectorPaths.value.length || 1;
  const start = index / count;
  const end = (index + 1) / count;
  const p = flowWireProgress.value;
  if (p <= start) return 0;
  if (p >= end - 0.001) return 1;
  return (p - start) / (end - start);
}

function flowProgressDash(index) {
  const drawn = flowSegmentProgress(index) * 100;
  return `${drawn} 100`;
}

function isFlowDotLit(index) {
  const count = flowConnectorDots.value.length;
  if (flowWireProgress.value >= 0.99) return true;
  if (count <= 1) return flowWireProgress.value > 0.02;
  const threshold = index / (count - 1);
  return flowWireProgress.value >= threshold - 0.02;
}

function onFlowScroll() {
  if (flowScrollRaf) return;
  flowScrollRaf = requestAnimationFrame(() => {
    flowScrollRaf = 0;
    updateFlowWireProgress();
  });
}

function onFlowResize() {
  updateFlowConnectors();
  updateFlowWireProgress();
}

function setupFlowConnectors() {
  flowResizeObserver?.disconnect();
  updateFlowConnectors();
  updateFlowWireProgress();
  requestAnimationFrame(() => {
    updateFlowConnectors();
    updateFlowWireProgress();
  });

  if (typeof ResizeObserver !== "undefined" && flowListRef.value) {
    flowResizeObserver = new ResizeObserver(() => {
      updateFlowConnectors();
      updateFlowWireProgress();
    });
    flowResizeObserver.observe(flowListRef.value);
    flowListRef.value.querySelectorAll("img").forEach((img) => {
      if (!img.complete) {
        img.addEventListener(
          "load",
          () => {
            updateFlowConnectors();
            updateFlowWireProgress();
          },
          { once: true },
        );
      }
    });
  }
}

/** One focused card at a time (Juspay-style infinite center carousel). */
const experienceCount = computed(() => experienceCards.value.length);

const experienceMaxIndex = computed(() =>
  Math.max(experienceCount.value - 1, 0),
);

/** Triple the slides so first can enter after last without rewinding. */
const experienceSlides = computed(() => {
  const cards = experienceCards.value;
  if (!cards.length) return [];
  if (cards.length === 1) {
    return [{ ...cards[0], sourceIndex: 0, key: "solo-0" }];
  }
  const slides = [];
  for (let copy = 0; copy < 3; copy += 1) {
    cards.forEach((card, sourceIndex) => {
      slides.push({
        ...card,
        sourceIndex,
        key: `${copy}-${sourceIndex}-${card.title}`,
      });
    });
  }
  return slides;
});

const experienceLoopEnabled = computed(() => experienceCount.value > 1);

function syncExperienceLogicalIndex() {
  const n = experienceCount.value;
  if (!n) {
    experienceIndex.value = 0;
    return;
  }
  experienceIndex.value =
    ((experienceTrackIndex.value % n) + n) % n;
}

function resetExperienceTrackToMiddle() {
  const n = experienceCount.value;
  if (!n) {
    experienceTrackIndex.value = 0;
    experienceIndex.value = 0;
    return;
  }
  if (!experienceLoopEnabled.value) {
    experienceTrackIndex.value = 0;
    experienceIndex.value = 0;
    return;
  }
  // Start on the middle copy so we can move either direction.
  experienceTrackIndex.value = n + experienceIndex.value;
  syncExperienceLogicalIndex();
}

const experienceTrackStyle = computed(() => {
  const vw = expViewportWidth.value || 0;
  const slide = expSlideWidth.value || 850;
  const step = slide + EXP_GAP;
  const x = vw / 2 - slide / 2 - experienceTrackIndex.value * step;
  return {
    transform: `translate3d(${x}px, 0, 0)`,
  };
});

function experienceStepLabel(sourceIndex) {
  return String(sourceIndex + 1);
}

function experienceCardStyle(trackIndex) {
  const active = trackIndex === experienceTrackIndex.value;
  // During loop snap, keep transforms lock-step with the track jump (no scale tween).
  const style = {
    transform: `scale(${active ? 1 : EXP_SIDE_SCALE})`,
    opacity: active ? 1 : EXP_SIDE_OPACITY,
  };
  if (expTrackInstant.value) {
    style.transition = "none";
  }
  return style;
}

function measureExpViewport() {
  const viewport = expViewportRef.value;
  if (viewport) expViewportWidth.value = viewport.clientWidth;
  const slide = expTrackRef.value?.querySelector(".col-exp__slide");
  if (slide) {
    // Offset width ignores outer scale so track math stays stable.
    expSlideWidth.value = slide.offsetWidth || slide.getBoundingClientRect().width;
  }
}

function normalizeExperienceLoop() {
  const n = experienceCount.value;
  if (!experienceLoopEnabled.value || n <= 1) return;
  if (expTrackInstant.value) return;

  let i = experienceTrackIndex.value;
  let jumped = false;
  while (i >= n * 2) {
    i -= n;
    jumped = true;
  }
  while (i < n) {
    i += n;
    jumped = true;
  }
  if (!jumped) {
    syncExperienceLogicalIndex();
    return;
  }

  // Freeze all motion, jump to the equivalent middle clone, then re-enable.
  // Skipping this freeze is what caused the visible scale hitch on wrap.
  expTrackInstant.value = true;
  experienceTrackIndex.value = i;
  syncExperienceLogicalIndex();

  nextTick(() => {
    const track = expTrackRef.value;
    if (track) {
      // Force style flush so the jump commits while transitions are off.
      void track.offsetWidth;
    }
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        expTrackInstant.value = false;
      });
    });
  });
}

function onExperienceTrackTransitionEnd(event) {
  if (event.target !== expTrackRef.value) return;
  if (event.propertyName && event.propertyName !== "transform") return;
  normalizeExperienceLoop();
}

function stopExperienceAutoscroll() {
  if (expAutoTimer) {
    window.clearInterval(expAutoTimer);
    expAutoTimer = 0;
  }
}

function clearExperienceResume() {
  if (expResumeTimer) {
    window.clearTimeout(expResumeTimer);
    expResumeTimer = 0;
  }
}

function canExperienceAutoscroll() {
  return (
    !expReduceMotion &&
    !expHoverPaused &&
    !expUserPaused &&
    expInView &&
    typeof document !== "undefined" &&
    !document.hidden &&
    experienceLoopEnabled.value
  );
}

function startExperienceAutoscroll() {
  stopExperienceAutoscroll();
  if (!canExperienceAutoscroll()) return;
  expAutoTimer = window.setInterval(() => {
    if (!canExperienceAutoscroll()) {
      stopExperienceAutoscroll();
      return;
    }
    experienceNext({ fromAuto: true });
  }, EXP_AUTOSCROLL_MS);
}

function pauseExperienceAutoscrollForUser() {
  expUserPaused = true;
  stopExperienceAutoscroll();
  clearExperienceResume();
  expResumeTimer = window.setTimeout(() => {
    expUserPaused = false;
    startExperienceAutoscroll();
  }, EXP_RESUME_MS);
}

function onExperienceHoverEnter() {
  expHoverPaused = true;
  stopExperienceAutoscroll();
}

function onExperienceHoverLeave() {
  expHoverPaused = false;
  if (!expUserPaused) startExperienceAutoscroll();
}

function experiencePrev(options = {}) {
  if (!experienceCount.value) return;
  if (!options.fromAuto) pauseExperienceAutoscrollForUser();
  if (!experienceLoopEnabled.value) {
    experienceTrackIndex.value = Math.max(experienceTrackIndex.value - 1, 0);
  } else {
    experienceTrackIndex.value -= 1;
  }
  syncExperienceLogicalIndex();
  if (expReduceMotion) normalizeExperienceLoop();
}

function experienceNext(options = {}) {
  if (!experienceCount.value) return;
  if (!options.fromAuto) pauseExperienceAutoscrollForUser();
  if (!experienceLoopEnabled.value) {
    experienceTrackIndex.value = Math.min(
      experienceTrackIndex.value + 1,
      experienceMaxIndex.value,
    );
  } else {
    experienceTrackIndex.value += 1;
  }
  syncExperienceLogicalIndex();
  if (expReduceMotion) normalizeExperienceLoop();
}

function experienceGoToTrack(trackIndex) {
  if (trackIndex === experienceTrackIndex.value) return;
  pauseExperienceAutoscrollForUser();
  experienceTrackIndex.value = trackIndex;
  syncExperienceLogicalIndex();
  if (expReduceMotion) normalizeExperienceLoop();
}

function onExperienceKeydown(event) {
  if (event.key === "ArrowLeft") {
    event.preventDefault();
    experiencePrev();
  } else if (event.key === "ArrowRight") {
    event.preventDefault();
    experienceNext();
  }
}

function setupExperienceAutoscroll() {
  expReduceMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  expIntersectObserver?.disconnect();
  if (typeof IntersectionObserver !== "undefined" && expSectionRef.value) {
    expIntersectObserver = new IntersectionObserver(
      ([entry]) => {
        expInView = Boolean(entry?.isIntersecting);
        if (expInView) startExperienceAutoscroll();
        else stopExperienceAutoscroll();
      },
      { threshold: 0.35 },
    );
    expIntersectObserver.observe(expSectionRef.value);
  }

  if (!expVisibilityHandler) {
    expVisibilityHandler = () => {
      if (document.hidden) stopExperienceAutoscroll();
      else startExperienceAutoscroll();
    };
    document.addEventListener("visibilitychange", expVisibilityHandler);
  }

  startExperienceAutoscroll();
}

function teardownExperienceAutoscroll() {
  stopExperienceAutoscroll();
  clearExperienceResume();
  expIntersectObserver?.disconnect();
  expIntersectObserver = null;
  if (expVisibilityHandler) {
    document.removeEventListener("visibilitychange", expVisibilityHandler);
    expVisibilityHandler = null;
  }
}

function setupExperienceCarousel() {
  resetExperienceTrackToMiddle();
  measureExpViewport();
  expResizeObserver?.disconnect();
  if (typeof ResizeObserver !== "undefined") {
    expResizeObserver = new ResizeObserver(() => {
      measureExpViewport();
    });
    if (expViewportRef.value) expResizeObserver.observe(expViewportRef.value);
    if (expTrackRef.value) {
      expResizeObserver.observe(expTrackRef.value);
      expTrackRef.value.querySelectorAll("img").forEach((img) => {
        if (!img.complete) {
          img.addEventListener("load", measureExpViewport, { once: true });
        }
      });
    }
  }
  requestAnimationFrame(measureExpViewport);
  setupExperienceAutoscroll();
}

function setFinalStatValues() {
  statDisplays.value = pageStats.value.map((stat) => stat.value);
}

function resetStatValues() {
  statDisplays.value = parsedStats.value.map((parsed) => formatStatValue(parsed, 0));
}

function runStatsCountUp() {
  cancelStatAnimation?.();
  if (!parsedStats.value.length) return;
  cancelStatAnimation = animateStatValues(parsedStats.value, {
    duration: 1800,
    onFrame: (values) => {
      statDisplays.value = values;
    },
    onComplete: setFinalStatValues,
  });
}

function setupStatsObserver() {
  statsObserver?.disconnect();
  if (!pageStats.value.length) return;

  if (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    setFinalStatValues();
    return;
  }

  resetStatValues();
  statsObserver = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return;
      runStatsCountUp();
      statsObserver?.disconnect();
    },
    { threshold: 0.25, rootMargin: "0px 0px -8% 0px" },
  );

  if (statsRef.value) statsObserver.observe(statsRef.value);
}

function setupSmarterObserver() {
  smarterObserver?.disconnect();
  if (!smarterRef.value) return;
  if (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    smarterReady.value = true;
    return;
  }
  smarterObserver = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return;
      smarterReady.value = true;
      smarterObserver?.disconnect();
    },
    { threshold: 0.2 },
  );
  smarterObserver.observe(smarterRef.value);
}

onMounted(() => {
  flowReduceMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  requestAnimationFrame(() => {
    heroReady.value = true;
  });
  window.addEventListener("scroll", onFlowScroll, { passive: true });
  window.addEventListener("resize", onFlowResize, { passive: true });
  window.addEventListener("keydown", onExperienceKeydown);
  resetStatValues();
  nextTick(() => {
    setupStatsObserver();
    setupSmarterObserver();
    setupFlowConnectors();
    setupExperienceCarousel();
  });
});

onBeforeUnmount(() => {
  statsObserver?.disconnect();
  smarterObserver?.disconnect();
  flowResizeObserver?.disconnect();
  expResizeObserver?.disconnect();
  teardownExperienceAutoscroll();
  cancelStatAnimation?.();
  if (flowScrollRaf) cancelAnimationFrame(flowScrollRaf);
  window.removeEventListener("scroll", onFlowScroll);
  window.removeEventListener("resize", onFlowResize);
  window.removeEventListener("keydown", onExperienceKeydown);
});

watch(pageStats, async () => {
  resetStatValues();
  await nextTick();
  setupStatsObserver();
});

watch(experienceCards, async () => {
  experienceIndex.value = 0;
  await nextTick();
  setupExperienceCarousel();
});

watch(
  flowSteps,
  async () => {
    await nextTick();
    setupFlowConnectors();
  },
  { deep: true },
);
</script>

<template>
  <main class="col-page">
    <!-- Hero — Figma 330:2221 -->
    <section class="col-hero" :class="{ 'col-hero--ready': heroReady }">
      <div class="col-hero__bg" aria-hidden="true">
        <img
          class="col-hero__bg-img"
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="col-hero__inner">
        <div class="col-hero__copy">
          <p v-if="page.eyebrow" class="col-hero__eyebrow">{{ page.eyebrow }}</p>
          <div class="col-hero__cta-block">
            <div class="col-hero__text">
              <h1 class="col-hero__title">{{ page.title }}</h1>
              <p class="col-hero__intro">{{ page.intro }}</p>
            </div>
            <RouterLink to="/contact" class="col-hero__cta">
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
        </div>

        <div
          v-if="pageStats.length"
          ref="statsRef"
          class="col-stats"
          aria-label="Collections outcomes"
        >
          <article
            v-for="(stat, index) in pageStats"
            :key="stat.label"
            class="col-stats__card"
          >
            <p class="col-stats__value">{{ statDisplays[index] || stat.value }}</p>
            <p class="col-stats__label">{{ stat.label }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Smarter way diagram — Figma 466:22218 -->
    <section v-if="page.smarter" ref="smarterRef" class="col-smarter">
      <div class="col-smarter__head">
        <h2 class="col-smarter__title">{{ page.smarter.title }}</h2>
        <p class="col-smarter__body">{{ page.smarter.body }}</p>
      </div>
      <div class="col-smarter__visual">
        <CollectionsSmarterDiagram :ready="smarterReady" />
      </div>
    </section>

    <!-- Payment journey flow — Figma 466:22604+ -->
    <section v-if="page.flow" class="col-flow">
      <div class="col-flow__head">
        <h2 class="col-flow__title">{{ page.flow.title }}</h2>
        <p class="col-flow__body">{{ page.flow.body }}</p>
      </div>

      <div
        ref="flowListRef"
        class="col-flow__list"
        aria-label="Payment journey steps"
      >
        <svg
          v-if="flowConnectorPaths.length"
          class="col-flow__wires"
          :viewBox="`0 0 ${flowSvgSize.w} ${flowSvgSize.h}`"
          :width="flowSvgSize.w"
          :height="flowSvgSize.h"
          aria-hidden="true"
        >
          <defs>
            <filter
              id="col-wire-progress-glow"
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
            v-for="(d, i) in flowConnectorPaths"
            :key="`path-${i}`"
            :d="d"
            class="col-flow__wire"
            pathLength="100"
          />
          <path
            v-for="(d, i) in flowConnectorPaths"
            :key="`progress-${i}`"
            :d="d"
            class="col-flow__wire-progress"
            pathLength="100"
            :stroke-dasharray="flowProgressDash(i)"
          />
          <circle
            v-for="(dot, i) in flowConnectorDots"
            :key="`dot-${i}`"
            :cx="dot.x"
            :cy="dot.y"
            r="3"
            class="col-flow__wire-dot"
            :class="{ 'col-flow__wire-dot--lit': isFlowDotLit(i) }"
          />
        </svg>

        <article
          v-for="(step, index) in flowSteps"
          :key="step.title"
          class="col-flow__row"
          :class="{ 'col-flow__row--reverse': step.side === 'right' }"
        >
          <div class="col-flow__copy">
            <span
              :ref="(el) => setFlowNumRef(el, index)"
              class="col-flow__num"
            >
              {{ step.number }}
            </span>
            <div class="col-flow__text">
              <h3 class="col-flow__name">{{ step.title }}</h3>
              <p class="col-flow__desc">{{ step.body }}</p>
            </div>
          </div>

          <div class="col-flow__visual" aria-hidden="true">
            <img
              v-if="flowVisual(step)"
              class="col-flow__media"
              :src="flowVisual(step).src"
              alt=""
              :width="flowVisual(step).width"
              :height="flowVisual(step).height"
              decoding="async"
              loading="lazy"
            />
          </div>
        </article>
      </div>
    </section>

    <!-- Experiences carousel — Juspay-style center focus + autoscroll -->
    <section
      v-if="page.experiences"
      ref="expSectionRef"
      class="col-exp"
      @mouseenter="onExperienceHoverEnter"
      @mouseleave="onExperienceHoverLeave"
    >
      <div class="col-exp__head">
        <h2 class="col-exp__title">{{ page.experiences.title }}</h2>
        <p class="col-exp__body">{{ page.experiences.body }}</p>
      </div>

      <div ref="expViewportRef" class="col-exp__viewport">
        <div
          ref="expTrackRef"
          class="col-exp__track"
          :class="{ 'col-exp__track--instant': expTrackInstant }"
          :style="experienceTrackStyle"
          aria-label="Payment experiences"
          aria-live="polite"
          @transitionend="onExperienceTrackTransitionEnd"
        >
          <article
            v-for="(slide, trackIndex) in experienceSlides"
            :key="slide.key"
            class="col-exp__slide"
            :class="{ 'col-exp__slide--active': experienceTrackIndex === trackIndex }"
            :style="experienceCardStyle(trackIndex)"
            @click="experienceGoToTrack(trackIndex)"
          >
            <div class="col-exp__marker col-exp__marker--left" aria-hidden="true">
              <span class="col-exp__marker-num">{{ experienceStepLabel(slide.sourceIndex) }}</span>
              <span class="col-exp__marker-line" />
            </div>

            <div class="col-exp__panel">
              <div class="col-exp__visual">
                <img
                  class="col-exp__media"
                  :src="slide.image"
                  :alt="slide.image_alt || slide.title"
                  width="480"
                  height="350"
                  decoding="async"
                  loading="lazy"
                />
              </div>
              <div class="col-exp__card-text">
                <h3 class="col-exp__card-title">{{ slide.title }}</h3>
                <p class="col-exp__card-body">{{ slide.body }}</p>
              </div>
            </div>

            <div class="col-exp__marker col-exp__marker--right" aria-hidden="true">
              <span class="col-exp__marker-line" />
              <span class="col-exp__marker-num">{{ experienceStepLabel(slide.sourceIndex) }}</span>
            </div>
          </article>
        </div>
      </div>

      <div v-if="experienceCards.length > 1" class="col-exp__nav">
        <button
          type="button"
          class="col-exp__nav-btn col-exp__nav-btn--prev"
          aria-label="Previous experience"
          @click="experiencePrev"
        >
          <img
            src="/images/figma-collections/experiences/nav-chevron.svg"
            alt=""
            width="24"
            height="24"
            decoding="async"
          />
        </button>
        <button
          type="button"
          class="col-exp__nav-btn col-exp__nav-btn--next"
          aria-label="Next experience"
          @click="experienceNext"
        >
          <img
            src="/images/figma-collections/experiences/nav-chevron.svg"
            alt=""
            width="24"
            height="24"
            decoding="async"
          />
        </button>
      </div>
    </section>

    <!-- Journey — Figma 466:22565 -->
    <section v-if="page.journey" class="col-journey">
      <div class="col-journey__copy">
        <h2 class="col-journey__title">{{ page.journey.title }}</h2>
        <p class="col-journey__body">{{ page.journey.body }}</p>
      </div>
      <div class="col-journey__grid" aria-label="Collection journey">
        <article
          v-for="card in journeyCards"
          :key="card.title"
          class="col-journey__card"
        >
          <div class="col-journey__icon" aria-hidden="true">
            <img
              :src="card.icon"
              alt=""
              width="28"
              height="28"
              decoding="async"
            />
          </div>
          <h3 class="col-journey__card-title">{{ card.title }}</h3>
          <p class="col-journey__card-body">{{ card.body }}</p>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.col-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

/* —— Hero — Figma 330:2221 —— */
.col-hero {
  position: relative;
  width: 100%;
  margin: 0;
  margin-top: calc(-1 * var(--page-nav-offset, 129px));
  padding-top: var(--page-nav-offset, 129px);
  overflow: hidden;
  background: #ffffff;
}

.col-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.col-hero__bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center top;
}

.col-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  padding: 80px 100px 12px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 72px;
}

.col-hero__copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  width: min(809px, 100%);
  text-align: center;
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.55s ease,
    transform 0.55s ease;
}

.col-hero--ready .col-hero__copy {
  opacity: 1;
  transform: none;
}

.col-hero__eyebrow {
  margin: 0;
  padding: 8px 16px;
  border: 1px solid #0292b8;
  border-radius: 29px;
  font-size: 12px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 1.7836px;
  text-transform: uppercase;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.col-hero__cta-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  width: 100%;
}

.col-hero__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.col-hero__title {
  margin: 0;
  max-width: 809px;
  font-size: 42px;
  font-weight: 700;
  line-height: normal;
  text-transform: capitalize;
  color: #252b37;
}

.col-hero__intro {
  margin: 0;
  max-width: 669px;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.56px;
  color: #535862;
}

.col-hero__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  box-sizing: border-box;
  border-radius: 8px;
  background: #097495;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.col-hero__cta:hover {
  background: #0a86ad;
}

.col-hero__cta img {
  display: block;
  width: 18px;
  height: 18px;
}

.col-stats {
  display: flex;
  align-items: stretch;
  gap: 52px;
  width: 100%;
  max-width: 1208px;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.6s ease 0.12s,
    transform 0.6s ease 0.12s;
}

.col-hero--ready .col-stats {
  opacity: 1;
  transform: none;
}

.col-stats__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex: 1 1 0;
  min-width: 0;
  height: 174px;
  padding: 20px 16px;
  box-sizing: border-box;
  background: #ffffff;
  border: 1px solid #e9eaeb;
  border-radius: 14.141px;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.1),
    0 1px 2px -1px rgba(0, 0, 0, 0.1);
}

.col-stats__value {
  margin: 0;
  min-height: 72px;
  font-size: 64px;
  font-weight: 600;
  line-height: 72px;
  letter-spacing: -1.92px;
  text-align: center;
  color: #181d27;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.col-stats__label {
  margin: 0;
  max-width: 185px;
  font-size: 20px;
  font-weight: 600;
  line-height: 32px;
  letter-spacing: -0.6px;
  text-align: center;
  color: #414651;
}

/* —— Smarter diagram —— */
.col-smarter {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 80px 74px 40px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 56px;
}

.col-smarter__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(880px, 100%);
  text-align: center;
}

.col-smarter__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.col-smarter__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.col-smarter__visual {
  width: 100%;
  max-width: 1291px;
}

/* —— Flow — Figma 466:22604+ —— */
.col-flow {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 80px 100px 40px;
  box-sizing: border-box;
}

.col-flow__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  max-width: 684px;
  margin: 0 auto 72px;
  text-align: center;
}

.col-flow__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.col-flow__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.col-flow__list {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 88px;
  max-width: 960px;
  margin-inline: auto;
}

.col-flow__wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: visible;
}

.col-flow__wire {
  fill: none;
  stroke: #252b37;
  stroke-width: 1;
  stroke-dasharray: 6 6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.col-flow__wire-progress {
  fill: none;
  stroke: #06b6d4;
  stroke-width: 2.5;
  stroke-dashoffset: 0;
  stroke-linecap: round;
  stroke-linejoin: round;
  filter: url(#col-wire-progress-glow);
  opacity: 0.95;
}

.col-flow__wire-dot {
  fill: #252b37;
  transition:
    fill 0.2s ease,
    filter 0.2s ease;
}

.col-flow__wire-dot--lit {
  fill: #06b6d4;
  filter: drop-shadow(0 0 5px rgba(6, 182, 212, 0.9));
}

@media (prefers-reduced-motion: reduce) {
  .col-flow__wire-progress {
    filter: none;
  }
}

.col-flow__row {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 48px;
  align-items: center;
  min-height: 220px;
}

.col-flow__row--reverse {
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
}

.col-flow__row--reverse .col-flow__copy {
  order: 2;
}

.col-flow__row--reverse .col-flow__visual {
  order: 1;
}

.col-flow__copy {
  display: flex;
  gap: 7px;
  align-items: flex-start;
  max-width: 401px;
}

.col-flow__num {
  flex: 0 0 auto;
  min-width: 36px;
  font-size: 24px;
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.24px;
  color: #252b37;
}

.col-flow__text {
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 0;
}

.col-flow__name {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  line-height: normal;
  letter-spacing: -0.24px;
  color: #222831;
}

.col-flow__desc {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  line-height: 24px;
  color: #535862;
}

.col-flow__visual {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 220px;
}

.col-flow__media {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  object-fit: contain;
}

/* —— Journey —— */
.col-journey {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 60px 100px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 108px;
}

.col-journey__copy {
  flex: 0 1 440px;
  width: min(440px, 100%);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.col-journey__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.col-journey__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.col-journey__grid {
  flex: 1 1 682px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  min-width: 0;
}

.col-journey__card {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 12px;
  min-height: 263px;
  padding: 20px;
  box-sizing: border-box;
  background: #f8fafc;
  border-radius: 12px;
}

.col-journey__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 54.568px;
  height: 54.568px;
  padding: 13.284px;
  box-sizing: border-box;
  background: #097495;
  border-radius: 6.642px;
}

.col-journey__icon img {
  display: block;
  width: 28px;
  height: 28px;
}

.col-journey__card-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
  color: #252b37;
}

.col-journey__card-body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #535862;
}

/* —— Experiences — Juspay-style center carousel —— */
.col-exp {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 60px 40px 80px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  background: #ffffff;
  overflow: hidden;
}

.col-exp__head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(976px, 100%);
  text-align: center;
}

.col-exp__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.col-exp__body {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.col-exp__viewport {
  width: 100%;
  overflow: hidden;
  padding: 24px 0;
}

.col-exp__track {
  display: flex;
  align-items: center;
  gap: 24px;
  width: max-content;
  will-change: transform;
  transition: transform 0.5s ease-in-out;
}

.col-exp__track--instant {
  transition: none !important;
}

.col-exp__track--instant .col-exp__slide {
  transition: none !important;
}

.col-exp__slide {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  width: min(980px, 92vw);
  transform-origin: center center;
  transition:
    transform 0.5s ease-in-out,
    opacity 0.5s ease-in-out;
  will-change: transform, opacity;
  cursor: pointer;
}

.col-exp__slide--active {
  z-index: 2;
}

.col-exp__marker {
  display: none;
  flex: 0 0 auto;
  align-items: center;
  gap: 8px;
}

.col-exp__marker-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  box-sizing: border-box;
  border: 1px solid #9fd0e0;
  border-radius: 5px;
  color: #097495;
  font-size: 18px;
  font-weight: 600;
  line-height: 1;
}

.col-exp__marker-line {
  display: block;
  width: 36px;
  height: 1px;
  background: #097495;
}

.col-exp__marker--right {
  flex-direction: row;
}

.col-exp__panel {
  flex: 1 1 auto;
  min-width: 0;
  display: flex;
  align-items: stretch;
  gap: 0;
  width: 100%;
  min-height: 275px;
  padding: 6px;
  box-sizing: border-box;
  background: #f8fafb;
  border-radius: 24px;
}

.col-exp__visual {
  flex: 0 0 42%;
  max-width: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: stretch;
  padding: 12px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
}

.col-exp__media {
  display: block;
  width: 100%;
  max-height: min(360px, 100%);
  height: auto;
  margin: 0 auto;
  object-fit: contain;
  object-position: center center;
}

.col-exp__card-text {
  flex: 1 1 auto;
  align-self: stretch;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 16px;
  padding: 24px 28px 24px 32px;
  box-sizing: border-box;
}

.col-exp__card-title {
  margin: 0;
  font-size: clamp(20px, 2.4vw, 36px);
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.72px;
  color: #1c1c1c;
}

.col-exp__card-body {
  margin: 0;
  font-size: clamp(13px, 1.1vw, 16px);
  font-weight: 400;
  line-height: 1.6;
  color: #5f5f5f;
}

.col-exp__nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.col-exp__nav-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 68px;
  height: 44px;
  padding: 0;
  box-sizing: border-box;
  border: 1px solid #e7e7e7;
  border-radius: 999px;
  background: #ffffff;
  cursor: pointer;
  transition: transform 0.15s ease-in-out;
}

.col-exp__nav-btn:hover {
  transform: scale(1.05);
}

.col-exp__nav-btn img {
  display: block;
  width: 24px;
  height: 24px;
}

.col-exp__nav-btn--prev img {
  transform: rotate(180deg);
}

.col-exp__nav-btn--next {
  border-color: #0d0c0d;
  background: #0d0c0d;
}

.col-exp__nav-btn--next img {
  filter: brightness(0) invert(1);
}

@media (min-width: 1101px) {
  .col-exp {
    padding: 60px 80px 100px;
    gap: 48px;
  }

  .col-exp__marker {
    display: flex;
  }

  .col-exp__panel {
    min-height: 440px;
    padding: 16px;
  }

  .col-exp__visual {
    flex: 0 0 360px;
    max-width: 360px;
    padding: 12px;
  }

  .col-exp__card-text {
    gap: 32px;
    padding: 32px 65px 32px 50px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .col-exp__track,
  .col-exp__slide,
  .col-exp__nav-btn {
    transition: none;
  }
}

@media (max-width: 1100px) {
  .col-hero__inner,
  .col-journey,
  .col-exp,
  .col-flow,
  .col-smarter {
    padding-left: 40px;
    padding-right: 40px;
  }

  .col-stats {
    gap: 20px;
  }

  .col-stats__value {
    font-size: 48px;
    line-height: 56px;
    min-height: 56px;
  }

  .col-stats__label {
    font-size: 16px;
    line-height: 24px;
  }

  .col-flow__row,
  .col-flow__row--reverse {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .col-flow__row--reverse .col-flow__copy,
  .col-flow__row--reverse .col-flow__visual {
    order: unset;
  }

  .col-flow__list {
    gap: 56px;
  }

  .col-flow__wires {
    display: none;
  }

  .col-journey {
    flex-direction: column;
    align-items: stretch;
    gap: 40px;
  }

  .col-journey__copy {
    flex: none;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .col-hero__inner {
    padding-top: 48px;
    gap: 40px;
  }

  .col-hero__title,
  .col-smarter__title,
  .col-flow__title,
  .col-journey__title,
  .col-exp__title {
    font-size: 28px;
    line-height: 1.3;
  }

  .col-stats {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  .col-stats__card {
    height: auto;
    min-height: 140px;
  }

  .col-journey__grid {
    grid-template-columns: 1fr;
  }

  .col-journey__card {
    min-height: 0;
  }

  .col-exp {
    padding: 40px 16px 64px;
    gap: 28px;
  }

  .col-exp__panel {
    flex-direction: column;
    min-height: 0;
  }

  .col-exp__visual {
    flex: 0 0 auto;
    max-width: none;
    width: 100%;
    min-height: 160px;
    align-self: stretch;
  }

  .col-exp__media {
    max-height: 220px;
  }

  .col-exp__card-text {
    padding: 20px 16px 24px;
    gap: 10px;
  }

  .col-exp__nav-btn {
    width: 60px;
    height: 40px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .col-hero__copy,
  .col-stats {
    transition: none;
  }
}
</style>
