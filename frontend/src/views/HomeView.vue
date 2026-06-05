<script setup>
import { onMounted, ref } from "vue";
import { fetchHomepage } from "@/api/client";
import { applySeo } from "@/utils/seo";
import HeroSection from "@/components/HeroSection.vue";
import ProblemTrio from "@/components/ProblemTrio.vue";
import ValueProp from "@/components/ValueProp.vue";
import PersonasGrid from "@/components/PersonasGrid.vue";
import ProductCatalogue from "@/components/ProductCatalogue.vue";
import PaymentSolution from "@/components/PaymentSolution.vue";
import PartnersMarquee from "@/components/PartnersMarquee.vue";
import FeaturesSection from "@/components/FeaturesSection.vue";
import StatsBand from "@/components/StatsBand.vue";
import WhyChoose from "@/components/WhyChoose.vue";
import Testimonials from "@/components/Testimonials.vue";
import FaqSection from "@/components/FaqSection.vue";

defineProps({
  site: { type: Object, default: null },
  footer: { type: Object, default: null },
});

const data = ref(null);
const error = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    data.value = await fetchHomepage();
    applySeo(data.value.seo, data.value.structured_data);
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading" class="page-loading">
    <div class="loading-screen__spinner" />
  </div>

  <div v-else-if="error" class="page-loading page-loading--error">
    <p>{{ error }}</p>
  </div>

  <main v-else>
    <HeroSection :hero="data.hero" :dashboard="data.dashboard_preview" :site="data.site" />
    <ProblemTrio :problem="data.problem_trio" />
    <ValueProp :value-prop="data.value_prop" :checkout="data.checkout_demo" />
    <PersonasGrid :personas="data.personas" />
    <ProductCatalogue :catalogue="data.product_catalogue" />
    <PaymentSolution :section="data.payment_solution" />
    <PartnersMarquee title="Banking Partners" :partners="data.banking_partners" />
    <PartnersMarquee
      title="Merchant Partners"
      :partners="data.merchant_partners"
      variant="merchants"
    />
    <FeaturesSection :features="data.features" />
    <StatsBand :stats="data.stats" />
    <WhyChoose :section="data.why_choose" />
    <Testimonials :section="data.testimonials" />
      <FaqSection :faqs="data.faqs" />
    </main>
</template>

<style scoped>
.page-loading {
  min-height: 40vh;
  display: grid;
  place-items: center;
}

.page-loading--error {
  color: #c0392b;
}

.loading-screen__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
