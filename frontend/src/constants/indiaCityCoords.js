import { projectIndiaMap } from "@/constants/indiaMapProjection";

/** Approximate lat/lng for Indian cities used on the admin map. */
export const INDIA_CITY_COORDS = {
  mumbai: [19.076, 72.8777],
  "mumbai suburban": [19.076, 72.8777],
  delhi: [28.6139, 77.209],
  "new delhi": [28.6139, 77.209],
  bengaluru: [12.9716, 77.5946],
  bangalore: [12.9716, 77.5946],
  hyderabad: [17.385, 78.4867],
  chennai: [13.0827, 80.2707],
  kolkata: [22.5726, 88.3639],
  pune: [18.5204, 73.8567],
  ahmedabad: [23.0225, 72.5714],
  jaipur: [26.9124, 75.7873],
  lucknow: [26.8467, 80.9462],
  surat: [21.1702, 72.8311],
  indore: [22.7196, 75.8577],
  nagpur: [21.1458, 79.0882],
  kochi: [9.9312, 76.2673],
  cochin: [9.9312, 76.2673],
  bhopal: [23.2599, 77.4126],
  visakhapatnam: [17.6868, 83.2185],
  patna: [25.5941, 85.1376],
  vadodara: [22.3072, 73.1812],
  ghaziabad: [28.6692, 77.4538],
  ludhiana: [30.901, 75.8573],
  agra: [27.1767, 78.0081],
  nashik: [19.9975, 73.7898],
  faridabad: [28.4089, 77.3178],
  meerut: [28.9845, 77.7064],
  rajkot: [22.3039, 70.8022],
  varanasi: [25.3176, 82.9739],
  srinagar: [34.0837, 74.7973],
  amritsar: [31.634, 74.8723],
  ranchi: [23.3441, 85.3096],
  guwahati: [26.1445, 91.7362],
  chandigarh: [30.7333, 76.7794],
  thiruvananthapuram: [8.5241, 76.9366],
  trivandrum: [8.5241, 76.9366],
};

const STATE_NAME_TO_ID = {
  "andhra pradesh": "ap",
  bihar: "br",
  chandigarh: "ch",
  delhi: "dl",
  goa: "ga",
  gujarat: "gj",
  haryana: "hr",
  "himachal pradesh": "hp",
  karnataka: "ka",
  kerala: "kl",
  "madhya pradesh": "mp",
  maharashtra: "mh",
  punjab: "pb",
  rajasthan: "rj",
  "tamil nadu": "tn",
  telangana: "tg",
  "uttar pradesh": "up",
  "west bengal": "wb",
};

export function stateIdFromName(state = "") {
  return STATE_NAME_TO_ID[state.trim().toLowerCase()] || null;
}

export function cityCoords(city, state = "") {
  const key = (city || "").trim().toLowerCase();
  if (INDIA_CITY_COORDS[key]) return INDIA_CITY_COORDS[key];
  const stateKey = (state || "").trim().toLowerCase();
  if (INDIA_CITY_COORDS[stateKey]) return INDIA_CITY_COORDS[stateKey];
  return [20.5937, 78.9629];
}

/** Map API `summary.map_cities_today` entries to SVG pin locations. */
export function mapCitiesTodayToLocations(cities = []) {
  return cities
    .map((entry, index) => {
      const city = (entry.city || "").trim();
      if (!city) return null;

      const state = (entry.state || "").trim();
      const [lat, lon] = cityCoords(city, state);
      const { x, y } = projectIndiaMap(lat, lon);

      return {
        id: `${city.toLowerCase()}|${state.toLowerCase()}|${index}`,
        city,
        state,
        state_id: stateIdFromName(state),
        txn_count: Number(entry.txn_count) || 0,
        amount_with_fees: Number(entry.amount_with_fees) || 0,
        lat,
        lon,
        x,
        y,
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
    const [lat, lon] = cityCoords(city, state);
    const { x, y } = projectIndiaMap(lat, lon);
    const existing = groups.get(key) || {
      id: key,
      city,
      state,
      state_id: stateIdFromName(state),
      count: 0,
      amount: 0,
      lat,
      lon,
      x,
      y,
    };
    existing.count += 1;
    existing.amount += Number(tx.amount) || 0;
    groups.set(key, existing);
  }

  return [...groups.values()];
}
