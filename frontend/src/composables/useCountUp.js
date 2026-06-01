/**
 * Parse display values like "75%", "02+", "30+" into animatable parts.
 */
export function parseStatValue(value) {
  const raw = String(value);
  const match = raw.match(/^([^0-9]*)([0-9]+(?:\.[0-9]+)?)(.*)$/);
  if (!match) {
    return { prefix: "", target: 0, suffix: raw, padMin: 0 };
  }
  const [, prefix, numStr, suffix] = match;
  return {
    prefix,
    target: Number(numStr),
    suffix,
    padMin: /^0\d/.test(numStr) ? numStr.length : 0,
  };
}

export function formatStatValue(parsed, amount) {
  const int = Math.round(amount);
  const numPart =
    parsed.padMin > 0
      ? String(int).padStart(parsed.padMin, "0")
      : String(int);
  return `${parsed.prefix}${numPart}${parsed.suffix}`;
}

/**
 * Ease-out cubic 0 → 1
 */
function easeOutCubic(t) {
  return 1 - (1 - t) ** 3;
}

/**
 * Animate parsed stats; calls onFrame with formatted strings each tick.
 */
export function animateStatValues(parsedList, { duration = 1800, onFrame, onComplete }) {
  const start = performance.now();
  let frameId = 0;

  function tick(now) {
    const progress = Math.min(1, (now - start) / duration);
    const eased = easeOutCubic(progress);
    onFrame(
      parsedList.map((parsed) => formatStatValue(parsed, parsed.target * eased)),
    );
    if (progress < 1) {
      frameId = requestAnimationFrame(tick);
    } else {
      onComplete?.();
    }
  }

  frameId = requestAnimationFrame(tick);

  return () => {
    if (frameId) cancelAnimationFrame(frameId);
  };
}
