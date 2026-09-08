<script setup>
import { RouterLink } from "vue-router";
import HomePerformControlGraphic from "@/components/HomePerformControlGraphic.vue";
import HomePerformReconcileGraphic from "@/components/HomePerformReconcileGraphic.vue";
import HomePerformSuccessGraphic from "@/components/HomePerformSuccessGraphic.vue";

defineProps({
  section: { type: Object, required: true },
});
</script>

<template>
  <section class="home-perform" aria-label="Payments that perform">
    <div class="home-perform__intro">
      <h2>{{ section.title }}</h2>
      <p>{{ section.body }}</p>
    </div>

    <div class="home-perform__grid">
      <article class="home-perform__card home-perform__card--tall">
        <div class="home-perform__copy home-perform__copy--tall">
          <h3>{{ section.cards[0].title }}</h3>
          <p>{{ section.cards[0].body }}</p>
        </div>
        <HomePerformControlGraphic class="home-perform__graphic home-perform__graphic--control" />
      </article>

      <div class="home-perform__stack">
        <article class="home-perform__card home-perform__card--success">
          <div class="home-perform__copy">
            <h3>{{ section.cards[1].title }}</h3>
            <p>{{ section.cards[1].body }}</p>
          </div>
          <HomePerformSuccessGraphic class="home-perform__graphic home-perform__graphic--success" />
        </article>

        <article class="home-perform__card home-perform__card--reconcile">
          <div class="home-perform__copy home-perform__copy--reconcile">
            <h3>{{ section.cards[2].title }}</h3>
            <p>{{ section.cards[2].body }}</p>
          </div>
          <HomePerformReconcileGraphic
            class="home-perform__graphic home-perform__graphic--reconcile"
            :title="section.cards[2].title"
          />
        </article>
      </div>
    </div>

    <RouterLink to="/contact" class="home-perform__cta">
      <span>{{ section.cta }}</span>
      <img
        src="/images/figma-contact/nav-arrow.svg"
        alt=""
        width="18"
        height="18"
        decoding="async"
      />
    </RouterLink>
  </section>
</template>

<style scoped>
.home-perform {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 36px;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.home-perform__intro {
  max-width: 510px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.home-perform__intro h2 {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
}

.home-perform__intro p {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

/* Figma Frame 2147225718 — columns share one row height */
.home-perform__grid {
  display: grid;
  grid-template-columns: 367px minmax(0, 859px);
  gap: 14px;
  width: 100%;
  max-width: 1240px;
  align-items: stretch;
}

.home-perform__stack {
  display: flex;
  flex-direction: column;
  gap: 28px;
  min-width: 0;
  min-height: 0;
}

.home-perform__card {
  background: #ffffff;
  border: 1px solid #f4f4f4;
  border-radius: 14px;
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  overflow: hidden;
}

/* Stretch to match success + gap + reconcile stack in the sibling column */
.home-perform__card--tall {
  height: 100%;
  min-height: 0;
  padding: 22px 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
}

.home-perform__copy {
  width: 100%;
  max-width: 787px;
}

.home-perform__copy--tall {
  width: 321px;
  max-width: calc(100% - 40px);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.home-perform__copy h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  line-height: 32px;
  color: #252b37;
}

.home-perform__copy p {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: #535862;
}

.home-perform__graphic {
  display: block;
  flex-shrink: 0;
}

.home-perform__graphic--control {
  flex: 1 1 auto;
  min-height: 0;
  width: 396px;
  max-width: calc(100% - 40px);
  max-height: 290px;
  height: auto;
  aspect-ratio: 396 / 290;
}

/* Figma 1:5618 — 859×227 */
.home-perform__card--success {
  height: 227px;
  padding: 25px 21px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.home-perform__graphic--success {
  width: 100%;
  max-width: 748px;
  height: auto;
  aspect-ratio: 748 / 87;
}

/* Figma 73:1345 — full reconcile card SVG (805×244) */
.home-perform__card--reconcile {
  flex: none;
  width: 100%;
  max-width: 859px;
  align-self: stretch;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
}

.home-perform__graphic--reconcile {
  display: block;
  width: 100%;
  max-width: 805px;
  height: auto;
}

.home-perform__copy--reconcile {
  max-width: 556px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.home-perform__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: #097495;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  text-decoration: none;
  box-sizing: border-box;
}

.home-perform__cta:hover {
  filter: brightness(1.05);
}

@media (max-width: 1240px) {
  .home-perform__grid {
    grid-template-columns: minmax(280px, 367px) minmax(0, 1fr);
  }
}

@media (max-width: 1100px) {
  .home-perform__grid {
    grid-template-columns: 1fr;
    height: auto;
  }

  .home-perform__stack {
    height: auto;
  }

  .home-perform__card--tall,
  .home-perform__card--success,
  .home-perform__card--reconcile {
    height: auto;
    flex: none;
  }

  .home-perform__graphic--control {
    flex: none;
    height: auto;
    max-height: none;
  }

  .home-perform__graphic--success {
    height: auto;
    max-height: none;
  }
}

@media (max-width: 768px) {
  .home-perform__intro h2 {
    font-size: 32px;
    line-height: 42px;
  }

  .home-perform__card--success {
    padding: 20px 16px;
  }
}

@media (max-width: 480px) {
  .home-perform {
    padding: 0 19px 80px;
    gap: 24px;
  }

  .home-perform__intro {
    gap: 12px;
    max-width: 309px;
  }

  .home-perform__intro h2 {
    font-size: 36px;
    line-height: 46px;
    letter-spacing: 0;
  }

  .home-perform__intro p {
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0.48px;
  }

  .home-perform__grid,
  .home-perform__stack {
    gap: 20px;
  }

  .home-perform__card--tall {
    padding: 20px 22px;
    gap: 8px;
  }

  .home-perform__card--success,
  .home-perform__card--reconcile {
    padding: 20px 22px;
  }

  .home-perform__card--reconcile {
    gap: 19px;
  }

  .home-perform__card--success {
    gap: 20px;
  }

  .home-perform__copy h3 {
    font-size: 16px;
    line-height: 24px;
    text-align: center;
  }

  .home-perform__copy p {
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0.48px;
    text-align: center;
  }

  .home-perform__copy,
  .home-perform__copy--tall,
  .home-perform__copy--reconcile {
    max-width: 309px;
    margin: 0 auto;
    align-items: center;
    text-align: center;
  }

  .home-perform__graphic--control {
    width: 309px;
    max-width: 100%;
    aspect-ratio: 309 / 294;
    margin: 0 auto;
  }

  .home-perform__graphic--success {
    width: 220px;
    max-width: 100%;
    aspect-ratio: 220 / 310;
    margin: 0 auto;
  }

  .home-perform__graphic--reconcile {
    width: 336px;
    max-width: 100%;
    margin: 0 auto;
  }

  .home-perform__cta {
    min-width: 142px;
    height: 40px;
    padding: 10px 16px;
    font-size: 16px;
  }
}
</style>
