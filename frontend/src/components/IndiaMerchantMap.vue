<script setup>
import { computed, nextTick, onMounted, ref, watch } from "vue";
import indiaSvgRaw from "@svg-maps/india/india.svg?raw";
import { pinPosition } from "@/constants/indiaMapAnchors";
import { INDIA_MAP_VIEWBOX } from "@/constants/indiaMapProjection";

const VIEWBOX_W = 612;
const VIEWBOX_H = 696;
const GLOW_FILTER_PAD = 48;
const BUBBLE_W = 220;
const BUBBLE_H = 52;
const BUBBLE_GAP = 12;

const indiaMapPaths = (() => {
  const match = indiaSvgRaw.match(/<svg[^>]*>([\s\S]*)<\/svg>/i);
  if (!match) return "";
  // @svg-maps/india adds aria-label on <path>, which Lighthouse flags as prohibited.
  return match[1].replace(/\s*aria-label="[^"]*"/gi, "");
})();

const props = defineProps({
  map: { type: Object, required: true },
  variant: {
    type: String,
    default: "light",
    validator: (value) => value === "light" || value === "admin",
  },
  hint: { type: String, default: "Hover a point to see partners" },
  compact: { type: Boolean, default: false },
  ariaLabel: {
    type: String,
    default: "Map of India showing Urbanrupee merchant locations",
  },
});

const hoveredId = ref(null);
const svgRoot = ref(null);

const locations = computed(() =>
  (props.map.locations || []).map((loc) => ({
    ...loc,
    stateId: loc.state_id,
    ...pinPosition(loc),
  })),
);

const activeLocation = computed(() =>
  locations.value.find((loc) => loc.id === hoveredId.value),
);

function onEnter(id) {
  hoveredId.value = id;
}

function onLeave() {
  hoveredId.value = null;
}

function updateStateHighlight() {
  const root = svgRoot.value;
  if (!root) return;

  root.querySelectorAll(".india-map__states path").forEach((path) => {
    path.classList.remove("india-map__state--active");
  });

  const loc = activeLocation.value;
  if (loc?.stateId) {
    root.querySelector(`#${CSS.escape(loc.stateId)}`)?.classList.add(
      "india-map__state--active",
    );
  }
}

watch(hoveredId, () => {
  nextTick(updateStateHighlight);
});

onMounted(() => {
  nextTick(updateStateHighlight);
});

function bubbleTransform(loc) {
  const aboveY = loc.y - BUBBLE_GAP - BUBBLE_H;
  const y = aboveY < 8 ? loc.y + BUBBLE_GAP + 8 : aboveY;
  return `translate(${loc.x}, ${y})`;
}
</script>

<template>
  <div class="india-map" :class="[`india-map--${variant}`, { 'india-map--compact': compact }]">
    <div class="india-map__frame">
      <div class="india-map__map-wrap">
        <svg
          ref="svgRoot"
          class="india-map__svg"
          :viewBox="INDIA_MAP_VIEWBOX"
          preserveAspectRatio="xMidYMid meet"
          role="img"
          :aria-label="ariaLabel"
        >
          <defs>
            <linearGradient
              id="india-map-brand-gradient"
              gradientUnits="userSpaceOnUse"
              x1="0"
              :y1="VIEWBOX_H"
              :x2="VIEWBOX_W"
              y2="0"
            >
              <stop offset="0%" stop-color="#1a365d" />
              <stop offset="100%" stop-color="#06b6d4" />
            </linearGradient>
            <filter
              id="india-map-pin-glow"
              filterUnits="userSpaceOnUse"
              :x="-GLOW_FILTER_PAD"
              :y="-GLOW_FILTER_PAD"
              :width="VIEWBOX_W + GLOW_FILTER_PAD * 2"
              :height="VIEWBOX_H + GLOW_FILTER_PAD * 2"
            >
              <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur" />
              <feFlood flood-color="#ffffff" flood-opacity="0.75" result="color" />
              <feComposite in="color" in2="blur" operator="in" result="glow" />
              <feMerge>
                <feMergeNode in="glow" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <filter
              id="india-map-pin-glow-strong"
              filterUnits="userSpaceOnUse"
              :x="-GLOW_FILTER_PAD"
              :y="-GLOW_FILTER_PAD"
              :width="VIEWBOX_W + GLOW_FILTER_PAD * 2"
              :height="VIEWBOX_H + GLOW_FILTER_PAD * 2"
            >
              <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
              <feFlood flood-color="#ffffff" flood-opacity="0.9" result="color" />
              <feComposite in="color" in2="blur" operator="in" result="glow" />
              <feMerge>
                <feMergeNode in="glow" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <g class="india-map__states" v-html="indiaMapPaths" />
          <g
            v-for="(loc, index) in locations"
            :key="loc.id"
            class="india-map__marker"
            :class="{
              'india-map__marker--active': hoveredId === loc.id,
              'india-map__marker--payin': loc.kind === 'payin',
              'india-map__marker--payout': loc.kind !== 'payin',
            }"
            :style="{ '--pulse-delay': `${(index % 7) * 0.42}s` }"
            @mouseenter="onEnter(loc.id)"
            @mouseleave="onLeave"
            @focusin="onEnter(loc.id)"
            @focusout="onLeave"
          >
            <circle
              class="india-map__halo"
              :cx="loc.x"
              :cy="loc.y"
              r="5"
              pointer-events="none"
            />
            <circle
              class="india-map__ripple"
              :cx="loc.x"
              :cy="loc.y"
              r="5"
              pointer-events="none"
            />
            <circle
              class="india-map__hit"
              :cx="loc.x"
              :cy="loc.y"
              r="10"
              tabindex="0"
              role="button"
              :aria-label="loc.company"
            />
            <circle
              class="india-map__dot"
              :cx="loc.x"
              :cy="loc.y"
              r="2.5"
              pointer-events="none"
            />
          </g>

          <g
            v-if="activeLocation"
            class="india-map__bubble-layer"
            :transform="bubbleTransform(activeLocation)"
            pointer-events="none"
          >
            <foreignObject
              :x="-BUBBLE_W / 2"
              y="0"
              :width="BUBBLE_W"
              :height="BUBBLE_H"
              class="india-map__bubble-fo"
            >
              <div
                xmlns="http://www.w3.org/1999/xhtml"
                class="india-map__bubble-inner"
                :class="{ 'india-map__bubble-inner--admin': variant === 'admin' }"
              >
                {{ activeLocation.company }}
              </div>
            </foreignObject>
          </g>
        </svg>
      </div>

      <p v-if="hint" class="india-map__hint">{{ hint }}</p>
    </div>
  </div>
</template>

<style scoped>
.india-map {
  --map-pin-core: #ffffff;
  --map-pin-stroke: #1a365d;
  --map-pin-glow: rgba(255, 255, 255, 0.9);
  --map-pin-glow-soft: rgba(255, 255, 255, 0.5);
  width: 100%;
}

.india-map__frame {
  margin-top: 0;
}

.india-map__map-wrap {
  position: relative;
  overflow: visible;
}

.india-map__svg {
  display: block;
  width: 100%;
  max-width: none;
  min-height: 280px;
  background: transparent;
  overflow: visible;
}

.india-map__states :deep(path) {
  fill: url(#india-map-brand-gradient);
  stroke: #ffffff;
  stroke-width: 1;
  pointer-events: none;
  transition:
    stroke 0.2s ease,
    stroke-width 0.2s ease;
}

.india-map__states :deep(path.india-map__state--active) {
  stroke: var(--map-pin-core);
  stroke-width: 1.25;
}

.india-map__marker {
  pointer-events: all;
  cursor: pointer;
}

.india-map__marker--payout {
  --map-pin-core: #ff9f0a;
  --map-pin-stroke: #ff6b00;
  --map-pin-glow: rgba(255, 159, 10, 0.95);
  --map-pin-glow-soft: rgba(255, 107, 0, 0.55);
}

.india-map__marker--payin {
  --map-pin-core: #32ff7e;
  --map-pin-stroke: #00ff88;
  --map-pin-glow: rgba(0, 255, 136, 0.95);
  --map-pin-glow-soft: rgba(50, 255, 126, 0.55);
}

.india-map__marker--payout .india-map__halo,
.india-map__marker--payout .india-map__dot,
.india-map__marker--payin .india-map__halo,
.india-map__marker--payin .india-map__dot {
  filter: drop-shadow(0 0 4px var(--map-pin-glow))
    drop-shadow(0 0 8px var(--map-pin-glow-soft));
}

.india-map__marker--payout:hover .india-map__halo,
.india-map__marker--payout.india-map__marker--active .india-map__halo,
.india-map__marker--payout:hover .india-map__dot,
.india-map__marker--payout.india-map__marker--active .india-map__dot,
.india-map__marker--payin:hover .india-map__halo,
.india-map__marker--payin.india-map__marker--active .india-map__halo,
.india-map__marker--payin:hover .india-map__dot,
.india-map__marker--payin.india-map__marker--active .india-map__dot {
  filter: drop-shadow(0 0 6px var(--map-pin-glow))
    drop-shadow(0 0 12px var(--map-pin-glow))
    drop-shadow(0 0 18px var(--map-pin-glow-soft));
}

.india-map__halo {
  fill: var(--map-pin-core);
  opacity: 0.32;
  transform-origin: center;
  transform-box: fill-box;
  pointer-events: none;
  animation: map-halo-breathe 3.6s ease-in-out infinite;
  animation-delay: var(--pulse-delay, 0s);
  filter: url(#india-map-pin-glow)
    drop-shadow(0 0 5px var(--map-pin-glow-soft));
}

.india-map__ripple {
  fill: none;
  stroke: var(--map-pin-core);
  stroke-width: 2;
  transform-origin: center;
  transform-box: fill-box;
  pointer-events: none;
  opacity: 0;
  animation: map-ripple 3.2s cubic-bezier(0.22, 0.61, 0.36, 1) infinite;
  animation-delay: var(--pulse-delay, 0s);
  filter: drop-shadow(0 0 4px var(--map-pin-glow));
}

.india-map__dot {
  fill: var(--map-pin-core);
  stroke: var(--map-pin-stroke);
  stroke-width: 1.25;
  transform-origin: center;
  transform-box: fill-box;
  animation: map-dot-breathe 3.6s ease-in-out infinite;
  animation-delay: var(--pulse-delay, 0s);
  filter: url(#india-map-pin-glow)
    drop-shadow(0 0 4px var(--map-pin-glow))
    drop-shadow(0 0 8px var(--map-pin-glow-soft))
    drop-shadow(0 1px 2px rgba(26, 54, 93, 0.5));
}

.india-map__hit {
  fill: transparent;
  stroke: none;
}

.india-map__marker:hover .india-map__halo,
.india-map__marker--active .india-map__halo {
  opacity: 0.55;
  animation-duration: 2.4s;
  filter: url(#india-map-pin-glow-strong)
    drop-shadow(0 0 8px var(--map-pin-glow));
}

.india-map__marker:hover .india-map__ripple,
.india-map__marker--active .india-map__ripple {
  animation-duration: 2.2s;
  stroke: var(--map-pin-core);
  stroke-width: 2.5;
  opacity: 1;
  filter: drop-shadow(0 0 6px var(--map-pin-glow));
}

.india-map__marker:hover .india-map__dot,
.india-map__marker--active .india-map__dot {
  animation: none;
  transform: scale(1.2);
  fill: var(--map-pin-core);
  stroke: var(--map-pin-stroke);
  filter: url(#india-map-pin-glow-strong)
    drop-shadow(0 0 6px var(--map-pin-glow))
    drop-shadow(0 0 12px var(--map-pin-glow))
    drop-shadow(0 0 18px var(--map-pin-glow-soft));
}

.india-map__bubble-fo {
  overflow: visible;
}

.india-map__bubble-inner {
  box-sizing: border-box;
  width: 100%;
  padding: 8px 12px;
  border-radius: 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-card);
  font-size: 12px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--text-primary);
  text-align: center;
  word-break: break-word;
}

.india-map__bubble-inner--admin {
  background: var(--ur-card-bg, #162528);
  border-color: var(--ur-card-border, #1e3538);
  color: var(--ur-text, #f0fafb);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
}

.india-map__hint {
  margin: 12px 0 0;
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
}

@keyframes map-ripple {
  0% {
    transform: scale(1);
    opacity: 0.85;
  }
  100% {
    transform: scale(3.2);
    opacity: 0;
  }
}

@keyframes map-halo-breathe {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.5;
  }
}

@keyframes map-dot-breathe {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.08);
  }
}

.india-map--admin .india-map__hint {
  color: var(--ur-muted, #4a8890);
}

.india-map--compact {
  height: 100%;
}

.india-map--compact .india-map__frame {
  height: 100%;
}

.india-map--compact .india-map__map-wrap {
  height: 100%;
}

.india-map--compact .india-map__svg {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 0;
  max-height: none;
}

.india-map--compact .india-map__hint {
  margin-top: 6px;
  font-size: 11px;
}

@media (min-width: 900px) {
  .india-map:not(.india-map--compact) .india-map__svg {
    min-height: 340px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .india-map__ripple {
    animation: none;
    opacity: 0.25;
    transform: scale(1.6);
  }

  .india-map__halo,
  .india-map__dot {
    animation: none;
  }

  .india-map__halo {
    opacity: 0.45;
  }

  .india-map__ripple {
    opacity: 0.6;
  }

  .india-map__states :deep(path),
  .india-map__dot {
    transition: none;
  }
}
</style>
