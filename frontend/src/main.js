import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initAnalytics } from "./utils/analytics.js";
import { initScrollRestoration } from "./utils/scrollRestoration.js";
import "./assets/main.css";
import "./assets/admin.css";

initScrollRestoration(router);
initAnalytics();

createApp(App).use(router).mount("#app");
