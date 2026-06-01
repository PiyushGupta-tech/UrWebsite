<script setup>
import { useAboutEco } from "@/composables/useAboutEco.js";
import { LOGO_PATHS } from "@/constants/logos.js";

const eco = useAboutEco();
const {
  nodes,
  activeId,
  activeNode,
  lockedId,
  onNodeEnter,
  onNodeLeave,
  onNodeClick,
  onHubClick,
} = eco;
</script>

<template>
  <div
    class="eco"
    :class="[
      { 'eco--ready': eco.ready },
      eco.ready && activeId ? `eco--focus-${activeId}` : '',
    ]"
      role="group"
      aria-label="Interactive payments ecosystem"
    >
      <svg class="eco__lines" viewBox="0 0 320 320" aria-hidden="true">
        <defs>
          <linearGradient id="ecoLine" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1a365d" stop-opacity="0.45" />
            <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.85" />
          </linearGradient>
          <linearGradient id="ecoLineActive" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#1a365d" />
            <stop offset="100%" stop-color="#06b6d4" />
          </linearGradient>
        </defs>

        <circle
          class="eco__orbit eco__orbit--outer"
          cx="160"
          cy="160"
          r="118"
          fill="none"
          stroke="url(#ecoLine)"
          stroke-width="1.5"
          stroke-dasharray="6 10"
        />
        <circle
          class="eco__orbit eco__orbit--inner"
          cx="160"
          cy="160"
          r="100"
          fill="none"
          stroke="url(#ecoLine)"
          stroke-width="2"
          stroke-dasharray="4 8"
        />

        <g class="eco__spokes">
          <line
            v-for="(node, i) in nodes"
            :key="node.id"
            x1="160"
            y1="160"
            :x2="node.spoke.x2"
            :y2="node.spoke.y2"
            class="eco__spoke"
            :class="{ 'eco__spoke--active': eco.ready && activeId === node.id }"
            :style="{ '--spoke-i': i }"
          />
        </g>

        <circle
          v-if="eco.ready"
          :key="activeId"
          class="eco__pulse-dot"
          r="5"
          fill="#06b6d4"
        >
          <animateMotion
            dur="1.4s"
            repeatCount="indefinite"
            :path="`M160,160 L${activeNode.spoke.x2},${activeNode.spoke.y2}`"
            keyTimes="0;1"
            keySplines="0.4 0 0.2 1"
            calcMode="spline"
          />
        </circle>
      </svg>

      <button
        type="button"
        class="eco__hub"
        :class="{ 'eco__hub--active': eco.ready }"
        aria-label="Payments hub — click to resume auto highlight"
        @click="onHubClick"
      >
        <span class="eco__hub-ring eco__hub-ring--1" aria-hidden="true" />
        <span class="eco__hub-ring eco__hub-ring--2" aria-hidden="true" />
        <span class="eco__hub-inner">
          <img
            class="eco__hub-mark"
            :src="LOGO_PATHS.icon"
            alt=""
            width="20"
            height="20"
            decoding="async"
            aria-hidden="true"
          />
          <span class="eco__hub-label">Payments</span>
        </span>
      </button>

      <div
        v-for="(node, index) in nodes"
        :key="node.id"
        class="eco__node"
        :class="[
          `eco__node--${node.pos}`,
          { 'eco__node--active': eco.ready && activeId === node.id },
        ]"
      >
        <button
          type="button"
          class="eco__card"
          :class="{
            'eco__card--visible': eco.ready,
            'eco__card--active': eco.ready && activeId === node.id,
            'eco__card--locked': lockedId === node.id,
          }"
          :style="{ '--delay': `${0.1 + index * 0.06}s`, '--float-phase': `${index * 0.35}s` }"
          :aria-pressed="lockedId === node.id"
          :aria-label="`${node.label}: ${node.hint}`"
          @mouseenter="onNodeEnter(node.id)"
          @mouseleave="onNodeLeave"
          @click="onNodeClick(node.id)"
        >
          <span class="eco__icon" :class="`eco__icon--${node.icon}`" aria-hidden="true" />
          <span class="eco__label">{{ node.label }}</span>
        </button>
      </div>
    </div>
</template>

<style scoped>
.eco {
  --navy: #1a365d;
  --cyan: #06b6d4;
  --grad: linear-gradient(135deg, var(--navy), var(--cyan));
  --size: min(100%, 384px);
  position: relative;
  width: var(--size);
  aspect-ratio: 1;
}

.eco__lines {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.eco__orbit {
  opacity: 0.5;
  transform-origin: 160px 160px;
}

.eco--ready .eco__orbit--inner {
  animation: eco-spin 16s linear infinite;
}

.eco--ready .eco__orbit--outer {
  animation: eco-spin-rev 22s linear infinite;
}

@keyframes eco-spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes eco-spin-rev {
  to {
    transform: rotate(-360deg);
  }
}

.eco--ready .eco__orbit--inner {
  opacity: 0.75;
}

.eco__spoke {
  stroke: url(#ecoLine);
  stroke-width: 2;
  stroke-dasharray: 8 10;
  opacity: 0.4;
  transition:
    stroke-width 0.25s ease,
    opacity 0.25s ease;
}

.eco--ready .eco__spoke {
  animation: eco-dash-march 1.2s linear infinite;
  animation-delay: calc(var(--spoke-i, 0) * -0.2s);
}

@keyframes eco-dash-march {
  to {
    stroke-dashoffset: -36;
  }
}

.eco__spoke--active {
  stroke: url(#ecoLineActive);
  stroke-width: 3.5;
  opacity: 1;
  animation:
    eco-dash-march 0.7s linear infinite,
    eco-spoke-glow 1.4s ease-in-out infinite;
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

.eco__pulse-dot {
  opacity: 0.95;
  filter: drop-shadow(0 0 6px rgba(6, 182, 212, 0.9));
}

/* Hub */
.eco__hub {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 4;
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
  border-radius: 50%;
}

.eco__hub-ring {
  position: absolute;
  left: 50%;
  top: 50%;
  border-radius: 50%;
  border: 2px solid var(--cyan);
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0.85);
  opacity: 0;
}

.eco--ready .eco__hub-ring--1 {
  width: 110px;
  height: 110px;
  animation: eco-ring-expand 2.2s ease-out infinite;
}

.eco--ready .eco__hub-ring--2 {
  width: 110px;
  height: 110px;
  animation: eco-ring-expand 2.2s ease-out infinite 1.1s;
}

@keyframes eco-ring-expand {
  0% {
    transform: translate(-50%, -50%) scale(0.75);
    opacity: 0.7;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.35);
    opacity: 0;
  }
}

.eco__hub-inner {
  position: relative;
  z-index: 1;
  width: 92px;
  height: 92px;
  border-radius: 50%;
  background: var(--grad);
  box-shadow:
    0 8px 32px rgba(6, 182, 212, 0.45),
    0 0 0 6px #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  opacity: 0;
  transform: scale(0.75);
  transition:
    opacity 0.5s ease 0.05s,
    transform 0.55s cubic-bezier(0.34, 1.4, 0.64, 1) 0.05s,
    box-shadow 0.3s ease;
}

.eco--ready .eco__hub-inner {
  opacity: 1;
  transform: scale(1);
}

.eco--ready .eco__hub--active .eco__hub-inner,
.eco__hub:hover .eco__hub-inner,
.eco__hub:focus-visible .eco__hub-inner {
  animation: eco-hub-breathe 2s ease-in-out infinite;
}

@keyframes eco-hub-breathe {
  0%,
  100% {
    transform: scale(1);
    box-shadow:
      0 8px 32px rgba(6, 182, 212, 0.45),
      0 0 0 6px #fff;
  }
  50% {
    transform: scale(1.08);
    box-shadow:
      0 12px 40px rgba(6, 182, 212, 0.65),
      0 0 0 6px #fff,
      0 0 24px rgba(6, 182, 212, 0.35);
  }
}

.eco__hub-mark {
  width: 20px;
  height: 20px;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.25));
}

.eco__hub-label {
  font-size: 10px;
  font-weight: 600;
  color: #fff;
}

/* Nodes */
.eco__node {
  position: absolute;
  z-index: 3;
}

.eco__node--top {
  left: 50%;
  top: 0;
  transform: translateX(-50%);
}

.eco__node--top-right {
  right: 0;
  top: 18%;
}

.eco__node--bottom-right {
  right: 0;
  bottom: 18%;
}

.eco__node--bottom {
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
}

.eco__node--bottom-left {
  left: 0;
  bottom: 18%;
}

.eco__node--top-left {
  left: 0;
  top: 18%;
}

.eco__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  border: none;
  background: none;
  padding: 4px;
  cursor: pointer;
  opacity: 0;
  transform: scale(0.8) translateY(8px);
  transition:
    opacity 0.4s ease var(--delay, 0s),
    transform 0.45s cubic-bezier(0.34, 1.35, 0.64, 1) var(--delay, 0s);
}

.eco__card--visible {
  opacity: 1;
  transform: scale(1) translateY(0);
}

.eco--ready .eco__card--visible:not(.eco__card--active) .eco__icon {
  animation: eco-float 2.8s ease-in-out infinite;
  animation-delay: var(--float-phase, 0s);
}

.eco__card--active .eco__icon {
  animation: eco-float-active 1.6s ease-in-out infinite;
}

@keyframes eco-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

@keyframes eco-float-active {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-10px) scale(1.06);
  }
}

.eco__card:focus-visible {
  outline: 2px solid var(--cyan);
  outline-offset: 4px;
  border-radius: 12px;
}

.eco__icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #e2e8f0;
  box-shadow: 0 4px 16px rgba(26, 54, 93, 0.1);
  position: relative;
  transition:
    border-color 0.25s ease,
    box-shadow 0.25s ease,
    transform 0.25s ease;
}

.eco__card--active .eco__icon,
.eco__card:hover .eco__icon {
  border-color: var(--cyan);
  box-shadow:
    0 8px 24px rgba(6, 182, 212, 0.35),
    0 0 0 3px rgba(6, 182, 212, 0.15);
}

.eco__card--locked .eco__icon {
  border-color: var(--navy);
  box-shadow:
    0 8px 24px rgba(26, 54, 93, 0.25),
    0 0 0 3px rgba(26, 54, 93, 0.12);
}

.eco__label {
  font-size: 12px;
  font-weight: 600;
  color: var(--navy);
  white-space: nowrap;
  transition: color 0.2s ease, transform 0.2s ease;
}

.eco__card--active .eco__label,
.eco__card:hover .eco__label {
  color: var(--cyan);
  transform: scale(1.05);
}

/* Icons */
.eco__icon--vision::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -60%);
  border: 6px solid transparent;
  border-bottom: 10px solid var(--cyan);
}

.eco__icon--mission::after {
  content: "";
  position: absolute;
  inset: 14px;
  border: 2px solid var(--cyan);
  border-radius: 50%;
}

.eco__icon--mission::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 6px;
  height: 6px;
  margin: -3px 0 0 -3px;
  background: var(--cyan);
  border-radius: 50%;
}

.eco__icon--solutions::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 20px;
  height: 12px;
  margin: -6px 0 0 -10px;
  background: linear-gradient(90deg, var(--navy) 50%, var(--cyan) 50%);
  border-radius: 2px;
}

.eco__icon--growth::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 12px;
  width: 22px;
  height: 16px;
  margin-left: -11px;
  background: linear-gradient(to top, var(--navy) 35%, transparent 35% 100%) 2px 0 / 5px 100%
      no-repeat,
    linear-gradient(to top, var(--cyan) 65%, transparent 65% 100%) 9px 0 / 5px 100% no-repeat,
    linear-gradient(to top, var(--cyan) 50%, transparent 50% 100%) 16px 0 / 5px 100% no-repeat;
}

.eco__icon--security::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 14px;
  height: 16px;
  margin: -9px 0 0 -7px;
  border: 2px solid var(--navy);
  border-radius: 3px 3px 6px 6px;
  background: rgba(6, 182, 212, 0.15);
}

.eco__icon--trust::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 8px;
  height: 14px;
  margin: -9px 0 0 -6px;
  border: solid var(--cyan);
  border-width: 0 0 3px 3px;
  transform: rotate(-45deg);
}

@media (prefers-reduced-motion: reduce) {
  .eco--ready .eco__orbit,
  .eco--ready .eco__spoke,
  .eco--ready .eco__hub-ring,
  .eco--ready .eco__hub-inner,
  .eco--ready .eco__card--visible .eco__icon,
  .eco__card--active .eco__icon,
  .eco__pulse-dot {
    animation: none !important;
  }

  .eco__hub-inner,
  .eco__card--visible {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
