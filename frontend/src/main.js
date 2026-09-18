import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initScrollRestoration } from "./utils/scrollRestoration.js";
import "./assets/main.css";
import "./assets/admin.css";

initScrollRestoration(router);

createApp(App).use(router).mount("#app");
