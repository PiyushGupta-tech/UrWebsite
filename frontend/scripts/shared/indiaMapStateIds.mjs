/** State / UT name → @svg-maps/india path id */
export const STATE_NAME_TO_ID = {
  "andaman and nicobar islands": "an",
  "andhra pradesh": "ap",
  "arunachal pradesh": "ar",
  assam: "as",
  bihar: "br",
  chandigarh: "ch",
  chhattisgarh: "ct",
  delhi: "dl",
  goa: "ga",
  gujarat: "gj",
  haryana: "hr",
  "himachal pradesh": "hp",
  jharkhand: "jh",
  "jammu and kashmir": "jk",
  ladakh: "jk",
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
  "dadra and nagar haveli and daman and diu": "dn",
  puducherry: "py",
  lakshadweep: "ld",
};

export const STATE_ALIASES = {
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

export const CITY_ALIASES = {
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

export function normalize(text = "") {
  return text
    .trim()
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[.'’`]/g, "")
    .replace(/\s+/g, " ");
}

export function normalizeState(state = "") {
  const key = normalize(state);
  return STATE_ALIASES[key] || key;
}

export function normalizeCity(city = "") {
  const key = normalize(city);
  return CITY_ALIASES[key] || key;
}

export function stateIdFromName(state = "") {
  return STATE_NAME_TO_ID[normalizeState(state)] || null;
}
