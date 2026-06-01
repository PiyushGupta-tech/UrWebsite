import { chromium } from "playwright";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import indiaMap from "@svg-maps/india";

const __dirname = dirname(fileURLToPath(import.meta.url));
const map = indiaMap.default ?? indiaMap;

const STATE_ANCHORS = {
  pb: { x: 155, y: 158 },
  ch: { x: 180, y: 160 },
  hr: { x: 171, y: 197 },
  dl: { x: 187, y: 211 },
  mp: { x: 213, y: 314 },
  mh: { x: 168, y: 427 },
  ka: { x: 174, y: 517 },
  tg: { x: 226, y: 458 },
  tn: { x: 211, y: 600 },
  rj: { x: 148, y: 275 },
  gj: { x: 80, y: 355 },
};

const py = readFileSync(
  join(__dirname, "../../backend/website/merchant_map.py"),
  "utf8",
);
const pins = [];
for (const block of py.matchAll(
  /"id":\s*"([^"]+)"[^}]*"state_id":\s*"([^"]+)"[^}]*"offset_x":\s*(-?\d+)[^}]*"offset_y":\s*(-?\d+)/g,
)) {
  pins.push({ id: block[1], stateId: block[2], ox: +block[3], oy: +block[4] });
}

const pathsHtml = map.locations
  .map((l) => `<path id="${l.id}" d="${l.path}"/>`)
  .join("");

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent(
  `<!DOCTYPE html><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 696">${pathsHtml}</svg>`,
);

const check = async (stateId, x, y) =>
  page.evaluate(
    ({ stateId, x, y }) => {
      const path = document.getElementById(stateId);
      return path?.isPointInFill(new DOMPoint(x, y)) ?? false;
    },
    { stateId, x, y },
  );

const findContaining = async (x, y) =>
  page.evaluate(
    ({ x, y, ids }) => {
      return ids.filter((id) => {
        const path = document.getElementById(id);
        return path?.isPointInFill(new DOMPoint(x, y));
      });
    },
    { x, y, ids: map.locations.map((l) => l.id) },
  );

console.log("Chromium isPointInFill validation\n");

const failures = [];
const fixes = [];

for (const pin of pins) {
  const a = STATE_ANCHORS[pin.stateId];
  const x = a.x + pin.ox;
  const y = a.y + pin.oy;
  const ok = await check(pin.stateId, x, y);
  const actual = ok ? [pin.stateId] : await findContaining(x, y);
  if (!ok) failures.push({ ...pin, x, y, actual });
  console.log(
    `${ok ? "OK" : "FAIL"} ${pin.id.padEnd(22)} ${pin.stateId} @(${x},${y})` +
      (ok ? "" : ` -> [${actual.join(", ") || "outside"}]`),
  );
}

console.log(`\n${failures.length}/${pins.length} misaligned\n`);

for (const f of failures) {
  const a = STATE_ANCHORS[f.stateId];
  let best = null;
  for (let dx = -120; dx <= 120; dx += 4) {
    for (let dy = -120; dy <= 120; dy += 4) {
      const x = f.x + dx;
      const y = f.y + dy;
      if (await check(f.stateId, x, y)) {
        const dist = dx * dx + dy * dy;
        if (!best || dist < best.dist) best = { x, y, dist, ox: x - a.x, oy: y - a.y };
      }
    }
  }
  if (best) {
    fixes.push({ id: f.id, ...best });
    console.log(`FIX ${f.id}: offset_x=${best.ox}, offset_y=${best.oy}`);
  }
}

// Sample anchor points inside each state used by pins
console.log("\nInterior sample per state:");
const stateIds = [...new Set(pins.map((p) => p.stateId))];
for (const id of stateIds) {
  let sample = null;
  for (let y = 0; y <= 696; y += 6) {
    for (let x = 0; x <= 612; x += 6) {
      if (await check(id, x, y)) {
        sample = { x, y };
        break;
      }
    }
    if (sample) break;
  }
  console.log(`  ${id}: ${sample ? `(${sample.x}, ${sample.y})` : "none"}`);
}

await browser.close();

if (fixes.length) {
  console.log("\n--- Apply to merchant_map.py ---");
  for (const f of fixes) {
    console.log(`${f.id}: offset_x=${f.ox}, offset_y=${f.oy}`);
  }
}
