<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

const MODES = ["cards", "wallet", "netbanking", "upi"];
const CYCLE_MS = 2600;

const activeIndex = ref(1); // start on wallet (matches Figma default)
const reduceMotion = ref(false);
let timer = null;

const activeMode = computed(() => MODES[activeIndex.value]);

function isActive(mode) {
  return activeMode.value === mode;
}

function startCycle() {
  stopCycle();
  if (reduceMotion.value) return;
  timer = window.setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % MODES.length;
  }, CYCLE_MS);
}

function stopCycle() {
  if (timer != null) {
    window.clearInterval(timer);
    timer = null;
  }
}

onMounted(() => {
  reduceMotion.value = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  startCycle();
});

onUnmounted(stopCycle);
</script>

<template>
  <svg
    class="control-graphic"
    :class="{ 'control-graphic--static': reduceMotion }"
    width="396"
    height="290"
    viewBox="0 0 396 290"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="Payment routing across cards, wallet, netbanking, and UPI"
  >
    <!-- Hub rings -->
    <g class="control-graphic__orbits" aria-hidden="true">
      <circle
        class="control-graphic__orbit control-graphic__orbit--1"
        cx="196.545"
        cy="135.001"
        r="44.2273"
        fill="none"
        stroke="#097495"
        stroke-width="0.636364"
      />
      <circle
        class="control-graphic__orbit control-graphic__orbit--2"
        cx="197.273"
        cy="134.999"
        r="56.9545"
        fill="none"
        stroke="#097495"
        stroke-width="0.636364"
      />
      <circle
        class="control-graphic__orbit control-graphic__orbit--3"
        cx="197"
        cy="135"
        r="69.6818"
        fill="none"
        stroke="#097495"
        stroke-width="0.636364"
      />
    </g>

    <!-- Connection paths (muted base) -->
    <path
      class="control-graphic__path"
      :class="{ 'is-active': isActive('cards') }"
      d="M78 27L100.201 27C106.829 27 112.201 32.3726 112.201 39V123C112.201 129.627 117.574 135 124.201 135L163 135"
    />
    <path
      class="control-graphic__path"
      :class="{ 'is-active': isActive('wallet') }"
      d="M316 28H293.799C287.171 28 281.799 33.3726 281.799 40V82V124C281.799 130.627 276.426 136 269.799 136L231 136"
    />
    <path
      class="control-graphic__path"
      :class="{ 'is-active': isActive('netbanking') }"
      d="M316 244H293.799C287.171 244 281.799 238.627 281.799 232V148C281.799 141.373 276.426 136 269.799 136L231 136"
    />
    <path
      class="control-graphic__path"
      :class="{ 'is-active': isActive('upi') }"
      d="M78 243H100.201C106.829 243 112.201 237.627 112.201 231V147C112.201 140.373 117.574 135 124.201 135L163 135"
    />

    <!-- Center hub -->
    <g filter="url(#controlHubShadow)">
      <rect x="162.527" y="99.8076" width="70" height="70" rx="35" fill="#097495" />
      <rect
        x="169.527"
        y="106.807"
        width="56"
        height="56"
        rx="28"
        stroke="#00B7DB"
        stroke-opacity="0.188235"
        stroke-width="1.27273"
      />
      <path
        d="M197.423 127.392H189.082C189 127.392 188.935 127.326 188.935 127.245V124.61C188.935 124.549 188.984 124.499 189.046 124.499H205.801C205.977 124.499 206.119 124.641 206.119 124.817V126.73V130.523V135.432L206.071 136.441C206.012 137.714 205.711 138.964 205.185 140.125L204.892 140.684C204.374 141.671 203.78 142.617 203.114 143.511C203.048 143.601 202.915 143.604 202.845 143.517L198.376 138.04C198.31 137.958 198.353 137.835 198.456 137.814L199.493 137.599C199.504 137.597 199.514 137.594 199.524 137.59L199.871 137.448C200.548 137.171 201.16 136.754 201.665 136.224L201.732 136.154C202.096 135.772 202.392 135.33 202.608 134.848C203.01 133.948 203.114 132.942 202.905 131.978L202.851 131.729C202.615 130.639 202.047 129.648 201.226 128.893L201.189 128.86C200.162 127.916 198.818 127.392 197.423 127.392Z"
        fill="white"
      />
      <path
        d="M197.309 130.032H189.058C188.99 130.032 188.935 130.087 188.935 130.155V133.816V135.736C188.935 136.969 189.153 138.193 189.579 139.35L189.689 139.649C189.928 140.299 190.25 140.915 190.647 141.481C191.471 142.657 192.595 143.589 193.903 144.181L194.054 144.249C194.845 144.608 195.687 144.845 196.549 144.951L197.87 145.115H198.235C198.79 145.115 199.342 145.028 199.87 144.857C199.971 144.824 200.009 144.702 199.945 144.617L192.752 135.088C192.709 135.032 192.749 134.952 192.82 134.952H197.361C198.159 134.952 198.934 134.689 199.567 134.205C199.897 133.953 200.13 133.597 200.229 133.194L200.311 132.859C200.4 132.495 200.386 132.114 200.269 131.759L200.259 131.726C200.14 131.362 199.913 131.043 199.609 130.81C198.948 130.306 198.14 130.032 197.309 130.032Z"
        fill="white"
      />
    </g>

    <!-- Cards -->
    <g class="control-graphic__mode" :class="{ 'is-active': isActive('cards') }">
      <rect x="13.5" y="0" width="56" height="56" rx="28" fill="white" />
      <rect
        class="control-graphic__ring"
        x="14.3675"
        y="0.867474"
        width="54.2651"
        height="54.2651"
        rx="27.1325"
        fill="none"
      />
      <path
        class="control-graphic__icon"
        d="M33.166 26.3332H49.834M34.8328 22.166H48.1672C49.0878 22.166 49.834 22.9123 49.834 23.8329V32.1672C49.834 33.0877 49.0878 33.834 48.1672 33.834H34.8328C33.9123 33.834 33.166 33.0877 33.166 32.1672V23.8329C33.166 22.9123 33.9123 22.166 34.8328 22.166Z"
        fill="none"
        stroke-width="2"
        stroke-linecap="round"
      />
      <text class="control-graphic__label" x="41.5" y="72" text-anchor="middle">CARDS</text>
      <g transform="translate(-3 80)">
        <g class="control-graphic__badge">
          <rect width="89" height="19" rx="2" fill="#097495" fill-opacity="0.12549" />
          <text x="44.5" y="13" text-anchor="middle">OPTIMIZED ROUTE</text>
        </g>
      </g>
    </g>

    <!-- Wallet -->
    <g class="control-graphic__mode" :class="{ 'is-active': isActive('wallet') }">
      <rect x="323.5" y="0" width="56" height="56" rx="28" fill="white" />
      <rect
        class="control-graphic__ring"
        x="324.5"
        y="1"
        width="54"
        height="54"
        rx="27"
        fill="none"
      />
      <path
        class="control-graphic__icon"
        d="M359 31.3343V34.6676C359 34.8887 358.912 35.1006 358.756 35.2569C358.6 35.4132 358.388 35.501 358.167 35.501H345.667C345.225 35.501 344.801 35.3254 344.488 35.0128C344.176 34.7003 344 34.2763 344 33.8343V22.1676C344 21.7256 344.176 21.3017 344.488 20.9891C344.801 20.6766 345.225 20.501 345.667 20.501H356.5C356.721 20.501 356.933 20.5888 357.089 20.7451C357.246 20.9013 357.333 21.1133 357.333 21.3343V23.8343M344 22.1676C344 22.6097 344.176 23.0336 344.488 23.3462C344.801 23.6587 345.225 23.8343 345.667 23.8343H358.167C358.388 23.8343 358.6 23.9221 358.756 24.0784C358.912 24.2347 359 24.4466 359 24.6676V28.001M359 28.001H356.5C356.058 28.001 355.634 28.1766 355.321 28.4891C355.009 28.8017 354.833 29.2256 354.833 29.6676C354.833 30.1097 355.009 30.5336 355.321 30.8462C355.634 31.1587 356.058 31.3343 356.5 31.3343H359M359 28.001C359.221 28.001 359.433 28.0888 359.589 28.2451C359.746 28.4013 359.833 28.6133 359.833 28.8343V30.501C359.833 30.722 359.746 30.934 359.589 31.0902C359.433 31.2465 359.221 31.3343 359 31.3343"
        fill="none"
        stroke-width="2"
        stroke-linecap="round"
      />
      <text class="control-graphic__label" x="351.5" y="72" text-anchor="middle">WALLET</text>
      <g transform="translate(307 80)">
        <g class="control-graphic__badge">
          <rect width="89" height="19" rx="2" fill="#097495" fill-opacity="0.12549" />
          <text x="44.5" y="13" text-anchor="middle">OPTIMIZED ROUTE</text>
        </g>
      </g>
    </g>

    <!-- Netbanking -->
    <g class="control-graphic__mode" :class="{ 'is-active': isActive('netbanking') }">
      <rect x="324" y="190" width="56" height="56" rx="28" fill="white" />
      <rect
        class="control-graphic__ring"
        x="324.867"
        y="190.867"
        width="54.2651"
        height="54.2651"
        rx="27.1325"
        fill="none"
      />
      <path
        class="control-graphic__icon"
        d="M352.001 216.334H352.009M352.001 219.668H352.009M352.001 213.001H352.009M355.334 216.334H355.342M355.334 219.668H355.342M355.334 213.001H355.342M348.668 216.334H348.676M348.668 219.668H348.676M348.668 213.001H348.676M349.501 226.335V223.835C349.501 223.614 349.589 223.402 349.745 223.245C349.902 223.089 350.113 223.001 350.334 223.001H353.667C353.888 223.001 354.1 223.089 354.257 223.245C354.413 223.402 354.501 223.614 354.501 223.835V226.335M347.001 209.667H357C357.921 209.667 358.667 210.413 358.667 211.334V224.668C358.667 225.589 357.921 226.335 357 226.335H347.001C346.081 226.335 345.335 225.589 345.335 224.668V211.334C345.335 210.413 346.081 209.667 347.001 209.667Z"
        fill="none"
        stroke-width="1.73495"
        stroke-linecap="round"
      />
      <text class="control-graphic__label" x="352" y="262" text-anchor="middle">NETBANKING</text>
      <g transform="translate(307 270)">
        <g class="control-graphic__badge">
          <rect width="89" height="19" rx="2" fill="#097495" fill-opacity="0.12549" />
          <text x="44.5" y="13" text-anchor="middle">OPTIMIZED ROUTE</text>
        </g>
      </g>
    </g>

    <!-- UPI -->
    <g class="control-graphic__mode" :class="{ 'is-active': isActive('upi') }">
      <rect x="14" y="190" width="56" height="56" rx="28" fill="white" />
      <rect
        class="control-graphic__ring"
        x="14.8675"
        y="190.867"
        width="54.2651"
        height="54.2651"
        rx="27.1325"
        fill="none"
      />
      <g clip-path="url(#controlUpiClip)">
        <path
          class="control-graphic__icon"
          d="M44.0766 221.858C43.8928 221.904 43.6989 221.886 43.5268 221.807C41.212 220.671 39.3387 218.8 38.1997 216.487C38.1154 216.314 38.0935 216.117 38.1379 215.929C38.1822 215.742 38.2901 215.576 38.4431 215.459L38.8331 215.166C39.0401 215.011 39.2081 214.81 39.3238 214.578C39.4396 214.347 39.4998 214.092 39.4998 213.833V211.333C39.4998 210.891 39.3242 210.467 39.0116 210.154C38.699 209.842 38.2751 209.666 37.833 209.666H35.3328C34.8908 209.666 34.4668 209.842 34.1542 210.154C33.8416 210.467 33.666 210.891 33.666 211.333C33.666 215.311 35.2465 219.127 38.0598 221.94C40.873 224.754 44.6886 226.334 48.6672 226.334C49.1093 226.334 49.5332 226.158 49.8458 225.846C50.1584 225.533 50.334 225.109 50.334 224.667V222.167C50.334 221.725 50.1584 221.301 49.8458 220.988C49.5332 220.676 49.1093 220.5 48.6672 220.5H46.167C45.9083 220.5 45.653 220.56 45.4216 220.676C45.1902 220.792 44.9888 220.96 44.8336 221.167L44.5377 221.554C44.423 221.705 44.2603 221.812 44.0766 221.858Z"
          fill="none"
          stroke-width="2"
          stroke-linecap="round"
        />
      </g>
      <text class="control-graphic__label" x="42" y="262" text-anchor="middle">UPI</text>
      <g transform="translate(-3 270)">
        <g class="control-graphic__badge">
          <rect width="89" height="19" rx="2" fill="#097495" fill-opacity="0.12549" />
          <text x="44.5" y="13" text-anchor="middle">OPTIMIZED ROUTE</text>
        </g>
      </g>
    </g>

    <defs>
      <filter
        id="controlHubShadow"
        x="149.8"
        y="92.1713"
        width="95.4545"
        height="95.4545"
        filterUnits="userSpaceOnUse"
        color-interpolation-filters="sRGB"
      >
        <feFlood flood-opacity="0" result="BackgroundImageFix" />
        <feColorMatrix
          in="SourceAlpha"
          type="matrix"
          values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
          result="hardAlpha"
        />
        <feOffset dy="5.09091" />
        <feGaussianBlur stdDeviation="6.36364" />
        <feComposite in2="hardAlpha" operator="out" />
        <feColorMatrix
          type="matrix"
          values="0 0 0 0 0.0392157 0 0 0 0 0.0666667 0 0 0 0 0.156863 0 0 0 0.25098 0"
        />
        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow" />
        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow" result="shape" />
      </filter>
      <clipPath id="controlUpiClip">
        <rect width="20" height="20" fill="white" transform="translate(32 208)" />
      </clipPath>
    </defs>
  </svg>
</template>

<style scoped>
.control-graphic {
  display: block;
  width: 396px;
  max-width: 100%;
  height: auto;
  overflow: visible;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.control-graphic__orbits {
  pointer-events: none;
}

.control-graphic__orbit {
  transform-box: fill-box;
  transform-origin: center;
  animation: control-orbit-ripple 2.8s ease-in-out infinite;
}

.control-graphic__orbit--1 {
  stroke-opacity: 0.14;
  animation-delay: 0s;
}

.control-graphic__orbit--2 {
  stroke-opacity: 0.11;
  animation-delay: 0.35s;
}

.control-graphic__orbit--3 {
  stroke-opacity: 0.07;
  animation-delay: 0.7s;
}

.control-graphic__path {
  fill: none;
  stroke: #d5d7da;
  stroke-width: 1.2;
  stroke-dasharray: 3.4 10;
  stroke-linecap: round;
  transition: stroke 0.35s ease;
}

.control-graphic__path.is-active {
  stroke: #097495;
  stroke-width: 1.6;
  stroke-dasharray: 3.4 10;
  animation: control-dots 1s linear infinite;
}

.control-graphic__ring {
  stroke: #d5d7da;
  stroke-opacity: 0.8;
  stroke-width: 1.73495;
  transition:
    stroke 0.35s ease,
    stroke-width 0.35s ease,
    stroke-opacity 0.35s ease;
}

.control-graphic__icon {
  stroke: #344054;
  transition: stroke 0.35s ease;
}

.control-graphic__label {
  fill: #535862;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.2px;
  transition: fill 0.35s ease;
}

.control-graphic__mode.is-active .control-graphic__ring {
  stroke: #097495;
  stroke-opacity: 0.8;
  stroke-width: 2;
}

.control-graphic__mode.is-active .control-graphic__icon {
  stroke: #097495;
}

.control-graphic__mode.is-active .control-graphic__label {
  fill: #097495;
}

.control-graphic__badge {
  opacity: 0;
  transform: scale(0.72);
  transform-box: fill-box;
  transform-origin: center;
  pointer-events: none;
}

.control-graphic__mode.is-active .control-graphic__badge {
  animation: control-badge-pop 0.4s cubic-bezier(0.22, 1.4, 0.36, 1) forwards;
}

.control-graphic__badge text {
  fill: #0292b8;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.2857px;
}

@keyframes control-orbit-ripple {
  0%,
  100% {
    transform: scale(0.96);
    stroke-opacity: 0.05;
  }

  40% {
    transform: scale(1.04);
    stroke-opacity: 0.28;
  }

  70% {
    transform: scale(1.08);
    stroke-opacity: 0.1;
  }
}

@keyframes control-dots {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes control-badge-pop {
  0% {
    opacity: 0;
    transform: scale(0.72);
  }

  70% {
    opacity: 1;
    transform: scale(1.06);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .control-graphic__orbit {
    animation: none;
  }

  .control-graphic__orbit--1 {
    stroke-opacity: 0.12;
  }

  .control-graphic__orbit--2 {
    stroke-opacity: 0.12;
  }

  .control-graphic__orbit--3 {
    stroke-opacity: 0.06;
  }

  .control-graphic__path.is-active {
    animation: none;
    stroke-dasharray: 3.4 10;
  }

  .control-graphic__mode.is-active .control-graphic__badge {
    animation: none;
    opacity: 1;
    transform: scale(1);
  }
}
</style>
