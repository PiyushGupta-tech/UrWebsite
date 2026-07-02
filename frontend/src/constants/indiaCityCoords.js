import cityIndex from "@/constants/indiaCityIndex.json";
import { STATE_ANCHORS } from "@/constants/indiaMapAnchors";
import { projectIndiaMap } from "@/constants/indiaMapProjection";

const { byKey, byCity } = cityIndex;

const STATE_ALIASES = {
  "andaman and nicobar islands": "andaman and nicobar islands",
  "andaman & nicobar islands": "andaman and nicobar islands",
  "jammu and kashmir": "jammu and kashmir",
  "jammu & kashmir": "jammu and kashmir",
  "dadra and nagar haveli and daman and diu": "dadra and nagar haveli",
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
  trichy: "tiruchirappalli",
  vizag: "visakhapatnam",
};

const STATE_NAME_TO_ID = {
  "andaman and nicobar islands": "an",
  "andhra pradesh": "ap",
  "arunachal pradesh": "ar",
  assam: "as",
  bihar: "br",
  chandigarh: "ch",
  chhattisgarh: "cg",
  delhi: "dl",
  goa: "ga",
  gujarat: "gj",
  haryana: "hr",
  "himachal pradesh": "hp",
  jharkhand: "jh",
  karnataka: "ka",
  kerala: "kl",
  "madhya pradesh": "mp",
  maharashtra: "mh",
  manipur: "mn",
  meghalaya: "ml",
  mizoram: "mz",
  nagaland: "nl",
  odisha: "or",
  punjab: "pb",
  rajasthan: "rj",
  sikkim: "sk",
  "tamil nadu": "tn",
  telangana: "tg",
  tripura: "tr",
  "uttar pradesh": "up",
  uttarakhand: "ut",
  "west bengal": "wb",
  "dadra and nagar haveli": "dn",
  "daman and diu": "dd",
  ladakh: "la",
  puducherry: "py",
  lakshadweep: "ld",
};

/** Approximate state centroids when city is unknown but state is known. */
const STATE_CENTROID = {
  an: [11.6234, 92.7265],
  ap: [15.9129, 79.74],
  ar: [28.218, 94.7278],
  as: [26.2006, 92.9376],
  br: [25.0961, 85.3131],
  cg: [21.2787, 81.8661],
  ch: [30.7333, 76.7794],
  dl: [28.6139, 77.209],
  ga: [15.2993, 74.124],
  gj: [22.2587, 71.1924],
  hp: [31.1048, 77.1734],
  hr: [29.0588, 76.0856],
  jh: [23.6102, 85.2799],
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
  la: [34.1526, 77.577],
  py: [11.9416, 79.8083],
  ld: [10.5667, 72.6417],
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

export function stateIdFromName(state = "") {
  return STATE_NAME_TO_ID[normalizeState(state)] || null;
}

function lookupCityCoords(city, state = "") {
  const cityKey = normalizeCity(city);
  const stateKey = normalizeState(state);

  if (!cityKey) return null;

  if (stateKey && byKey[`${cityKey}|${stateKey}`]) {
    return byKey[`${cityKey}|${stateKey}`];
  }

  const entry = byCity[cityKey];
  if (entry) {
    const [lat, lon, entryState] = entry;
    if (!stateKey || entryState === stateKey) return [lat, lon];
    if (byKey[`${cityKey}|${entryState}`]) return byKey[`${cityKey}|${entryState}`];
  }

  return null;
}

/**
 * Resolve SVG pin position for a city/state pair.
 * 1. Census city index (528+ cities, pop > 100k, 2011 + manual fixes)
 * 2. State SVG anchor
 * 3. State centroid projection
 * 4. India geographic center (last resort)
 */
export function resolveMapPin(city, state = "") {
  const state_id = stateIdFromName(state);
  const coords = lookupCityCoords(city, state);

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

/** Map API `summary.map_cities_today` entries to SVG pin locations. */
export function mapCitiesTodayToLocations(cities = []) {
  return cities
    .map((entry, index) => {
      const city = (entry.city || "").trim();
      if (!city) return null;

      const state = (entry.state || "").trim();
      const pin = resolveMapPin(city, state);

      return {
        id: `${city.toLowerCase()}|${state.toLowerCase()}|${index}`,
        city,
        state,
        state_id: pin.state_id,
        txn_count: Number(entry.txn_count) || 0,
        amount_with_fees: Number(entry.amount_with_fees) || 0,
        lat: pin.lat,
        lon: pin.lon,
        x: pin.x,
        y: pin.y,
      };
    })
    .filter(Boolean);
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
