<script setup>
defineProps({
  section: { type: Object, required: true },
});
</script>

<template>
  <section class="home-eco">
    <div class="home-eco__panel">
      <div class="home-eco__rings" aria-hidden="true">
        <span /><span /><span /><span />
      </div>

      <div class="home-eco__hub">
        <p class="home-eco__eyebrow">{{ section.eyebrow }}</p>
        <h2 class="home-eco__title">{{ section.title }}</h2>
        <p class="home-eco__body">{{ section.body }}</p>
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
  position: relative;
  min-height: 950px;
  border-radius: 24px;
  overflow: hidden;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
  display: grid;
  place-items: center;
}

.home-eco__rings {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  pointer-events: none;
}

.home-eco__rings span {
  position: absolute;
  border: 1px solid #80dbed;
  border-radius: 50%;
}

.home-eco__rings span:nth-child(1) {
  width: 966px;
  height: 946px;
}
.home-eco__rings span:nth-child(2) {
  width: 794px;
  height: 794px;
}
.home-eco__rings span:nth-child(3) {
  width: 634px;
  height: 628px;
}
.home-eco__rings span:nth-child(4) {
  width: 473px;
  height: 473px;
}

.home-eco__hub {
  position: relative;
  z-index: 2;
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
  gap: 8px;
  text-align: center;
}

.home-eco__eyebrow {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  line-height: 24px;
  color: #535862;
}

.home-eco__title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 28px;
  letter-spacing: -0.6px;
  color: #000000;
}

.home-eco__body {
  margin: 0;
  font-size: 12px;
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
    min-height: auto;
    padding: 64px 32px;
    display: flex;
    flex-direction: column;
    gap: 40px;
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
  .home-eco__hub {
    width: min(317px, 90vw);
    height: auto;
    aspect-ratio: 1;
    padding: 40px 28px;
  }

  .home-eco__points {
    grid-template-columns: 1fr;
  }
}
</style>
