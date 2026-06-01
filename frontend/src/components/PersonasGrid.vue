<script setup>
defineProps({
  personas: { type: Array, required: true },
});
</script>

<template>
  <section class="personas section--tight">
    <div class="container">
      <p class="eyebrow">Tailored Payment Solutions</p>
      <h2 class="section-title">
        Designed for Businesses Scaling Digitally
      </h2>
      <div class="personas__grid">
        <a
          v-for="persona in personas"
          :key="persona.title"
          href="/contact"
          class="personas__card card"
        >
          <h3>{{ persona.title }}</h3>
          <p>{{ persona.body }}</p>
          <span class="personas__arrow" aria-hidden="true">→</span>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.personas__grid {
  display: grid;
  gap: 16px;
  margin-top: 32px;
}

.personas__card {
  padding: 24px;
  display: block;
  position: relative;
  transition: border-color 0.15s, transform 0.15s;
}

.personas__card:hover {
  border-color: var(--accent-blue);
  transform: translateY(-2px);
}

.personas__card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.personas__card p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  padding-right: 28px;
}

.personas__arrow {
  position: absolute;
  right: 20px;
  bottom: 20px;
  color: var(--text-muted);
}

@media (min-width: 640px) {
  .personas__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1000px) {
  .personas__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
