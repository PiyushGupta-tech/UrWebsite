/** Project lat/lon to @svg-maps/india viewBox (0 0 612 696). */
const VIEWBOX = { width: 612, height: 696 };
const BOUNDS = { minLon: 68.0, maxLon: 97.5, minLat: 6.5, maxLat: 37.5 };

export function projectIndiaMap(lat, lon) {
  const x =
    ((lon - BOUNDS.minLon) / (BOUNDS.maxLon - BOUNDS.minLon)) * VIEWBOX.width * 0.86 +
    VIEWBOX.width * 0.07;
  const y =
    ((BOUNDS.maxLat - lat) / (BOUNDS.maxLat - BOUNDS.minLat)) * VIEWBOX.height * 0.9 +
    VIEWBOX.height * 0.05;
  return { x, y };
}

export const INDIA_MAP_VIEWBOX = `0 0 ${VIEWBOX.width} ${VIEWBOX.height}`;
