# HyperFrames gotchas that bite these kits

Collected while building the nine styles (HyperFrames 0.8.81). Each one cost a debugging round.

## Layout and contrast checks

- Text with a fully transparent fill (ghost / outline-only letters) fails `text_not_painted`. Use at least a 15 % fill
  plus the stroke, and `visibility: hidden` for whole lines that have not appeared yet.
- `data-layout-allow-overlap` must sit on the text element itself; on a parent it has no effect.
- Elements under a 3D perspective (rotateX) are checked by their projected bounding boxes, which overlap where the
  real glyphs do not. Pull genuinely close text apart first; mark intended layering on the text element.
- The contrast check samples inside the element's own box: a stamp with a same-coloured double border reads as its
  own background (false 1.2:1). Wrap the text in a span.
- A layer that covers text (an overlay, a badge) makes both `text_occluded` and contrast fail. Give it its own space
  instead of covering the scene.

## Timing and determinism

- Every frame must be a pure function of t: no `Math.random`, `Date.now`, network fetches; seed with
  `ExplainerCore.hash`.
- Durations live in static HTML (`data-duration`). When the story is re-timed, run `tools/stamp.py` (elements carry
  `data-stamp="story" | "narration"`).
- A camera driven by your own Hermite keys needs Fritsch–Carlson tangent limiting, or a long hold followed by a fast
  move overshoots by hundreds of pixels (`ExplainerCore.track` does this).
- Pixel-still holds read as a frozen video (freezedetect `n=-60dB:d=0.4`). Check snapshot pairs 0.3 s apart (mean
  absolute difference > 0.001) in mid-chapter, between lines, the closing line and the end of the recap; a parked
  camera or a recap push that eases to a full stop are the usual causes.

## Three.js (V6, V9)

- Use the Three.js adapter: the root carries `data-no-timeline`, render on the `hf-seek` event.
- HTML labels projected with `vector.project(camera)` need `camera.updateMatrixWorld()` right after `lookAt` in the
  per-frame camera code, or they use last frame's matrices (wrong positions after any seek).
- With `VSMShadowMap`, `castShadow = false` is not enough for glass, light cones or ghosts: meshes that receive
  shadows are still drawn into the shadow map. Turn both off (V9 `noShadow`) and hide see-through things from GTAO
  (`noAO`).

## Fonts and text

- Subset fonts to the characters used (`tools/fonts.py` scans `index.html`, root `*.js` and `lib/**/*.js`); rerun it
  after every text change, including text written from JavaScript.
- ZCOOL XiaoWei draws 回 with a solid inner square; V3 borrows that one glyph from Noto Serif SC (`fix-56de.woff2`).
  Check display fonts for broken CJK glyphs before relying on them.
- ZCOOL KuaiLe has no `≈ → ∝ ✓`; condensed Latin display faces squeeze CJK — set CJK in a CJK face.

## CLI

- `hyperframes snapshot -o <dir>` empties `<dir>` first.
- `snapshot` sends frames to a vision model when `GEMINI_API_KEY` is set; pass `--describe false` to keep them local.
- Do not edit a shell script while it runs — bash reads it lazily and the edit can land mid-run.
