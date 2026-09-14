<p align="right"><img src="docs/aineko.svg" alt="" width="56" /></p>

# cortex-hit-encode

Encode hit vs matched non-hit stimuli with [VideoCortex](https://github.com/sw30labs/videocortex) / [TRIBE v2](https://github.com/facebookresearch/tribev2). Compare predicted **average-subject** cortical maps. Learn whether “hitness” leaves a fingerprint in the encoding — not whether a song will chart.

**Status:** self-contained instrument + design phase (hypothesis + ADR + plan + Phase 1 freeze checklist). Clone and install this repo to encode — no sibling VideoCortex checkout. No batch encodes required to clone. No results yet.

## What this is

- A **separate** sw30labs experiment repo.
- **Encoding only:** stimulus in → predicted fMRI out.
- Comparative: commercial hits vs genre-matched non-hits, with confound controls.
- Cool on purpose. Honest on purpose.

## What this is not

- Not a decoder (no fMRI → song).
- Not a mind-reader; not *your* cortex — TRIBE’s **average subject**. Never “this is what someone is thinking.”
- Not a hit predictor. Never `hit_probability`, “likely a hit,” “% chance,” Billboard / chart forecast, or “ensure a hit.”
- **Not wired** into [artist-twin](https://github.com/sw30labs) Compose Album / Track. Artist-twin’s Insight `hit_patterns` craft scores stay separate.

See [docs/non-goals.md](docs/non-goals.md).

## Documents

| Doc | Role |
|---|---|
| [docs/hypothesis.md](docs/hypothesis.md) | H1 / H0 / H2 / H3 (H4 deferred), predictions, falsifiers |
| [docs/adr/001-cortex-hit-encode.md](docs/adr/001-cortex-hit-encode.md) | Experiment decision record |
| [docs/adr/002-self-contained-instrument.md](docs/adr/002-self-contained-instrument.md) | Vendored `che` instrument |
| [docs/experiment-plan.md](docs/experiment-plan.md) | Phased plan; primary endpoint `mean_auditory_roi_energy` |
| [docs/protocol.md](docs/protocol.md) | Phase 1 freeze checklist + pilot steps |
| [docs/non-goals.md](docs/non-goals.md) | Binding non-goals + canonical language ban |
| [NOTICE.md](NOTICE.md) | TRIBE NC + stimulus rights |

## Instrument

This repo vendors the VideoCortex **encode / render / doctor / fetch** path as package `cortex_hit_encode`. CLI: **`che`** (also `cortex-hit-encode`). VideoCortex is an upstream *reference* only — do not depend on a sibling checkout at runtime, do not edit that tree, do not re-download weights when a local cache already has them.

This repo still does **not** vendor TRIBE weights or media. Copy or hardlink them in.

```bash
python -m pip install -e '.[dev]'          # renderer + doctor (no torch)
# python -m pip install -e '.[predict,dev]'  # + tribev2 + torch, for encodes

# Weights: copy from an existing VideoCortex / HuggingFace cache. Never re-download.
scripts/import-weights.sh --from /path/to/videocortex-or-hf-cache
# or, if the hub and feature cache live in different places:
# scripts/import-weights.sh \
#   --hf-src "$HF_HOME/hub" \
#   --feature-src /path/to/videocortex/.videocortex-cache

che doctor --offline
che render --audio path/to/stimulus.wav    # v0 is audio-primary; --video only if freeze says so
```

### Caches (private data root)

| What | Default | Override |
|---|---|---|
| Feature cache (`--cache-dir`) | `./.che-cache` (gitignored) | `CORTEX_HIT_ENCODE_CACHE` |
| HuggingFace hub (TRIBE + four encoders) | `$HF_HOME/hub` or `~/.cache/huggingface/hub` | `HF_HOME` or `HUGGINGFACE_HUB_CACHE` |

Point `HF_HOME` / `HUGGINGFACE_HUB_CACHE` at a **private** volume (e.g. `/Volumes/DATA/cortex-hit-encode/hf`), not a VideoCortex checkout. `import-weights.sh` prefers hardlinks when source and dest share a filesystem. It never calls HuggingFace when the sources exist.

`che fetch` is a last-resort download if you truly have no local copy. Prefer the import script.

The VideoCortex command deck (`serve` / web) is **not** vendored.

## Layout

```
src/cortex_hit_encode/   # vendored encode instrument (che)
scripts/import-weights.sh
stimuli/                 # rights-cleared clips live outside git; manifests only
runs/                    # encode outputs / pointers (binaries gitignored)
analysis/                # Phase 4 outline only — no results yet
docs/                    # hypothesis, ADRs, plan, protocol, non-goals
.che-cache/              # feature cache (gitignored)
```

## Language ban list (UX + papers)

Canonical copy lives in [docs/non-goals.md](docs/non-goals.md). Same list here:

**Say:** *hit-labeled cohort*, *encode separation*, *predicted cortical response*, *predicted average-subject maps*. *hit-shaped craft* only if bridging later (H4, deferred).

**Never:** `hit_probability`, “likely a hit,” “% chance,” Billboard forecast, chart forecast, “ensure a hit,” “this is what someone is thinking,” mind-reading, decoder claims.

## License

Code in this repository: MIT (see `LICENSE` if present).

TRIBE v2 weights and upstream model: **CC-BY-NC-4.0** — research / non-commercial. Stimulus files: you must hold rights; do not commit unlicensed media.
