<p align="right"><img src="docs/aineko.svg" alt="" width="56" /></p>

# cortex-hit-encode

Encode hit vs matched non-hit stimuli with [VideoCortex](https://github.com/sw30labs/videocortex) / [TRIBE v2](https://github.com/facebookresearch/tribev2). Compare predicted **average-subject** cortical maps. Learn whether “hitness” leaves a fingerprint in the encoding — not whether a song will chart.

**Status:** design phase (hypothesis + ADR + plan + Phase 1 freeze checklist). No batch encodes required to clone this repo. No results yet.

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
| [docs/adr/001-cortex-hit-encode.md](docs/adr/001-cortex-hit-encode.md) | Decision record |
| [docs/experiment-plan.md](docs/experiment-plan.md) | Phased plan; primary endpoint `mean_auditory_roi_energy` |
| [docs/protocol.md](docs/protocol.md) | Phase 1 freeze checklist + pilot steps |
| [docs/non-goals.md](docs/non-goals.md) | Binding non-goals + canonical language ban |
| [NOTICE.md](NOTICE.md) | TRIBE NC + stimulus rights |

## Instrument

Use the sibling VideoCortex CLI/deck for encodes. This repo stores **cohort manifests, run metadata, analysis, and claims discipline** — it does not vendor TRIBE weights.

```bash
# later, once past design phase:
# videocortex doctor
# videocortex render --audio path/to/stimulus.wav   # v0 is audio-primary; video only if freeze says so
```

## Layout

```
stimuli/     # rights-cleared clips live outside git by default; manifests only
runs/        # encode outputs / pointers (large binaries gitignored); receipt schema
analysis/    # Phase 4 outline only — no results yet
docs/        # hypothesis, ADR, plan, protocol, non-goals
```

## Language ban list (UX + papers)

Canonical copy lives in [docs/non-goals.md](docs/non-goals.md). Same list here:

**Say:** *hit-labeled cohort*, *encode separation*, *predicted cortical response*, *predicted average-subject maps*. *hit-shaped craft* only if bridging later (H4, deferred).

**Never:** `hit_probability`, “likely a hit,” “% chance,” Billboard forecast, chart forecast, “ensure a hit,” “this is what someone is thinking,” mind-reading, decoder claims.

## License

Code in this repository: MIT (see `LICENSE` if present).

TRIBE v2 weights and upstream model: **CC-BY-NC-4.0** — research / non-commercial. Stimulus files: you must hold rights; do not commit unlicensed media.
