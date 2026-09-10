<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

defineProps({
  section: { type: Object, required: true },
});

const DESIGN_W = 1328;
const DESIGN_H = 820;
/** Fixed nav + spacer (~129px) + small gap under the bar */
const NAV_CLEARANCE = 148;

const frameRef = ref(null);
const panelRef = ref(null);
let resizeObserver = null;

function applyScale() {
  const frame = frameRef.value;
  const panel = panelRef.value;
  if (!frame || !panel) return;

  const availW = frame.clientWidth;
  if (availW <= 0) return;

  const availH = Math.max(window.innerHeight - NAV_CLEARANCE, 240);
  const scale = Math.min(availW / DESIGN_W, availH / DESIGN_H);

  panel.style.setProperty("--eco-scale", String(scale));
  panel.style.aspectRatio = "auto";
  panel.style.width = `${DESIGN_W * scale}px`;
  panel.style.height = `${DESIGN_H * scale}px`;
}

onMounted(() => {
  const frame = frameRef.value;
  if (!frame) return;

  applyScale();
  window.addEventListener("resize", applyScale, { passive: true });

  if (typeof ResizeObserver === "undefined") return;

  resizeObserver = new ResizeObserver(() => applyScale());
  resizeObserver.observe(frame);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", applyScale);
  resizeObserver?.disconnect();
  resizeObserver = null;
});
</script>

<template>
  <section class="home-eco">
    <div ref="frameRef" class="home-eco__frame">
      <div ref="panelRef" class="home-eco__panel">
        <div class="home-eco__canvas">
          <div class="home-eco__rings" aria-hidden="true">
            <span class="home-eco__ring home-eco__ring--4" />
            <span class="home-eco__ring home-eco__ring--3" />
            <span class="home-eco__ring home-eco__ring--2" />
            <span class="home-eco__ring home-eco__ring--1" />
          </div>

          <div class="home-eco__hub">
            <img
              class="home-eco__logo"
              src="/images/figma-home/eco-hub-logo.svg"
              alt=""
              width="31"
              height="37"
              decoding="async"
            />
            <div class="home-eco__hub-copy">
              <p class="home-eco__eyebrow">{{ section.eyebrow }}</p>
              <p class="home-eco__body">{{ section.body }}</p>
            </div>
          </div>

          <ul class="home-eco__points">
            <li
              v-for="item in section.items || []"
              :key="item.number"
              class="home-eco__point"
              :class="`home-eco__point--${item.side}`"
            >
              <div class="home-eco__point-head">
                <span class="home-eco__num">{{ item.number }}</span>
                <strong>{{ item.title }}</strong>
              </div>
              <p>{{ item.body }}</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/*
  Fixed 1328×820 canvas. Scale = min(width, viewport-below-nav) so laptop
  fits under the navbar; narrower widths still shrink the whole graphic.
*/
.home-eco {
  max-width: 1328px;
  margin-inline: auto;
  padding: 0 24px;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.home-eco__frame {
  width: 100%;
  display: flex;
  justify-content: center;
}

.home-eco__panel {
  --eco-scale: 1;
  position: relative;
  width: 100%;
  max-width: 100%;
  /* Fallback before JS; JS sets exact scaled width/height */
  aspect-ratio: 1328 / 820;
  max-height: calc(100svh - 148px);
  border-radius: 24px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.home-eco__canvas {
  position: absolute;
  left: 0;
  top: 0;
  width: 1328px;
  height: 820px;
  transform: scale(var(--eco-scale));
  transform-origin: top left;
}

.home-eco__rings {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.home-eco__ring {
  --ring-size: 473px;
  position: absolute;
  left: 50%;
  top: 50%;
  width: var(--ring-size);
  height: var(--ring-size);
  border: 1px solid #80dbed;
  border-radius: 50%;
  box-sizing: border-box;
  opacity: 0.28;
  transform: translate(-50%, -50%);
  animation: eco-ring-pulse 3s ease-in-out infinite;
}

.home-eco__ring--1 {
  --ring-size: 800px;
  animation-delay: 2.25s;
}

.home-eco__ring--2 {
  --ring-size: 672px;
  animation-delay: 1.5s;
}

.home-eco__ring--3 {
  --ring-size: 531px;
  animation-delay: 0.75s;
}

.home-eco__ring--4 {
  --ring-size: 400px;
  animation-delay: 0s;
}

@keyframes eco-ring-pulse {
  0%,
  100% {
    opacity: 0.22;
  }

  18%,
  32% {
    opacity: 0.78;
  }

  50% {
    opacity: 0.22;
  }
}

@media (prefers-reduced-motion: reduce) {
  .home-eco__ring {
    animation: none;
    opacity: 0.45;
  }
}

.home-eco__hub {
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: 2;
  transform: translate(-50%, -50%);
  width: 317px;
  height: 317px;
  padding: 64px 45px;
  box-sizing: border-box;
  border-radius: 50%;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  text-align: center;
}

.home-eco__logo {
  display: block;
  width: 36.679px;
  height: 44.005px;
  flex-shrink: 0;
}

.home-eco__hub-copy {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.home-eco__eyebrow {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  line-height: 24px;
  color: #535862;
}

.home-eco__body {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  line-height: 18px;
  color: #535862;
}

.home-eco__points {
  position: absolute;
  inset: 0;
  z-index: 2;
  margin: 0;
  padding: 0;
  list-style: none;
}

.home-eco__point {
  position: absolute;
  width: 250px;
  color: #ffffff;
}

.home-eco__point--left {
  text-align: left;
}

.home-eco__point--right {
  text-align: right;
}

/* Fixed coords on 1328×820 canvas (center = 664) */
.home-eco__point--left.home-eco__point:nth-child(1) {
  left: 171px;
  top: 140px;
  width: 250px;
}

.home-eco__point--left.home-eco__point:nth-child(2) {
  left: 35px;
  top: 390px;
  width: 250px;
}

.home-eco__point--left.home-eco__point:nth-child(3) {
  left: 147px;
  top: 640px;
  width: 250px;
}

.home-eco__point--right.home-eco__point:nth-child(4) {
  left: 974px;
  right: auto;
  top: 140px;
  width: 183px;
}

.home-eco__point--right.home-eco__point:nth-child(5) {
  left: 1072px;
  right: auto;
  top: 390px;
  width: 221px;
}

.home-eco__point--right.home-eco__point:nth-child(6) {
  left: 960px;
  right: auto;
  top: 640px;
  width: 221px;
}

.home-eco__point-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.home-eco__point--right .home-eco__point-head {
  justify-content: flex-end;
}

.home-eco__num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 21px;
  width: 21px;
  height: 21px;
  border-radius: 10px;
  background: #ffffff;
  color: #252b37;
  font-size: 12px;
  font-weight: 500;
  line-height: 14px;
}

.home-eco__point strong {
  flex: 0 1 auto;
  min-width: 0;
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
}

.home-eco__point p {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  color: rgba(255, 255, 255, 0.9);
}

@media (max-width: 1200px) {
  .home-eco {
    max-width: 1024px;
    padding: 0 70px;
  }

  .home-eco__panel {
    border-radius: 16px;
  }
}

@media (max-width: 700px) {
  .home-eco {
    padding: 0 19px;
  }

  .home-eco__panel {
    border-radius: 14px;
  }
}
</style>
