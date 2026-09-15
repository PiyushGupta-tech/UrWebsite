<script setup>
defineProps({
  title: { type: String, default: "" },
  items: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: "Industries we serve" },
  paddingBottom: { type: String, default: "0" },
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
  padding: 0 24px var(--section-pad-bottom, 0);
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
  font-size: 42px;
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

/* Tablet (Figma 208:5805 — 762×586 panel, 2×2 cards) */
@media (max-width: 1200px) {
  .marketing-audiences {
    max-width: 1024px;
    padding: 0 70px var(--section-pad-bottom, 0);
  }

  .marketing-audiences__panel {
    width: 100%;
    max-width: 762px;
    margin-inline: auto;
    padding: 36px;
    border-radius: 24px;
    box-sizing: border-box;
  }

  .marketing-audiences__title {
    margin: 0 auto 0;
    max-width: 689px;
    height: auto;
    font-size: 42px;
    line-height: 52px;
    letter-spacing: -0.96px;
  }

  .marketing-audiences__grid {
    display: grid;
    grid-template-columns: minmax(0, 304fr) minmax(0, 333fr);
    gap: 24px 47px;
    width: 100%;
    max-width: 684px;
    margin: 24px auto 0;
  }

  .marketing-audiences__card {
    min-height: 189px;
    height: auto;
    padding: 16px 20px;
    border-radius: 18px;
  }

  .marketing-audiences__card:nth-child(3),
  .marketing-audiences__card:nth-child(4) {
    min-height: 235px;
  }

  .marketing-audiences__num {
    margin-bottom: 20px;
    font-size: 56px;
    line-height: 64px;
    letter-spacing: -1.68px;
  }

  .marketing-audiences__copy {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .marketing-audiences__copy h3 {
    margin: 0;
    font-size: 20px;
    line-height: 28px;
    letter-spacing: -0.6px;
  }

  .marketing-audiences__copy p {
    margin: 0;
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0.48px;
  }
}

/* Phone: single column */
@media (max-width: 700px) {
  .marketing-audiences {
    padding-left: 19px;
    padding-right: 19px;
    padding-bottom: var(--section-pad-bottom, 0);
  }

  .marketing-audiences__panel {
    max-width: none;
    padding: 28px 16px;
    border-radius: 18px;
  }

  .marketing-audiences__title {
    margin: 0 auto 20px;
    max-width: 313px;
    font-size: 42px;
    line-height: 1.22;
  }

  .marketing-audiences__grid {
    grid-template-columns: 1fr;
    gap: 12px;
    max-width: 304px;
    margin: 0 auto;
  }

  .marketing-audiences__card,
  .marketing-audiences__card:nth-child(3),
  .marketing-audiences__card:nth-child(4) {
    min-height: 0;
  }

  .marketing-audiences__card:hover {
    transform: none;
    box-shadow: none;
  }

  .marketing-audiences__num {
    font-size: 42px;
    line-height: 1.05;
  }

  .marketing-audiences__copy h3 {
    font-size: 18px;
    line-height: 1.25;
  }
}
</style>
