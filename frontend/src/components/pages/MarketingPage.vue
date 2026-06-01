<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { checkoutMethodHeroFor } from "@/constants/checkoutMethodHero";
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

const checkoutMethodDetail = computed(() =>
  checkoutMethodHeroFor(activeCheckoutMethod.value),
);

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
  <main>
    <PageHero
      :title="page.title"
      :intro="page.intro"
      :split="hasSplitHero"
      :ready="heroReady"
      :graphic-position="heroGraphicPosition"
    >
      <template
        v-if="syncsCheckoutHeroCopy || syncsWalletHeroCopy || syncsOrchestrationHeroCopy"
        #copy-extra
      >
        <Transition name="hero-method" mode="out-in">
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
        <p v-if="section.body" class="marketing-section__body">{{ section.body }}</p>

        <ul v-if="section.bullets?.length" class="marketing-section__bullets">
          <li v-for="b in section.bullets" :key="b">{{ b }}</li>
        </ul>

        <div v-if="section.tags?.length" class="marketing-section__tags">
          <span v-for="tag in section.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <div v-if="section.cards?.length" class="marketing-section__cards">
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

    <section v-if="page.cta" class="section cta-inline">
      <div class="container card cta-inline__inner">
        <h2>{{ page.cta.title }}</h2>
        <p>{{ page.cta.body }}</p>
        <RouterLink :to="page.cta.href" class="btn btn--primary">{{ page.cta.button }}</RouterLink>
      </div>
    </section>
  </main>
</template>

<style scoped>
.hero-orchestration-line {
  margin: 0;
  font-size: 16px;
  line-height: 1.55;
  color: var(--text-secondary);
  font-weight: 500;
}

.hero-method-detail__headline {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.hero-method-detail__body {
  margin: 0 0 14px;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.55;
}

.hero-method-detail__bullets {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.hero-method-detail__bullets li {
  padding-left: 18px;
  position: relative;
  font-size: 14px;
  color: var(--text-secondary);
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
  max-width: 800px;
}

.marketing-section__title {
  font-size: 24px;
  margin: 0 0 12px;
  letter-spacing: -0.02em;
}

.marketing-section__body {
  margin: 0 0 20px;
  color: var(--text-secondary);
  line-height: 1.65;
}

.marketing-section__bullets {
  margin: 0 0 20px;
  padding-left: 20px;
  color: var(--text-secondary);
}

.marketing-section__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
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

.marketing-card,
.highlight-card {
  padding: 24px;
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
  gap: 16px;
  padding: 20px;
  align-items: flex-start;
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
  background: var(--bg-muted);
  text-align: center;
}

.closing-band__text {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  max-width: 640px;
  margin-inline: auto;
}

.cta-inline__inner {
  text-align: center;
  padding: 48px 32px;
}

.cta-inline__inner h2 {
  margin: 0 0 8px;
}

.cta-inline__inner p {
  color: var(--text-secondary);
  margin: 0 0 24px;
}
</style>
