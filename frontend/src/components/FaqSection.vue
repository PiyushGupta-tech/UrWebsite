<script setup>
import { ref } from "vue";

defineProps({
  faqs: { type: Object, required: true },
});

const openIndex = ref(0);

function toggle(index) {
  openIndex.value = openIndex.value === index ? -1 : index;
}
</script>

<template>
  <section class="faq section">
    <div class="container faq__layout">
      <div>
        <p class="eyebrow">{{ faqs.eyebrow }}</p>
        <h2 class="section-title">Frequently asked questions</h2>
      </div>
      <div class="faq__list">
        <div
          v-for="(item, index) in faqs.items"
          :key="item.question"
          class="faq__item card"
          :class="{ 'faq__item--open': openIndex === index }"
        >
          <button
            type="button"
            class="faq__question"
            :aria-expanded="openIndex === index"
            @click="toggle(index)"
          >
            {{ item.question }}
            <span class="faq__icon">{{ openIndex === index ? "−" : "+" }}</span>
          </button>
          <div v-show="openIndex === index" class="faq__answer">
            <p>{{ item.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq {
  background: var(--bg-page);
}

.faq__layout {
  display: grid;
  gap: 40px;
}

.faq__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.faq__item {
  overflow: hidden;
  padding: 0;
}

.faq__question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 24px;
  border: none;
  background: none;
  text-align: left;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.faq__icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-page);
  font-size: 18px;
  color: var(--text-muted);
}

.faq__answer {
  padding: 0 24px 20px;
}

.faq__answer p {
  margin: 0;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.65;
}

.faq__item--open {
  border-color: var(--accent-blue);
}

@media (min-width: 900px) {
  .faq__layout {
    grid-template-columns: 0.9fr 1.1fr;
    align-items: start;
  }
}
</style>
