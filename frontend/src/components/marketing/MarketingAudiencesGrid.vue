<script setup>
defineProps({
  title: { type: String, default: "" },
  items: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: "Industries we serve" },
  paddingBottom: { type: String, default: "100px" },
});
</script>

<template>
  <section class="marketing-audiences" :aria-label="ariaLabel" :style="{ '--section-pad-bottom': paddingBottom }">
    <div class="marketing-audiences__panel">
      <h2 v-if="title" class="marketing-audiences__title">{{ title }}</h2>
      <div class="marketing-audiences__grid">
        <article
          v-for="item in items"
          :key="item.number"
          class="marketing-audiences__card"
        >
          <span class="marketing-audiences__num" aria-hidden="true">{{ item.number }}</span>
          <div class="marketing-audiences__copy">
            <h3>{{ item.title }}</h3>
            <p>{{ item.body }}</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.marketing-audiences {
  max-width: 1328px;
  margin: 0 auto;
  padding: 0 24px var(--section-pad-bottom, 100px);
}

.marketing-audiences__panel {
  padding: 70px 44px;
  border-radius: 24px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.marketing-audiences__title {
  margin: 0 auto 56px;
  max-width: 517px;
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.2px;
  color: #ffffff;
}

.marketing-audiences__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 17px;
}

.marketing-audiences__card {
  min-height: 212px;
  padding: 16px 20px;
  border-radius: 18px;
  border: 1px solid rgba(200, 200, 200, 0.19);
  background: rgba(255, 255, 255, 0.06);
  transform: translateY(0) scale(1);
  transition:
    transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
    background 0.25s ease,
    border-color 0.25s ease,
    box-shadow 0.25s ease;
}

.marketing-audiences__card:hover {
  transform: translateY(-8px) scale(1.03);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
}

.marketing-audiences__num {
  display: block;
  margin-bottom: 20px;
  font-size: 68px;
  font-weight: 700;
  line-height: 72px;
  letter-spacing: -2.059px;
  background: linear-gradient(180deg, #636363 0%, #ffffff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.marketing-audiences__copy h3 {
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  letter-spacing: -0.66px;
  color: #ffffff;
}

.marketing-audiences__copy p {
  margin: 0;
  font-size: 14px;
  line-height: 19px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

@media (prefers-reduced-motion: reduce) {
  .marketing-audiences__card {
    transition: none;
  }

  .marketing-audiences__card:hover {
    transform: none;
  }
}

@media (max-width: 1200px) {
  .marketing-audiences__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .marketing-audiences__title {
    font-size: 32px;
    line-height: 1.2;
  }

  .marketing-audiences__grid {
    display: flex;
    overflow-x: auto;
    gap: 17px;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 8px;
  }

  .marketing-audiences__card {
    flex: 0 0 min(280px, 78vw);
    scroll-snap-align: start;
  }
}

@media (max-width: 480px) {
  .marketing-audiences {
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: min(var(--section-pad-bottom, 100px), 72px);
  }

  .marketing-audiences__panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    padding: 36px 20px;
    border-radius: 24px;
  }

  .marketing-audiences__title {
    margin: 0;
    max-width: 313px;
    font-size: 32px;
    font-weight: 700;
    line-height: 36px;
    letter-spacing: -0.96px;
    text-align: center;
  }

  .marketing-audiences__grid {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 304px;
    gap: 12px;
    overflow: visible;
    padding-bottom: 0;
    scroll-snap-type: none;
  }

  .marketing-audiences__card {
    flex: none;
    width: 100%;
    min-height: 0;
    height: auto;
    padding: 16px 20px;
    border-radius: 18px;
  }

  .marketing-audiences__card:hover {
    transform: none;
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(200, 200, 200, 0.19);
    box-shadow: none;
  }

  .marketing-audiences__num {
    margin-bottom: 20px;
    font-size: 56px;
    font-weight: 700;
    line-height: 64px;
    letter-spacing: -1.68px;
  }

  .marketing-audiences__copy h3 {
    margin: 0 0 6px;
    font-size: 20px;
    font-weight: 700;
    line-height: 28px;
    letter-spacing: -0.6px;
  }

  .marketing-audiences__copy p {
    font-size: 12px;
    font-weight: 400;
    line-height: 20px;
    letter-spacing: 0.48px;
  }
}
</style>
