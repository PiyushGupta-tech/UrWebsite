<script setup>
import { computed } from "vue";

const props = defineProps({
  problem: { type: Object, required: true },
});

const icons = {
  partners: "/images/figma-home/icon-partners.svg",
  control: "/images/figma-home/icon-control.svg",
  failed: "/images/figma-home/icon-failed.svg",
  reconcile: "/images/figma-home/icon-reconcile.svg",
};

const leftCards = computed(() => (props.problem.items || []).slice(0, 2));
const rightCards = computed(() => (props.problem.items || []).slice(2, 4));
</script>

<template>
  <section class="home-problem">
    <div class="home-problem__inner">
      <div class="home-problem__copy">
        <h2 class="home-problem__title">{{ problem.title }}</h2>
        <p class="home-problem__intro">{{ problem.intro }}</p>
      </div>

      <div class="home-problem__cards">
        <div class="home-problem__col">
          <article
            v-for="item in leftCards"
            :key="item.title"
            class="home-problem__card"
          >
            <span class="home-problem__icon" aria-hidden="true">
              <img :src="icons[item.icon]" alt="" width="26" height="26" />
            </span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.body }}</p>
          </article>
        </div>
        <div class="home-problem__col home-problem__col--offset">
          <article
            v-for="item in rightCards"
            :key="item.title"
            class="home-problem__card"
          >
            <span class="home-problem__icon" aria-hidden="true">
              <img :src="icons[item.icon]" alt="" width="26" height="26" />
            </span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.body }}</p>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-problem {
  position: relative;
  overflow: hidden;
  background: rgba(237, 244, 233, 0.1);
  font-family: "Manrope", "DM Sans", system-ui, sans-serif;
  color: #252b37;
}

.home-problem__inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 100px 100px 120px;
  display: flex;
  align-items: center;
  gap: 41px;
  box-sizing: border-box;
}

.home-problem__copy {
  flex: 0 1 549px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.home-problem__title {
  margin: 0;
  max-width: 571px;
  font-size: 42px;
  font-weight: 700;
  line-height: 56px;
}

.home-problem__intro {
  margin: 0;
  max-width: 510px;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.64px;
  color: #535862;
}

.home-problem__cards {
  flex: 1 1 649px;
  display: grid;
  grid-template-columns: 315px 317px;
  gap: 17px;
  align-items: start;
}

.home-problem__col {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.home-problem__col--offset {
  padding-top: 69px;
}

.home-problem__card {
  min-height: 197px;
  padding: 20px;
  box-sizing: border-box;
  border-radius: 14.141px;
  background: #ffffff;
  box-shadow:
    0 1px 2px -1px rgba(0, 0, 0, 0.1),
    0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.home-problem__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50.57px;
  height: 50.57px;
  margin-bottom: 16px;
  border-radius: 6.642px;
  background: rgba(9, 116, 149, 0.1);
}

.home-problem__icon img {
  width: 26px;
  height: 26px;
  object-fit: contain;
}

.home-problem__card h3 {
  margin: 0 0 7px;
  font-size: 16px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0.48px;
}

.home-problem__card p {
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.42px;
  color: #535862;
}

@media (max-width: 1100px) {
  .home-problem__inner {
    flex-direction: column;
    align-items: stretch;
    padding: 64px 40px;
  }

  .home-problem__cards {
    grid-template-columns: 1fr 1fr;
    width: 100%;
  }

  .home-problem__col--offset {
    padding-top: 36px;
  }
}

@media (max-width: 768px) {
  .home-problem__inner {
    padding: 48px 24px;
  }

  .home-problem__title {
    font-size: 28px;
    line-height: 1.25;
  }

  .home-problem__cards {
    grid-template-columns: 1fr;
  }

  .home-problem__col--offset {
    padding-top: 0;
  }
}
</style>
