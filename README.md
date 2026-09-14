# cortex-hit-encode

Encode hit vs matched non-hit stimuli with [VideoCortex](https://github.com/sw30labs/videocortex) / [TRIBE v2](https://github.com/facebookresearch/tribev2). Compare predicted **average-subject** cortical maps. Learn whether “hitness” leaves a fingerprint in the encoding — not whether a song will chart.

**Status:** design phase (hypothesis + ADR + plan). No batch encodes required to clone this repo.

## What this is

- A **separate** sw30labs experiment repo.
- **Encoding only:** stimulus in → predicted fMRI out.
- Comparative: commercial hits vs genre-matched non-hits, with confound controls.
- Cool on purpose. Honest on purpose.

## What this is not

- Not a decoder (no fMRI → song).
- Not a mind-reader; not *your* cortex — TRIBE’s **average subject**.
- Not a hit predictor. Never `hit_probability`. Never “ensure a hit.”
- **Not wired** into [artist-twin](https://github.com/sw30labs) Compose Album / Track. Artist-twin’s Insight `hit_patterns` craft scores stay separate.

See [docs/non-goals.md](docs/non-goals.md).

## Documents

| Doc | Role |
|---|---|
| [docs/hypothesis.md](docs/hypothesis.md) | H1 / H0 / confound alternatives, predictions, falsifiers |
| [docs/adr/001-cortex-hit-encode.md](docs/adr/001-cortex-hit-encode.md) | Decision record |
| [docs/experiment-plan.md](docs/experiment-plan.md) | Phased plan, metrics, risks |
| [docs/protocol.md](docs/protocol.md) | Pilot checklist (e.g. 8+8 rock-español / Indio-adjacent) |
| [NOTICE.md](NOTICE.md) | TRIBE NC + stimulus rights |

## Instrument

Use the sibling VideoCortex CLI/deck for encodes. This repo stores **cohort manifests, run metadata, analysis, and claims discipline** — it does not vendor TRIBE weights.

```bash
# later, once past design phase:
# videocortex doctor
# videocortex render --video path/to/stimulus.mp4   # or audio-primary workflow per VideoCortex docs
```

## Layout

```
stimuli/     # rights-cleared clips live outside git by default; manifests only
runs/        # encode outputs / pointers (large binaries gitignored)
analysis/    # notebooks / scripts for ROI diffs
docs/        # hypothesis, ADR, plan, protocol
```

## Language ban list (UX + papers)

Say: *hit-labeled cohort*, *encode separation*, *predicted cortical response*, *hit-shaped craft* (only if bridging later).

Never: `hit_probability`, “likely a hit,” “% chance,” Billboard forecast, “this is what someone is thinking,” decoder claims.

## License

Code in this repository: MIT (see `LICENSE` if present).

TRIBE v2 weights and upstream model: **CC-BY-NC-4.0** — research / non-commercial. Stimulus files: you must hold rights; do not commit unlicensed media.
