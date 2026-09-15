<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  title: { type: String, default: "" },
  intro: { type: String, default: "" },
  items: { type: Array, default: () => [] },
  variant: { type: String, default: "split" },
  numbered: { type: Boolean, default: true },
  initialOpenIndex: { type: Number, default: 0 },
  ariaLabel: { type: String, default: "Frequently asked questions" },
  paddingTop: { type: String, default: "0" },
  paddingBottom: { type: String, default: "0" },
});

const openIndex = ref(props.initialOpenIndex);

function toggle(index) {
  openIndex.value = openIndex.value === index ? -1 : index;
}
</script>

<template>
  <section
    class="marketing-faq"
    :class="`marketing-faq--${variant}`"
    :aria-label="ariaLabel"
    :style="{ '--faq-pad-top': paddingTop, '--faq-pad-bottom': paddingBottom }"
  >
    <div
      class="marketing-faq__inner"
      :class="{ 'marketing-faq__inner--simple': variant === 'simple' }"
    >
      <div v-if="title || intro" class="marketing-faq__intro">
        <h2 v-if="title" class="marketing-faq__title">{{ title }}</h2>
        <p v-if="intro" class="marketing-faq__body">{{ intro }}</p>
      </div>

      <div class="marketing-faq__list">
        <div
          v-for="(item, index) in items"
          :key="item.number || item.question || index"
          class="marketing-faq__item"
          :class="{ 'marketing-faq__item--open': openIndex === index }"
        >
          <button
            type="button"
            class="marketing-faq__trigger"
            :aria-expanded="openIndex === index"
            @click="toggle(index)"
          >
            <span v-if="numbered && item.number" class="marketing-faq__num">{{ item.number }}</span>
            <span class="marketing-faq__question">{{ item.question }}</span>
            <span class="marketing-faq__icon" aria-hidden="true">{{ openIndex === index ? "−" : "+" }}</span>
          </button>
          <div v-show="openIndex === index" class="marketing-faq__answer">
            <p>{{ item.answer }}</p>
            <ul v-if="item.links?.length" class="marketing-faq__links">
              <li v-for="link in item.links" :key="link.href">
                <RouterLink :to="link.href">{{ link.label }}</RouterLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.marketing-faq {
  box-sizing: border-box;
  padding-top: var(--faq-pad-top, 0);
  padding-bottom: var(--faq-pad-bottom, 0);
}

.marketing-faq--split {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding-left: 100px;
  padding-right: 100px;
}

.marketing-faq--simple {
  max-width: 720px;
}

.marketing-faq__inner {
  display: grid;
  grid-template-columns: 501px 627px;
  gap: 94px;
  width: 1240px;
  max-width: 100%;
  margin: 0 auto;
  align-items: start;
}

.marketing-faq__inner--simple {
  display: block;
  width: auto;
}

.marketing-faq__intro {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 118px;
}

.marketing-faq__title {
  margin: 0;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
  color: #252b37;
  text-transform: capitalize;
}

.marketing-faq__body {
  margin: 0;
  max-width: 510px;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.marketing-faq__list {
  width: 100%;
}

.marketing-faq__item {
  border-bottom: 1px solid #f0f9f3;
}

.marketing-faq--simple .marketing-faq__item {
  margin-bottom: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  overflow: hidden;
  background: var(--bg-page);
}

.marketing-faq__trigger {
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
  color: #252b37;
}

.marketing-faq--simple .marketing-faq__trigger {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  min-height: 0;
  padding: 20px 24px;
}

.marketing-faq__num,
.marketing-faq__question {
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
}

.marketing-faq__icon {
  font-size: 22px;
  line-height: 1;
  text-align: center;
  color: #252b37;
}

.marketing-faq--simple .marketing-faq__icon {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--bg-page);
  color: var(--text-muted);
  flex-shrink: 0;
}

.marketing-faq__answer {
  padding: 0 24px 24px 76px;
}

.marketing-faq--simple .marketing-faq__answer {
  padding: 0 24px 20px;
}

.marketing-faq__answer p {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  color: #535862;
}

.marketing-faq--simple .marketing-faq__answer p {
  line-height: 1.65;
  color: var(--text-secondary);
}

.marketing-faq__links {
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
}

.marketing-faq__links a {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-blue);
}

/* Tablet FAQ: centered ~627px column (Figma 208:5682) */
@media (max-width: 1200px) {
  .marketing-faq--split {
    padding-left: 40px;
    padding-right: 40px;
  }

  .marketing-faq__inner {
    grid-template-columns: 1fr;
    gap: 24px;
    max-width: 627px;
    margin-inline: auto;
  }

  .marketing-faq__intro {
    padding-top: 0;
    align-items: center;
    gap: 20px;
    text-align: center;
  }

  .marketing-faq__title {
    max-width: 520px;
    margin-inline: auto;
    font-size: 42px;
    line-height: 56px;
    letter-spacing: -0.4px;
  }

  .marketing-faq__body {
    max-width: 100%;
    font-size: 16px;
    line-height: 24px;
    letter-spacing: 0.48px;
  }

  .marketing-faq__trigger {
    grid-template-columns: auto 1fr 20px;
    gap: 16px;
    min-height: 0;
    padding: 24px;
  }

  .marketing-faq__num,
  .marketing-faq__question {
    font-size: 18px;
    line-height: 28px;
  }

  .marketing-faq__answer {
    padding: 0 24px 24px;
  }

  .marketing-faq--simple .marketing-faq__answer {
    padding: 0 24px 20px;
  }
}

@media (max-width: 700px) {
  .marketing-faq--split {
    padding-left: 19px;
    padding-right: 19px;
  }

  .marketing-faq__inner {
    max-width: none;
    gap: 16px;
  }

  .marketing-faq__title {
    font-size: 42px;
    line-height: 1.25;
  }

  .marketing-faq__trigger {
    gap: 12px;
    padding: 18px 16px;
  }

  .marketing-faq__num,
  .marketing-faq__question {
    font-size: 16px;
    line-height: 24px;
  }

  .marketing-faq__answer {
    padding: 0 16px 18px 56px;
  }
}
</style>
