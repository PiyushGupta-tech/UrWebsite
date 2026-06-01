import { chromium } from "playwright";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import indiaMap from "@svg-maps/india";

const __dirname = dirname(fileURLToPath(import.meta.url));
const map = indiaMap.default ?? indiaMap;

const PIN_GROUPS = [
  { stateId: "pb", ids: ["ludhiana"] },
  { stateId: "ch", ids: ["chandigarh"] },
  { stateId: "hr", ids: ["kurukshetra", "gurugram"] },
  { stateId: "dl", ids: ["delhi-shadval", "delhi-mobitm", "delhi-evelocy"] },
  { stateId: "mp", ids: ["rajgarh-greenweb", "indore", "mp-greenweb-bhopal"] },
  { stateId: "mh", ids: ["pune"] },
  { stateId: "ka", ids: ["bengaluru-quickwave", "bengaluru-vyaptrix", "bengaluru-aai", "ka-syllogi"] },
  { stateId: "tg", ids: ["hyderabad-indyapay", "hyderabad-skriptonic"] },
  { stateId: "tn", ids: ["tn-kuberan", "tn-unibeck"] },
  { stateId: "rj", ids: ["rajasthan-groots"] },
  { stateId: "gj", ids: ["gujarat-ojct", "gujarat-luxpay"] },
];

const NEEDED = [...new Set(PIN_GROUPS.map((g) => g.stateId))];
const pathsHtml = map.locations
  .filter((l) => NEEDED.includes(l.id))
  .map((l) => `<path id="${l.id}" d="${l.path}"/>`)
  .join("");

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent(
  `<!DOCTYPE html><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 696">${pathsHtml}</svg>`,
);

const interior = await page.evaluate((ids) => {
  const step = 4;
  const out = {};
  for (const id of ids) {
    const path = document.getElementById(id);
    const pts = [];
    for (let y = 0; y <= 696; y += step) {
      for (let x = 0; x <= 612; x += step) {
        if (path?.isPointInFill(new DOMPoint(x, y))) pts.push({ x, y });
      }
    }
    out[id] = pts;
  }
  return out;
}, NEEDED);

for (const id of NEEDED) console.log(`${id}: ${interior[id].length} samples`);

function dist(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

const MIN_DIST = 32;
const placements = {};
const anchors = {};

for (const group of PIN_GROUPS) {
  const pool = interior[group.stateId];
  const cx = pool.reduce((s, p) => s + p.x, 0) / pool.length;
  const cy = pool.reduce((s, p) => s + p.y, 0) / pool.length;
  const anchor = pool.reduce((best, p) =>
    !best || dist(p, { x: cx, y: cy }) < dist(best, { x: cx, y: cy }) ? p : best,
  );
  anchors[group.stateId] = { x: Math.round(anchor.x), y: Math.round(anchor.y) };

  const placed = [];
  for (const pinId of group.ids) {
    let best = null;
    for (const p of pool) {
      if (placed.some((q) => dist(p, q) < MIN_DIST)) continue;
      const score = dist(p, anchor);
      if (!best || score < best.score) best = { ...p, score };
    }
    if (!best && pool.length) best = { ...pool[0], score: 0 };
    placed.push({ x: best.x, y: best.y });
    placements[pinId] = {
      stateId: group.stateId,
      offset_x: Math.round(best.x - anchor.x),
      offset_y: Math.round(best.y - anchor.y),
    };
  }
}

console.log("\nSTATE_ANCHORS =", JSON.stringify(anchors, null, 2));
console.log("\nOffsets:");
for (const [id, p] of Object.entries(placements)) {
  console.log(`  ${id}: offset_x=${p.offset_x}, offset_y=${p.offset_y}`);
}

await browser.close();
