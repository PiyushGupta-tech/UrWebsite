<script setup>
defineProps({
  problem: { type: Object, required: true },
});
</script>

<template>
  <section class="problem section--tight">
    <div class="container">
      <h2 class="section-title problem__title">{{ problem.title }}</h2>
      <div class="problem__grid">
        <article
          v-for="item in problem.items"
          :key="item.title"
          class="problem__card card"
        >
          <h3>{{ item.title }}</h3>
          <p>{{ item.body }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.problem {
  background: var(--bg-surface);
  border-block: 1px solid var(--border);
}

.problem__title {
  text-align: center;
  max-width: 720px;
  margin-inline: auto;
  margin-bottom: 40px;
}

.problem__grid {
  display: grid;
  gap: 20px;
}

.problem__card {
  padding: 28px;
}

.problem__card h3 {
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 700;
}

.problem__card p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 15px;
}

@media (min-width: 768px) {
  .problem__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
