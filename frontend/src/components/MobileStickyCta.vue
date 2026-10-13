<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const bar = ref(null);
const shown = computed(() => route.name !== "contact" && route.name !== "thank-you");

let media = null;

async function applyOffset() {
  await nextTick();
  const phone = media?.matches ?? false;
  const height = shown.value && phone && bar.value ? `${bar.value.offsetHeight}px` : "0px";
  document.documentElement.style.setProperty("--ur-sticky-cta", height);
}

onMounted(() => {
  media = window.matchMedia("(max-width: 767px)");
  media.addEventListener("change", applyOffset);
  applyOffset();
});

watch(shown, applyOffset);

onBeforeUnmount(() => {
  media?.removeEventListener("change", applyOffset);
  document.documentElement.style.removeProperty("--ur-sticky-cta");
});
</script>

<template>
  <div v-show="shown" ref="bar" class="sticky-cta">
    <RouterLink to="/contact" class="sticky-cta__btn">Talk to an Expert</RouterLink>
  </div>
</template>

<style scoped>
.sticky-cta {
  display: none;
}

@media (max-width: 767px) {
  .sticky-cta {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    display: flex;
    justify-content: center;
    padding: 10px 16px calc(10px + env(safe-area-inset-bottom));
    box-sizing: border-box;
    border-top: 1px solid #e9eaeb;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(12px);
  }

  .sticky-cta__btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 420px;
    height: 44px;
    border-radius: 8px;
    background: #097495;
    color: #ffffff;
    font-family: "Manrope", "DM Sans", system-ui, sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: -0.3px;
    text-decoration: none;
  }

  .sticky-cta__btn:focus-visible {
    outline: 2px solid #097495;
    outline-offset: 2px;
  }
}
</style>
