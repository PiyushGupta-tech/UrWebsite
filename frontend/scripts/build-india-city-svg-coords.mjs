/**
 * Snap every indexed city to a point inside its state on @svg-maps/india.
 * Run: node scripts/build-india-city-svg-coords.mjs
 * Requires: playwright (devDependency)
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import indiaMap from "@svg-maps/india";
import {
  normalizeCity,
  normalizeState,
  stateIdFromName,
} from "./shared/indiaMapStateIds.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const indexPath = join(__dirname, "../src/constants/indiaCityIndex.json");
const outPath = join(__dirname, "../src/constants/indiaCitySvgCoords.json");

const VIEWBOX = { width: 612, height: 696 };
const BOUNDS = { minLon: 68.0, maxLon: 97.5, minLat: 6.5, maxLat: 37.5 };

function project(lat, lon) {
  const x =
    ((lon - BOUNDS.minLon) / (BOUNDS.maxLon - BOUNDS.minLon)) * VIEWBOX.width * 0.86 +
    VIEWBOX.width * 0.07;
  const y =
    ((BOUNDS.maxLat - lat) / (BOUNDS.maxLat - BOUNDS.minLat)) * VIEWBOX.height * 0.9 +
    VIEWBOX.height * 0.05;
  return { x, y };
}

function round1(n) {
  return Math.round(n * 10) / 10;
}

const map = indiaMap.default ?? indiaMap;
const index = JSON.parse(readFileSync(indexPath, "utf8"));

const html = map.locations
  .map((l) => `<path id="${l.id}" d="${l.path}"/>`)
  .join("");

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent(
  `<!DOCTYPE html><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 696">${html}</svg>`,
);

const stateCentroids = await page.evaluate(() => {
  const step = 6;
  const out = {};
  for (const path of document.querySelectorAll("path")) {
    const pts = [];
    for (let y = 0; y <= 696; y += step) {
      for (let x = 0; x <= 612; x += step) {
        if (path.isPointInFill(new DOMPoint(x, y))) pts.push({ x, y });
      }
    }
    if (!pts.length) continue;
    const cx = pts.reduce((s, p) => s + p.x, 0) / pts.length;
    const cy = pts.reduce((s, p) => s + p.y, 0) / pts.length;
    out[path.id] = { x: Math.round(cx), y: Math.round(cy) };
  }
  return out;
});

async function snapToState(stateId, lat, lon) {
  const target = project(lat, lon);
  const centroid = stateCentroids[stateId];

  const result = await page.evaluate(
    ({ stateId, target, centroid }) => {
      const path = document.getElementById(stateId);
      if (!path) return { kind: "missing" };

      const inside = (x, y) => path.isPointInFill(new DOMPoint(x, y));

      if (inside(target.x, target.y)) {
        return { kind: "exact", x: target.x, y: target.y };
      }

      if (centroid) {
        let best = null;
        for (let t = 0.02; t <= 1; t += 0.02) {
          const x = target.x + (centroid.x - target.x) * t;
          const y = target.y + (centroid.y - target.y) * t;
          if (inside(x, y)) best = { x, y, t };
        }
        if (best) return { kind: "snapped", x: best.x, y: best.y };
      }

      let spiral = null;
      for (let r = 0; r <= 80; r += 1) {
        for (let a = 0; a < 360; a += 10) {
          const x = target.x + r * Math.cos((a * Math.PI) / 180);
          const y = target.y + r * Math.sin((a * Math.PI) / 180);
          if (!inside(x, y)) continue;
          if (!spiral || r < spiral.r) spiral = { x, y, r };
        }
        if (spiral && spiral.r < r - 4) break;
      }
      if (spiral) return { kind: "snapped", x: spiral.x, y: spiral.y };

      return { kind: "fallback" };
    },
    { stateId, target, centroid },
  );

  if (result.kind === "exact" || result.kind === "snapped") {
    return { x: round1(result.x), y: round1(result.y), method: result.kind };
  }

  const stateCenter = stateCentroids[stateId];
  if (stateCenter) {
    return { x: stateCenter.x, y: stateCenter.y, method: "centroid" };
  }

  return { x: round1(target.x), y: round1(target.y), method: "raw" };
}

/** @type {Record<string, [number, number, string]>} */
const byKey = {};
/** @type {Record<string, [number, number, string]>} */
const byCity = {};

const stats = { exact: 0, snapped: 0, centroid: 0, raw: 0, skipped: 0 };

for (const [key, coords] of Object.entries(index.byKey)) {
  const [cityPart, statePart] = key.split("|");
  const lat = coords[0];
  const lon = coords[1];
  const stateId = stateIdFromName(statePart);

  if (!stateId) {
    stats.skipped += 1;
    continue;
  }

  const pin = await snapToState(stateId, lat, lon);
  stats[pin.method] += 1;
  byKey[key] = [pin.x, pin.y, stateId];
}

for (const [city, entry] of Object.entries(index.byCity)) {
  const [, , stateName] = entry;
  const key = `${city}|${normalizeState(stateName)}`;
  if (byKey[key]) {
    byCity[city] = byKey[key];
    continue;
  }
  const [lat, lon] = entry;
  const stateId = stateIdFromName(stateName);
  if (!stateId) continue;
  const pin = await snapToState(stateId, lat, lon);
  byCity[city] = [pin.x, pin.y, stateId];
}

const output = {
  _meta: {
    source: "indiaCityIndex.json snapped to @svg-maps/india",
    count: Object.keys(byKey).length,
    stats,
    built: new Date().toISOString().slice(0, 10),
  },
  byKey,
  byCity,
};

writeFileSync(outPath, `${JSON.stringify(output)}\n`);
console.log(`Wrote ${outPath}`);
console.log(stats);
await browser.close();
