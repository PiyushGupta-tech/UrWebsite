<script setup>
import { onMounted, ref } from "vue";

defineProps({
  image: { type: String, required: true },
  alt: { type: String, default: "" },
});

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});

/** Exact Figma strokes — artboard 391:11616 (1291×813) */
const ARTBOARD = { w: 1291, h: 813 };

/**
 * Left fan wires — absolute matrices composed from parent + relativeTransform.
 * Top → bottom: 391:11734, 391:11728, 391:11739, 391:11723.
 */
const LEFT_WIRES = {
  strokeWidth: 1.5,
  dash: [3.4, 10],
  wires: [
    {
      id: "391:11734",
      matrix: [
        0.9997628927230835, -0.02177814394235611, 0.018100649118423462,
        0.9998362064361572, 320.4090299606323, 169.6015625,
      ],
      d: "M 0.000184657719778253 0 C -0.08236908808572853 2.279134823508215 27.538646782804022 4.67486183298916 35.611602410328594 12.844941391763522 C 43.684558037853165 21.01502095053788 54.867133350719676 68.90763060504722 65.29998976488334 95.76038045618725 C 75.73284617904699 122.61313030732728 89.47534262348594 119.950424966293 89.47534262348594 119.950424966293 L 95.28785705566406 120.11847686767578",
    },
    {
      id: "391:11728",
      matrix: [
        0.9997671246528625, -0.021582037210464478, 0.018265146762132645,
        0.9998332262039185, 319.9999723434448, 240.2265625,
      ],
      d: "M 0.00019802235114187841 0 C -0.0850451799670853 0.9333980293583704 27.37440538196109 0.6890050472496121 36.77177396933995 5.26052374109336 C 46.1691425567188 9.832042434937108 56.654617355001164 28.22046773630853 67.42735975981304 39.217756811590164 C 78.20010216462492 50.21504588687179 92.39030373240485 49.12456108683974 92.39030373240485 49.12456108683974 L 98.39218139648436 49.193382263183594",
    },
    {
      id: "391:11739",
      matrix: [
        0.9997628927230835, -0.02177814394235611, -0.018100649118423462,
        -0.9998362064361572, 323.7574462890625, 317.65234375,
      ],
      d: "M 0.00018430405538439904 0 C -0.07915353674684975 0.5380678342664826 25.477998613547733 0.39718483404297844 34.22434931913532 3.0324884023589975 C 42.97070002472291 5.667791970675017 52.729775576410916 16.268007511386365 62.75621897339104 22.607518908986215 C 72.78266237037117 28.947030306586065 85.98981394905657 28.318407532250035 85.98981394905657 28.318407532250035 L 91.5759048461914 28.358081817626953",
    },
    {
      id: "391:11723",
      matrix: [
        0.9997628927230835, 0.02177814394235611, 0.018100649118423462,
        -0.9998362064361572, 323.23876953125, 393.97265625,
      ],
      d: "M 0.00018148701716274218 0 C -0.08095475450595037 2.0461814403533936 27.06579542144966 4.197036266326904 35.00013415934346 11.532041549682617 C 42.93447289723726 18.86704683303833 53.92504292170916 61.86450386047363 64.17876074588747 85.97259521484375 C 74.4324785700658 110.08068656921387 87.93900558975999 107.69012451171875 87.93900558975999 107.69012451171875 L 93.6517105102539 107.84100341796875",
    },
  ],
};

/** Right forks 391:11798 / 391:11797 — mirrored; reverse for hub→right flow */
const RIGHT_WIRES = {
  strokeWidth: 1.0580846071243286,
  dash: [3.4, 10],
  wires: [
    {
      id: "391:11798",
      matrix: [
        -0.999943733215332, -0.010600101202726364, -0.03717530146241188,
        0.999308705329895, 965.9998931884766, 238.76856994628906,
      ],
      d: "M 0.0003553186063475815 0 C -0.15849467445427182 0.8249711764562787 52.98989117635671 1.6921446801351672 68.52388221238054 4.649442474465292 C 84.05787324840438 7.606740268795416 105.57540513775882 24.942278273712915 125.65031824206169 34.662082196520096 C 145.72523134636455 44.38188611932728 172.16854650756602 43.41807429835471 172.16854650756602 43.41807429835471 L 183.3529815673828 43.47890090942383",
    },
    {
      id: "391:11797",
      matrix: [
        -0.999943733215332, 0.010600101202726364, -0.03717530146241188,
        -0.999308705329895, 965.9998931884766, 323.53224182128906,
      ],
      d: "M 0.00035529474134485267 0 C -0.15848403317952503 0.8521678267751999 52.986333570692665 1.7479290443356605 68.51928247510747 4.802719329482779 C 84.05223137952228 7.857509614629897 105.56831948257474 25.764544634209848 125.64188505379992 35.8047787470213 C 145.7154506250251 45.84501285983276 172.15699429120627 44.849426363516095 172.15699429120627 44.849426363516095 L 183.34068298339844 44.91225814819336",
    },
  ],
};

/** Down 391:11792 inside 391:11791 @ (638, 465) — path methods→hub; reverse */
const DOWN_WIRE = {
  id: "391:11792",
  strokeWidth: 1.5648747682571411,
  dash: [3.4, 10],
  matrix: [
    -1.0408340855860843e-16, -1, 0.9999925494194031, -0.003874043468385935, 643,
    519.1236763000488,
  ],
  d: "M 0 0.02136107372914134 L 21.343199159057075 0 L 27.678577646722033 0.4331850902385793 L 34.53064475608201 1.032570139692355 L 50.119354248046875 1.0865756273269653",
};

function matrixAttr(m) {
  return `matrix(${m.join(" ")})`;
}

function dashAttr(dash) {
  return dash.join(" ");
}
</script>

<template>
  <div
    class="foi-baas"
    :class="{ 'foi-baas--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="foi-baas__img"
      :src="image"
      :alt="alt"
      width="1291"
      height="813"
      decoding="async"
      loading="lazy"
      draggable="false"
    />

    <svg
      class="foi-baas__fx"
      :viewBox="`0 0 ${ARTBOARD.w} ${ARTBOARD.h}`"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- Left fan — customers → BAAS -->
      <g
        v-for="(wire, i) in LEFT_WIRES.wires"
        :key="wire.id"
        :transform="matrixAttr(wire.matrix)"
      >
        <path
          class="foi-baas__dash"
          :d="wire.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="LEFT_WIRES.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(LEFT_WIRES.dash)"
        />
        <circle
          v-show="!reduceMotion"
          class="foi-baas__flow-dot"
          r="2.4"
        >
          <animateMotion
            :dur="`${2.8 + i * 0.28}s`"
            :begin="`${i * 0.4}s`"
            repeatCount="indefinite"
            :path="wire.d"
          />
        </circle>
      </g>

      <!-- Right forks — BAAS → businesses (L→R) -->
      <g
        v-for="(wire, i) in RIGHT_WIRES.wires"
        :key="wire.id"
        :transform="matrixAttr(wire.matrix)"
      >
        <path
          class="foi-baas__dash foi-baas__dash--rtl"
          :d="wire.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="RIGHT_WIRES.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(RIGHT_WIRES.dash)"
        />
        <circle
          v-show="!reduceMotion"
          class="foi-baas__flow-dot"
          r="2.2"
        >
          <animateMotion
            :dur="`${2.8 + i * 0.28}s`"
            :begin="`${0.2 + i * 0.4}s`"
            repeatCount="indefinite"
            calcMode="linear"
            keyPoints="1;0"
            keyTimes="0;1"
            :path="wire.d"
          />
        </circle>
      </g>

      <!-- Down — BAAS → payment methods -->
      <g :transform="matrixAttr(DOWN_WIRE.matrix)">
        <path
          class="foi-baas__dash foi-baas__dash--rtl"
          :d="DOWN_WIRE.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="DOWN_WIRE.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(DOWN_WIRE.dash)"
        />
        <circle
          v-show="!reduceMotion"
          class="foi-baas__flow-dot"
          r="2.2"
        >
          <animateMotion
            dur="2.6s"
            begin="0.6s"
            repeatCount="indefinite"
            calcMode="linear"
            keyPoints="1;0"
            keyTimes="0;1"
            :path="DOWN_WIRE.d"
          />
        </circle>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.foi-baas {
  position: relative;
  width: fit-content;
  max-width: 100%;
  margin-inline: auto;
  line-height: 0;
  border-radius: 14px;
  overflow: hidden;
}

.foi-baas__img {
  display: block;
  width: auto;
  height: auto;
  max-width: min(1291px, calc(100vw - 20px));
  max-height: calc(100svh - var(--page-nav-offset, 129px) - 20px);
  object-fit: contain;
  pointer-events: none;
  user-select: none;
}

.foi-baas__fx {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.foi-baas--motion .foi-baas__dash {
  animation: foi-dash-march 1.1s linear infinite;
}

.foi-baas--motion .foi-baas__dash--rtl {
  animation-name: foi-dash-march-rtl;
}

.foi-baas__flow-dot {
  fill: #80dbed;
  filter: drop-shadow(0 0 3px rgba(128, 219, 237, 0.95));
}

@keyframes foi-dash-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes foi-dash-march-rtl {
  to {
    stroke-dashoffset: 13.4;
  }
}

@media (prefers-reduced-motion: reduce) {
  .foi-baas--motion .foi-baas__dash,
  .foi-baas--motion .foi-baas__dash--rtl {
    animation: none;
  }
}
</style>
