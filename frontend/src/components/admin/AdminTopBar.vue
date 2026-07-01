<script setup>
import { computed } from "vue";
import BrandLogo from "@/components/BrandLogo.vue";
import { secondsAgo } from "@/utils/adminFormat";

const props = defineProps({
  generatedAt: { type: String, default: "" },
  refreshing: { type: Boolean, default: false },
});

const emit = defineEmits(["logout"]);

const ago = computed(() => {
  const secs = secondsAgo(props.generatedAt);
  return secs == null ? "—" : `${secs}s ago`;
});
</script>

<template>
  <header class="admin-topbar">
    <div class="admin-topbar__brand">
      <BrandLogo variant="on-dark" alt="UrbanRupee" priority />
    </div>

    <div class="admin-topbar__status">
      <span class="admin-topbar__live">LIVE</span>
      <span class="admin-topbar__updated">
        Last updated {{ ago }}
        <span v-if="refreshing" class="admin-topbar__refreshing" aria-hidden="true" />
      </span>
    </div>

    <button type="button" class="admin-topbar__logout" @click="emit('logout')">
      Logout
    </button>
  </header>
</template>

<style scoped>
.admin-topbar {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 16px;
  min-height: 64px;
  padding: 8px 16px;
  flex-shrink: 0;
  background: var(--btn-primary-gradient);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.admin-topbar__brand {
  display: flex;
  align-items: center;
}

.admin-topbar__status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-topbar__live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.admin-topbar__live::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.65);
}

.admin-topbar__updated {
  font-size: 12px;
  color: rgba(240, 250, 251, 0.75);
}

.admin-topbar__refreshing {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-left: 6px;
  border-radius: 50%;
  background: #fff;
  animation: pulse 1s ease-in-out infinite;
}

.admin-topbar__logout {
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  color: var(--ur-text);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.admin-topbar__logout:hover {
  background: rgba(255, 255, 255, 0.08);
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.35;
  }

  50% {
    opacity: 1;
  }
}

@media (max-width: 900px) {
  .admin-topbar {
    grid-template-columns: 1fr;
  }

  .admin-topbar__status {
    justify-content: flex-start;
  }
}
</style>
