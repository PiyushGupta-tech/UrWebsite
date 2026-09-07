<script setup>
defineProps({
  section: { type: Object, required: true },
});
</script>

<template>
  <section class="home-eco">
    <div class="home-eco__panel">
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
  </section>
</template>

<style scoped>
.home-eco {
  max-width: 1328px;
  margin: 0 auto;
  padding: 0 24px 100px;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.home-eco__panel {
  --eco-scale: 0.688;
  position: relative;
  height: calc(820px * var(--eco-scale));
  min-height: min(calc(820px * var(--eco-scale)), 72svh);
  border-radius: 24px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.home-eco__canvas {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 100%;
  height: 820px;
  transform: translate(-50%, -50%) scale(var(--eco-scale));
  transform-origin: center center;
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

.home-eco__point--left.home-eco__point:nth-child(1) {
  left: calc(50% - 493px);
  top: 140px;
}
.home-eco__point--left.home-eco__point:nth-child(2) {
  left: calc(50% - 629px);
  top: 390px;
}
.home-eco__point--left.home-eco__point:nth-child(3) {
  left: calc(50% - 517px);
  top: 640px;
}
.home-eco__point--right.home-eco__point:nth-child(4) {
  right: calc(50% - 493px);
  top: 140px;
  width: 183px;
}
.home-eco__point--right.home-eco__point:nth-child(5) {
  right: calc(50% - 629px);
  top: 390px;
  width: 221px;
}
.home-eco__point--right.home-eco__point:nth-child(6) {
  right: calc(50% - 517px);
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
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
}

.home-eco__point p {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  color: rgba(255, 255, 255, 0.9);
}

@media (max-width: 1200px) {
  .home-eco__panel {
    height: auto;
    min-height: auto;
    padding: 64px 32px;
    display: flex;
    flex-direction: column;
    gap: 40px;
  }

  .home-eco__canvas {
    position: relative;
    left: auto;
    top: auto;
    width: auto;
    height: auto;
    transform: none;
  }

  .home-eco__hub {
    position: relative;
    left: auto;
    top: auto;
    transform: none;
    margin: 0 auto;
  }

  .home-eco__rings,
  .home-eco__points {
    position: static;
  }

  .home-eco__rings {
    display: none;
  }

  .home-eco__points {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }

  .home-eco__point {
    position: static !important;
    width: auto !important;
  }

  .home-eco__point--right {
    text-align: left;
  }

  .home-eco__point--right .home-eco__point-head {
    justify-content: flex-start;
  }
}

@media (max-width: 700px) {
  .home-eco {
    padding: 0 16px 80px;
  }

  .home-eco__panel {
    height: 332px;
    min-height: 332px;
    padding: 0;
    display: block;
    border-radius: 18px;
  }

  .home-eco__canvas {
    position: relative;
    left: auto;
    top: auto;
    width: 100%;
    height: 100%;
    transform: none;
  }

  .home-eco__rings {
    display: block;
    position: absolute;
    inset: 0;
  }

  .home-eco__ring--1 {
    display: none;
  }

  .home-eco__ring--2 {
    --ring-size: 308px;
  }

  .home-eco__ring--3 {
    --ring-size: 234px;
  }

  .home-eco__ring--4 {
    --ring-size: 182px;
  }

  .home-eco__hub {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 150px;
    height: 150px;
    aspect-ratio: auto;
    padding: 18px 14px;
    gap: 6px;
  }

  .home-eco__logo {
    width: 22px;
    height: 28px;
  }

  .home-eco__hub-copy {
    gap: 6px;
  }

  .home-eco__eyebrow {
    font-size: 10px;
    line-height: 14px;
  }

  .home-eco__body {
    font-size: 8px;
    line-height: 11px;
  }

  .home-eco__points {
    position: absolute;
    inset: 0;
    display: block;
  }

  .home-eco__point {
    position: absolute !important;
    width: 96px !important;
  }

  .home-eco__point strong {
    font-size: 10px;
    line-height: 14px;
  }

  .home-eco__point p {
    font-size: 7px;
    line-height: 11px;
  }

  .home-eco__point-head {
    gap: 6px;
    margin-bottom: 8px;
  }

  .home-eco__num {
    width: 16px;
    height: 16px;
    font-size: 9px;
    line-height: 10px;
  }

  .home-eco__point--left.home-eco__point:nth-child(1) {
    left: 62px;
    top: 30px;
    width: 82px;
  }

  .home-eco__point--left.home-eco__point:nth-child(2) {
    left: 14px;
    top: 136px;
    width: 100px;
  }

  .home-eco__point--left.home-eco__point:nth-child(3) {
    left: 62px;
    top: 230px;
    width: 90px;
  }

  .home-eco__point--right.home-eco__point:nth-child(4) {
    right: 62px;
    top: 30px;
    width: 82px;
  }

  .home-eco__point--right.home-eco__point:nth-child(5) {
    right: 14px;
    top: 136px;
    width: 100px;
  }

  .home-eco__point--right.home-eco__point:nth-child(6) {
    right: 62px;
    top: 230px;
    width: 90px;
  }

  .home-eco__point--right {
    text-align: right;
  }

  .home-eco__point--right .home-eco__point-head {
    justify-content: flex-end;
  }
}
</style>
