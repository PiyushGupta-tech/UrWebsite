<script setup>
defineProps({
  items: { type: Array, required: true },
});
</script>

<template>
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <ol class="breadcrumbs__list">
      <li
        v-for="(item, index) in items"
        :key="`${item.name}-${index}`"
        class="breadcrumbs__item"
      >
        <RouterLink
          v-if="!item.current && item.path"
          :to="item.path"
          class="breadcrumbs__link"
        >
          {{ item.name }}
        </RouterLink>
        <span v-else class="breadcrumbs__current" aria-current="page">
          {{ item.name }}
        </span>
        <span
          v-if="index < items.length - 1"
          class="breadcrumbs__sep"
          aria-hidden="true"
        >
          /
        </span>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.breadcrumbs {
  padding: 16px 0 0;
}

.breadcrumbs__list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 8px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 13px;
}

.breadcrumbs__item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.breadcrumbs__link {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.15s;
}

.breadcrumbs__link:hover {
  color: var(--accent-blue);
}

.breadcrumbs__current {
  color: var(--text-secondary);
  font-weight: 500;
}

.breadcrumbs__sep {
  color: var(--text-muted);
  opacity: 0.6;
}
</style>
