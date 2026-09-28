<script setup>
import { onMounted, ref } from "vue";

defineProps({
  ready: { type: Boolean, default: false },
  alt: { type: String, default: "Urbanrupee withdrawals platform diagram" },
});

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});

/**
 * Exact Figma strokes — artboard 385:7673 (1291×813).
 * Left fan 385:7778 @ (310, 159.88); right 385:7855 / 385:7854; down 385:7848.
 */
const ARTBOARD = { w: 1291, h: 813 };

const LEFT_FAN = {
  x: 310,
  y: 159.88174438476562,
  w: 168.40603637695312,
  h: 239.23651123046875,
  strokeWidth: 1.3734196424484253,
  dash: [3.4, 10],
  /** Top → bottom — transforms composed into fan-local space */
  wires: [
    {
      id: "385:7791",
      matrix: [
        0.9997236132621765, -0.023510374128818512, 0.016766736283898354,
        0.9998594522476196, 11.378905773162842, 4.6015625,
      ],
      d: "M 0.0002518088820549861 0 C -0.11232277757823075 1.9440304700052475 37.55313272584712 3.9875104152050413 48.5618353887394 10.956331847267696 C 59.57053805163167 17.925153279330353 74.81968003935931 58.77604612520419 89.04646629798684 81.68059892989127 C 103.27325255661437 104.58515173457836 122.0132362977454 102.31394765212373 122.0132362977454 102.31394765212373 L 129.93948364257812 102.45729064941406",
    },
    {
      id: "385:7785",
      matrix: [
        0.9997236132621765, -0.023510374128818512, 0.016766736283898354,
        0.9998594522476196, 10.999972343444824, 79.2265625,
      ],
      d: "M 0.0002620158374098356 0 C -0.11252863082501552 0.7348929329152623 36.22079885624576 0.5424748328585545 48.655048756181564 4.141771890626286 C 61.08929865611737 7.741068948394018 74.96329037507873 22.21884089173895 89.21738394643968 30.87734430448586 C 103.47147751780064 39.53584771723277 122.24742642132777 38.67727554567381 122.24742642132777 38.67727554567381 L 130.1888885498047 38.73146057128906",
    },
    {
      id: "385:7796",
      matrix: [
        0.9997236132621765, -0.023510374128818512, -0.016766736283898354,
        -0.9998594522476196, 14.480468273162842, 157.064453125,
      ],
      d: "M 0.00025678860846489797 0 C -0.11028367906180338 0.5380553334227276 35.498192123531425 0.3971755122331593 47.68437812157467 3.0324178608324805 C 59.87056411961791 5.667660209431801 73.46776901602647 16.267629349552635 87.43749271403689 22.606993537212535 C 101.40721641204732 28.946357724872435 119.80858420419045 28.317750052455345 119.80858420419045 28.317750052455345 L 127.59161376953124 28.357421875",
    },
    {
      id: "385:7780",
      matrix: [
        0.9997236132621765, 0.023510374128818512, 0.016766736283898354,
        -0.9998594522476196, 14, 232.97265625,
      ],
      d: "M 0.00024322281456697818 0 C -0.10849283705438462 1.863770842552185 36.27266511216284 3.8228845596313477 46.905999396481484 10.503997802734375 C 57.53933368080013 17.185111045837402 72.26852537411169 56.34948539733887 86.01021323624529 78.30841827392578 C 99.7519010983789 100.2673511505127 117.85290063108093 98.08990478515625 117.85290063108093 98.08990478515625 L 125.50888061523438 98.22732543945312",
    },
  ],
};

/** Absolute to artboard — matrix a < 0 (mirrored); flow hub → beneficiaries = reverse */
const RIGHT_WIRES = {
  strokeWidth: 1.0580846071243286,
  dash: [3.4, 10],
  wires: [
    {
      id: "385:7855",
      matrix: [
        -0.9998769164085388, -0.01568710431456566, -0.02512788027524948,
        0.99968421459198, 970, 261.943359375,
      ],
      d: "M 0.0002400961529929191 0 C -0.10709813862922601 0.8246613144874573 35.806368827819824 1.6915090084075928 46.303009033203125 4.647696018218994 C 56.799649238586426 7.6038830280303955 71.33948993682861 24.932909965515137 84.90452575683594 34.64906311035156 C 98.46956157684326 44.36521625518799 116.33786010742188 43.40176773071289 116.33786010742188 43.40176773071289 L 123.89541625976562 43.46257019042969",
    },
    {
      id: "385:7854",
      matrix: [
        -0.9998769164085388, 0.01568710431456566, -0.02512788027524948,
        -0.99968421459198, 970, 346.70703125,
      ],
      d: "M 0.00024008001491893083 0 C -0.10709094260528218 0.8518478870391846 35.803964614868164 1.7472729682922363 46.29990005493164 4.8009161949157715 C 56.79583549499512 7.854559421539307 71.33470249176025 25.754871368408203 84.8988265991211 35.79133605957031 C 98.46295070648193 45.82780075073242 116.33004760742188 44.83258819580078 116.33004760742188 44.83258819580078 L 123.88710021972656 44.89539337158203",
    },
  ],
};

/** Down connector 385:7849 inside 385:7848 @ (639, 465) */
const DOWN_WIRE = {
  id: "385:7849",
  strokeWidth: 1.5648747682571411,
  dash: [3.4, 10],
  matrix: [
    -1.0408340855860843e-16, -1, 0.9999925494194031, -0.003874043468385935, 644,
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
    class="po-platform"
    :class="{
      'po-platform--ready': ready,
      'po-platform--motion': ready && !reduceMotion,
    }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="po-platform__full"
      data-po-part="diagram"
      src="/images/figma-payouts/platform/diagram-graphic.png?v=5"
      alt=""
      width="1291"
      height="813"
      decoding="async"
    />

    <!-- Animated dotted connectors — exact Figma paths; dots stay in PNG -->
    <svg
      class="po-platform__fx"
      :viewBox="`0 0 ${ARTBOARD.w} ${ARTBOARD.h}`"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- Left fan 385:7778 -->
      <g
        :transform="`translate(${LEFT_FAN.x} ${LEFT_FAN.y})`"
      >
        <g
          v-for="(wire, i) in LEFT_FAN.wires"
          :key="wire.id"
          :transform="matrixAttr(wire.matrix)"
        >
          <path
            class="po-platform__dash"
            :d="wire.d"
            fill="none"
            stroke="#ffffff"
            :stroke-width="LEFT_FAN.strokeWidth"
            stroke-linecap="round"
            stroke-linejoin="round"
            :stroke-dasharray="dashAttr(LEFT_FAN.dash)"
          />
          <circle
            v-show="ready && !reduceMotion"
            class="po-platform__flow-dot"
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
      </g>

      <!-- Right forks 385:7855 / 385:7854 — L→R via rtl dash + reverse motion -->
      <g
        v-for="(wire, i) in RIGHT_WIRES.wires"
        :key="wire.id"
        :transform="matrixAttr(wire.matrix)"
      >
        <path
          class="po-platform__dash po-platform__dash--rtl"
          :d="wire.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="RIGHT_WIRES.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(RIGHT_WIRES.dash)"
        />
        <circle
          v-show="ready && !reduceMotion"
          class="po-platform__flow-dot"
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

      <!-- Down 385:7849 — path runs methods→hub; reverse for hub→methods flow -->
      <g :transform="matrixAttr(DOWN_WIRE.matrix)">
        <path
          class="po-platform__dash po-platform__dash--rtl"
          :d="DOWN_WIRE.d"
          fill="none"
          stroke="#ffffff"
          :stroke-width="DOWN_WIRE.strokeWidth"
          stroke-linecap="round"
          stroke-linejoin="round"
          :stroke-dasharray="dashAttr(DOWN_WIRE.dash)"
        />
        <circle
          v-show="ready && !reduceMotion"
          class="po-platform__flow-dot"
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
.po-platform {
  /* Figma diagram group 385:7673 — 1291×813 (heading excluded) */
  --po-platform-w: 1291;
  --po-platform-h: 813;
  /* Fill the band under the navbar with 10px pad top + bottom */
  --po-platform-max-h: calc(100svh - var(--page-nav-offset, 129px) - 20px);
  position: relative;
  width: min(
    1291px,
    100%,
    calc(var(--po-platform-max-h) * var(--po-platform-w) / var(--po-platform-h))
  );
  margin-inline: auto;
  flex-shrink: 1;
  min-width: 0;
  line-height: 0;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.8s ease,
    transform 0.8s ease;
}

.po-platform--ready {
  opacity: 1;
  transform: translateY(0);
}

.po-platform__full {
  display: block;
  width: 100%;
  height: auto;
  pointer-events: none;
  user-select: none;
}

.po-platform__fx {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.po-platform--motion .po-platform__dash {
  animation: po-dash-march 1.1s linear infinite;
}

.po-platform--motion .po-platform__dash--rtl {
  animation-name: po-dash-march-rtl;
}

.po-platform__flow-dot {
  fill: #80dbed;
  filter: drop-shadow(0 0 3px rgba(128, 219, 237, 0.95));
}

@keyframes po-dash-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes po-dash-march-rtl {
  to {
    stroke-dashoffset: 13.4;
  }
}

@media (prefers-reduced-motion: reduce) {
  .po-platform--motion .po-platform__dash,
  .po-platform--motion .po-platform__dash--rtl {
    animation: none;
  }
}
</style>
