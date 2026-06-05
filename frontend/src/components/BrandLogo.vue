<script setup>
import { computed, ref, watch } from "vue";
import { LOGO_PATHS } from "@/constants/logos.js";

const props = defineProps({
  /**
   * on-dark  — urwhite.png (white “rupee”, dark backgrounds)
   * on-light — urblack.png (black “rupee”, light backgrounds)
   * icon     — urlogo.png (shield only)
   * full     — alias for on-dark
   */
  variant: {
    type: String,
    default: "on-dark",
    validator: (v) => ["on-dark", "on-light", "icon", "full"].includes(v),
  },
  alt: { type: String, default: "Urbanrupee" },
  priority: { type: Boolean, default: false },
});

const failed = ref(false);

const resolvedVariant = computed(() =>
  props.variant === "full" ? "on-dark" : props.variant,
);

const src = computed(() => {
  switch (resolvedVariant.value) {
    case "on-light":
      return LOGO_PATHS.onLight;
    case "icon":
      return LOGO_PATHS.icon;
    default:
      return LOGO_PATHS.onDark;
  }
});

const dimensions = computed(() => {
  switch (resolvedVariant.value) {
    case "icon":
      return { width: 28, height: 28 };
    default:
      return { width: 112, height: 28 };
  }
});

watch(src, () => {
  failed.value = false;
});
</script>

<template>
  <img
    v-if="!failed"
    class="brand-logo"
    :class="`brand-logo--${resolvedVariant}`"
    :src="src"
    :alt="alt"
    :width="dimensions.width"
    :height="dimensions.height"
    :fetchpriority="priority ? 'high' : undefined"
    :loading="priority ? 'eager' : 'lazy'"
    decoding="async"
    @error="failed = true"
  />
  <span
    v-else
    class="brand-logo__fallback"
    :class="`brand-logo__fallback--${resolvedVariant}`"
  >
    UR
  </span>
</template>

<style scoped>
.brand-logo {
  display: block;
  width: auto;
  object-fit: contain;
}

.brand-logo--on-dark,
.brand-logo--on-light {
  height: 28px;
  max-width: 168px;
}

.brand-logo--icon {
  height: 28px;
  width: 28px;
}

.brand-logo__fallback {
  display: inline-grid;
  place-items: center;
  font-weight: 800;
  border-radius: 8px;
  background: linear-gradient(135deg, #1a365d, #06b6d4);
  color: #fff;
}

.brand-logo__fallback--on-dark,
.brand-logo__fallback--on-light {
  width: 32px;
  height: 28px;
  font-size: 12px;
}

.brand-logo__fallback--icon {
  width: 28px;
  height: 28px;
  font-size: 12px;
}
</style>
