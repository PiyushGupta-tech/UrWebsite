<script setup>
import { useRateCycle } from "@/composables/useRateCycle.js";

/** Figma 283:9106 — Your Branding and Logo graphic */
const ASSET = "/images/figma-custom-checkout/showcase";

const { rateLabel, rateOpacity, chartOffset, chartOpacity } = useRateCycle(72.6);
</script>

<template>
  <div class="cfb">
    <div class="cfb__screen">
      <div class="cfb__grid" />
      <svg class="cfb__waves" viewBox="0 0 400 180" preserveAspectRatio="none">
        <path
          class="cfb__wave cfb__wave--a"
          d="M0 90 C40 60, 80 120, 120 85 S200 40, 240 70 S320 130, 400 80"
          fill="none"
          stroke="rgba(255,255,255,0.35)"
          stroke-width="1.5"
        />
        <path
          class="cfb__wave cfb__wave--b"
          d="M0 110 C50 80, 90 140, 140 100 S220 55, 280 90 S340 140, 400 100"
          fill="none"
          stroke="rgba(255,255,255,0.22)"
          stroke-width="1.25"
        />
      </svg>
      <div class="cfb__pulse">
        <span /><span /><span /><span />
      </div>
    </div>

    <article class="cfb__flow">
      <p class="cfb__flow-title">Checkout Flow</p>
      <div class="cfb__steps">
        <div class="cfb__step">
          <span class="cfb__step-dot"><img :src="`${ASSET}/check.svg`" alt="" width="10" height="10" /></span>
          <span>Cart</span>
        </div>
        <span class="cfb__step-line" />
        <div class="cfb__step">
          <span class="cfb__step-dot"><img :src="`${ASSET}/check.svg`" alt="" width="10" height="10" /></span>
          <span>Details</span>
        </div>
        <span class="cfb__step-line" />
        <div class="cfb__step cfb__step--active">
          <span class="cfb__step-dot"><img :src="`${ASSET}/check.svg`" alt="" width="10" height="10" /></span>
          <span>Payment</span>
        </div>
        <span class="cfb__step-line" />
        <div class="cfb__step">
          <span class="cfb__step-dot">
            <img :src="`${ASSET}/check.svg`" alt="" width="10" height="10" />
          </span>
          <span>Success</span>
        </div>
      </div>
      <div class="cfb__rate">
        <div class="cfb__rate-copy">
          <p>Conversion Rate</p>
          <p
            class="cfb__rate-value"
            :style="{ opacity: rateOpacity }"
          >
            {{ rateLabel }}
          </p>
        </div>
        <!-- Figma Vector_12 from 283:9106 trending-up chart -->
        <svg
          class="cfb__chart"
          viewBox="40 285 204 64"
          preserveAspectRatio="xMidYMid meet"
          aria-hidden="true"
        >
          <path
            class="cfb__chart-path"
            pathLength="1"
            d="M41.8892 347.162L45.8082 340.976C50.6842 333.28 60.7563 330.79 68.6568 335.327C75.9112 339.492 85.1174 337.768 90.3719 331.258L95.4278 324.995C100.706 318.457 110.718 318.604 115.801 325.295C121.727 333.095 133.834 331.738 137.886 322.82L139.219 319.888C144.499 308.269 161.002 308.269 166.282 319.888L167.423 322.399C171.948 332.357 184.866 335.011 192.95 327.644L216.306 306.361L241.772 286.818H222.806L241.772 286.818V305.232"
            fill="none"
            stroke="#097495"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            :style="{
              strokeDasharray: 1,
              strokeDashoffset: chartOffset,
              opacity: chartOpacity,
            }"
          />
        </svg>
      </div>
    </article>

    <div class="cfb__phone">
      <span class="cfb__phone-speaker" />
      <span class="cfb__phone-menu" />
      <p class="cfb__phone-brand">Your Brand</p>
      <div class="cfb__phone-summary">
        <p class="cfb__phone-label">Order Summary</p>
        <div class="cfb__phone-row">
          <span>Premium Plan</span>
          <span>$99.00</span>
        </div>
      </div>
      <div class="cfb__phone-cta">Pay Now</div>
      <p class="cfb__phone-foot">Smart Checkout</p>
    </div>
  </div>
</template>

<style scoped>
.cfb {
  position: relative;
  width: 100%;
  aspect-ratio: 637 / 349;
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
}

.cfb__screen {
  position: absolute;
  left: 29.77%;
  right: 10%;
  top: 16.04%;
  bottom: 6.74%;
  overflow: hidden;
  border-radius: 14px;
  background: linear-gradient(180deg, #0292b8 0%, #134e66 100%);
}

.cfb__grid {
  position: absolute;
  inset: -20%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 28px 28px;
  opacity: 0.7;
}

.cfb__waves {
  position: absolute;
  inset: 10% 0 20%;
  width: 100%;
  height: 70%;
}

.cfb__wave {
  stroke-dasharray: 3.4 10;
  animation: cfb-dash 1.4s linear infinite;
}

.cfb__wave--b {
  animation-duration: 1.8s;
  animation-direction: reverse;
}

.cfb__pulse {
  position: absolute;
  left: 48%;
  top: 68%;
  width: 28px;
  height: 28px;
}

.cfb__pulse span {
  position: absolute;
  inset: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.45);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: cfb-ring 2.8s ease-out infinite;
}

.cfb__pulse span:nth-child(1) {
  width: 28px;
  height: 28px;
  background: radial-gradient(
    circle,
    rgba(220, 245, 255, 0.95) 0%,
    rgba(180, 230, 255, 0.55) 45%,
    rgba(180, 230, 255, 0) 72%
  );
  border: none;
  animation: none;
  filter: blur(6px);
  box-shadow: 0 0 18px 6px rgba(180, 230, 255, 0.35);
}

.cfb__pulse span:nth-child(2) {
  animation-delay: 0.4s;
}
.cfb__pulse span:nth-child(3) {
  animation-delay: 0.9s;
}
.cfb__pulse span:nth-child(4) {
  animation-delay: 1.4s;
}

.cfb__flow {
  position: absolute;
  left: 0;
  top: 42.1%;
  width: 40.8%;
  padding: 14px;
  box-sizing: border-box;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #ffffff;
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.02),
    0 8px 12px rgba(0, 0, 0, 0.05);
  animation: cfb-float 5s ease-in-out infinite;
}

.cfb__flow-title {
  margin: 0 0 10px;
  font-size: clamp(8px, 1.35vw, 11px);
  font-weight: 600;
  color: #252b37;
}

.cfb__steps {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 2px;
  margin-bottom: 12px;
}

.cfb__step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  font-size: clamp(6px, 1.1vw, 8px);
  font-weight: 600;
  color: #6b7280;
}

.cfb__step--active {
  color: #097495;
}

.cfb__step-dot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #f8f9fc;
  border: 1px solid #e5e7eb;
}

.cfb__step-dot img {
  width: 9px;
  height: 9px;
  filter: brightness(0) saturate(100%) invert(45%) sepia(8%) saturate(500%);
}

.cfb__step--active .cfb__step-dot {
  background: #097495;
  border-color: transparent;
}

.cfb__step--active .cfb__step-dot img {
  filter: brightness(0) invert(1);
}

.cfb__step-line {
  flex: 1;
  height: 0;
  margin-top: 9px;
  border-top: 1px dashed #d1d5db;
  min-width: 8px;
}

.cfb__rate {
  position: relative;
  padding: 10px;
  border-radius: 6px;
  background: #f7f8fb;
  overflow: hidden;
}

.cfb__rate-copy p {
  margin: 0;
  font-size: clamp(7px, 1.2vw, 9px);
  font-weight: 600;
  color: #252b37;
}

.cfb__rate-value {
  margin-top: 4px !important;
  font-size: clamp(14px, 2.4vw, 18px) !important;
  font-variant-numeric: tabular-nums;
  transition: none;
}

.cfb__chart {
  position: absolute;
  right: 6px;
  bottom: 4px;
  width: 58%;
  height: 48px;
  overflow: visible;
}

.cfb__phone {
  position: absolute;
  right: 0;
  top: 0;
  width: 28.25%;
  height: 91.7%;
  padding: 10px 8px;
  box-sizing: border-box;
  border: 3px solid #d1d5db;
  border-radius: 24px;
  background: #ffffff;
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.02),
    0 8px 12px rgba(0, 0, 0, 0.05);
  animation: cfb-float 5.5s ease-in-out infinite reverse;
}

.cfb__phone-speaker {
  display: block;
  width: 40px;
  height: 4px;
  margin: 0 auto 8px;
  border-radius: 2px;
  background: #d1d5db;
}

.cfb__phone-menu {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 12px;
  height: 10px;
  background:
    linear-gradient(#6b7280, #6b7280) 0 0 / 100% 2px no-repeat,
    linear-gradient(#6b7280, #6b7280) 0 4px / 100% 2px no-repeat,
    linear-gradient(#6b7280, #6b7280) 0 8px / 100% 2px no-repeat;
}

.cfb__phone-brand {
  margin: 28px 0 12px;
  text-align: center;
  font-size: clamp(11px, 2vw, 15px);
  font-weight: 600;
  color: #252b37;
}

.cfb__phone-summary {
  padding: 8px;
  border-radius: 8px;
  background: #f7f8fb;
}

.cfb__phone-label {
  margin: 0 0 6px;
  font-size: clamp(7px, 1.2vw, 8px);
  font-weight: 600;
  color: #6b7280;
}

.cfb__phone-row {
  display: flex;
  justify-content: space-between;
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 600;
  color: #252b37;
}

.cfb__phone-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 28px;
  margin: 14px 4px 0;
  border-radius: 6px;
  background: #097495;
  color: #ffffff;
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 700;
}

.cfb__phone-foot {
  margin: 18px 0 0;
  text-align: center;
  font-size: clamp(7px, 1.2vw, 8px);
  font-weight: 600;
  color: #252b37;
}

@keyframes cfb-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

@keyframes cfb-dash {
  to {
    stroke-dashoffset: -13.4;
  }
}

@keyframes cfb-ring {
  0% {
    width: 28px;
    height: 28px;
    opacity: 0.7;
  }
  100% {
    width: 220px;
    height: 220px;
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cfb__flow,
  .cfb__phone,
  .cfb__wave,
  .cfb__pulse span {
    animation: none;
  }
}
</style>
