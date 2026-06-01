<script setup>
import { ref } from "vue";
import PageHero from "./PageHero.vue";

const props = defineProps({
  page: { type: Object, required: true },
});

const active = ref(props.page.sections[0]?.id || "introduction");
</script>

<template>
  <main>
    <PageHero :title="page.title" :intro="page.intro" />

    <section class="section">
      <div class="container privacy-layout">
        <nav class="privacy-nav card">
          <button
            v-for="section in page.sections"
            :key="section.id"
            type="button"
            class="privacy-nav__btn"
            :class="{ 'privacy-nav__btn--active': active === section.id }"
            @click="active = section.id"
          >
            {{ section.title }}
          </button>
        </nav>

        <article class="privacy-content card">
          <template v-for="section in page.sections" :key="section.id">
            <div v-show="active === section.id">
              <h2>{{ section.title }}</h2>
              <p>{{ section.body }}</p>
            </div>
          </template>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.privacy-layout {
  display: grid;
  gap: 24px;
  align-items: start;
}

.privacy-nav {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.privacy-nav__btn {
  text-align: left;
  padding: 10px 14px;
  border: none;
  background: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
}

.privacy-nav__btn--active,
.privacy-nav__btn:hover {
  background: var(--bg-page);
  color: var(--text-primary);
}

.privacy-content {
  padding: 32px;
}

.privacy-content h2 {
  margin: 0 0 12px;
  font-size: 22px;
}

.privacy-content p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

@media (min-width: 900px) {
  .privacy-layout {
    grid-template-columns: 240px 1fr;
  }
}
</style>
