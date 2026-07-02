/**
 * Build compact city coordinate index from india-cities-source.json
 * Source: Vynex/indian-cities-geodata (Census 2011 cities pop > 100k)
 * Run: node scripts/build-india-city-index.mjs
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(__dirname, "data/india-cities-source.json");
const outPath = join(__dirname, "../src/constants/indiaCityIndex.json");

const STATE_ALIASES = {
  "andaman and nicobar islands": "andaman and nicobar islands",
  "andaman & nicobar islands": "andaman and nicobar islands",
  "jammu and kashmir": "jammu and kashmir",
  "jammu & kashmir": "jammu and kashmir",
  "dadra and nagar haveli and daman and diu": "dadra and nagar haveli",
  "dadra and nagar haveli": "dadra and nagar haveli",
  "daman and diu": "daman and diu",
  orissa: "odisha",
  pondicherry: "puducherry",
  "nct of delhi": "delhi",
  "delhi nct": "delhi",
};

const CITY_ALIASES = {
  gurgaon: "gurugram",
  bangalore: "bengaluru",
  bombay: "mumbai",
  cochin: "kochi",
  trivandrum: "thiruvananthapuram",
  calcutta: "kolkata",
  "new delhi": "delhi",
  "fatehgarh saheb": "fatehgarh sahib",
  "mumbai suburban": "mumbai",
  "sahibzada ajit singh nagar": "mohali",
  baroda: "vadodara",
  benares: "varanasi",
  banaras: "varanasi",
  mysore: "mysuru",
  mangalore: "mangaluru",
  calicut: "kozhikode",
  pondicherry: "puducherry",
  pondy: "puducherry",
  trichy: "tiruchirappalli",
  trichinopoly: "tiruchirappalli",
  vizag: "visakhapatnam",
  vizianagaram: "vizianagaram",
};

function normalize(text = "") {
  return text
    .trim()
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[.'’`]/g, "")
    .replace(/\s+/g, " ");
}

function normalizeState(state = "") {
  const key = normalize(state);
  return STATE_ALIASES[key] || key;
}

function normalizeCity(city = "") {
  const key = normalize(city);
  return CITY_ALIASES[key] || key;
}

function roundCoord(n) {
  return Math.round(Number(n) * 10000) / 10000;
}

const source = JSON.parse(readFileSync(sourcePath, "utf8"));

/** @type {Record<string, [number, number]>} */
const byKey = {};
/** @type {Record<string, { lat: number, lon: number, state: string, pop: number }>} */
const byCity = {};

for (const row of source) {
  const city = normalizeCity(row.city);
  const district = normalizeCity(row.district);
  const state = normalizeState(row.state);
  const lat = roundCoord(row.latitude);
  const lon = roundCoord(row.longitude);
  const pop = Number(row.population) || 0;

  if (!city || !state || !Number.isFinite(lat) || !Number.isFinite(lon)) continue;

  const coords = [lat, lon];
  byKey[`${city}|${state}`] = coords;

  if (district && district !== city) {
    byKey[`${district}|${state}`] = coords;
  }

  const existing = byCity[city];
  if (!existing || pop > existing.pop) {
    byCity[city] = { lat, lon, state, pop };
  }
}

// Manual fixes / NCR & common merchant profile labels not in census list
const manual = [
  ["gurugram", "haryana", 28.4595, 77.0266],
  ["noida", "uttar pradesh", 28.5355, 77.391],
  ["greater noida", "uttar pradesh", 28.4744, 77.504],
  ["fatehgarh sahib", "punjab", 30.6478, 76.3922],
  ["mumbai suburban", "maharashtra", 19.076, 72.8777],
  ["gautam buddha nagar", "uttar pradesh", 28.5355, 77.391],
  ["gautam buddh nagar", "uttar pradesh", 28.5355, 77.391],
];

for (const [city, state, lat, lon] of manual) {
  const c = normalizeCity(city);
  const s = normalizeState(state);
  byKey[`${c}|${s}`] = [lat, lon];
  if (!byCity[c]) byCity[c] = { lat, lon, state: s, pop: 0 };
}

const output = {
  _meta: {
    source: "Vynex/indian-cities-geodata + manual NCR fixes",
    count: Object.keys(byKey).length,
    built: new Date().toISOString().slice(0, 10),
  },
  byKey,
  byCity: Object.fromEntries(
    Object.entries(byCity).map(([k, v]) => [k, [v.lat, v.lon, v.state]]),
  ),
};

writeFileSync(outPath, `${JSON.stringify(output)}\n`);
console.log(`Wrote ${outPath} (${output._meta.count} city|state keys, ${Object.keys(byCity).length} cities)`);
