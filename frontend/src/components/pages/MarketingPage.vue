<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { checkoutMethodHeroFor } from "@/constants/checkoutMethodHero";
import { customCheckoutMethodHeroFor } from "@/constants/customCheckoutMethodHero";
import { walletMetricHeroFor } from "@/constants/walletMetricHero";
import { orchestrationStoryLineFor } from "@/constants/orchestrationStoryHero";
import PageHero from "./PageHero.vue";
import PaymentServicesHeroGraphic from "./PaymentServicesHeroGraphic.vue";
import AmlDetectorHeroGraphic from "./AmlDetectorHeroGraphic.vue";
import ReconciliationHeroGraphic from "./ReconciliationHeroGraphic.vue";
import PaymentOrchestrationHeroGraphic from "./PaymentOrchestrationHeroGraphic.vue";
import CustomCheckoutHeroGraphic from "./CustomCheckoutHeroGraphic.vue";
import HyperCheckoutHeroGraphic from "./HyperCheckoutHeroGraphic.vue";
import DashboardHeroGraphic from "./DashboardHeroGraphic.vue";
import UpiSwitchHeroGraphic from "./UpiSwitchHeroGraphic.vue";
import AffordabilityHeroGraphic from "./AffordabilityHeroGraphic.vue";
import PayoutPortalHeroGraphic from "./PayoutPortalHeroGraphic.vue";
import CloseRouteWalletHeroGraphic from "./CloseRouteWalletHeroGraphic.vue";

const props = defineProps({
  page: { type: Object, required: true },
  checkout: { type: Object, default: null },
  dashboard: { type: Object, default: null },
  relatedLinks: { type: Array, default: () => [] },
});

const route = useRoute();
const heroReady = ref(false);
const activeCheckoutMethod = ref("upi");
const activeWalletMetric = ref("wallets");
const activeOrchestrationStory = ref("smart");

const syncsCheckoutHeroCopy = computed(
  () => route.name === "custom-checkout" || route.name === "hyper-checkout",
);

const syncsWalletHeroCopy = computed(
  () => route.name === "close-route-wallet",
);

const syncsOrchestrationHeroCopy = computed(
  () => route.name === "orchestration",
);

const showPaymentServicesHeroExtra = computed(
  () => route.name === "payment-services" && !!props.page?.hero_extra,
);

const checkoutMethodDetail = computed(() => {
  const heroFor =
    route.name === "custom-checkout"
      ? customCheckoutMethodHeroFor
      : checkoutMethodHeroFor;
  return heroFor(activeCheckoutMethod.value);
});

const walletMetricDetail = computed(() =>
  walletMetricHeroFor(activeWalletMetric.value),
);

const orchestrationStoryLine = computed(() =>
  orchestrationStoryLineFor(activeOrchestrationStory.value),
);

function onCheckoutMethodChange(methodId) {
  if (syncsCheckoutHeroCopy.value) {
    activeCheckoutMethod.value = methodId;
  }
}

function onWalletMetricChange(metricId) {
  if (syncsWalletHeroCopy.value) {
    activeWalletMetric.value = metricId;
  }
}

function onOrchestrationStoryChange(storyId) {
  if (syncsOrchestrationHeroCopy.value) {
    activeOrchestrationStory.value = storyId;
  }
}

const HERO_PAGES = {
  "payment-services": {
    component: PaymentServicesHeroGraphic,
    graphicPosition: "right",
  },
  "aml-detector": {
    component: AmlDetectorHeroGraphic,
    graphicPosition: "right",
  },
  "automatic-reconciliation": {
    component: ReconciliationHeroGraphic,
    graphicPosition: "right",
  },
  orchestration: {
    component: PaymentOrchestrationHeroGraphic,
    graphicPosition: "right",
  },
  "custom-checkout": {
    component: CustomCheckoutHeroGraphic,
    graphicPosition: "right",
    needsCheckout: true,
  },
  "hyper-checkout": {
    component: HyperCheckoutHeroGraphic,
    graphicPosition: "right",
    needsCheckout: true,
  },
  "upi-switch": {
    component: UpiSwitchHeroGraphic,
    graphicPosition: "right",
  },
  "white-label": {
    component: DashboardHeroGraphic,
    graphicPosition: "right",
    needsDashboard: true,
    graphicProps: { themeBreathe: true, logoPlaceholder: true },
  },
  affordability: {
    component: AffordabilityHeroGraphic,
    graphicPosition: "right",
  },
  "payout-portal": {
    component: PayoutPortalHeroGraphic,
    graphicPosition: "right",
  },
  "close-route-wallet": {
    component: CloseRouteWalletHeroGraphic,
    graphicPosition: "right",
  },
};

const heroConfig = computed(() => HERO_PAGES[route.name] ?? null);
const heroGraphic = computed(() => heroConfig.value?.component ?? null);
const heroGraphicPosition = computed(
  () => heroConfig.value?.graphicPosition ?? "right",
);

const heroBind = computed(() => {
  const cfg = heroConfig.value;
  if (!cfg) return {};
  const bind = {
    ready: heroReady.value,
    ...(cfg.graphicProps || {}),
  };
  if (cfg.needsCheckout && props.checkout) bind.checkout = props.checkout;
  if (cfg.needsDashboard && props.dashboard) bind.dashboard = props.dashboard;
  return bind;
});

const hasSplitHero = computed(() => {
  const cfg = heroConfig.value;
  if (!cfg) return false;
  if (cfg.needsCheckout && !props.checkout) return false;
  if (cfg.needsDashboard && !props.dashboard) return false;
  return true;
});

onMounted(() => {
  requestAnimationFrame(() => {
    heroReady.value = true;
  });
});
</script>

<template>
  <main class="marketing-page">
    <PageHero
      :title="page.title"
      :intro="page.intro"
      :split="hasSplitHero"
      :ready="heroReady"
      :graphic-position="heroGraphicPosition"
    >
      <template
        v-if="
          showPaymentServicesHeroExtra ||
          syncsCheckoutHeroCopy ||
          syncsWalletHeroCopy ||
          syncsOrchestrationHeroCopy
        "
        #copy-extra
      >
        <div v-if="showPaymentServicesHeroExtra" class="hero-payment-extra">
          <h3 class="hero-payment-extra__heading">
            {{ page.hero_extra.why_heading }}
          </h3>
          <ul class="hero-payment-extra__list">
            <li
              v-for="item in page.hero_extra.why_items"
              :key="item"
            >
              {{ item }}
            </li>
          </ul>
          <h3 class="hero-payment-extra__heading">
            {{ page.hero_extra.methods_heading }}
          </h3>
          <p class="hero-payment-extra__methods">
            {{ page.hero_extra.methods }}
          </p>
          <p class="hero-payment-extra__tagline">
            {{ page.hero_extra.tagline }}
          </p>
        </div>
        <Transition v-else name="hero-method" mode="out-in">
          <p
            v-if="syncsOrchestrationHeroCopy"
            :key="`orch-${activeOrchestrationStory}`"
            class="hero-orchestration-line"
          >
            {{ orchestrationStoryLine }}
          </p>
          <div
            v-else-if="syncsCheckoutHeroCopy"
            :key="`checkout-${activeCheckoutMethod}`"
            class="hero-method-detail"
          >
            <p class="hero-method-detail__headline">
              {{ checkoutMethodDetail.headline }}
            </p>
            <p class="hero-method-detail__body">
              {{ checkoutMethodDetail.body }}
            </p>
            <p
              v-if="checkoutMethodDetail.bullets_heading"
              class="hero-method-detail__bullets-head"
            >
              {{ checkoutMethodDetail.bullets_heading }}
            </p>
            <ul class="hero-method-detail__bullets">
              <li
                v-for="bullet in checkoutMethodDetail.bullets"
                :key="bullet"
              >
                {{ bullet }}
              </li>
            </ul>
          </div>
          <div
            v-else-if="syncsWalletHeroCopy"
            :key="`wallet-${activeWalletMetric}`"
            class="hero-method-detail"
          >
            <p class="hero-method-detail__headline">
              {{ walletMetricDetail.headline }}
            </p>
            <p class="hero-method-detail__body">
              {{ walletMetricDetail.body }}
            </p>
            <p
              v-if="walletMetricDetail.bullets_heading"
              class="hero-method-detail__bullets-head"
            >
              {{ walletMetricDetail.bullets_heading }}
            </p>
            <ul class="hero-method-detail__bullets">
              <li
                v-for="bullet in walletMetricDetail.bullets"
                :key="bullet"
              >
                {{ bullet }}
              </li>
            </ul>
          </div>
        </Transition>
      </template>

      <template v-if="hasSplitHero" #graphic>
        <component
          :is="heroGraphic"
          v-bind="heroBind"
          @method-change="onCheckoutMethodChange"
          @metric-change="onWalletMetricChange"
          @story-change="onOrchestrationStoryChange"
        />
      </template>
    </PageHero>

    <section
      v-for="(section, i) in page.sections"
      :key="section.title"
      class="section"
      :class="{ 'section--alt': i % 2 === 1 }"
    >
      <div class="container marketing-section">
        <h2 class="marketing-section__title">{{ section.title }}</h2>
        <h3 v-if="section.subhead" class="marketing-section__subhead">
          {{ section.subhead }}
        </h3>
        <p v-if="section.body" class="marketing-section__body">{{ section.body }}</p>

        <h4 v-if="section.bullets_heading" class="marketing-section__bullets-head">
          {{ section.bullets_heading }}
        </h4>
        <ul v-if="section.bullets?.length" class="marketing-section__bullets">
          <li v-for="b in section.bullets" :key="b">{{ b }}</li>
        </ul>

        <div v-if="section.tags?.length" class="marketing-section__tags">
          <span v-for="tag in section.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <div
          v-if="section.cards?.length"
          class="marketing-section__cards"
          :class="{ 'marketing-section__cards--four': section.cards.length === 4 }"
        >
          <article v-for="card in section.cards" :key="card.title" class="card marketing-card">
            <h3>{{ card.title }}</h3>
            <p>{{ card.body }}</p>
          </article>
        </div>

        <ol v-if="section.steps?.length" class="marketing-section__steps">
          <li v-for="(step, idx) in section.steps" :key="step.title" class="card step-card">
            <span class="step-card__num">{{ idx + 1 }}</span>
            <div>
              <h3>{{ step.title }}</h3>
              <p>{{ step.body }}</p>
            </div>
          </li>
        </ol>
      </div>
    </section>

    <section v-if="page.highlights?.length" class="section section--alt">
      <div class="container highlights">
        <article
          v-for="h in page.highlights"
          :key="h.title"
          class="card highlight-card"
        >
          <h3>{{ h.title }}</h3>
          <p>{{ h.body }}</p>
        </article>
      </div>
    </section>

    <section v-if="page.closing" class="section--tight closing-band">
      <div class="container">
        <p class="closing-band__text">{{ page.closing }}</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.marketing-page {
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.hero-payment-extra {
  display: grid;
  gap: 12px;
  text-align: left;
}

.hero-payment-extra__heading {
  margin: 8px 0 0;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-primary);
}

.hero-payment-extra__heading:first-child {
  margin-top: 0;
}

.hero-payment-extra__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
  justify-items: start;
}

.hero-payment-extra__list li {
  display: inline-block;
  padding-left: 18px;
  position: relative;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  text-align: left;
}

.hero-payment-extra__list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 7px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent-blue);
}

.hero-payment-extra__methods {
  margin: 0;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  line-height: 1.55;
  text-align: left;
}

.hero-payment-extra__tagline {
  margin: 4px 0 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
  text-align: left;
}

.hero-orchestration-line {
  margin: 0;
  font-size: 16px;
  line-height: 1.55;
  color: var(--text-secondary);
  font-weight: 500;
  text-align: left;
}

.hero-method-detail__headline {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  text-align: left;
}

.hero-method-detail__body {
  margin: 0 0 14px;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.55;
  text-align: left;
}

.hero-method-detail__bullets-head {
  margin: 14px 0 8px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-primary);
}

.hero-method-detail__bullets {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
  justify-items: start;
}

.hero-method-detail__bullets li {
  display: inline-block;
  padding-left: 18px;
  position: relative;
  font-size: 14px;
  color: var(--text-secondary);
  text-align: left;
}

.hero-method-detail__bullets li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 7px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent-blue);
}

.hero-method-enter-active,
.hero-method-leave-active {
  transition:
    opacity 0.28s ease,
    transform 0.28s ease;
}

.hero-method-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.hero-method-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (prefers-reduced-motion: reduce) {
  .hero-method-enter-active,
  .hero-method-leave-active {
    transition: opacity 0.15s ease;
  }

  .hero-method-enter-from,
  .hero-method-leave-to {
    transform: none;
  }
}

.section--alt {
  background: var(--bg-surface);
  border-block: 1px solid var(--border);
}

.marketing-section {
  position: relative;
  max-width: 860px;
  padding: 28px;
  border: 1px solid var(--border);
  border-radius: calc(var(--radius-card) + 2px);
  background:
    radial-gradient(120% 140% at 0% 0%, rgba(6, 182, 212, 0.07) 0%, transparent 48%),
    var(--bg-page);
  box-shadow: 0 10px 26px rgba(26, 54, 93, 0.06);
  text-align: left;
}

.section--alt .marketing-section {
  background:
    radial-gradient(110% 120% at 100% 0%, rgba(26, 54, 93, 0.07) 0%, transparent 45%),
    var(--bg-surface);
}

.marketing-section__title {
  position: relative;
  font-size: clamp(30px, 4vw, 40px);
  margin: 0 0 10px;
  line-height: 1.15;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.marketing-section__title::after {
  content: "";
  display: block;
  width: 72px;
  height: 3px;
  margin-top: 12px;
  border-radius: 999px;
  background: var(--btn-primary-gradient);
}

.marketing-section__body {
  margin: 0 0 20px;
  color: var(--text-secondary);
  line-height: 1.65;
  white-space: pre-line;
}

.marketing-section__subhead {
  margin: 0 0 18px;
  font-size: clamp(18px, 2.2vw, 22px);
  line-height: 1.45;
  font-weight: 500;
  letter-spacing: -0.01em;
  color: var(--text-secondary);
}

.marketing-section__bullets-head {
  margin: 18px 0 8px;
  font-size: 14px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-primary);
}

.marketing-section__bullets {
  margin: 0 0 20px;
  padding: 0;
  list-style: none;
  color: var(--text-secondary);
}

.marketing-section__bullets li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 8px;
}

.marketing-section__bullets li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.62em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-blue);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.16);
}

.marketing-section__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-start;
}

.tag {
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  background: var(--accent-blue-tint);
  color: var(--accent-blue);
}

.marketing-section__cards,
.highlights {
  display: grid;
  gap: 16px;
  margin-top: 24px;
}

@media (min-width: 640px) {
  .marketing-section__cards,
  .highlights {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 960px) {
  .marketing-section__cards.marketing-section__cards--four {
    grid-template-columns: repeat(4, 1fr);
  }
}

.marketing-card,
.highlight-card {
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  background:
    linear-gradient(180deg, rgba(6, 182, 212, 0.06) 0%, rgba(6, 182, 212, 0) 18%),
    var(--bg-surface);
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease;
  text-align: left;
}

.marketing-card:hover,
.highlight-card:hover {
  transform: translateY(-3px);
  border-color: rgba(6, 182, 212, 0.28);
  box-shadow: 0 12px 24px rgba(26, 54, 93, 0.09);
}

.marketing-card h3,
.highlight-card h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.marketing-card p,
.highlight-card p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.marketing-section__steps {
  list-style: none;
  padding: 0;
  margin: 24px 0 0;
  display: grid;
  gap: 12px;
}

.step-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  align-items: flex-start;
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  background: var(--bg-page);
  text-align: left;
}

.step-card__num {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  background: var(--btn-primary-gradient);
  color: #fff;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 700;
}

.step-card h3 {
  margin: 0 0 6px;
  font-size: 16px;
}

.step-card p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.closing-band {
  background:
    linear-gradient(120deg, rgba(26, 54, 93, 0.06), rgba(6, 182, 212, 0.06)),
    var(--bg-muted);
  text-align: center;
}

.closing-band__text {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  max-width: 640px;
  margin-inline: auto;
}

</style>
