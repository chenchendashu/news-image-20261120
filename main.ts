// news-image-20261120 entry (Node 22, standard library only): the image is the
// entry.png beside this file, and the program copies it to /output/entry.png.
// The image is a 1024x1024 infographic drawn by render.py (Pillow) summing up
// the world news of Friday, 20 November 2026: the Trump-Putin-Xi peace
// declaration, the ICJ genocide ruling on Myanmar, COP31, Ukraine, the
// Anthropic IPO, plus the day's other headlines. The copy is byte-identical
// on every run, so the program is deterministic with no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
