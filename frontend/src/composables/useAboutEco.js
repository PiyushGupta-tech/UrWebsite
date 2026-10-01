import {
  ref,
  computed,
  watch,
  onMounted,
  onUnmounted,
  provide,
  inject,
} from "vue";

export const ABOUT_ECO_KEY = Symbol("aboutEco");

export const ABOUT_ECO_NODES = [
  {
    id: "vision",
    label: "Vision",
    icon: "vision",
    pos: "top",
    hint: "Trusted payment infrastructure for growth and inclusion.",
    spoke: { x2: 160, y2: 42 },
  },
  {
    id: "mission",
    label: "Mission",
    icon: "mission",
    pos: "top-right",
    hint: "RBI PA-PG by 2027: secure payments that scale with you.",
    spoke: { x2: 248, y2: 110 },
  },
  {
    id: "solutions",
    label: "Solutions",
    icon: "solutions",
    pos: "bottom-right",
    hint: "UPI, cards, netbanking, wallets, and EMI in one stack.",
    spoke: { x2: 248, y2: 210 },
  },
  {
    id: "growth",
    label: "Growth",
    icon: "growth",
    pos: "bottom",
    hint: "Analytics and insights that turn volume into momentum.",
    spoke: { x2: 160, y2: 278 },
  },
  {
    id: "security",
    label: "Security",
    icon: "security",
    pos: "bottom-left",
    hint: "Bank-grade protection across every transaction flow.",
    spoke: { x2: 72, y2: 210 },
  },
  {
    id: "trust",
    label: "Trust",
    icon: "trust",
    pos: "top-left",
    hint: "Transparent settlement and support customers can feel.",
    spoke: { x2: 72, y2: 110 },
  },
];

export function provideAboutEco(readyRef) {
  const nodes = ABOUT_ECO_NODES;
  const autoIndex = ref(0);
  const hoveredId = ref(null);
  const lockedId = ref(null);
  const isPaused = ref(false);

  const activeId = computed(() => {
    if (lockedId.value) return lockedId.value;
    if (hoveredId.value) return hoveredId.value;
    return nodes[autoIndex.value]?.id ?? nodes[0].id;
  });

  const activeNode = computed(
    () => nodes.find((n) => n.id === activeId.value) ?? nodes[0],
  );

  let cycleTimer = null;

  function startCycle() {
    stopCycle();
    cycleTimer = setInterval(() => {
      if (!readyRef.value || isPaused.value || lockedId.value) return;
      autoIndex.value = (autoIndex.value + 1) % nodes.length;
    }, 2800);
  }

  function stopCycle() {
    if (cycleTimer) {
      clearInterval(cycleTimer);
      cycleTimer = null;
    }
  }

  function onNodeEnter(id) {
    hoveredId.value = id;
    isPaused.value = true;
  }

  function onNodeLeave() {
    hoveredId.value = null;
    if (!lockedId.value) isPaused.value = false;
  }

  function onNodeClick(id) {
    lockedId.value = lockedId.value === id ? null : id;
    isPaused.value = !!lockedId.value;
  }

  function onHubClick() {
    lockedId.value = null;
    isPaused.value = false;
  }

  watch(
    readyRef,
    (ready) => {
      if (ready) startCycle();
      else stopCycle();
    },
    { immediate: true },
  );

  onMounted(() => {
    if (readyRef.value) startCycle();
  });

  onUnmounted(stopCycle);

  const api = {
    nodes,
    activeId,
    activeNode,
    lockedId,
    ready: readyRef,
    onNodeEnter,
    onNodeLeave,
    onNodeClick,
    onHubClick,
  };

  provide(ABOUT_ECO_KEY, api);
  return api;
}

export function useAboutEco() {
  const eco = inject(ABOUT_ECO_KEY);
  if (!eco) {
    throw new Error("useAboutEco() must be used under provideAboutEco()");
  }
  return eco;
}
