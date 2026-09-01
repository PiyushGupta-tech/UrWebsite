import cityIndex from "@/constants/indiaCityIndex.json";
import svgCoords from "@/constants/indiaCitySvgCoords.json";
import { STATE_ANCHORS } from "@/constants/indiaMapAnchors";
import { projectIndiaMap } from "@/constants/indiaMapProjection";
import {
  normalize,
  normalizeCity,
  normalizeState,
  stateIdFromName,
} from "@/constants/indiaMapStateIds";

const { byKey: geoByKey, byCity: geoByCity } = cityIndex;
const { byKey: svgByKey, byCity: svgByCity } = svgCoords;

/** Approximate state centroids when city is unknown but state is known. */
const STATE_CENTROID = {
  an: [11.6234, 92.7265],
  ap: [15.9129, 79.74],
  ar: [28.218, 94.7278],
  as: [26.2006, 92.9376],
  br: [25.0961, 85.3131],
  ct: [21.2787, 81.8661],
  ch: [30.7333, 76.7794],
  dl: [28.6139, 77.209],
  ga: [15.2993, 74.124],
  gj: [22.2587, 71.1924],
  hp: [31.1048, 77.1734],
  hr: [29.0588, 76.0856],
  jh: [23.6102, 85.2799],
  jk: [34.0837, 77.577],
  ka: [15.3173, 75.7139],
  kl: [10.8505, 76.2711],
  mh: [19.7515, 75.7139],
  ml: [25.467, 91.3662],
  mn: [24.6637, 93.9063],
  mp: [22.9734, 78.6569],
  mz: [23.1645, 92.9376],
  nl: [26.1584, 94.5624],
  or: [20.9517, 85.0985],
  pb: [31.1471, 75.3412],
  rj: [27.0238, 74.2179],
  sk: [27.533, 88.5122],
  tg: [18.1124, 79.0193],
  tn: [11.1271, 78.6569],
  tr: [23.9408, 91.9882],
  up: [26.8467, 80.9462],
  ut: [30.0668, 79.0193],
  wb: [22.9868, 87.855],
  dn: [20.1809, 73.0169],
  dd: [20.4283, 72.8397],
  py: [11.9416, 79.8083],
  ld: [10.5667, 72.6417],
};

export { normalize, normalizeCity, normalizeState, stateIdFromName };

function lookupCityCoords(city, state = "") {
  const cityKey = normalizeCity(city);
  const stateKey = normalizeState(state);

  if (!cityKey) return null;

  if (stateKey && geoByKey[`${cityKey}|${stateKey}`]) {
    return geoByKey[`${cityKey}|${stateKey}`];
  }

  const entry = geoByCity[cityKey];
  if (entry) {
    const [lat, lon, entryState] = entry;
    if (!stateKey || entryState === stateKey) return [lat, lon];
    if (geoByKey[`${cityKey}|${entryState}`]) return geoByKey[`${cityKey}|${entryState}`];
  }

  return null;
}

function lookupSvgPin(city, state = "") {
  const cityKey = normalizeCity(city);
  const stateKey = normalizeState(state);

  if (!cityKey) return null;

  if (stateKey && svgByKey[`${cityKey}|${stateKey}`]) {
    const [x, y, state_id] = svgByKey[`${cityKey}|${stateKey}`];
    return { x, y, state_id };
  }

  const entry = svgByCity[cityKey];
  if (entry) {
    const [x, y, state_id] = entry;
    if (!stateKey || stateIdFromName(stateKey) === state_id) {
      return { x, y, state_id };
    }
  }

  return null;
}

/**
 * Resolve SVG viewBox pin for a city/state pair.
 * Uses precomputed coordinates snapped to @svg-maps/india state boundaries.
 */
export function resolveMapPin(city, state = "") {
  const coords = lookupCityCoords(city, state);
  const svgPin = lookupSvgPin(city, state);
  const state_id = stateIdFromName(state);

  if (svgPin) {
    return {
      lat: coords?.[0] ?? null,
      lon: coords?.[1] ?? null,
      state_id: svgPin.state_id,
      x: svgPin.x,
      y: svgPin.y,
    };
  }

  if (coords) {
    const [lat, lon] = coords;
    const { x, y } = projectIndiaMap(lat, lon);
    return { lat, lon, state_id, x, y };
  }

  if (state_id && STATE_ANCHORS[state_id]) {
    const { x, y } = STATE_ANCHORS[state_id];
    return { lat: null, lon: null, state_id, x, y };
  }

  if (state_id && STATE_CENTROID[state_id]) {
    const [lat, lon] = STATE_CENTROID[state_id];
    const { x, y } = projectIndiaMap(lat, lon);
    return { lat, lon, state_id, x, y };
  }

  const [lat, lon] = [20.5937, 78.9629];
  const { x, y } = projectIndiaMap(lat, lon);
  return { lat, lon, state_id, x, y };
}

/** @deprecated Use resolveMapPin; returns [lat, lon] only. */
export function cityCoords(city, state = "") {
  const coords = lookupCityCoords(city, state);
  if (coords) return coords;
  const state_id = stateIdFromName(state);
  if (state_id && STATE_CENTROID[state_id]) return STATE_CENTROID[state_id];
  return [20.5937, 78.9629];
}

/** Build city → merchant name lookup from top_providers_today. */
export function buildCityMerchantLookup(providers = [], kind = "payout") {
  const byCityState = new Map();
  const byCity = new Map();
  const byStats = new Map();

  for (const provider of providers) {
    const name = (provider.name || provider.userid || "").trim();
    if (!name) continue;

    const city = normalizeCity(provider.location?.city || provider.city || "");
    const state = normalizeState(provider.location?.state || provider.state || "");
    if (!city) continue;

    const cityStateKey = `${kind}|${city}|${state}`;
    if (!byCityState.has(cityStateKey)) {
      byCityState.set(cityStateKey, name);
    }

    const cityKey = `${kind}|${city}`;
    if (!byCity.has(cityKey)) {
      byCity.set(cityKey, name);
    }

    const txnCount = Number(provider.txn_count) || 0;
    const amount = roundAmount(provider.amount_with_fees ?? provider.amount);
    const statsKey = `${kind}|${txnCount}|${amount}`;
    if (!byStats.has(statsKey)) {
      byStats.set(statsKey, name);
    }
  }

  return { byCityState, byCity, byStats };
}

function roundAmount(value) {
  return Math.round((Number(value) || 0) * 100) / 100;
}

/** Extend lookup using latest_transactions grouped by merchant city. */
export function extendMerchantLookupFromTransactions(lookup, transactions = [], kind = "payout") {
  const txByCityState = new Map();
  const txByCity = new Map();

  for (const tx of transactions) {
    const merchant = tx.merchant || {};
    const location = merchant.location || {};
    const name = (merchant.name || tx.userid || "").trim();
    const city = normalizeCity(location.city || merchant.city || tx.city || "");
    const state = normalizeState(location.state || merchant.state || tx.state || "");
    if (!name || !city) continue;

    const cityStateKey = `${kind}|${city}|${state}`;
    const cityKey = `${kind}|${city}`;
    const cityStateCounts = txByCityState.get(cityStateKey) || {};
    cityStateCounts[name] = (cityStateCounts[name] || 0) + 1;
    txByCityState.set(cityStateKey, cityStateCounts);

    const cityCounts = txByCity.get(cityKey) || {};
    cityCounts[name] = (cityCounts[name] || 0) + 1;
    txByCity.set(cityKey, cityCounts);
  }

  for (const [key, counts] of txByCityState) {
    if (lookup.byCityState.has(key)) continue;
    const top = topMerchantName(counts);
    if (top) lookup.byCityState.set(key, top);
  }

  for (const [key, counts] of txByCity) {
    if (lookup.byCity.has(key)) continue;
    const top = topMerchantName(counts);
    if (top) lookup.byCity.set(key, top);
  }

  return lookup;
}

function topMerchantName(counts) {
  let best = "";
  let bestCount = 0;
  for (const [name, count] of Object.entries(counts)) {
    if (count > bestCount) {
      best = name;
      bestCount = count;
    }
  }
  return best;
}

/** Resolve merchant display name for a map city entry. */
export function resolveMerchantName(entry, kind, lookup) {
  const explicit = (entry.merchant_name || "").trim();
  if (explicit) return explicit;

  const city = normalizeCity(entry.city || "");
  const state = normalizeState(entry.state || "");
  if (!city) return "";

  const txnCount = Number(entry.txn_count) || 0;
  const amount = roundAmount(entry.amount_with_fees ?? entry.amount);
  const statsKey = `${kind}|${txnCount}|${amount}`;

  return (
    lookup.byCityState.get(`${kind}|${city}|${state}`)
    || lookup.byCity.get(`${kind}|${city}`)
    || lookup.byStats.get(statsKey)
    || ""
  );
}

/** Map API `summary.map_cities_today` entries to SVG pin locations. */
export function mapCitiesTodayToLocations(cities = [], kind = "payout") {
  return cities
    .map((entry, index) => {
      const city = (entry.city || "").trim();
      if (!city) return null;

      const state = (entry.state || "").trim();
      const pin = resolveMapPin(city, state);
      const amount =
        Number(entry.amount_with_fees) || Number(entry.amount) || 0;

      return {
        id: `${kind}|${city.toLowerCase()}|${state.toLowerCase()}|${index}`,
        kind,
        city,
        state,
        merchant_name: (entry.merchant_name || "").trim(),
        state_id: pin.state_id,
        txn_count: Number(entry.txn_count) || 0,
        amount_with_fees: amount,
        lat: pin.lat,
        lon: pin.lon,
        x: pin.x,
        y: pin.y,
      };
    })
    .filter(Boolean);
}

/** Merge payout + payin city pins; nudge payin pins when they overlap payout. */
export function mergeMapCityLayers(payoutCities = [], payinCities = []) {
  const payout = mapCitiesTodayToLocations(payoutCities, "payout");
  const payin = mapCitiesTodayToLocations(payinCities, "payin");
  const occupied = new Set(payout.map((loc) => `${Math.round(loc.x)}|${Math.round(loc.y)}`));

  for (const loc of payin) {
    const key = `${Math.round(loc.x)}|${Math.round(loc.y)}`;
    if (occupied.has(key)) {
      loc.x += 8;
      loc.y -= 8;
    }
    occupied.add(`${Math.round(loc.x)}|${Math.round(loc.y)}`);
  }

  return [...payout, ...payin];
}

export function groupTransactionsByCity(transactions = []) {
  const groups = new Map();

  for (const tx of transactions) {
    const location = tx.merchant?.location;
    const city = (location?.city || tx.merchant?.city || tx.city || "").trim();
    if (!city) continue;

    const state = (location?.state || tx.merchant?.state || tx.state || "").trim();
    const key = `${city.toLowerCase()}|${state.toLowerCase()}`;
    const pin = resolveMapPin(city, state);
    const existing = groups.get(key) || {
      id: key,
      city,
      state,
      state_id: pin.state_id,
      count: 0,
      amount: 0,
      lat: pin.lat,
      lon: pin.lon,
      x: pin.x,
      y: pin.y,
    };
    existing.count += 1;
    existing.amount += Number(tx.amount) || 0;
    groups.set(key, existing);
  }

  return [...groups.values()];
}
