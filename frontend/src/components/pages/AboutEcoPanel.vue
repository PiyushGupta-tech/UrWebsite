<script setup>
import { useAboutEco } from "@/composables/useAboutEco.js";

const eco = useAboutEco();
const { activeNode, activeId } = eco;
</script>

<template>
  <div
    class="eco__panel"
    :class="{
      'eco__panel--ready': eco.ready,
      'eco__panel--live': eco.ready && activeId,
    }"
    aria-live="polite"
  >
    <p class="eco__panel-kicker">Explore</p>
    <p class="eco__panel-title">{{ activeNode.label }}</p>
    <p class="eco__panel-hint">{{ activeNode.hint }}</p>
  </div>
</template>

<style scoped>
.eco__panel {
  width: 100%;
  padding: 12px 18px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #f8fafc 0%, #fff 100%);
  text-align: left;
  opacity: 0;
  transform: translateY(10px);
  transition:
    opacity 0.4s ease 0.2s,
    transform 0.4s cubic-bezier(0.22, 1, 0.36, 1) 0.2s,
    border-color 0.25s ease,
    box-shadow 0.25s ease;
}

.eco__panel--ready {
  opacity: 1;
  transform: translateY(0);
}

.eco__panel--live {
  border-color: rgba(6, 182, 212, 0.45);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.12);
}

.eco__panel-kicker {
  margin: 0 0 2px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #06b6d4;
}

.eco__panel-title {
  margin: 0 0 4px;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
  color: #1a365d;
  transition: color 0.2s ease;
}

.eco__panel-hint {
  margin: 0;
  font-size: 12px;
  line-height: 1.35;
  white-space: nowrap;
  color: #64748b;
}

@media (max-width: 700px) {
  .eco__panel-hint {
    white-space: normal;
  }
}

@media (prefers-reduced-motion: reduce) {
  .eco__panel--ready {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
