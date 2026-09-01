<script setup>
import { RouterLink } from "vue-router";

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
        <img
          class="home-perform__graphic home-perform__graphic--control"
          :src="section.cards[0].graphic"
          alt=""
          width="365"
          height="332"
          loading="lazy"
          decoding="async"
        />
      </article>

      <div class="home-perform__stack">
        <article class="home-perform__card home-perform__card--success">
          <div class="home-perform__copy">
            <h3>{{ section.cards[1].title }}</h3>
            <p>{{ section.cards[1].body }}</p>
          </div>
          <img
            class="home-perform__graphic home-perform__graphic--success"
            :src="section.cards[1].graphic"
            alt=""
            width="817"
            height="87"
            loading="lazy"
            decoding="async"
          />
        </article>

        <article class="home-perform__card home-perform__card--reconcile">
          <div class="home-perform__copy">
            <h3>{{ section.cards[2].title }}</h3>
            <p>{{ section.cards[2].body }}</p>
          </div>
          <img
            class="home-perform__graphic home-perform__graphic--reconcile"
            :src="section.cards[2].graphic"
            alt=""
            width="817"
            height="180"
            loading="lazy"
            decoding="async"
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
  padding: 0 24px 100px;
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

/* Figma Frame 2147225718 — 1240×529 */
.home-perform__grid {
  display: grid;
  grid-template-columns: 367px minmax(0, 859px);
  gap: 14px;
  width: 100%;
  max-width: 1240px;
  height: 529px;
  align-items: stretch;
}

.home-perform__stack {
  display: flex;
  flex-direction: column;
  gap: 28px;
  height: 529px;
  min-width: 0;
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

/* Figma 1:5552 — 367×529 */
.home-perform__card--tall {
  height: 529px;
  padding: 22px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 51px;
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
  width: 365px;
  max-width: calc(100% - 40px);
  height: 332px;
  object-fit: contain;
  object-position: center bottom;
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
  max-width: 817px;
  height: 87px;
  object-fit: contain;
  object-position: left center;
}

/* Figma 1:5670 — fills remaining stack height for bottom alignment */
.home-perform__card--reconcile {
  flex: 1;
  min-height: 270px;
  padding: 25px 21px;
  display: flex;
  flex-direction: column;
}

.home-perform__card--reconcile .home-perform__copy {
  flex-shrink: 0;
}

.home-perform__graphic--reconcile {
  width: 100%;
  max-width: 817px;
  height: 180px;
  object-fit: contain;
  object-position: left bottom;
  margin-top: auto;
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

  .home-perform__card--reconcile .home-perform__graphic--reconcile {
    margin-top: 16px;
  }

  .home-perform__graphic--control {
    height: auto;
  }

  .home-perform__graphic--success,
  .home-perform__graphic--reconcile {
    height: auto;
    max-height: none;
  }
}

@media (max-width: 768px) {
  .home-perform__intro h2 {
    font-size: 32px;
    line-height: 42px;
  }

  .home-perform__card--success,
  .home-perform__card--reconcile {
    padding: 20px 16px;
  }
}
</style>
