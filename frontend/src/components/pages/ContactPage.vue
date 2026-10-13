<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { submitContactForm } from "@/api/client.js";
import { trackEvent } from "@/utils/analytics.js";
import { contactFieldSchemas, contactSchema } from "@/validation/contactSchema.js";

defineProps({
  page: { type: Object, required: true },
  relatedLinks: { type: Array, default: () => [] },
});

const router = useRouter();

const form = ref({
  name: "",
  email: "",
  phone: "",
  subject: "",
  message: "",
});

/* Bump ?v= when the PDF is replaced: /downloads/ is served with a 1-year immutable cache. */
const CATALOGUE_HREF = "/downloads/urbanrupee-product-catalogue.pdf?v=2";

const submitted = ref(false);
const submitting = ref(false);
const successHeading = ref(null);
const error = ref("");
const fieldErrors = ref({
  name: "",
  email: "",
  phone: "",
  subject: "",
  message: "",
});
const touched = ref({
  name: false,
  email: false,
  phone: false,
  subject: false,
  message: false,
});
const CONTROL_INPUT_TYPES = new Set([
  "deleteContentBackward",
  "deleteContentForward",
  "deleteByCut",
  "deleteByDrag",
  "historyUndo",
  "historyRedo",
  "insertLineBreak",
  "insertParagraph",
]);

function sanitizeName(value) {
  return String(value || "").replace(/[^A-Za-z\s]/g, "");
}

function sanitizeEmail(value) {
  const cleaned = String(value || "")
    .replace(/\s+/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9@._+-]/g, "");

  const [local = "", ...rest] = cleaned.split("@");
  if (!rest.length) return local;

  const domain = rest.join("").replace(/@/g, "");
  return `${local}@${domain}`;
}

function sanitizePhone(value) {
  return String(value || "").replace(/\D/g, "").slice(0, 10);
}

function sanitizeMessage(value) {
  return String(value || "").slice(0, 500);
}

function setFieldError(field, message = "") {
  fieldErrors.value[field] = message;
}

function validateField(field) {
  const schema = contactFieldSchemas[field];
  if (!schema) return true;

  const { error: validationError } = schema.validate(form.value[field], { abortEarly: true });
  setFieldError(field, validationError?.details?.[0]?.message || "");
  return !validationError;
}

function validateForm() {
  const { error: validationError, value } = contactSchema.validate(form.value, {
    abortEarly: false,
  });

  form.value = { ...form.value, ...value };
  const nextErrors = {
    name: "",
    email: "",
    phone: "",
    subject: "",
    message: "",
  };

  validationError?.details?.forEach((detail) => {
    const field = detail.path?.[0];
    if (field && !nextErrors[field]) {
      nextErrors[field] = detail.message;
    }
  });

  fieldErrors.value = nextErrors;
  return !validationError;
}

function updateField(key, event, sanitizer = (value) => value) {
  form.value[key] = sanitizer(event?.target?.value);
  if (touched.value[key] || fieldErrors.value[key]) {
    validateField(key);
  }
}

function onFieldBlur(field) {
  touched.value[field] = true;
  validateField(field);
}

function onNameBeforeInput(event) {
  if (CONTROL_INPUT_TYPES.has(event.inputType)) return;
  if (!/^[A-Za-z\s]*$/.test(event.data || "")) {
    event.preventDefault();
  }
}

function onEmailBeforeInput(event) {
  if (CONTROL_INPUT_TYPES.has(event.inputType)) return;
  const data = event.data || "";
  if (!/^[A-Za-z0-9@._+-]*$/.test(data)) {
    event.preventDefault();
    return;
  }

  if (data.includes("@")) {
    const target = event.target;
    const existing = target?.value || "";
    const selected = existing.slice(target.selectionStart || 0, target.selectionEnd || 0);
    const nextAtCount = existing.split("@").length - 1 - (selected.includes("@") ? 1 : 0) + data.split("@").length - 1;
    if (nextAtCount > 1) {
      event.preventDefault();
    }
  }
}

function onPhoneBeforeInput(event) {
  if (CONTROL_INPUT_TYPES.has(event.inputType)) return;
  const data = event.data || "";
  if (!/^\d*$/.test(data)) {
    event.preventDefault();
    return;
  }

  const target = event.target;
  const existing = target?.value || "";
  const start = target?.selectionStart || 0;
  const end = target?.selectionEnd || 0;
  const nextValue = `${existing.slice(0, start)}${data}${existing.slice(end)}`;

  if (nextValue.length > 10) {
    event.preventDefault();
    return;
  }

  if (nextValue.length > 0 && !/^[6-9]/.test(nextValue)) {
    event.preventDefault();
  }
}

function handlePaste(field, event, sanitizer = (value) => value) {
  event.preventDefault();
  const pasted = event.clipboardData?.getData("text") || "";
  form.value[field] = sanitizer(pasted);
  touched.value[field] = true;
  validateField(field);
}

function handlePhonePaste(event) {
  event.preventDefault();
  const pasted = event.clipboardData?.getData("text") || "";
  const digitsOnly = sanitizePhone(pasted);
  form.value.phone = /^[6-9]/.test(digitsOnly) ? digitsOnly : "";
  touched.value.phone = true;
  validateField("phone");
}

const canSubmit = computed(() => {
  return contactSchema.validate(form.value, { abortEarly: false }).error == null;
});

async function onSubmit() {
  if (submitting.value) return;
  touched.value = {
    name: true,
    email: true,
    phone: true,
    subject: true,
    message: true,
  };
  if (!validateForm()) return;

  submitting.value = true;
  error.value = "";
  try {
    const { value } = contactSchema.validate(form.value, { abortEarly: false });
    await submitContactForm({ ...value });
    submitted.value = true;
    trackEvent("generate_lead", { form_name: "contact" });
    await router.push({ name: "thank-you" });
  } catch (e) {
    if (e.fieldErrors && Object.keys(e.fieldErrors).length) {
      fieldErrors.value = { ...fieldErrors.value, ...e.fieldErrors };
    }
    error.value =
      e.message ||
      "We could not send your message. Please try again or email us directly.";
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <main class="contact-page">
    <!-- Hero: Figma Frame 122 + background (1440×628) -->
    <section class="contact-hero">
      <div class="contact-hero__bg" aria-hidden="true">
        <img
          src="/images/herobg.svg"
          alt=""
          width="1440"
          height="600"
          decoding="async"
        />
      </div>

      <div class="contact-hero__inner">
        <div class="contact-hero__copy">
          <h1 class="contact-hero__title">{{ page.title }}</h1>
          <p class="contact-hero__intro">{{ page.intro }}</p>
        </div>

        <!-- Contact card: Figma image 216 — 1193×688 @ (123, 358) -->
        <div class="contact-card">
          <article class="contact-card__info">
            <div class="contact-card__info-body">
              <p class="contact-card__company">{{ page.company }}</p>

              <div class="contact-card__block">
                <span class="contact-card__label">Phone number</span>
                <a
                  class="contact-card__link"
                  :href="`tel:${String(page.phone).replace(/\s/g, '')}`"
                >{{ page.phone }}</a>
              </div>

              <div class="contact-card__block">
                <span class="contact-card__label">Email address</span>
                <a class="contact-card__link" :href="`mailto:${page.email}`">{{ page.email }}</a>
              </div>

              <div class="contact-card__block contact-card__block--last">
                <span class="contact-card__label">Our location</span>
                <p class="contact-card__address">{{ page.address }}</p>
              </div>
            </div>

            <figure class="contact-card__photo">
              <img
                src="/logos/uroffice.JPG"
                alt="Urbanrupee office entrance at NX-One, Greater Noida"
                width="800"
                height="600"
                loading="lazy"
                decoding="async"
              />
            </figure>
          </article>

          <div
            v-if="submitted"
            id="contact-form"
            class="contact-card__form contact-success"
            role="status"
          >
            <span class="contact-success__icon" aria-hidden="true">
              <img
                src="/images/figma-contact/success-checkmark.png"
                alt=""
                width="57"
                height="57"
                decoding="async"
              />
            </span>
            <div class="contact-success__text">
              <h2 ref="successHeading" class="contact-success__title" tabindex="-1">
                Thank You for Connecting with Us!
              </h2>
              <p class="contact-success__body">
                Your message has been successfully submitted. In the meantime, explore our
                solutions to discover how Urbanrupee can help your business grow.
              </p>
            </div>
            <div class="contact-success__actions">
              <a
                class="contact-success__download"
                :href="CATALOGUE_HREF"
                download="Urbanrupee-Product-Catalogue.pdf"
              >
                <img
                  src="/images/figma-contact/download.svg"
                  alt=""
                  width="20"
                  height="20"
                  decoding="async"
                />
                Get Your Free Product Catalogue
              </a>
              <p class="contact-success__caption">
                Explore our payment solutions, features, and capabilities in one place.
              </p>
            </div>
          </div>

          <form v-else id="contact-form" class="contact-card__form" @submit.prevent="onSubmit">
            <p v-if="error" class="contact-card__error" role="alert">{{ error }}</p>

            <label class="contact-card__field">
              <span>Full Name <em>*</em></span>
              <input
                :value="form.name"
                type="text"
                required
                autocomplete="name"
                maxlength="50"
                :disabled="submitting"
                @beforeinput="onNameBeforeInput"
                @input="updateField('name', $event, sanitizeName)"
                @paste="handlePaste('name', $event, sanitizeName)"
                @blur="onFieldBlur('name')"
              />
              <small v-if="fieldErrors.name" class="contact-card__error-text">{{ fieldErrors.name }}</small>
            </label>
            <label class="contact-card__field">
              <span>Email Address <em>*</em></span>
              <input
                :value="form.email"
                type="email"
                required
                inputmode="email"
                autocomplete="email"
                maxlength="254"
                :disabled="submitting"
                @beforeinput="onEmailBeforeInput"
                @input="updateField('email', $event, sanitizeEmail)"
                @paste="handlePaste('email', $event, sanitizeEmail)"
                @blur="onFieldBlur('email')"
              />
              <small v-if="fieldErrors.email" class="contact-card__error-text">{{ fieldErrors.email }}</small>
            </label>
            <label class="contact-card__field">
              <span>Phone Number <em>*</em></span>
              <input
                :value="form.phone"
                type="tel"
                required
                inputmode="numeric"
                autocomplete="tel"
                maxlength="10"
                :disabled="submitting"
                @beforeinput="onPhoneBeforeInput"
                @input="updateField('phone', $event, sanitizePhone)"
                @paste="handlePhonePaste"
                @blur="onFieldBlur('phone')"
              />
              <small v-if="fieldErrors.phone" class="contact-card__error-text">{{ fieldErrors.phone }}</small>
            </label>
            <label class="contact-card__field">
              <span>Subject <em>*</em></span>
              <input
                :value="form.subject"
                type="text"
                required
                autocomplete="off"
                :disabled="submitting"
                @input="updateField('subject', $event)"
                @blur="onFieldBlur('subject')"
              />
              <small v-if="fieldErrors.subject" class="contact-card__error-text">{{ fieldErrors.subject }}</small>
            </label>
            <label class="contact-card__field contact-card__field--message">
              <span>Message <em>*</em></span>
              <textarea
                :value="form.message"
                required
                maxlength="500"
                :disabled="submitting"
                @input="updateField('message', $event, sanitizeMessage)"
                @blur="onFieldBlur('message')"
              />
              <small class="contact-card__hint">Maximum 500 characters.</small>
              <small v-if="fieldErrors.message" class="contact-card__error-text">{{ fieldErrors.message }}</small>
            </label>

            <button
              type="submit"
              class="contact-card__submit"
              :disabled="!canSubmit || submitting"
            >
              {{ submitting ? "Sending…" : "Submit Now" }}
              <img
                v-if="!submitting"
                src="/images/figma-contact/nav-arrow.svg"
                alt=""
                width="18"
                height="18"
                decoding="async"
              />
            </button>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.contact-page {
  --contact-ink: #252b37;
  --contact-muted: #535861;
  --contact-teal: #097495;
  --contact-font: "Manrope", "DM Sans", system-ui, sans-serif;
  font-family: var(--contact-font);
  background: #ffffff;
  color: var(--contact-ink);
  /* Pull hero under the fixed floating nav (Figma overlays nav on the hero bg) */
  margin-top: -129px;
  overflow-x: clip;
  max-width: 100%;
}

/* ===== Hero + contact card (Figma background 1440×628, card 1193×688) ===== */
.contact-hero {
  position: relative;
  width: 100%;
  max-width: none;
  margin: 0;
  overflow: hidden;
}

.contact-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.contact-hero__bg img {
  display: block;
  position: absolute;
  left: 50%;
  top: 0;
  width: 100%;
  min-width: 100%;
  height: 100%;
  min-height: 100%;
  transform: translateX(-50%);
  object-fit: cover;
  object-position: center top;
}

.contact-hero__inner {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: var(--ur-page-max, 1440px);
  margin: 0 auto;
  min-height: 1046px; /* card bottom: 358 + 688 */
  padding: 188px var(--ur-gutter) 0; /* title @ y=188; card→FAQ gap handled by .contact-faq */
  box-sizing: border-box;
}

.contact-hero__copy {
  position: relative;
  z-index: 1;
  width: 500px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.contact-hero__title {
  margin: 0;
  width: 500px;
  font-family: var(--contact-font);
  font-size: var(--ur-heading-lg, 42px);
  font-weight: 700;
  line-height: 1.37;
  letter-spacing: -1.26px;
  color: var(--contact-ink);
}

.contact-hero__intro {
  margin: 0;
  width: 500px;
  font-family: var(--contact-font);
  font-size: 14px;
  font-weight: 400;
  line-height: 19.124px;
  letter-spacing: -0.42px;
  color: var(--contact-muted);
}

.contact-card {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  width: 1193px;
  max-width: 100%;
  min-height: 688px;
  margin: 59px auto 0; /* 358 - (188+111) = 59 */
}

.contact-card__info,
.contact-card__form {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #eceef2;
  box-shadow: 0 12px 40px rgba(37, 43, 55, 0.08);
  overflow: hidden;
}

.contact-card__info {
  display: flex;
  flex-direction: column;
  min-height: 688px;
}

.contact-card__info-body {
  padding: 32px 32px 24px;
  flex: 0 0 auto;
}

.contact-card__company {
  margin: 0 0 24px;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.35;
  color: var(--contact-ink);
}

.contact-card__block {
  margin-bottom: 20px;
}

.contact-card__block--last {
  margin-bottom: 0;
}

.contact-card__label {
  display: block;
  margin-bottom: 6px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #8b919a;
}

.contact-card__link {
  font-size: 15px;
  font-weight: 600;
  color: var(--contact-teal);
  text-decoration: none;
}

.contact-card__link:hover {
  text-decoration: underline;
}

.contact-card__address {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.55;
  color: var(--contact-muted);
}

.contact-card__photo {
  margin: 0;
  flex: 1 1 auto;
  min-height: 280px;
  overflow: hidden;
}

.contact-card__photo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 40%;
}

.contact-card__form {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 28px 28px 24px;
  min-height: 688px;
  box-sizing: border-box;
}

.contact-card__field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: var(--contact-ink);
}

.contact-card__field em {
  color: #e11d48;
  font-style: normal;
}

.contact-card__hint {
  font-size: 12px;
  line-height: 16px;
  color: #8b919a;
}

.contact-card__error-text {
  font-size: 12px;
  line-height: 16px;
  color: #b91c1c;
}

.contact-card__field input,
.contact-card__field textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid #d9dee7;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  color: var(--contact-ink);
  background: #fff;
}

.contact-card__field textarea {
  min-height: 120px;
  resize: vertical;
}

.contact-card__field input:focus,
.contact-card__field textarea:focus {
  outline: none;
  border-color: var(--contact-teal);
  box-shadow: 0 0 0 3px rgba(9, 116, 149, 0.15);
}

.contact-card__submit {
  margin-top: auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  width: 100%;
  height: 48px;
  padding: 16px;
  box-sizing: border-box;
  border: 0;
  border-radius: 8px;
  font-family: inherit;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  color: #ffffff;
  cursor: pointer;
  background: #097495;
}

.contact-card__submit img {
  display: block;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.contact-card__submit:hover:not(:disabled) {
  opacity: 0.92;
}

.contact-card__submit:disabled {
  background: #d5d7da;
  color: #535862;
  cursor: not-allowed;
  opacity: 1;
}

.contact-card__submit:disabled img {
  filter: brightness(0) invert(35%);
}

/* ===== Success state (Figma 957:6058) ===== */
.contact-success {
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 24px;
  text-align: center;
}

.contact-success__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 88px;
  height: 89px;
  flex-shrink: 0;
  box-sizing: border-box;
  border: 3.708px solid var(--contact-teal);
  border-radius: 50%;
}

.contact-success__icon img {
  display: block;
  width: 56.861px;
  height: 56.861px;
  object-fit: contain;
}

.contact-success__text {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.contact-success__title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  line-height: 32px;
  color: var(--contact-ink);
}

.contact-success__title:focus {
  outline: none;
}

.contact-success__body,
.contact-success__caption {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  color: #535862;
  opacity: 0.8;
}

.contact-success__body {
  font-weight: 500;
}

.contact-success__caption {
  max-width: 480px;
  font-weight: 400;
}

.contact-success__actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 11px;
  width: 100%;
}

.contact-success__download {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: min(100%, 479px);
  height: 52px;
  padding: 16px;
  box-sizing: border-box;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.32px;
  color: #ffffff;
  text-decoration: none;
  background: var(--contact-teal);
  transition: opacity 0.15s ease;
}

.contact-success__download img {
  display: block;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.contact-success__download:hover {
  opacity: 0.92;
}

.contact-success__download:focus-visible {
  outline: 3px solid rgba(9, 116, 149, 0.35);
  outline-offset: 2px;
}

.contact-card__error {
  margin: 0;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
}

/* ===== FAQ (Figma 1240×440, columns 501 + 94 + 627) ===== */
.contact-faq {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 180px 100px 0; /* form/card bottom → first FAQ trigger = 180px */
  box-sizing: border-box;
  background: #ffffff;
}

.contact-faq__inner {
  display: grid;
  grid-template-columns: 501px 627px;
  gap: 94px;
  width: 1240px;
  max-width: 100%;
  min-height: 440px;
  margin: 0 auto;
  align-items: start;
}

.contact-faq__intro {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 501px;
  padding-top: 118px; /* visually aligns with accordion in Figma (1378-1260) */
}

.contact-faq__title {
  margin: 0;
  width: 501px;
  font-size: 40px;
  font-weight: 700;
  line-height: 56px;
  letter-spacing: 0;
  color: var(--contact-ink);
}

.contact-faq__body {
  margin: 0;
  width: 510px;
  max-width: 100%;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: var(--contact-muted);
}

.contact-faq__list {
  width: 627px;
  max-width: 100%;
}

.contact-faq__item {
  border-bottom: 1px solid #f0f9f3;
}

.contact-faq__trigger {
  display: grid;
  grid-template-columns: 36px 1fr 24px;
  align-items: center;
  gap: 16px;
  width: 100%;
  min-height: 76px;
  padding: 24px;
  box-sizing: border-box;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  color: var(--contact-ink);
}

.contact-faq__item--open .contact-faq__trigger {
  min-height: 0;
  padding-bottom: 16px;
}

.contact-faq__num {
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
}

.contact-faq__question {
  font-size: 18px;
  font-weight: 600;
  line-height: 28px;
}

.contact-faq__icon {
  font-size: 22px;
  font-weight: 400;
  line-height: 1;
  text-align: center;
  color: var(--contact-ink);
}

.contact-faq__answer {
  padding: 0 24px 24px 76px;
}

.contact-faq__answer p {
  margin: 0;
  max-width: 579px;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: var(--contact-muted);
}

/* ===== CTA (Figma 1240×331, radius 16) ===== */
.contact-cta {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 180px 100px 94px; /* 1880-1700 ≈ 180; footer gap 94 */
  box-sizing: border-box;
  background: #ffffff;
}

.contact-cta__panel {
  position: relative;
  width: 1240px;
  max-width: 100%;
  height: 331px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
}

.contact-cta__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.contact-cta__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  height: 100%;
  padding: 40px 24px;
  box-sizing: border-box;
  text-align: center;
}

.contact-cta__title {
  margin: 0;
  max-width: 669px;
  font-size: 40px;
  font-weight: 500;
  line-height: 52px;
  letter-spacing: 1.6px;
  color: #ffffff;
}

.contact-cta__body {
  margin: 0;
  max-width: 509px;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0.56px;
  color: rgba(255, 255, 255, 0.8);
}

.contact-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-width: 153px;
  height: 52px;
  padding: 0 16px;
  border-radius: 8px;
  background: #ffffff;
  color: var(--contact-teal);
  font-size: 16px;
  font-weight: 500;
  letter-spacing: -0.32px;
  line-height: 21.856px;
  text-decoration: none;
}

.contact-cta__btn span {
  font-size: 18px;
  line-height: 1;
}

.contact-cta__btn:hover {
  opacity: 0.92;
}

@media (max-width: 1280px) {
  .contact-page {
    margin-top: -113px;
  }

  .contact-hero__inner,
  .contact-faq,
  .contact-cta {
    padding-left: 40px;
    padding-right: 40px;
  }

  .contact-card,
  .contact-faq__inner,
  .contact-cta__panel {
    width: 100%;
  }

  .contact-faq__inner {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr);
    gap: 48px;
  }

  .contact-faq__intro,
  .contact-faq__title,
  .contact-faq__list {
    width: 100%;
  }
}

@media (max-width: 1200px) {
  .contact-page {
    margin-top: -82px;
  }

  .contact-hero__inner {
    min-height: 0;
    padding: 110px var(--ur-gutter) 0;
  }

  .contact-hero__copy {
    width: 100%;
    max-width: min(var(--ur-stack-max), 100%);
    margin-top: 0;
    gap: 12px;
  }

  .contact-hero__title,
  .contact-hero__intro {
    width: 100%;
  }

  .contact-hero__title {
    font-size: var(--ur-heading-stack, 28px);
    line-height: 1.25;
    letter-spacing: -0.8px;
  }

  .contact-hero__intro {
    font-size: clamp(13px, 2.5vw, 15px);
    line-height: 1.5;
  }

  .contact-card {
    grid-template-columns: 1fr;
    margin-top: 40px;
    min-height: 0;
  }

  .contact-card__info,
  .contact-card__form {
    min-height: 0;
  }

  .contact-faq {
    padding-top: 64px;
    padding-left: var(--ur-gutter);
    padding-right: var(--ur-gutter);
  }

  .contact-faq__inner {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .contact-faq__intro {
    padding-top: 0;
  }

  .contact-faq__title {
    font-size: var(--ur-heading-stack, 28px);
    line-height: 1.3;
  }

  .contact-cta {
    padding: 64px var(--ur-gutter) 48px;
  }

  .contact-cta__panel {
    height: auto;
    min-height: 280px;
  }

  .contact-cta__title {
    font-size: var(--ur-heading-stack, 28px);
    line-height: 1.3;
    letter-spacing: 0.5px;
  }
}

/* Tablet (Figma 931:18733): 714px heading over a two-column card, 888px wide at 1024 */
@media (min-width: 768px) and (max-width: 1024px) {
  /* The bg layer clips itself; letting the hero overflow keeps the card shadow from being cut flat. */
  .contact-hero {
    overflow: visible;
  }

  .contact-hero__inner {
    /* gutter: 40@768 → 68@1024 */
    padding: 162px clamp(40px, calc(-44px + 10.9375vw), 68px) 0;
  }

  .contact-hero__copy {
    max-width: 714px;
    gap: 20px;
  }

  .contact-hero__title {
    font-size: 36px;
    line-height: 44px;
    letter-spacing: -1.08px;
  }

  .contact-hero__intro {
    font-size: 16px;
    line-height: 20px;
    letter-spacing: 0.64px;
  }

  .contact-card {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
    width: 100%;
    max-width: 888px;
    margin-top: 24px;
  }

  .contact-card__info-body,
  .contact-card__form {
    padding: 24px;
  }

  .contact-card__photo {
    min-height: 220px;
  }
}

@media (max-width: 480px) {
  .contact-page {
    margin-top: -88px;
  }

  .contact-hero__inner {
    padding: 104px 16px 0;
  }

  .contact-hero__copy {
    gap: 12px;
  }

  .contact-hero__title {
    font-size: 28px;
  }

  .contact-hero__intro {
    font-size: 13px;
    line-height: 20px;
  }

  .contact-card {
    margin-top: 28px;
    gap: 16px;
  }

  .contact-card__info-body,
  .contact-card__form {
    padding: 20px 16px;
  }

  .contact-card__form {
    gap: 12px;
  }

  .contact-success {
    gap: 20px;
    padding: 32px 16px;
  }

  .contact-success__title {
    font-size: 20px;
    line-height: 28px;
  }

  .contact-success__download {
    height: auto;
    min-height: 52px;
    font-size: 15px;
  }

  .contact-card__field {
    gap: 5px;
    font-size: 13px;
  }

  .contact-card__field input,
  .contact-card__field textarea {
    padding: 11px 12px;
    font-size: 13px;
  }

  .contact-faq {
    padding-top: 48px;
  }
}
</style>
