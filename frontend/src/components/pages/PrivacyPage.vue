<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import ResourceLayout from "./ResourceLayout.vue";

const props = defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const active = ref(props.page.sections[0]?.id || "");
const sectionEls = ref([]);
const navEl = ref(null);
let observer = null;
const visible = new Set();

/** Jumps to a section; the URL is left alone so the router doesn't re-scroll. */
function jumpTo(id) {
  const el = document.getElementById(id);
  if (!el) return;
  active.value = id;
  const reduce = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
}

/** Highlights the first section whose heading is in the upper part of the viewport. */
function onIntersect(entries) {
  for (const entry of entries) {
    if (entry.isIntersecting) visible.add(entry.target.id);
    else visible.delete(entry.target.id);
  }
  const first = props.page.sections.find((s) => visible.has(s.id));
  if (first) active.value = first.id;
}

/** Keeps the highlighted link visible when the sticky nav is taller than the viewport. */
watch(active, async (id) => {
  await nextTick();
  const nav = navEl.value;
  const link = nav?.querySelector(`[href="#${id}"]`);
  if (!link || nav.scrollHeight <= nav.clientHeight) return;
  const top = link.getBoundingClientRect().top - nav.getBoundingClientRect().top + nav.scrollTop;
  if (top < nav.scrollTop) nav.scrollTop = top - 12;
  else if (top + link.offsetHeight > nav.scrollTop + nav.clientHeight) {
    nav.scrollTop = top + link.offsetHeight - nav.clientHeight + 12;
  }
});

onMounted(async () => {
  if (typeof IntersectionObserver === "undefined") return;
  await nextTick();
  observer = new IntersectionObserver(onIntersect, { rootMargin: "-120px 0px -60% 0px" });
  sectionEls.value.forEach((el) => observer.observe(el));
});

onBeforeUnmount(() => observer?.disconnect());
</script>

<template>
  <ResourceLayout :title="page.title" :intro="page.intro">
    <div class="privacy-layout">
      <nav ref="navEl" class="privacy-nav" :aria-label="`${page.title} sections`">
        <p class="privacy-nav__label">On this page</p>
        <a
          v-for="section in page.sections"
          :key="section.id"
          :href="`#${section.id}`"
          class="privacy-nav__btn"
          :class="{ 'privacy-nav__btn--active': active === section.id }"
          :aria-current="active === section.id ? 'location' : undefined"
          @click.prevent="jumpTo(section.id)"
        >
          {{ section.title }}
        </a>
      </nav>

      <article class="privacy-content">
        <section
          v-for="section in page.sections"
          :id="section.id"
          :key="section.id"
          ref="sectionEls"
          class="privacy-section"
        >
          <h2>{{ section.title }}</h2>
          <p v-if="section.body" class="privacy-content__body">{{ section.body }}</p>
          <ul v-if="section.bullets?.length" class="privacy-content__bullets">
            <li v-for="bullet in section.bullets" :key="bullet">{{ bullet }}</li>
          </ul>
          <p v-if="section.closing" class="privacy-content__body">{{ section.closing }}</p>
        </section>
      </article>
    </div>
  </ResourceLayout>
</template>

<style scoped>
.privacy-layout {
  display: grid;
  gap: 24px;
  align-items: start;
}

.privacy-nav,
.privacy-content {
  background: #ffffff;
  border: 1px solid var(--rs-line);
  border-radius: var(--rs-radius);
  box-shadow: var(--rs-shadow);
}

.privacy-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 20px 12px;
}

.privacy-nav__label {
  margin: 0 12px 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--rs-subtle);
}

.privacy-nav__btn {
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
  color: var(--rs-muted);
  text-decoration: none;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.privacy-nav__btn:hover {
  background: #f6f7f9;
  color: var(--rs-ink);
}

.privacy-nav__btn--active,
.privacy-nav__btn--active:hover {
  background: var(--rs-teal-tint);
  color: var(--rs-teal);
  font-weight: 600;
}

.privacy-content {
  padding: 40px 48px;
}

/* Clears the floating site header when jumping to a section. */
.privacy-section {
  scroll-margin-top: 120px;
}

.privacy-section + .privacy-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid var(--rs-line);
}

.privacy-content h2 {
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.35;
  letter-spacing: -0.01em;
  color: var(--rs-ink);
}

.privacy-content__body {
  margin: 0;
  font-size: 15px;
  line-height: 1.75;
  color: var(--rs-muted);
  white-space: pre-line;
}

.privacy-content__body + .privacy-content__body,
.privacy-content__bullets + .privacy-content__body {
  margin-top: 12px;
}

.privacy-content__bullets {
  margin: 12px 0 0;
  padding-left: 1.25rem;
  font-size: 15px;
  line-height: 1.75;
  color: var(--rs-muted);
}

.privacy-content__bullets li::marker {
  color: var(--rs-teal);
}

.privacy-content__bullets li + li {
  margin-top: 6px;
}

@media (min-width: 900px) {
  .privacy-layout {
    grid-template-columns: 280px minmax(0, 1fr);
  }

  .privacy-nav {
    position: sticky;
    top: 120px;
    max-height: calc(100vh - 144px);
    overflow-y: auto;
  }
}

@media (max-width: 700px) {
  .privacy-content {
    padding: 28px 20px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .privacy-nav__btn {
    transition: none;
  }
}
</style>
