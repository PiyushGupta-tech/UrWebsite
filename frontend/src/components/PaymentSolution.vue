<script setup>
import IndiaMerchantMap from "@/components/IndiaMerchantMap.vue";

defineProps({
  section: { type: Object, required: true },
});
</script>

<template>
  <section class="payment section">
    <div class="container payment__grid">
      <div class="payment__eyebrows">
        <p
          v-if="section.merchant_map?.tag"
          class="eyebrow payment__map-eyebrow"
        >
          {{ section.merchant_map.tag }}
        </p>
        <p class="eyebrow payment__section-eyebrow">{{ section.eyebrow }}</p>
      </div>

      <IndiaMerchantMap
        v-if="section.merchant_map"
        class="payment__map"
        :map="section.merchant_map"
      />

      <div class="payment__content">
        <h2 class="section-title">{{ section.title }}</h2>
        <h3 class="payment__feature-title">{{ section.feature_title }}</h3>
        <p class="payment__body">{{ section.feature_body }}</p>
        <ul class="payment__bullets">
          <li v-for="item in section.bullets" :key="item">{{ item }}</li>
        </ul>
        <p class="payment__closing">{{ section.closing }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.payment__grid {
  display: grid;
  gap: 16px;
  align-items: start;
}

.payment__eyebrows {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 24px;
}

.payment__map-eyebrow {
  margin: 0;
}

.payment__section-eyebrow {
  margin: 0 0 0 auto;
  text-align: right;
}

.payment__feature-title {
  font-size: 22px;
  margin: 0 0 12px;
}

.payment__body,
.payment__closing {
  color: var(--text-secondary);
  font-size: 16px;
}

.payment__bullets {
  margin: 20px 0;
  padding-left: 20px;
  color: var(--text-secondary);
}

.payment__bullets li {
  margin-bottom: 8px;
}

.payment__closing {
  font-weight: 500;
  color: var(--text-primary);
}

@media (min-width: 900px) {
  .payment__grid {
    grid-template-columns: 1.15fr 1fr;
    column-gap: 48px;
    row-gap: 16px;
  }

  .payment__eyebrows {
    display: contents;
  }

  .payment__map-eyebrow {
    grid-column: 1;
    grid-row: 1;
  }

  .payment__section-eyebrow {
    grid-column: 2;
    grid-row: 1;
    text-align: left;
    margin: 0;
  }

  .payment__map {
    grid-column: 1;
    grid-row: 2;
  }

  .payment__content {
    grid-column: 2;
    grid-row: 2;
  }
}
</style>
