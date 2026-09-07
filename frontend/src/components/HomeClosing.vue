<script setup>
import { computed } from "vue";
import IndiaMerchantMap from "@/components/IndiaMerchantMap.vue";
import MarketingAudiencesGrid from "@/components/marketing/MarketingAudiencesGrid.vue";
import MarketingBannerCta from "@/components/marketing/MarketingBannerCta.vue";
import MarketingFaqAccordion from "@/components/marketing/MarketingFaqAccordion.vue";
import MarketingTestimonialsCarousel from "@/components/marketing/MarketingTestimonialsCarousel.vue";

const props = defineProps({
  section: { type: Object, required: true },
  showIndiaGrowth: { type: Boolean, default: true },
});

const indiaGrowth = computed(() => props.section.india_growth || null);
</script>

<template>
  <div class="home-close">
    <section
      v-if="showIndiaGrowth && indiaGrowth"
      class="home-close__india"
      aria-label="Growing across India"
    >
      <div class="home-close__india-intro">
        <h2>{{ indiaGrowth.title }}</h2>
        <p>{{ indiaGrowth.body }}</p>
      </div>

      <div class="home-close__india-grid">
        <IndiaMerchantMap
          v-if="indiaGrowth.merchant_map"
          class="home-close__india-map"
          :map="indiaGrowth.merchant_map"
          hint="Hover a point to see partners"
        />

        <div class="home-close__india-copy">
          <div class="home-close__india-side">
            <h3>{{ indiaGrowth.side_title }}</h3>
            <p>{{ indiaGrowth.side_body }}</p>
          </div>
          <ul class="home-close__india-points">
            <li
              v-for="item in indiaGrowth.points || []"
              :key="item.title"
            >
              <strong>{{ item.title }}</strong>
              <p>{{ item.body }}</p>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <MarketingTestimonialsCarousel
      :title="section.testimonials_title"
      :items="section.testimonials || []"
      variant="home"
      aria-label="Customer testimonials"
    />

    <MarketingAudiencesGrid
      :title="section.audiences_title"
      :items="section.audiences || []"
      aria-label="Industries we serve"
      padding-bottom="100px"
    />

    <MarketingFaqAccordion
      :title="section.faq_title"
      :intro="section.faq_intro"
      :items="section.faq_items || []"
      variant="split"
      aria-label="Frequently asked questions"
      padding-bottom="100px"
    />

    <MarketingBannerCta
      :title="section.cta_title"
      :body="section.cta_body"
      :label="section.cta_label"
      to="/contact"
      variant="home"
      aria-label="Call to action"
      icon-src="/images/figma-contact/nav-arrow-teal.svg"
      padding-bottom="94px"
    />
  </div>
</template>

<style scoped>
.home-close {
  --ink: #252b37;
  --muted: #535862;
  --teal: #097495;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: var(--ink);
}

.home-close__india {
  max-width: 1189px;
  margin: 0 auto;
  padding: 0 24px 120px;
}

.home-close__india-intro {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  max-width: 698px;
  margin: 0 auto 56px;
  text-align: center;
}

.home-close__india-intro h2 {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: var(--ink);
}

.home-close__india-intro p {
  margin: 0;
  max-width: 580px;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--muted);
}

.home-close__india-grid {
  display: grid;
  grid-template-columns: minmax(0, 573px) minmax(0, 518px);
  gap: 98px;
  align-items: center;
  justify-content: center;
}

.home-close__india-map {
  width: 100%;
  max-width: 573px;
  margin: 0 auto;
}

.home-close__india-copy {
  display: flex;
  flex-direction: column;
  gap: 48px;
  max-width: 518px;
}

.home-close__india-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.home-close__india-side h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  line-height: 32px;
  letter-spacing: -0.72px;
  color: var(--ink);
}

.home-close__india-side p {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--muted);
}

.home-close__india-points {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin: 0;
  padding: 0;
  list-style: none;
  max-width: 481px;
}

.home-close__india-points li {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.home-close__india-points strong {
  font-size: 18px;
  font-weight: 600;
  line-height: 24px;
  color: #414651;
}

.home-close__india-points p {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: -0.16px;
  color: var(--muted);
}

.home-close__testimonials {
  padding: 0 0 100px;
  overflow: hidden;
}

.home-close__ttitle {
  margin: 0 auto 64px;
  max-width: 788px;
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  line-height: 48px;
  color: var(--ink);
}

.home-close__track-wrap {
  overflow: hidden;
  width: 100%;
}

.home-close__track {
  --card-w: 612px;
  --gap: 24px;
  --active: 0;
  display: flex;
  gap: var(--gap);
  align-items: flex-start;
  width: max-content;
  min-height: 276px;
  position: relative;
  left: 50%;
  transform: translateX(
    calc(-1 * (var(--active) * (var(--card-w) + var(--gap)) + var(--card-w) / 2))
  );
  transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

.home-close__track--snap {
  transition: none;
}

.home-close__tcard {
  flex: 0 0 var(--card-w);
  width: var(--card-w);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 24px;
  min-height: 252px;
  padding: 32px;
  border-radius: 16px;
  background: #f8fafc;
  opacity: 0.4;
  transform: translateY(24px);
  transition:
    opacity 0.35s ease,
    transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
  cursor: pointer;
}

.home-close__tcard--active {
  opacity: 1;
  transform: translateY(0);
  cursor: default;
}

.home-close__tcard--inactive {
  opacity: 0.4;
}

.home-close__quote {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: -0.48px;
  color: #020617;
}

.home-close__author {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.home-close__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.home-close__meta {
  margin: 0;
  font-size: 18px;
  line-height: 26px;
  letter-spacing: -0.54px;
  color: #020617;
}

.home-close__meta span {
  color: #64748b;
}

.home-close__dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 36px;
}

.home-close__dot {
  width: 12px;
  height: 12px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #cbd5e1;
  cursor: pointer;
}

.home-close__dot--active {
  background: var(--teal);
}

.home-close__audiences {
  max-width: 1328px;
  margin: 0 auto;
  padding: 0 24px 100px;
}

.home-close__audiences-panel {
  padding: 70px 44px;
  border-radius: 24px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.home-close__audiences-panel h2 {
  margin: 0 auto 56px;
  max-width: 517px;
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: -1.2px;
  color: #ffffff;
}

.home-close__audiences-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 17px;
}

.home-close__audience {
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

.home-close__audience:hover {
  transform: translateY(-8px) scale(1.03);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
}

.home-close__audience > span {
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

.home-close__audience h3 {
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  letter-spacing: -0.66px;
  color: #ffffff;
}

.home-close__audience p {
  margin: 0;
  font-size: 14px;
  line-height: 19px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.home-close__faq {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 100px 100px;
  box-sizing: border-box;
}

.home-close__faq-inner {
  display: grid;
  grid-template-columns: 501px 627px;
  gap: 94px;
  width: 1240px;
  max-width: 100%;
  margin: 0 auto;
  align-items: start;
}

.home-close__faq-intro {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 118px;
}

.home-close__faq-intro h2 {
  margin: 0;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  text-transform: capitalize;
}

.home-close__faq-intro p {
  margin: 0;
  max-width: 510px;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--muted);
}

.home-close__faq-item {
  border-bottom: 1px solid #f0f9f3;
}

.home-close__faq-trigger {
  display: grid;
  grid-template-columns: 36px 1fr 24px;
  align-items: center;
  gap: 16px;
  width: 100%;
  min-height: 76px;
  padding: 24px;
  box-sizing: border-box;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
}

.home-close__faq-num,
.home-close__faq-q {
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
  color: var(--ink);
}

.home-close__faq-icon {
  font-size: 22px;
  line-height: 1;
  text-align: center;
  color: var(--ink);
}

.home-close__faq-answer {
  padding: 0 24px 24px 76px;
}

.home-close__faq-answer p {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: var(--muted);
}

.home-close__cta {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 100px 94px;
  box-sizing: border-box;
}

.home-close__cta-panel {
  position: relative;
  width: 1240px;
  max-width: 100%;
  height: 331px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.home-close__cta-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.home-close__cta-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  height: 100%;
  padding: 52px 24px;
  text-align: center;
}

.home-close__cta-content h2 {
  margin: 0;
  max-width: 728px;
  font-size: 40px;
  font-weight: 500;
  line-height: 52px;
  letter-spacing: 1.6px;
  color: #ffffff;
}

.home-close__cta-content p {
  margin: 0;
  max-width: 728px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.home-close__cta-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 52px;
  padding: 16px;
  border-radius: 8px;
  background: #ffffff;
  color: var(--teal);
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
}

.home-close__cta-btn img {
  width: 18px;
  height: 18px;
}

@media (prefers-reduced-motion: reduce) {
  .home-close__audience {
    transition: none;
  }

  .home-close__audience:hover {
    transform: none;
  }
}

@media (max-width: 1200px) {
  .home-close__india-grid {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .home-close__india-copy {
    max-width: 640px;
    margin: 0 auto;
  }

  .home-close__audiences-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .home-close__faq-inner {
    grid-template-columns: 1fr;
  }

  .home-close__faq-intro {
    padding-top: 0;
  }

  .home-close__faq,
  .home-close__cta {
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (max-width: 768px) {
  .home-close__india {
    padding-bottom: 80px;
  }

  .home-close__india-intro h2 {
    font-size: 32px;
    line-height: 1.2;
  }

  .home-close__ttitle,
  .home-close__audiences-panel h2,
  .home-close__faq-intro h2,
  .home-close__cta-content h2 {
    font-size: 32px;
    line-height: 1.2;
  }

  .home-close__audiences-grid {
    grid-template-columns: 1fr;
  }

  .home-close__track {
    --card-w: min(612px, calc(100vw - 48px));
  }

  .home-close__cta-panel {
    height: auto;
    min-height: 280px;
  }
}
</style>
