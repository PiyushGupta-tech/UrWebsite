<script setup>
import { ref } from "vue";
import { submitContactForm } from "@/api/client.js";
import PageHero from "./PageHero.vue";

defineProps({
  page: { type: Object, required: true },
});

const form = ref({
  name: "",
  email: "",
  phone: "",
  subject: "",
  message: "",
});

const submitted = ref(false);
const submitting = ref(false);
const error = ref("");

async function onSubmit() {
  submitting.value = true;
  error.value = "";
  try {
    await submitContactForm({ ...form.value });
    submitted.value = true;
  } catch (e) {
    error.value =
      e.message ||
      "We could not send your message. Please try again or email us directly.";
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <main>
    <PageHero :title="page.title" :intro="page.intro" />

    <section class="section">
      <div class="container contact-grid">
        <div class="contact-info card">
          <div class="contact-info__details">
            <p class="contact-info__company">{{ page.company }}</p>

            <div class="contact-info__block">
              <span class="contact-info__label">Phone number</span>
              <a :href="`tel:${page.phone.replace(/\s/g, '')}`">{{ page.phone }}</a>
            </div>

            <div class="contact-info__block">
              <span class="contact-info__label">Email address</span>
              <a :href="`mailto:${page.email}`">{{ page.email }}</a>
            </div>

            <div class="contact-info__block contact-info__block--last">
              <span class="contact-info__label">Our location</span>
              <p>{{ page.address }}</p>
            </div>
          </div>

          <figure class="contact-info__photo">
            <img
              src="/logos/uroffice.JPG"
              alt="Urbanrupee office entrance at NX-One, Greater Noida"
              width="800"
              height="600"
              loading="lazy"
              decoding="async"
            />
          </figure>
        </div>

        <form class="contact-form card" @submit.prevent="onSubmit">
          <p v-if="submitted" class="contact-form__success">
            Thank you — we'll get back to you shortly.
          </p>

          <template v-else>
            <p v-if="error" class="contact-form__error" role="alert">{{ error }}</p>
            <label>
              Full Name *
              <input v-model="form.name" type="text" required :disabled="submitting" />
            </label>
            <label>
              Email Address *
              <input v-model="form.email" type="email" required :disabled="submitting" />
            </label>
            <label>
              Phone Number *
              <input v-model="form.phone" type="tel" required :disabled="submitting" />
            </label>
            <label>
              Subject *
              <input v-model="form.subject" type="text" required :disabled="submitting" />
            </label>
            <label>
              Message *
              <textarea v-model="form.message" rows="5" required :disabled="submitting" />
            </label>
            <button type="submit" class="btn btn--primary" :disabled="submitting">
              {{ submitting ? "Sending…" : "Submit Now" }}
            </button>
          </template>
        </form>
      </div>
    </section>
  </main>
</template>

<style scoped>
.contact-grid {
  display: grid;
  gap: 24px;
}

@media (min-width: 900px) {
  .contact-grid {
    grid-template-columns: 1fr 1.2fr;
    align-items: stretch;
  }

  .contact-info {
    min-height: 640px;
  }
}

@media (max-width: 899px) {
  .contact-info {
    min-height: 520px;
  }
}

.contact-form {
  padding: 32px;
}

.contact-info {
  padding: 0;
  display: grid;
  grid-template-rows: 1fr 1fr;
  min-height: 100%;
  overflow: hidden;
}

.contact-info__details {
  padding: 32px 32px 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 0;
}

.contact-info__company {
  font-weight: 700;
  font-size: 18px;
  margin: 0 0 24px;
}

.contact-info__block {
  margin-bottom: 20px;
}

.contact-info__block--last {
  margin-bottom: 0;
}

.contact-info__photo {
  margin: 0;
  min-height: 0;
  overflow: hidden;
  border-top: 1px solid var(--border);
}

.contact-info__photo img {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 200px;
  object-fit: cover;
  object-position: center 40%;
}

.contact-info__label {
  display: block;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.contact-info__block a {
  font-weight: 600;
  color: var(--accent-blue);
}

.contact-info__block p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.55;
}

.contact-form label {
  display: block;
  margin-bottom: 16px;
  font-size: 14px;
  font-weight: 500;
}

.contact-form input,
.contact-form textarea {
  display: block;
  width: 100%;
  margin-top: 6px;
  padding: 12px 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-family: inherit;
  font-size: 15px;
}

.contact-form input:focus,
.contact-form textarea:focus {
  outline: 2px solid var(--accent-blue-tint);
  border-color: var(--accent-blue);
}

.contact-form .btn {
  width: 100%;
  margin-top: 8px;
}

.contact-form__success {
  margin: 0;
  text-align: center;
  color: var(--accent-green);
  font-weight: 600;
  padding: 24px 0;
}

.contact-form__error {
  margin: 0 0 16px;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 14px;
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
}
</style>
