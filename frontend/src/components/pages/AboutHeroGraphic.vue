<script setup>
import { computed } from "vue";
import { useAboutEco } from "@/composables/useAboutEco.js";

const VIEWBOX = 360;
const CENTER = 180;
const HUB_RADIUS = 52;
const INNER_ORBIT_RADIUS = 96;
const OUTER_ORBIT_RADIUS = 114;
const NODE_ORBIT_RADIUS = 148;

const COLORS = {
  navy: "#1a365d",
  cyan: "#06b6d4",
  pale: "#dde6f2",
  white: "#ffffff",
};

const NODE_LAYOUT = {
  vision: { angle: -90, side: "top" },
  mission: { angle: -30, side: "right" },
  solutions: { angle: 30, side: "right" },
  growth: { angle: 90, side: "bottom" },
  security: { angle: 150, side: "left" },
  trust: { angle: 210, side: "left" },
};

const eco = useAboutEco();
const { nodes, activeId, lockedId, onNodeEnter, onNodeLeave, onNodeClick, onHubClick } = eco;

function pointOnRadius(angleDeg, radius) {
  const radians = (angleDeg * Math.PI) / 180;
  return {
    x: CENTER + Math.cos(radians) * radius,
    y: CENTER + Math.sin(radians) * radius,
  };
}

function labelStyle(side) {
  if (side === "top") {
    return {
      left: "50%",
      bottom: "var(--eco-label-stack, 64px)",
      transform: "translateX(-50%)",
    };
  }

  if (side === "bottom") {
    return {
      left: "50%",
      top: "var(--eco-label-stack, 64px)",
      transform: "translateX(-50%)",
    };
  }

  if (side === "left") {
    return {
      right: "var(--eco-label-side, 64px)",
      top: "50%",
      transform: "translateY(-50%)",
      textAlign: "right",
    };
  }

  return {
    left: "var(--eco-label-side, 64px)",
    top: "50%",
    transform: "translateY(-50%)",
  };
}

const nodeModels = computed(() =>
  nodes.map((node, index) => {
    const layout = NODE_LAYOUT[node.id];
    const center = pointOnRadius(layout.angle, NODE_ORBIT_RADIUS);
    const spokeStart = pointOnRadius(layout.angle, HUB_RADIUS + 8);
    const spokeEnd = pointOnRadius(layout.angle, INNER_ORBIT_RADIUS);
    const isActive = eco.ready && activeId.value === node.id;
    const isSpecial = node.id === "vision" || node.id === "growth";
    return {
      ...node,
      index,
      center,
      spokeStart,
      spokeEnd,
      isSpecial,
      side: layout.side,
      wrapperStyle: {
        position: "absolute",
        left: `${(center.x / VIEWBOX) * 100}%`,
        top: `${(center.y / VIEWBOX) * 100}%`,
        width: "0",
        height: "0",
        zIndex: 3,
      },
      cardStyle: {
        position: "relative",
        transform: "translate(-50%, -50%)",
        padding: "0",
        border: "none",
        background: "transparent",
        cursor: "pointer",
        opacity: eco.ready ? "1" : "0",
      },
      iconStyle: {
        width: "var(--eco-node-size, 52px)",
        height: "var(--eco-node-size, 52px)",
        borderRadius: "50%",
        border: `2px solid ${isActive ? COLORS.cyan : COLORS.pale}`,
        background: COLORS.white,
        boxShadow: isActive
          ? "0 8px 24px rgba(6, 182, 212, 0.3), 0 0 0 3px rgba(6, 182, 212, 0.12)"
          : "0 4px 16px rgba(26, 54, 93, 0.12)",
        display: "grid",
        placeItems: "center",
      },
      labelStyle: {
        position: "absolute",
        fontFamily: '"Manrope", "DM Sans", system-ui, sans-serif',
        fontSize: "var(--eco-label-size, 12px)",
        fontWeight: "600",
        lineHeight: "1",
        whiteSpace: "nowrap",
        color: isActive ? COLORS.cyan : COLORS.navy,
        ...labelStyle(layout.side),
      },
      connectorPath: `M ${spokeStart.x} ${spokeStart.y} L ${spokeEnd.x} ${spokeEnd.y}`,
    };
  }),
);

const activeConnectorPath = computed(() => {
  const active = nodeModels.value.find((node) => node.id === activeId.value) ?? nodeModels.value[0];
  return active?.connectorPath ?? "";
});

function handleNodeKeydown(event, id) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    onNodeClick(id);
  }
}

function handleHubKeydown(event) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    onHubClick();
  }
}
</script>

<template>
  <div
    class="eco"
    :class="{ 'eco--ready': eco.ready }"
    role="group"
    aria-label="Interactive payments ecosystem"
  >
    <svg class="eco__lines" :viewBox="`0 0 ${VIEWBOX} ${VIEWBOX}`" aria-hidden="true">
      <defs>
        <linearGradient id="ecoLine" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1a365d" stop-opacity="0.38" />
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.82" />
        </linearGradient>
        <linearGradient id="ecoLineActive" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#1a365d" />
          <stop offset="100%" stop-color="#06b6d4" />
        </linearGradient>
        <linearGradient
          id="ecoLineActiveVertical"
          gradientUnits="userSpaceOnUse"
          x1="180"
          y1="84"
          x2="180"
          y2="276"
        >
          <stop offset="0%" stop-color="#1a365d" />
          <stop offset="100%" stop-color="#06b6d4" />
        </linearGradient>
      </defs>

      <circle
        class="eco__orbit eco__orbit--outer"
        :cx="CENTER"
        :cy="CENTER"
        :r="OUTER_ORBIT_RADIUS"
      />
      <circle
        class="eco__orbit eco__orbit--inner"
        :cx="CENTER"
        :cy="CENTER"
        :r="INNER_ORBIT_RADIUS"
      />

      <g v-for="node in nodeModels" :key="`${node.id}-connector`">
        <line
          v-if="!node.isSpecial"
          :x1="node.spokeStart.x"
          :y1="node.spokeStart.y"
          :x2="node.spokeEnd.x"
          :y2="node.spokeEnd.y"
          class="eco__spoke"
          :class="{ 'eco__spoke--active': eco.ready && activeId === node.id }"
          :style="{ '--spoke-i': node.index }"
        />
        <g v-else>
          <line
            :x1="node.spokeStart.x"
            :y1="node.spokeStart.y"
            :x2="node.spokeEnd.x"
            :y2="node.spokeEnd.y"
            class="eco__special-spoke-base"
            :class="{ 'eco__special-spoke-base--active': eco.ready && activeId === node.id }"
          />
        </g>
      </g>

      <circle
        v-if="eco.ready"
        :key="activeId"
        class="eco__pulse-dot"
        r="5"
      >
        <animateMotion
          dur="1.35s"
          repeatCount="indefinite"
          :path="activeConnectorPath"
          keyTimes="0;1"
          keySplines="0.4 0 0.2 1"
          calcMode="spline"
        />
      </circle>
    </svg>

    <button
      type="button"
      class="eco__hub"
      aria-label="Payments hub. Click to resume auto highlight."
      @click="onHubClick"
      @keydown="handleHubKeydown"
    >
      <span class="eco__hub-ring eco__hub-ring--1" aria-hidden="true" />
      <span class="eco__hub-ring eco__hub-ring--2" aria-hidden="true" />
      <span class="eco__hub-inner">
        <img
          class="eco__hub-mark"
          src="/logos/favicon.svg"
          alt=""
          width="43"
          height="31"
          decoding="async"
          aria-hidden="true"
        />
      </span>
    </button>

    <div
      v-for="node in nodeModels"
      :key="node.id"
      :style="node.wrapperStyle"
    >
      <button
        type="button"
        :style="node.cardStyle"
        :aria-pressed="lockedId === node.id"
        :aria-label="`${node.label}: ${node.hint}`"
        @mouseenter="onNodeEnter(node.id)"
        @mouseleave="onNodeLeave"
        @click="onNodeClick(node.id)"
        @keydown="handleNodeKeydown($event, node.id)"
      >
        <span :style="node.iconStyle" aria-hidden="true">
          <svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true">
            <polygon
              v-if="node.icon === 'vision'"
              points="13,5 5,19 21,19"
              :fill="COLORS.cyan"
            />
            <g v-else-if="node.icon === 'mission'">
              <circle cx="13" cy="13" r="8.5" fill="none" :stroke="COLORS.cyan" stroke-width="2.6" />
              <circle cx="13" cy="13" r="3.2" :fill="COLORS.cyan" />
            </g>
            <g v-else-if="node.icon === 'solutions'">
              <rect x="3.5" y="7" width="9.5" height="12" rx="2" :fill="COLORS.navy" />
              <rect x="13" y="7" width="9.5" height="12" rx="2" :fill="COLORS.cyan" />
            </g>
            <g v-else-if="node.icon === 'growth'">
              <rect x="3.5" y="14" width="5" height="7" :fill="COLORS.navy" />
              <rect x="10.5" y="9" width="5" height="12" :fill="COLORS.cyan" />
              <rect x="17.5" y="11" width="5" height="10" :fill="COLORS.cyan" />
            </g>
            <path
              v-else-if="node.icon === 'security'"
              d="M13 4 L19 7 V14 C19 18 15.5 20.5 13 21.5 C10.5 20.5 7 18 7 14 V7 Z"
              :fill="'rgba(6, 182, 212, 0.12)'"
              :stroke="COLORS.navy"
              stroke-width="2"
              stroke-linejoin="round"
            />
            <path
              v-else-if="node.icon === 'trust'"
              d="M5.5 13 L11 18.5 L20.5 8.5"
              fill="none"
              :stroke="COLORS.cyan"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </span>
        <span :style="node.labelStyle">{{ node.label }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.eco {
  width: min(100%, 360px);
  aspect-ratio: 1;
  position: relative;
  --navy: #1a365d;
  --cyan: #06b6d4;
  --eco-node-size: 52px;
  --eco-label-size: 12px;
  --eco-label-side: 64px;
  --eco-label-stack: 64px;
}

.eco__lines {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.eco__orbit {
  fill: none;
  stroke: url(#ecoLine);
  opacity: 0.5;
}

.eco__orbit--outer {
  stroke-width: 1.75;
  stroke-dasharray: 8 14;
}

.eco__orbit--inner {
  stroke-width: 2.5;
  stroke-dasharray: 5 11;
}

.eco--ready .eco__orbit--outer {
  animation: eco-orbit-drift 20s linear infinite;
}

.eco--ready .eco__orbit--inner {
  animation: eco-orbit-drift-reverse 14s linear infinite;
}

.eco__spoke {
  stroke: url(#ecoLine);
  stroke-width: 2;
  stroke-dasharray: 8 10;
  stroke-linecap: round;
  opacity: 0.4;
  transition:
    stroke-width 0.25s ease,
    opacity 0.25s ease;
}

.eco__special-spoke-base {
  stroke: rgba(148, 163, 184, 0.62);
  stroke-width: 2.25;
  stroke-linecap: round;
  stroke-dasharray: 8 10;
  animation: eco-dash-flow 1.2s linear infinite;
}

.eco__special-spoke-base--active {
  stroke: url(#ecoLineActiveVertical);
  stroke-width: 2.25;
  opacity: 1;
  animation:
    eco-dash-flow 0.75s linear infinite,
    eco-spoke-glow 1.4s ease-in-out infinite;
}

.eco--ready .eco__spoke {
  animation: eco-dash-flow 1.2s linear infinite;
  animation-delay: calc(var(--spoke-i, 0) * -0.18s);
}

.eco__spoke--active {
  stroke: url(#ecoLineActive);
  stroke-width: 3.5;
  opacity: 1;
  animation:
    eco-dash-flow 0.75s linear infinite,
    eco-spoke-glow 1.4s ease-in-out infinite;
}

.eco__pulse-dot {
  fill: var(--cyan);
  opacity: 0.95;
  filter: drop-shadow(0 0 6px rgba(6, 182, 212, 0.9));
}

.eco__hub {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 104px;
  height: 104px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  z-index: 4;
}

.eco__hub-ring {
  position: absolute;
  inset: 0;
  border: 2px solid var(--cyan);
  border-radius: 50%;
  opacity: 0;
  transform: scale(0.84);
}

.eco--ready .eco__hub-ring--1 {
  animation: eco-wave 2.2s ease-out infinite;
}

.eco--ready .eco__hub-ring--2 {
  animation: eco-wave 2.2s ease-out infinite 1.1s;
}

.eco__hub-inner {
  position: absolute;
  inset: 6px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #fff;
  box-shadow:
    0 8px 32px rgba(6, 182, 212, 0.22),
    0 0 0 2px rgba(6, 182, 212, 0.22);
  opacity: 0;
  transform: scale(0.78);
  transition:
    opacity 0.45s ease 0.05s,
    transform 0.5s cubic-bezier(0.34, 1.35, 0.64, 1) 0.05s;
}

.eco--ready .eco__hub-inner {
  opacity: 1;
  transform: scale(1);
}

.eco--ready .eco__orbit--inner {
  opacity: 0.75;
}

.eco--ready .eco__hub .eco__hub-inner,
.eco__hub:hover .eco__hub-inner,
.eco__hub:focus-visible .eco__hub-inner {
  animation: eco-hub-breathe 2s ease-in-out infinite;
}

.eco__hub-mark {
  width: 43px;
  height: 31px;
  object-fit: contain;
}

@keyframes eco-dash-flow {
  to {
    stroke-dashoffset: -36;
  }
}

@keyframes eco-spoke-glow {
  0%,
  100% {
    filter: drop-shadow(0 0 2px rgba(6, 182, 212, 0.4));
  }
  50% {
    filter: drop-shadow(0 0 8px rgba(6, 182, 212, 0.9));
  }
}

@keyframes eco-orbit-drift {
  to {
    stroke-dashoffset: -140;
  }
}

@keyframes eco-orbit-drift-reverse {
  to {
    stroke-dashoffset: 110;
  }
}

@keyframes eco-wave {
  0% {
    transform: scale(0.84);
    opacity: 0.65;
  }
  100% {
    transform: scale(1.38);
    opacity: 0;
  }
}

@keyframes eco-hub-breathe {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@media (prefers-reduced-motion: reduce) {
  .eco--ready .eco__orbit,
  .eco--ready .eco__spoke,
  .eco--ready .eco__hub-ring,
  .eco--ready .eco__hub-inner,
  .eco__pulse-dot {
    animation: none !important;
  }

  .eco__hub-inner {
    opacity: 1;
    transform: none;
    transition: none;
  }
}

@media (max-width: 700px) {
  .eco {
    width: 100%;
    max-width: 300px;
    margin-inline: auto;
    --eco-node-size: 44px;
    --eco-label-size: 11px;
    --eco-label-side: 50px;
    --eco-label-stack: 54px;
  }

  .eco__hub {
    width: 88px;
    height: 88px;
  }

  .eco__hub-mark {
    width: 36px;
    height: 26px;
  }
}
</style>
