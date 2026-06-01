import { chromium } from "playwright";
import indiaMap from "@svg-maps/india";

const map = indiaMap.default ?? indiaMap;
const anchors = {
  pb: { x: 152, y: 156 },
  ch: { x: 180, y: 160 },
  hr: { x: 168, y: 196 },
  dl: { x: 188, y: 212 },
  mp: { x: 212, y: 328 },
  mh: { x: 168, y: 420 },
  ka: { x: 168, y: 524 },
  tg: { x: 228, y: 460 },
  tn: { x: 216, y: 604 },
  rj: { x: 120, y: 260 },
  gj: { x: 72, y: 348 },
};
const pins = [
  ["ludhiana", "pb", 0, 0],
  ["chandigarh", "ch", 0, 0],
  ["kurukshetra", "hr", 0, 0],
  ["gurugram", "hr", 16, -28],
  ["delhi-shadval", "dl", 0, 0],
  ["delhi-mobitm", "dl", -4, -4],
  ["delhi-evelocy", "dl", 0, 4],
  ["rajgarh-greenweb", "mp", 0, 0],
  ["indore", "mp", 0, -32],
  ["mp-greenweb-bhopal", "mp", -32, 0],
  ["pune", "mh", 0, 0],
  ["bengaluru-quickwave", "ka", 0, 0],
  ["bengaluru-vyaptrix", "ka", 0, -32],
  ["bengaluru-aai", "ka", -32, 0],
  ["ka-syllogi", "ka", 0, 32],
  ["hyderabad-indyapay", "tg", 0, 0],
  ["hyderabad-skriptonic", "tg", 0, -32],
  ["tn-kuberan", "tn", 0, 0],
  ["tn-unibeck", "tn", 0, -32],
  ["rajasthan-groots", "rj", 0, 0],
  ["gujarat-ojct", "gj", 0, 0],
  ["gujarat-luxpay", "gj", 0, -32],
];

const html = map.locations.map((l) => `<path id="${l.id}" d="${l.path}"/>`).join("");
const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 696">${html}</svg>`,
);
const inside = (sid, x, y) =>
  page.evaluate(
    ({ sid, x, y }) =>
      document.getElementById(sid)?.isPointInFill(new DOMPoint(x, y)) ?? false,
    { sid, x, y },
  );
const find = (x, y) =>
  page.evaluate(
    ({ x, y, ids }) =>
      ids.filter((id) =>
        document.getElementById(id)?.isPointInFill(new DOMPoint(x, y)),
      ),
    { x, y, ids: map.locations.map((l) => l.id) },
  );

let ok = 0;
for (const [id, sid, ox, oy] of pins) {
  const a = anchors[sid];
  const x = a.x + ox;
  const y = a.y + oy;
  const v = await inside(sid, x, y);
  const act = v ? [sid] : await find(x, y);
  if (v) ok++;
  console.log(
    `${v ? "OK" : "FAIL"} ${id} @(${x},${y})${v ? "" : " -> " + act.join(",")}`,
  );
}
console.log(`${ok}/${pins.length}`);
await browser.close();
