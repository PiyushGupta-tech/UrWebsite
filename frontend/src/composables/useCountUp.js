/**
 * Parse display values like "75%", "02+", "30+", "99.8%" into animatable parts.
 * Values with no number, or a second number ("24/7"), are shown as-is.
 */
export function parseStatValue(value) {
  const raw = String(value);
  const match = raw.match(/^([^0-9]*)([0-9]+(?:\.[0-9]+)?)(.*)$/);
  if (!match || /[0-9]/.test(match[3])) {
    return { fixed: raw, prefix: "", target: 0, suffix: "", padMin: 0, decimals: 0 };
  }
  const [, prefix, numStr, suffix] = match;
  return {
    prefix,
    target: Number(numStr),
    suffix,
    padMin: /^0\d/.test(numStr) ? numStr.length : 0,
    decimals: numStr.split(".")[1]?.length || 0,
  };
}

export function formatStatValue(parsed, amount) {
  if (parsed.fixed !== undefined) return parsed.fixed;
  let numPart;
  if (parsed.decimals > 0) {
    numPart = amount.toFixed(parsed.decimals);
  } else {
    const int = Math.round(amount);
    numPart = parsed.padMin > 0 ? String(int).padStart(parsed.padMin, "0") : String(int);
  }
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
