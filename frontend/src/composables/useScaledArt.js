import { onBeforeUnmount } from "vue";

/**
 * Scales a graphic drawn at a fixed width down to its frame.
 * Bind the returned function as a ref on the frame; its first child is the graphic.
 * The frame gets `--<prefix>-art-scale` (frame width / graphic width) and
 * `--<prefix>-art-height` (scaled graphic height) for the CSS to use.
 */
export function useScaledArt(prefix) {
  const scaleVar = `--${prefix}-art-scale`;
  const heightVar = `--${prefix}-art-height`;
  const frames = new Set();
  let observer = null;

  function sync(frame) {
    const art = frame.firstElementChild;
    if (!art || !art.offsetWidth) return;
    const scale = frame.clientWidth / art.offsetWidth;
    frame.style.setProperty(scaleVar, String(scale));
    frame.style.setProperty(heightVar, `${art.offsetHeight * scale}px`);
  }

  function forget(frame) {
    frames.delete(frame);
    if (!observer) return;
    observer.unobserve(frame);
    if (frame.firstElementChild) observer.unobserve(frame.firstElementChild);
  }

  function register(frame) {
    if (!frame) {
      frames.forEach((known) => {
        if (!known.isConnected) forget(known);
      });
      return;
    }
    if (frames.has(frame)) return;
    frames.add(frame);
    if (typeof ResizeObserver === "undefined") {
      sync(frame);
      return;
    }
    if (!observer) {
      observer = new ResizeObserver((entries) => {
        entries.forEach(({ target }) => {
          const frameEl = frames.has(target) ? target : target.parentElement;
          if (!frameEl || !frames.has(frameEl)) return;
          if (frameEl.isConnected) sync(frameEl);
          else forget(frameEl);
        });
      });
    }
    observer.observe(frame);
    if (frame.firstElementChild) observer.observe(frame.firstElementChild);
  }

  onBeforeUnmount(() => {
    observer?.disconnect();
    observer = null;
    frames.clear();
  });

  return register;
}
