<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: "" },
  width: { type: [Number, String], default: 1240 },
  height: { type: [Number, String], default: 782 },
});

const WAIT_MS = 2200;
const RESULT_MS = 2800;
const GATEWAYS = [1, 2, 3, 4, 5, 6];

const host = ref(null);
const loaded = ref(false);
const reduceMotion = ref(false);

let svgRoot = null;
let cycleTimer = null;
let lastWinner = null;
let aborted = false;

function clearCycle() {
  if (cycleTimer) {
    clearTimeout(cycleTimer);
    cycleTimer = null;
  }
}

function setIconVisibility(gw, role) {
  if (!svgRoot) return;
  svgRoot.querySelectorAll(`.po-gw-icon[data-gw="${gw}"]`).forEach((el) => {
    const match = el.getAttribute("data-role") === role;
    el.setAttribute("visibility", match ? "visible" : "hidden");
  });
}

function resetPaths() {
  if (!svgRoot) return;
  svgRoot.querySelectorAll(".po-gw-path").forEach((el) => {
    el.classList.remove("is-success");
  });
}

function resetCards() {
  if (!svgRoot) return;
  svgRoot.querySelectorAll(".po-gw-card").forEach((card) => {
    card.classList.remove("is-waiting", "is-success", "is-fail");
  });
}

function setWaiting() {
  if (!svgRoot) return;
  resetPaths();
  resetCards();
  GATEWAYS.forEach((gw) => {
    const card = svgRoot.querySelector(`.po-gw-card[data-gw="${gw}"]`);
    if (card) card.classList.add("is-waiting");
    setIconVisibility(gw, "wait");
  });
}

/** Full center→gateway path segments for each winner (hub + needed trunk + branch). */
const WIN_PATHS = {
  1: ["po-hub-left", "po-trunk-left-up", "Arrow 9", "Arrow 9-head"],
  2: ["po-hub-left", "Line 623", "Line 623-head"],
  3: ["po-hub-left", "po-trunk-left-down", "Arrow 10", "Arrow 10-head"],
  4: ["po-hub-right", "po-trunk-right-up", "Arrow 9_2", "Arrow 9_2-head"],
  5: ["po-hub-right", "Line 623_2", "Line 623_2-head"],
  6: ["po-hub-right", "po-trunk-right-down", "Arrow 10_2", "Arrow 10_2-head"],
};

function setResult(winner) {
  if (!svgRoot) return;
  resetPaths();
  resetCards();

  (WIN_PATHS[winner] || []).forEach((id) => {
    const el =
      (svgRoot.ownerDocument || document).getElementById(id) ||
      svgRoot.querySelector(`[id="${id}"]`);
    if (el && svgRoot.contains(el)) el.classList.add("is-success");
  });

  GATEWAYS.forEach((gw) => {
    const card = svgRoot.querySelector(`.po-gw-card[data-gw="${gw}"]`);
    const won = gw === winner;
    if (card) card.classList.add(won ? "is-success" : "is-fail");
    setIconVisibility(gw, won ? "ok" : "fail");
  });
}

function pickWinner() {
  const pool = GATEWAYS.filter((g) => g !== lastWinner);
  const choice = pool[Math.floor(Math.random() * pool.length)] || GATEWAYS[0];
  lastWinner = choice;
  return choice;
}

function schedule(fn, ms) {
  clearCycle();
  cycleTimer = window.setTimeout(fn, ms);
}

function runCycle() {
  if (aborted || !svgRoot || reduceMotion.value) return;
  setWaiting();
  schedule(() => {
    if (aborted) return;
    setResult(pickWinner());
    schedule(runCycle, RESULT_MS);
  }, WAIT_MS);
}

function showStaticOk() {
  // Reduced motion: one fixed success path, no cycling.
  setResult(4);
}

async function mountSvg(url) {
  clearCycle();
  loaded.value = false;
  svgRoot = null;
  if (!host.value || !url) return;

  const res = await fetch(url, { credentials: "same-origin" });
  if (!res.ok) throw new Error(`Failed to load layer SVG (${res.status})`);
  const markup = await res.text();
  if (aborted) return;

  host.value.innerHTML = markup;
  const svg = host.value.querySelector("svg");
  if (!svg) throw new Error("Layer SVG root missing");

  svg.setAttribute("role", "img");
  if (props.alt) svg.setAttribute("aria-label", props.alt);
  svg.removeAttribute("width");
  svg.removeAttribute("height");
  svg.style.width = "100%";
  svg.style.height = "auto";
  svg.style.display = "block";

  svgRoot = svg;
  loaded.value = true;

  if (reduceMotion.value) {
    showStaticOk();
  } else {
    runCycle();
  }
}

onMounted(async () => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  try {
    await mountSvg(props.src);
  } catch (err) {
    console.error(err);
    // Fallback: plain image if inline fails
    if (host.value) {
      host.value.innerHTML = "";
      const img = document.createElement("img");
      img.className = "po-layer-visual__fallback";
      img.src = props.src;
      img.alt = props.alt || "";
      img.width = Number(props.width) || 1240;
      img.height = Number(props.height) || 782;
      img.decoding = "async";
      host.value.appendChild(img);
      loaded.value = true;
    }
  }
});

watch(
  () => props.src,
  async (next) => {
    if (!next) return;
    try {
      await mountSvg(next);
    } catch (err) {
      console.error(err);
    }
  },
);

onBeforeUnmount(() => {
  aborted = true;
  clearCycle();
  svgRoot = null;
});
</script>

<template>
  <div
    ref="host"
    class="po-layer-visual"
    :class="{ 'po-layer-visual--ready': loaded }"
    :style="{ aspectRatio: `${width} / ${height}` }"
  />
</template>

<style scoped>
.po-layer-visual {
  width: 100%;
  line-height: 0;
  min-height: 12rem;
}

.po-layer-visual :deep(svg),
.po-layer-visual__fallback {
  width: 100%;
  height: auto;
  display: block;
}

.po-layer-visual__fallback {
  max-width: 100%;
}
</style>
