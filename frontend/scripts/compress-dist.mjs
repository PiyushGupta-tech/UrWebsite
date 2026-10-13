/**
 * Write .br and .gz siblings for text assets in dist/ so Django can serve them
 * pre-compressed (see backend/website/static_serve.py). Runs after `vite build`.
 */
import { readdir, readFile, stat, writeFile } from "node:fs/promises";
import { join, extname } from "node:path";
import { fileURLToPath } from "node:url";
import { brotliCompressSync, constants, gzipSync } from "node:zlib";

const DIST = fileURLToPath(new URL("../dist", import.meta.url));
const EXTENSIONS = new Set([".js", ".css", ".svg", ".json", ".webmanifest", ".xml", ".txt", ".map"]);
const MIN_BYTES = 1024;
/* Brotli 11 is slow on multi-megabyte SVGs; 9 keeps the build quick for those. */
const LARGE_BYTES = 256 * 1024;

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(path);
    else if (entry.isFile()) yield path;
  }
}

let files = 0;
let before = 0;
let afterBr = 0;
const started = Date.now();

for await (const path of walk(DIST)) {
  if (!EXTENSIONS.has(extname(path).toLowerCase())) continue;
  const { size } = await stat(path);
  if (size < MIN_BYTES) continue;
  const source = await readFile(path);
  const br = brotliCompressSync(source, {
    params: {
      [constants.BROTLI_PARAM_QUALITY]: size > LARGE_BYTES ? 9 : 11,
      [constants.BROTLI_PARAM_SIZE_HINT]: size,
    },
  });
  const gz = gzipSync(source, { level: 9 });
  // Skip files that barely shrink; serving the original is just as fast.
  if (gz.length < size * 0.9) await writeFile(`${path}.gz`, gz);
  if (br.length < size * 0.9) await writeFile(`${path}.br`, br);
  files += 1;
  before += size;
  afterBr += Math.min(br.length, size);
}

const mb = (n) => (n / 1024 / 1024).toFixed(1);
console.log(
  `compress-dist: ${files} files, ${mb(before)} MB -> ${mb(afterBr)} MB brotli in ${((Date.now() - started) / 1000).toFixed(1)}s`,
);
