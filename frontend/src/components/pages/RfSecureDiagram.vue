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

/**
 * Exact Figma strokes — artboard 538:5076 (1291×706) cropped to 1291×568
 * (69px pad removed top + bottom). Connectors live in 538:5075.
 */
const Y_CROP = 69;
const ARTBOARD = { w: 1291, h: 568 };

/** Left fan — inputs → engine (top → bottom) */
const LEFT_WIRES = {
  strokeWidth: 1.5,
  dash: [3.4, 10],
  wires: [
    {
      id: "493:5351",
      matrix: [
        0.9997628927230835, -0.02177814394235611, 0.018100649118423462,
        0.9998362064361572, 339.4090299606323, 238.6015625 - Y_CROP,
      ],
      d: "M 0.000184657719778253 0 C -0.08236908808572853 2.279134823508215 27.538646782804022 4.67486183298916 35.611602410328594 12.844941391763522 C 43.684558037853165 21.01502095053788 54.867133350719676 68.90763060504722 65.29998976488334 95.76038045618725 C 75.73284617904699 122.61313030732728 89.47534262348594 119.950424966293 89.47534262348594 119.950424966293 L 95.28785705566406 120.11847686767578",
    },
    {
      id: "493:5347",
      matrix: [
        0.9997671246528625, -0.021582037210464478, 0.018265146762132645,
        0.9998332262039185, 338.9999723434448, 309.2265625 - Y_CROP,
      ],
      d: "M 0.00019802235114187841 0 C -0.0850451799670853 0.9333980293583704 27.37440538196109 0.6890050472496121 36.77177396933995 5.26052374109336 C 46.1691425567188 9.832042434937108 56.654617355001164 28.22046773630853 67.42735975981304 39.217756811590164 C 78.20010216462492 50.21504588687179 92.39030373240485 49.12456108683974 92.39030373240485 49.12456108683974 L 98.39218139648436 49.193382263183594",
    },
    {
      id: "493:5355",
      matrix: [
        0.9997628927230835, -0.02177814394235611, -0.018100649118423462,
        -0.9998362064361572, 342.7574462890625, 386.65234375 - Y_CROP,
      ],
      d: "M 0.00018430405538439904 0 C -0.07915353674684975 0.5380678342664826 25.477998613547733 0.39718483404297844 34.22434931913532 3.0324884023589975 C 42.97070002472291 5.667791970675017 52.729775576410916 16.268007511386365 62.75621897339104 22.607518908986215 C 72.78266237037117 28.947030306586065 85.98981394905657 28.318407532250035 85.98981394905657 28.318407532250035 L 91.5759048461914 28.358081817626953",
    },
    {
      id: "493:5343",
      matrix: [
        0.9997628927230835, 0.02177814394235611, 0.018100649118423462,
        -0.9998362064361572, 342.23876953125, 462.97265625 - Y_CROP,
      ],
      d: "M 0.00018148701716274218 0 C -0.08095475450595037 2.0461814403533936 27.06579542144966 4.197036266326904 35.00013415934346 11.532041549682617 C 42.93447289723726 18.86704683303833 53.92504292170916 61.86450386047363 64.17876074588747 85.97259521484375 C 74.4324785700658 110.08068656921387 87.93900558975999 107.69012451171875 87.93900558975999 107.69012451171875 L 93.6517105102539 107.84100341796875",
    },
  ],
};

/**
 * Right fan — mirrored so paths run through the gap (decision → outcomes).
 * Origins sit on outcome-card dots; a < 0 extends left toward the engine.
 * Reverse motion + rtl dash = L→R hub→outcomes flow.
 */
const RIGHT_WIRES = {
  strokeWidth: 1.5,
  dash: [3.4, 10],
  wires: [
    {
      id: "538:5058",
      matrix: [
        -0.9997628927230835, -0.02177814394235611, -0.018100649118423462,
        0.9998362064361572, 1026.7382540106773, 241.5 - Y_CROP,
      ],
      d: "M 0.000184657719778253 0 C -0.08236908808572853 2.279134823508215 27.538646782804022 4.67486183298916 35.611602410328594 12.844941391763522 C 43.684558037853165 21.01502095053788 54.867133350719676 68.90763060504722 65.29998976488334 95.76038045618725 C 75.73284617904699 122.61313030732728 89.47534262348594 119.950424966293 89.47534262348594 119.950424966293 L 95.28785705566406 120.11847686767578",
    },
    {
      id: "538:5054",
      matrix: [
        -0.9997671246528625, -0.021582037210464478, -0.018265146762132645,
        0.9998332262039185, 1025.7382540106773, 311.5 - Y_CROP,
      ],
      d: "M 0.00019802235114187841 0 C -0.0850451799670853 0.9333980293583704 27.37440538196109 0.6890050472496121 36.77177396933995 5.26052374109336 C 46.1691425567188 9.832042434937108 56.654617355001164 28.22046773630853 67.42735975981304 39.217756811590164 C 78.20010216462492 50.21504588687179 92.39030373240485 49.12456108683974 92.39030373240485 49.12456108683974 L 98.39218139648436 49.193382263183594",
    },
    {
      id: "538:5062",
      matrix: [
        -0.9997628927230835, -0.02177814394235611, 0.018100649118423462,
        -0.9998362064361572, 1027.7382540106773, 387.0885810852051 - Y_CROP,
      ],
      d: "M 0.00018430405538439904 0 C -0.07915353674684975 0.5380678342664826 25.477998613547733 0.39718483404297844 34.22434931913532 3.0324884023589975 C 42.97070002472291 5.667791970675017 52.729775576410916 16.268007511386365 62.75621897339104 22.607518908986215 C 72.78266237037117 28.947030306586065 85.98981394905657 28.318407532250035 85.98981394905657 28.318407532250035 L 91.5759048461914 28.358081817626953",
    },
    {
      id: "538:5050",
      matrix: [
        -0.9997628927230835, 0.02177814394235611, -0.018100649118423462,
        -0.9998362064361572, 1026.7382540106773, 464.5010757446289 - Y_CROP,
      ],
      d: "M 0.00018148701716274218 0 C -0.08095475450595037 2.0461814403533936 27.06579542144966 4.197036266326904 35.00013415934346 11.532041549682617 C 42.93447289723726 18.86704683303833 53.92504292170916 61.86450386047363 64.17876074588747 85.97259521484375 C 74.4324785700658 110.08068656921387 87.93900558975999 107.69012451171875 87.93900558975999 107.69012451171875 L 93.6517105102539 107.84100341796875",
    },
  ],
};

/**
 * Center bridges — Figma 493:5365 / 538:5032 (28×8 frames).
 * Each is a short dashed stub + cursor arrow. Positions in cropped artboard.
 */
const BRIDGES = [
  {
    id: "493:5365",
    x: 528,
    y: 355 - Y_CROP,
    w: 30,
    h: 12,
  },
  {
    id: "538:5032",
    x: 789,
    y: 356 - Y_CROP,
    w: 30,
    h: 12,
  },
];

/** Shared geometry inside each bridge frame (Figma local coords) */
const BRIDGE_LINE = {
  // Figma Line 607 relativeTransform → SVG matrix(a b c d e f)
  matrix: [
    0.9997593760490417, 0.021935544908046722, -0.017970746383070946,
    0.9998385310173035, 2.9659981727600098, 3.501508951187134,
  ],
  d: "M 0 0.5064674615859985 L 9.60391715126408 0.26335853949800714 L 14.50401880033487 0.13931969096293456 L 17.4440787725888 0.06489633992611248 L 19.991886138916016 0",
  strokeWidth: 1.5,
  dash: [3.4, 10],
};

/**
 * Cursor arrow — local vector path + frame relativeTransform (−134.4°).
 * Applying the frame matrix keeps the tip on the dash centerline (y ≈ 3.9).
 */
const BRIDGE_ARROW = {
  matrix: [
    -0.6996233463287354, 0.7145118713378906, -0.7145118713378906,
    -0.6996233463287354, 29.313081741333008, 3.5969865322113037,
  ],
  d: "M 1.126366215183593 0.045223279426653724 L 1.1252233726767205 0.045223279426653724 C 0.9747291445527981 -0.005885916196770549 0.8129336876807658 -0.013851295859665238 0.6581470392859038 0.022228567041062523 C 0.5033603908910418 0.05830842994179028 0.3617625142337131 0.1369930018117983 0.2493777615254531 0.24937774877305294 C 0.1369930088171931 0.3617624957343076 0.0583084329235015 0.5033603651507628 0.0222285681777621 0.6581470056303189 C -0.013851296567977296 0.8129336461098751 -0.005885916497757944 0.9747290947081927 0.04522328173923116 1.12522331513631 L 0.04579471150761724 1.1269376128687543 L 0.04693756678691449 1.1303661402140477 L 0.05150899641905332 1.1440804539540064 L 0.06979471494760864 1.196651887777789 L 0.13836614665726635 1.3966518366782534 L 0.38522331273296384 2.113794771393512 L 2.1395090743096095 7.2246520043063445 L 2.2126519484238307 7.437794947901945 L 2.2326519988322935 7.497223572655504 L 2.2383662794862547 7.5143662775015665 C 2.249924761898739 7.623726318592738 2.2929493516092 7.7273879426728875 2.362227192072007 7.81279168452914 C 2.431505032534814 7.898195426385392 2.5240630012913012 7.961676092040141 2.6286873564454245 7.995542934493433 C 2.7333117115995478 8.029409776946725 2.845512132673809 8.032209441219164 2.95169523454448 8.003602300039049 C 3.0578783364151505 7.974995158858934 3.153486969020962 7.9162091509502455 3.22693765005672 7.834366522716366 C 3.2715266915001173 7.7911629169099 3.3087770042200897 7.740981263239372 3.3372235527804848 7.685794960832467 C 3.3629378412681596 7.635509245965345 3.3817950598134368 7.578937654955793 3.4000807762132546 7.526366225389485 L 3.4006521634068916 7.524080676731813 L 3.969223565313218 5.884080714278271 L 4.3406522165382855 4.812080465013291 L 4.462366408091578 4.461794792735674 L 4.463509182478852 4.458937584435203 L 4.467509165312705 4.457794810106368 L 4.820080676755781 4.333223416476688 L 5.897223738060638 3.9520803850150745 C 6.446336504128724 3.7590555250337547 6.994533300013305 3.5634343207417283 7.541795426884547 3.365223260530436 L 7.568080872662213 3.3549377466141515 C 7.630938019460435 3.3303663167910176 7.743509539078346 3.2875091651169286 7.8337952636694 3.197223445142804 C 7.886562207687177 3.1444769013846474 7.928420523877561 3.0818512196702352 7.9569789312051835 3.0129239730191286 C 7.985537338532806 2.943996726368022 8.000236511230469 2.8701184112996256 8.000236511230469 2.7955091133702403 C 8.000236511230469 2.720899815440855 7.985537338532806 2.6470215003724586 7.9569789312051835 2.578094253721352 C 7.928420523877561 2.5091670070702454 7.886562207687177 2.4465413253558332 7.8337952636694 2.3937947815976766 L 7.828080846776242 2.3880803649967355 C 7.7964415006951615 2.3536381035504848 7.761620156178521 2.322260691703255 7.724080748139272 2.294366058072672 C 7.659090955520665 2.250201314580458 7.586994262202805 2.217535363114381 7.510938338600996 2.197794679087328 L 7.5097950192569325 2.197794679087328 L 7.489795105087667 2.190937624396742 L 7.428080928520566 2.170937575011019 L 7.209795216804372 2.098366228040704 L 6.468080688741511 1.8492233045421553 C 5.013819627330739 1.3594218212450362 3.559914558942612 0.8685645864019309 2.1063663010123137 0.3766518724912203 L 1.3943662230849265 0.13665185036415875 L 1.1955090383443625 0.06808042216102998 L 1.142366214638604 0.05150899378504406 L 1.1292233555105735 0.045794709165818674 L 1.126366215183593 0.045223279426653724 Z",
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
    class="rf-engine"
    :class="{ 'rf-engine--motion': !reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <img
      class="rf-engine__img"
      :src="image"
      :alt="alt"
      width="1291"
      height="568"
      decoding="async"
      loading="lazy"
      draggable="false"
    />

    <svg
      class="rf-engine__fx"
      :viewBox="`0 0 ${ARTBOARD.w} ${ARTBOARD.h}`"
      fill="none"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid meet"
    >
      <g
        v-for="(wire, i) in LEFT_WIRES.wires"
        :key="wire.id"
        :transform="matrixAttr(wire.matrix)"
      >
        <path
          class="rf-engine__dash"
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
          class="rf-engine__flow-dot"
          r="2.4"
        >
          <animateMotion
            :dur="`${2.8 + i * 0.28}s`"
            :begin="`${i * 0.35}s`"
            repeatCount="indefinite"
            :path="wire.d"
          />
        </circle>
      </g>

      <g
        v-for="(wire, i) in RIGHT_WIRES.wires"
        :key="wire.id"
        :transform="matrixAttr(wire.matrix)"
      >
        <path
          class="rf-engine__dash rf-engine__dash--rtl"
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
          class="rf-engine__flow-dot"
          r="2.4"
        >
          <!-- Path runs outer→hub; reverse for hub→outcomes -->
          <animateMotion
            :dur="`${2.8 + i * 0.28}s`"
            :begin="`${0.2 + i * 0.35}s`"
            repeatCount="indefinite"
            calcMode="linear"
            keyPoints="1;0"
            keyTimes="0;1"
            :path="wire.d"
          />
        </circle>
      </g>

      <!-- Center bridges — Figma 493:5365 / 538:5032 -->
      <g
        v-for="(bridge, bi) in BRIDGES"
        :key="bridge.id"
        :transform="`translate(${bridge.x} ${bridge.y})`"
      >
        <g :transform="matrixAttr(BRIDGE_LINE.matrix)">
          <path
            class="rf-engine__bridge-dash"
            :d="BRIDGE_LINE.d"
            fill="none"
            stroke="#62E9FE"
            :stroke-width="BRIDGE_LINE.strokeWidth"
            stroke-linecap="round"
            stroke-linejoin="round"
            :stroke-dasharray="dashAttr(BRIDGE_LINE.dash)"
          />
          <circle
            v-show="!reduceMotion"
            class="rf-engine__flow-dot"
            r="1.6"
          >
            <animateMotion
              :dur="`${1.4 + bi * 0.15}s`"
              :begin="`${bi * 0.25}s`"
              repeatCount="indefinite"
              :path="BRIDGE_LINE.d"
            />
          </circle>
        </g>
        <!-- Cursor arrow via Figma frame matrix (−134°) so tip sits on dash centerline -->
        <g
          v-show="!reduceMotion"
          class="rf-engine__bridge-arrow-wrap rf-engine__bridge-arrow-wrap--ghost"
        >
          <g :transform="matrixAttr(BRIDGE_ARROW.matrix)">
            <path
              class="rf-engine__bridge-arrow"
              :d="BRIDGE_ARROW.d"
              fill="#62E9FE"
              fill-opacity="0.35"
            />
          </g>
        </g>
        <g class="rf-engine__bridge-arrow-wrap">
          <g :transform="matrixAttr(BRIDGE_ARROW.matrix)">
            <path
              class="rf-engine__bridge-arrow"
              :d="BRIDGE_ARROW.d"
              fill="#62E9FE"
            />
          </g>
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.rf-engine {
  position: relative;
  width: min(1291px, 100%);
  aspect-ratio: 1291 / 568;
  margin-inline: auto;
  border-radius: 12px;
  overflow: hidden;
  line-height: 0;
}

.rf-engine__img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 12px;
  pointer-events: none;
  user-select: none;
}

.rf-engine__fx {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.rf-engine--motion .rf-engine__dash {
  animation: rf-dash-march 1.1s linear infinite;
}

.rf-engine--motion .rf-engine__dash--rtl {
  animation-name: rf-dash-march-rtl;
}

.rf-engine--motion .rf-engine__bridge-dash {
  animation: rf-bridge-dash-march 0.7s linear infinite;
}

.rf-engine--motion .rf-engine__bridge-arrow-wrap {
  animation: rf-bridge-arrow-nudge 1.1s ease-in-out infinite;
}

.rf-engine--motion .rf-engine__bridge-arrow-wrap--ghost {
  animation: rf-bridge-arrow-ghost 1.1s ease-in-out infinite;
}

.rf-engine__flow-dot {
  fill: #80dbed;
  filter: drop-shadow(0 0 3px rgba(128, 219, 237, 0.95));
}

.rf-engine__bridge-arrow {
  filter: drop-shadow(0 0 2px rgba(98, 233, 254, 0.85));
}

@keyframes rf-dash-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes rf-dash-march-rtl {
  to {
    stroke-dashoffset: 13.4;
  }
}

@keyframes rf-bridge-dash-march {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes rf-bridge-arrow-nudge {
  0%,
  100% {
    transform: translateX(0);
    opacity: 0.92;
  }
  50% {
    transform: translateX(2.5px);
    opacity: 1;
  }
}

@keyframes rf-bridge-arrow-ghost {
  0%,
  100% {
    transform: translateX(-3px);
    opacity: 0.2;
  }
  50% {
    transform: translateX(0);
    opacity: 0.45;
  }
}

@media (prefers-reduced-motion: reduce) {
  .rf-engine--motion .rf-engine__dash,
  .rf-engine--motion .rf-engine__dash--rtl,
  .rf-engine--motion .rf-engine__bridge-dash,
  .rf-engine--motion .rf-engine__bridge-arrow-wrap,
  .rf-engine--motion .rf-engine__bridge-arrow-wrap--ghost {
    animation: none;
  }
}
</style>
