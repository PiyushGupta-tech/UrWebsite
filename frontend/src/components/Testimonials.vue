<script setup>
defineProps({
  section: { type: Object, required: true },
});
</script>

<template>
  <section class="testimonials section">
    <div class="container">
      <h2 class="section-title">{{ section.title }}</h2>

      <div class="testimonials__layout">
        <div v-if="section.videos?.length" class="testimonials__videos">
          <article
            v-for="(item, index) in section.videos"
            :key="item.video || index"
            class="testimonials__card testimonials__card--video card"
          >
            <div class="testimonials__video-wrap">
              <video
                class="testimonials__video"
                controls
                playsinline
                preload="none"
                :src="item.video"
                :poster="item.poster"
              >
                <track
                  kind="captions"
                  srclang="en"
                  label="English captions"
                  src="/videos/testimonials/captions.vtt"
                  default
                />
              </video>
            </div>
            <footer class="testimonials__meta">
              <strong>{{ item.name }}</strong>
              <span>{{ item.role }}</span>
            </footer>
          </article>
        </div>

        <div v-if="section.quotes?.length" class="testimonials__quotes">
          <blockquote
            v-for="item in section.quotes"
            :key="item.name"
            class="testimonials__card testimonials__card--quote card"
          >
            <h3 class="testimonials__quote-title">{{ item.title }}</h3>
            <p class="testimonials__quote">"{{ item.quote }}"</p>
            <footer class="testimonials__meta">
              <strong>{{ item.name }}</strong>
              <span>{{ item.role }}</span>
            </footer>
          </blockquote>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.testimonials__layout {
  display: grid;
  gap: 24px;
  margin-top: 40px;
  align-items: start;
}

.testimonials__videos {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.testimonials__quotes {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.testimonials__card {
  margin: 0;
}

.testimonials__card--video {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.testimonials__card--quote {
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.testimonials__video-wrap {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
  aspect-ratio: 9 / 16;
}

.testimonials__video {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.testimonials__quote-title {
  font-size: 16px;
  margin: 0 0 12px;
}

.testimonials__quote {
  margin: 0 0 20px;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.6;
  flex: 1;
}

.testimonials__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 14px;
}

.testimonials__card--video .testimonials__meta {
  text-align: center;
}

.testimonials__meta span {
  color: var(--text-muted);
}

@media (min-width: 900px) {
  .testimonials__layout {
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
    gap: 32px;
    align-items: stretch;
  }

  .testimonials__quotes {
    justify-content: stretch;
  }
}

@media (max-width: 899px) {
  .testimonials__videos {
    max-width: 480px;
    margin-inline: auto;
  }
}
</style>
