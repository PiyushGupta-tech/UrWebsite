import { projectIndiaMap } from "@/constants/indiaMapProjection";

/**
 * ViewBox anchors per state — derived from SVG isPointInFill sampling on @svg-maps/india.
 * Pin positions = anchor + offset_x/offset_y from merchant_map.py.
 */
export const STATE_ANCHORS = {
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

export function pinPosition(loc) {
  if (loc.x != null && loc.y != null) {
    return { x: loc.x, y: loc.y };
  }

  const anchor = STATE_ANCHORS[loc.state_id];
  if (anchor) {
    return {
      x: anchor.x + (loc.offset_x ?? 0),
      y: anchor.y + (loc.offset_y ?? 0),
    };
  }

  if (loc.lat != null && loc.lon != null) {
    return projectIndiaMap(loc.lat, loc.lon);
  }

  return { x: 0, y: 0 };
}
