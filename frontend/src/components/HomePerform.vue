<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import HomePerformControlGraphic from "@/components/HomePerformControlGraphic.vue";
import HomePerformReconcileGraphic from "@/components/HomePerformReconcileGraphic.vue";
import HomePerformSuccessGraphic from "@/components/HomePerformSuccessGraphic.vue";

defineProps({
  section: { type: Object, required: true },
});

/* Desktop width at which the reconcile card's copy fits; tablet scales the graphic down from it as a whole */
const RECONCILE_DESIGN_WIDTH = 652;

const reconcileCard = ref(null);
const reconcileZoom = ref(1);
let reconcileObserver = null;

function updateReconcileZoom() {
  const card = reconcileCard.value;
  if (!card) return;
  const styles = window.getComputedStyle(card);
  const inner =
    card.clientWidth - parseFloat(styles.paddingLeft) - parseFloat(styles.paddingRight);
  if (inner > 0) {
    reconcileZoom.value = Math.min(1, inner / RECONCILE_DESIGN_WIDTH);
  }
}

onMounted(() => {
  updateReconcileZoom();
  if (typeof ResizeObserver !== "undefined" && reconcileCard.value) {
    reconcileObserver = new ResizeObserver(updateReconcileZoom);
    reconcileObserver.observe(reconcileCard.value);
  }
});

onBeforeUnmount(() => {
  reconcileObserver?.disconnect();
  reconcileObserver = null;
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

        <article
          ref="reconcileCard"
          class="home-perform__card home-perform__card--reconcile"
          :style="{ '--reconcile-zoom': reconcileZoom }"
        >
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
  margin-inline: auto;
  padding: 0 var(--ur-gutter);
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
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.2;
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
  gap: 14px;
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
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

.home-perform__graphic--reconcile {
  display: block;
  width: 100%;
  max-width: 805px;
  height: auto;
  overflow: visible;
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

/* Stacked full-width cards + vertical graphics (Figma 208:3641); 768–1024 keeps the desktop grid */
@media (max-width: 767px), (min-width: 1025px) and (max-width: 1200px) {
  .home-perform {
    padding: 0 70px;
    gap: 24px;
    max-width: 1024px;
  }

  .home-perform__intro {
    gap: 12px;
    max-width: 560px;
    margin-inline: auto;
    text-align: center;
  }

  .home-perform__intro h2 {
    font-size: 34px;
    line-height: 42px;
    letter-spacing: -0.4px;
  }

  .home-perform__intro p {
    font-size: 12px;
    line-height: 20px;
    letter-spacing: 0.48px;
  }

  .home-perform__grid {
    display: flex;
    flex-direction: column;
    grid-template-columns: none;
    gap: 24px;
    width: 100%;
    max-width: 523px;
    margin-inline: auto;
    height: auto;
  }

  .home-perform__stack {
    display: flex;
    flex-direction: column;
    gap: 24px;
    height: auto;
    width: 100%;
  }

  .home-perform__card--tall,
  .home-perform__card--success,
  .home-perform__card--reconcile {
    width: 100%;
    max-width: none;
    height: auto;
    flex: none;
  }

  .home-perform__card--tall {
    padding: 29px 32px;
    gap: 12px;
    border-radius: 20.5px;
  }

  .home-perform__card--success,
  .home-perform__card--reconcile {
    padding: 29px;
    border-radius: 21px;
  }

  .home-perform__card--success {
    gap: 12px;
  }

  .home-perform__card--reconcile {
    padding: 31px;
    gap: 28px;
  }

  .home-perform__copy h3 {
    font-size: 23.4px;
    line-height: 35px;
    text-align: center;
  }

  .home-perform__copy p {
    font-size: 17.5px;
    line-height: 29px;
    letter-spacing: 0.7px;
    text-align: center;
  }

  .home-perform__copy,
  .home-perform__copy--tall,
  .home-perform__copy--reconcile {
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    align-items: center;
    text-align: center;
  }

  .home-perform__copy--tall {
    max-width: 453px;
    gap: 6px;
  }

  .home-perform__graphic--control {
    flex: none;
    width: min(453px, 100%);
    max-width: 100%;
    max-height: none;
    height: auto;
    aspect-ratio: 396 / 290;
    margin: 0 auto;
  }

  .home-perform__graphic--success {
    width: min(322px, 100%);
    max-width: 100%;
    height: auto;
    max-height: none;
    aspect-ratio: auto;
    margin: 0 auto;
  }

  .home-perform__graphic--reconcile {
    width: min(336px, 100%);
    max-width: 100%;
    margin: 0 auto;
  }

  .home-perform__cta {
    min-width: 142px;
    height: 40px;
    margin-top: 0;
    padding: 10px 16px;
    font-size: 14px;
    letter-spacing: -0.28px;
  }
}

/* Tablet: desktop grid with proportional columns */
@media (min-width: 768px) and (max-width: 1024px) {
  .home-perform__grid {
    grid-template-columns: minmax(0, 300fr) minmax(0, 630fr);
  }

  .home-perform__card--success {
    height: auto;
    padding: 20px;
    gap: 16px;
  }

  .home-perform__card--reconcile {
    padding: 20px;
    gap: 12px;
  }

  .home-perform__copy h3 {
    line-height: 28px;
  }

  .home-perform__graphic--reconcile {
    width: 652px;
    max-width: none;
    zoom: var(--reconcile-zoom, 1);
  }
}

@media (max-width: 700px) {
  .home-perform {
    padding: 0 19px;
  }

  .home-perform__grid {
    max-width: none;
  }

  .home-perform__intro h2 {
    font-size: 28px;
    line-height: 1.2;
  }

  .home-perform__copy h3 {
    font-size: 16px;
    line-height: 24px;
  }

  .home-perform__copy p {
    font-size: 12px;
    line-height: 20px;
  }

  .home-perform__card--tall,
  .home-perform__card--success,
  .home-perform__card--reconcile {
    padding: 20px;
  }

  .home-perform__card--reconcile {
    gap: 16px;
  }

  .home-perform__graphic--control {
    width: min(309px, 100%);
  }

  .home-perform__graphic--success {
    width: min(220px, 100%);
  }

  .home-perform__graphic--reconcile {
    width: min(336px, 100%);
  }
}
</style>
