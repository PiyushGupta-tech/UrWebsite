<script setup>
import { onMounted, ref } from "vue";

defineProps({
  alt: {
    type: String,
    default: "Payout tracking stepper and recent payouts table with live statuses",
  },
});

/**
 * Figma 818:2820 — Payment Stepper Animation (6.5s loop).
 * Progress bar advances phase → phase, then Payout Completed toast pops.
 */
const ASSET = "/images/figma-payouts/control/stepper";

const ROWS = [
  {
    initials: "AS",
    avatarBg: "#eef2ff",
    avatarColor: "#4f46e5",
    name: "Acme Supplies",
    amount: "₹25,000",
    channel: "Bank Transfer",
    status: "Success",
    statusTone: "success",
    when: "Apr 28, 10:03 AM",
  },
  {
    initials: "BL",
    avatarBg: "#ecfdf5",
    avatarColor: "#059669",
    name: "Bright Logistics",
    amount: "₹10,000",
    channel: "UPI",
    status: "Processing",
    statusTone: "processing",
    when: "Apr 28, 09:45 AM",
  },
  {
    initials: "GT",
    avatarBg: "#fffbeb",
    avatarColor: "#d97706",
    name: "Global Traders",
    amount: "₹50,000",
    channel: "IMPS",
    status: "Scheduled",
    statusTone: "scheduled",
    when: "Apr 28, 11:30 AM",
  },
  {
    initials: "SP",
    avatarBg: "#fdf2f8",
    avatarColor: "#db2777",
    name: "Swift Partners",
    amount: "₹5,000",
    channel: "Wallet",
    status: "Failed",
    statusTone: "failed",
    when: "Apr 28, 09:12 AM",
  },
];

const reduceMotion = ref(false);

onMounted(() => {
  reduceMotion.value =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
});
</script>

<template>
  <div
    class="po-trk"
    :class="{ 'po-trk--static': reduceMotion }"
    role="img"
    :aria-label="alt"
  >
    <!-- Lifecycle tracker -->
    <div class="po-trk__tracker" aria-hidden="true">
      <div class="po-trk__steps">
        <div class="po-trk__line-bg" />
        <div class="po-trk__line po-trk__line--active" />
        <div class="po-trk__line po-trk__line--success" />

        <!-- Initiated — always on -->
        <div class="po-trk__step po-trk__step--initiated">
          <div class="po-trk__icon po-trk__icon--active">
            <img :src="`${ASSET}/send.svg`" alt="" width="15" height="15" />
          </div>
          <div class="po-trk__labels">
            <strong>Initiated</strong>
            <span>10:00 AM</span>
          </div>
        </div>

        <!-- Processing -->
        <div class="po-trk__step po-trk__step--processing po-trk__anim po-trk__anim--processing">
          <div class="po-trk__icon-wrap">
            <div class="po-trk__icon">
              <img :src="`${ASSET}/settings.svg`" alt="" width="15" height="15" />
            </div>
            <svg
              class="po-trk__sweep po-trk__anim po-trk__anim--sweep1"
              viewBox="0 0 36.656 36.656"
              fill="none"
              aria-hidden="true"
            >
              <path
                class="po-trk__sweep-path"
                pathLength="1"
                d="M18.3278 0C28.45 0 36.6556 8.20564 36.6556 18.3278C36.6556 28.45 28.45 36.6556 18.3278 36.6556C8.20564 36.6556 0 28.45 0 18.3278C0 8.20564 8.20564 0 18.4278 0.1"
                stroke="#097495"
                stroke-width="2"
              />
            </svg>
          </div>
          <div class="po-trk__labels">
            <strong>Processing</strong>
            <span>10:01 AM</span>
          </div>
        </div>

        <!-- Sent to Bank -->
        <div class="po-trk__step po-trk__step--sent po-trk__anim po-trk__anim--sent">
          <div class="po-trk__icon-wrap">
            <div class="po-trk__icon">
              <img :src="`${ASSET}/home.svg`" alt="" width="15" height="15" />
            </div>
            <svg
              class="po-trk__sweep po-trk__anim po-trk__anim--sweep2"
              viewBox="0 0 36.656 36.656"
              fill="none"
              aria-hidden="true"
            >
              <path
                class="po-trk__sweep-path"
                pathLength="1"
                d="M18.3278 0C28.45 0 36.6556 8.20564 36.6556 18.3278C36.6556 28.45 28.45 36.6556 18.3278 36.6556C8.20564 36.6556 0 28.45 0 18.3278C0 8.20564 8.20564 0 18.4278 0.1"
                stroke="#097495"
                stroke-width="2"
              />
            </svg>
          </div>
          <div class="po-trk__labels">
            <strong>Sent to Bank</strong>
            <span>10:02 AM</span>
          </div>
        </div>

        <!-- Successful -->
        <div class="po-trk__step po-trk__step--success po-trk__anim po-trk__anim--success">
          <div class="po-trk__vline" />
          <div class="po-trk__icon po-trk__icon--success">
            <img :src="`${ASSET}/check.svg`" alt="" width="20" height="20" />
          </div>
          <div class="po-trk__labels">
            <strong class="po-trk__labels-strong">Successful</strong>
            <span>10:03 AM</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Payouts card -->
    <div class="po-trk__card">
      <div class="po-trk__card-head">
        <p class="po-trk__card-title">Recent Payouts</p>
        <div class="po-trk__view-all">
          <span>View All</span>
          <img :src="`${ASSET}/arrow-right.svg`" alt="" width="10" height="10" />
        </div>
      </div>

      <div class="po-trk__table">
        <div class="po-trk__thead">
          <span class="po-trk__col po-trk__col--ben">Beneficiary</span>
          <span class="po-trk__col po-trk__col--amt">Amount</span>
          <span class="po-trk__col po-trk__col--ch">Channel</span>
          <span class="po-trk__col po-trk__col--st">Status</span>
          <span class="po-trk__col po-trk__col--dt">Date &amp; Time</span>
        </div>
        <div class="po-trk__rule" />
        <div
          v-for="(row, i) in ROWS"
          :key="row.name"
          class="po-trk__row-wrap"
        >
          <div class="po-trk__row">
            <div class="po-trk__col po-trk__col--ben po-trk__ben">
              <span
                class="po-trk__avatar"
                :style="{ background: row.avatarBg, color: row.avatarColor }"
              >{{ row.initials }}</span>
              <span class="po-trk__name">{{ row.name }}</span>
            </div>
            <span class="po-trk__col po-trk__col--amt po-trk__amt">{{ row.amount }}</span>
            <span class="po-trk__col po-trk__col--ch po-trk__muted">{{ row.channel }}</span>
            <div class="po-trk__col po-trk__col--st">
              <span
                class="po-trk__badge"
                :class="`po-trk__badge--${row.statusTone}`"
              >{{ row.status }}</span>
            </div>
            <span class="po-trk__col po-trk__col--dt po-trk__muted po-trk__dt">{{ row.when }}</span>
          </div>
          <div v-if="i < ROWS.length - 1" class="po-trk__rule" />
        </div>
      </div>
    </div>

    <!-- Payout Completed toast -->
    <div class="po-trk__toast po-trk__anim po-trk__anim--toast" aria-hidden="true">
      <div class="po-trk__toast-card">
        <div class="po-trk__toast-icon">
          <img :src="`${ASSET}/check-toast.svg`" alt="" width="14" height="14" />
        </div>
        <div class="po-trk__toast-copy">
          <strong>Payout Completed</strong>
          <span>₹25,000 sent to Acme Supplies</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.po-trk {
  --po-trk-ink: #252b37;
  --po-trk-muted: #535862;
  --po-trk-brand: #097495;
  --po-trk-success: #10b981;
  position: relative;
  width: 100%;
  max-width: 704px;
  aspect-ratio: 704 / 413;
  container-type: inline-size;
  font-family: Manrope, "DM Sans", system-ui, sans-serif;
  overflow: visible;
}

.po-trk__tracker {
  position: absolute;
  left: 0;
  top: calc(28 / 413 * 100%);
  width: 100%;
  padding: clamp(6px, 1.5cqi, 11px) 0;
  box-sizing: border-box;
}

.po-trk__steps {
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  min-height: calc(80 / 413 * 100cqh);
}

.po-trk__line-bg {
  position: absolute;
  left: calc(40.73 / 704 * 100%);
  top: calc(36.656 / 704 * 50cqi - 1.35px);
  width: calc(502.318 / 704 * 100%);
  height: 2.715px;
  border-radius: 2px;
  background: #e2e8f0;
}

.po-trk__line {
  position: absolute;
  top: calc(36.656 / 704 * 50cqi - 1.5px);
  height: 3px;
  border-radius: 2px;
  z-index: 1;
  pointer-events: none;
}

.po-trk__line--active {
  left: calc(41 / 704 * 100%);
  width: 0.01px;
  background: var(--po-trk-brand);
  animation: po-trk-line-active 6.5s linear infinite;
}

.po-trk__line--success {
  left: calc(380 / 704 * 100%);
  width: 0.01px;
  background: var(--po-trk-success);
  animation: po-trk-line-success 6.5s linear infinite;
}

.po-trk__step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(4px, 1.2cqi, 8px);
  width: calc(81.457 / 704 * 100%);
  flex-shrink: 0;
}

.po-trk__step--sent {
  width: calc(84 / 704 * 100%);
}

.po-trk__icon-wrap {
  position: relative;
  width: clamp(28px, 5.2cqi, 36.656px);
  aspect-ratio: 1;
}

.po-trk__icon {
  width: clamp(28px, 5.2cqi, 36.656px);
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #fff;
  border: 0.5px solid #d1d6de;
  box-sizing: border-box;
  overflow: visible;
}

.po-trk__icon--active {
  border-color: var(--po-trk-brand);
}

.po-trk__icon--success {
  border: none;
  background: var(--po-trk-success);
}

.po-trk__icon img {
  display: block;
  width: clamp(12px, 2.1cqi, 15px);
  height: clamp(12px, 2.1cqi, 15px);
  object-fit: contain;
  flex-shrink: 0;
}

.po-trk__icon--success img {
  width: clamp(14px, 2.8cqi, 20px);
  height: clamp(14px, 2.8cqi, 20px);
}

.po-trk__sweep {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.po-trk__sweep-path {
  fill: none;
  stroke-dasharray: 0 1;
  visibility: hidden;
}

.po-trk__labels {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  text-align: center;
  white-space: nowrap;
}

.po-trk__labels strong,
.po-trk__labels-strong {
  font-size: clamp(10px, 2cqi, 14px);
  font-weight: 700;
  color: var(--po-trk-ink);
  line-height: 1.2;
}

.po-trk__step--success .po-trk__labels-strong {
  font-weight: 800;
}

.po-trk__labels span {
  font-size: clamp(8px, 1.4cqi, 10px);
  font-weight: 400;
  color: var(--po-trk-muted);
  line-height: 1.2;
}

.po-trk__vline {
  position: absolute;
  left: 50%;
  top: 0;
  width: 2.715px;
  height: clamp(16px, 4.2cqi, 29.87px);
  background: var(--po-trk-success);
  transform: translate(-50%, -100%);
  border-radius: 1px;
}

.po-trk__step--processing .po-trk__icon,
.po-trk__step--sent .po-trk__icon {
  border-color: var(--po-trk-brand);
}

/* Recent payouts card */
.po-trk__card {
  position: absolute;
  left: 0;
  top: calc(128 / 413 * 100%);
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 2.5cqi, 17.5px);
  padding: clamp(12px, 3.3cqi, 23.37px);
  border-radius: clamp(8px, 1.7cqi, 11.685px);
  background: #fff;
  border: 0.873px solid #ebebeb;
  box-shadow:
    0 0.73px 0.73px rgba(0, 0, 0, 0.1),
    0 0.73px 1.095px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.po-trk__card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.po-trk__card-title {
  margin: 0;
  font-size: clamp(10px, 1.7cqi, 12px);
  font-weight: 800;
  color: #0b192c;
  white-space: nowrap;
}

.po-trk__view-all {
  display: flex;
  align-items: center;
  gap: 2px;
  color: var(--po-trk-brand);
  font-family: Inter, Manrope, sans-serif;
  font-size: clamp(8px, 1.45cqi, 10.225px);
  font-weight: 700;
  white-space: nowrap;
}

.po-trk__view-all img {
  display: block;
  width: clamp(8px, 1.45cqi, 10.225px);
  height: auto;
}

.po-trk__table {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
}

.po-trk__thead,
.po-trk__row {
  display: flex;
  align-items: center;
  width: 100%;
  min-width: 0;
}

.po-trk__thead {
  padding-bottom: clamp(4px, 1.2cqi, 8.764px);
  font-weight: 600;
  color: var(--po-trk-muted);
  font-size: clamp(8px, 1.4cqi, 10px);
}

.po-trk__thead .po-trk__col--st {
  font-family: Inter, Manrope, sans-serif;
  color: #50667a;
  font-size: clamp(8px, 1.35cqi, 9.494px);
}

.po-trk__row {
  padding: clamp(4px, 1.2cqi, 8.764px) 0;
}

.po-trk__col--ben {
  flex: 1 1 0;
  min-width: 0;
}

.po-trk__col--amt {
  width: calc(87.639 / 657 * 100%);
  flex-shrink: 0;
}

.po-trk__col--ch {
  width: calc(109.549 / 657 * 100%);
  flex-shrink: 0;
}

.po-trk__col--st {
  width: calc(102.245 / 657 * 100%);
  flex-shrink: 0;
}

.po-trk__col--dt {
  width: calc(116.852 / 657 * 100%);
  flex-shrink: 0;
  text-align: right;
}

.po-trk__ben {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1.2cqi, 8.764px);
  min-width: 0;
}

.po-trk__avatar {
  width: clamp(16px, 3.3cqi, 23.37px);
  aspect-ratio: 1;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-family: Inter, Manrope, sans-serif;
  font-size: clamp(7px, 1.25cqi, 8.764px);
  font-weight: 700;
  flex-shrink: 0;
}

.po-trk__name,
.po-trk__amt {
  font-size: clamp(9px, 1.7cqi, 12px);
  font-weight: 600;
  color: #0b192c;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.po-trk__muted {
  font-size: clamp(8px, 1.4cqi, 10px);
  font-weight: 400;
  color: var(--po-trk-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.po-trk__badge {
  display: inline-flex;
  padding: clamp(2px, 0.4cqi, 2.921px) clamp(6px, 1.2cqi, 8.764px);
  border-radius: 999px;
  border: 0.73px solid;
  font-size: clamp(7px, 1.1cqi, 8px);
  font-weight: 600;
  white-space: nowrap;
  box-sizing: border-box;
}

.po-trk__badge--success {
  background: #ecfdf5;
  border-color: #10b981;
  color: #10b981;
}

.po-trk__badge--processing {
  background: #eff6ff;
  border-color: #bfdbfe;
  color: #3b82f6;
}

.po-trk__badge--scheduled {
  background: #f5f3ff;
  border-color: #ddd6fe;
  color: #8b5cf6;
}

.po-trk__badge--failed {
  background: #fef2f2;
  border-color: #fecaca;
  color: #ef4444;
}

.po-trk__rule {
  width: 100%;
  height: 0;
  border-top: 0.73px solid #e5e7eb;
}

/* Toast */
.po-trk__toast {
  position: absolute;
  left: calc(477 / 704 * 100%);
  top: 0;
  width: calc(209 / 704 * 100%);
  z-index: 5;
}

.po-trk__toast-card {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.6cqi, 11px);
  padding: clamp(8px, 1.7cqi, 12px);
  border-radius: clamp(8px, 1.6cqi, 11px);
  background: #fff;
  border: 0.69px solid var(--po-trk-success);
  box-sizing: border-box;
}

.po-trk__toast-icon {
  width: clamp(20px, 3.9cqi, 27.581px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.1);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.po-trk__toast-icon img {
  width: 50%;
  height: auto;
  display: block;
}

.po-trk__toast-copy {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.po-trk__toast-copy strong {
  font-size: clamp(11px, 2cqi, 14px);
  font-weight: 700;
  color: var(--po-trk-ink);
  white-space: nowrap;
}

.po-trk__toast-copy span {
  font-size: clamp(8px, 1.4cqi, 10px);
  font-weight: 400;
  color: var(--po-trk-muted);
  white-space: nowrap;
}

/* —— 6.5s Figma loop (818:2820) —— */
.po-trk__anim {
  animation-duration: 6.5s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.po-trk__anim--processing {
  animation-name: po-trk-processing;
}

.po-trk__anim--sent {
  animation-name: po-trk-sent;
}

.po-trk__anim--success {
  animation-name: po-trk-success;
  transform-origin: center top;
}

.po-trk__anim--toast {
  animation-name: po-trk-toast;
  will-change: transform, opacity;
}

.po-trk__anim--sweep1 .po-trk__sweep-path {
  animation: po-trk-sweep1 6.5s linear infinite;
}

.po-trk__anim--sweep2 .po-trk__sweep-path {
  animation: po-trk-sweep2 6.5s linear infinite;
}

.po-trk__anim--sweep1 {
  animation-name: po-trk-sweep-fade1;
}

.po-trk__anim--sweep2 {
  animation-name: po-trk-sweep-fade2;
}

@keyframes po-trk-line-active {
  0% {
    width: 0.01px;
    animation-timing-function: ease-in-out;
  }
  9.231% {
    width: calc(188 / 704 * 100%);
  }
  20% {
    width: calc(188 / 704 * 100%);
    animation-timing-function: ease-in-out;
  }
  29.231%,
  100% {
    width: calc(339 / 704 * 100%);
  }
}

@keyframes po-trk-line-success {
  0%,
  40% {
    width: 0.01px;
    animation-timing-function: ease-in-out;
  }
  49.231%,
  100% {
    width: calc(267 / 704 * 100%);
  }
}

@keyframes po-trk-processing {
  0%,
  9.231% {
    opacity: 0;
    animation-timing-function: ease-out;
  }
  11.538%,
  76.923% {
    opacity: 1;
    animation-timing-function: ease-in-out;
  }
  84.615%,
  100% {
    opacity: 0;
  }
}

@keyframes po-trk-sent {
  0%,
  29.231% {
    opacity: 0;
    animation-timing-function: ease-out;
  }
  31.538%,
  76.923% {
    opacity: 1;
    animation-timing-function: ease-in-out;
  }
  84.615%,
  100% {
    opacity: 0;
  }
}

@keyframes po-trk-success {
  0%,
  49.231% {
    opacity: 0;
    transform: scale(0.5);
    animation-timing-function: ease-out;
  }
  53.846%,
  76.923% {
    opacity: 1;
    transform: scale(1);
    animation-timing-function: ease-in-out;
  }
  84.615%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

@keyframes po-trk-toast {
  0%,
  53.846% {
    opacity: 0;
    transform: translateY(-12px);
    animation-timing-function: ease-out;
  }
  60%,
  76.923% {
    opacity: 1;
    transform: translateY(0);
    animation-timing-function: ease-in-out;
  }
  84.615%,
  100% {
    opacity: 0;
    transform: translateY(0);
  }
}

@keyframes po-trk-sweep-fade1 {
  0%,
  10.769% {
    opacity: 0;
  }
  11.538%,
  100% {
    opacity: 1;
  }
}

@keyframes po-trk-sweep-fade2 {
  0%,
  30.769% {
    opacity: 0;
  }
  31.538%,
  100% {
    opacity: 1;
  }
}

@keyframes po-trk-sweep1 {
  0%,
  10.769% {
    stroke-dasharray: 0 1;
    visibility: hidden;
    animation-timing-function: ease-in-out;
  }
  20%,
  100% {
    stroke-dasharray: 1 1;
    visibility: visible;
  }
}

@keyframes po-trk-sweep2 {
  0%,
  30.769% {
    stroke-dasharray: 0 1;
    visibility: hidden;
    animation-timing-function: ease-in-out;
  }
  40%,
  100% {
    stroke-dasharray: 1 1;
    visibility: visible;
  }
}

.po-trk--static .po-trk__anim,
.po-trk--static .po-trk__line--active,
.po-trk--static .po-trk__line--success {
  animation: none;
}

.po-trk--static .po-trk__step--processing,
.po-trk--static .po-trk__step--sent,
.po-trk--static .po-trk__step--success,
.po-trk--static .po-trk__toast {
  opacity: 1;
  transform: none;
}

.po-trk--static .po-trk__line--active {
  width: calc(339 / 704 * 100%);
}

.po-trk--static .po-trk__line--success {
  width: calc(267 / 704 * 100%);
}

.po-trk--static .po-trk__sweep-path {
  stroke-dasharray: 1 1;
  visibility: visible;
}

.po-trk--static .po-trk__toast {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .po-trk__anim,
  .po-trk__line--active,
  .po-trk__line--success {
    animation: none;
  }

  .po-trk__step--processing,
  .po-trk__step--sent,
  .po-trk__step--success {
    opacity: 1;
    transform: none;
  }

  .po-trk__line--active {
    width: calc(339 / 704 * 100%);
  }

  .po-trk__line--success {
    width: calc(267 / 704 * 100%);
  }

  .po-trk__sweep-path {
    stroke-dasharray: 1 1;
    visibility: visible;
  }

  .po-trk__toast {
    opacity: 0;
  }
}
</style>
