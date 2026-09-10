/**
 * Maps viewport width onto a 0→1 band progress:
 *   0    = mobile anchor (390)
 *   0.5  = tablet / iPad Figma (1024)
 *   1    = laptop (1440)
 * Writes --ur-band on <html> for CSS that needs continuous proximity.
 */
const MOBILE = 390;
const TABLET = 1024;
const LAPTOP = 1440;

function bandProgress(width) {
  if (width <= MOBILE) return 0;
  if (width <= TABLET) return ((width - MOBILE) / (TABLET - MOBILE)) * 0.5;
  if (width <= LAPTOP) return 0.5 + ((width - TABLET) / (LAPTOP - TABLET)) * 0.5;
  return 1;
}

export function startResponsiveBand() {
  if (typeof window === "undefined") return () => {};

  let raf = 0;

  const apply = () => {
    raf = 0;
    const t = bandProgress(window.innerWidth);
    document.documentElement.style.setProperty("--ur-band", String(Number(t.toFixed(4))));
  };

  const onResize = () => {
    if (raf) return;
    raf = requestAnimationFrame(apply);
  };

  apply();
  window.addEventListener("resize", onResize, { passive: true });

  return () => {
    window.removeEventListener("resize", onResize);
    if (raf) cancelAnimationFrame(raf);
  };
}
