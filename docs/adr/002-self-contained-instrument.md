# ADR 002: Self-contained encode instrument

Date: 2026-09-14  
Status: Accepted  
Owner: Nicolas Cravino / sw30labs  
Supersedes (partial): ADR 001 “use VideoCortex as-is via a sibling checkout”

## Problem

ADR 001 correctly separated the experiment from artist-twin and from decoder /
hit-probability stories. It left the *instrument* as a sibling VideoCortex
checkout (`videocortex doctor` / `videocortex render`). That made this repo
unable to encode after a clean clone: runtime depended on another tree,
another CLI name, and VideoCortex’s HuggingFace / feature-cache layout.

We need encodes to be reproducible from **this** repo alone, without editing
or PRing VideoCortex, and without re-downloading ~20 GB of weights when a
local VideoCortex / HF cache already has them.

## Decision

Vendor the VideoCortex **encode / render / doctor / fetch** path into
`src/cortex_hit_encode/` (MIT wrapper, same TRIBE NC terms). Ship CLI
entrypoints **`che`** and `cortex-hit-encode`.

- VideoCortex remains an upstream *reference* only. Do not import it at
  runtime. Do not modify that repo for this experiment.
- Do **not** vendor TRIBE weights or media. Copy or hardlink from an existing
  VideoCortex / HuggingFace cache via `scripts/import-weights.sh`. Never call
  HuggingFace download when those sources exist.
- Feature cache: `$CORTEX_HIT_ENCODE_CACHE` else `./.che-cache` (gitignored).
- Hub cache: honor `HF_HOME` / `HUGGINGFACE_HUB_CACHE`, pointed at a
  **private** data root — not VideoCortex’s tree.
- Omit the VideoCortex command deck (`serve` / web) in v0. Karpathy-simple.
- Experiment non-goals stay binding: no decoder, no artist-twin wiring, no
  `hit_probability`. Audio-primary remains the v0 default
  (`che render --audio …`).

Vendored-from pin is `cortex_hit_encode.VENDOR_COMMIT` (see NOTICE).

## Consequences

### Positive

- Clone → `pip install -e .` → `che doctor --offline --renderer` works
  without a sibling checkout.
- Weights move as hardlinks when the filesystem allows; no second 20 GB
  download.
- Run receipts record `che` + the vendored VideoCortex commit.

### Negative / costs

- Instrument code can drift from VideoCortex. Pin the vendored commit; bump
  it deliberately.
- Operators must still accept Llama / TRIBE licences and hold stimulus
  rights. Vendoring the wrapper does not relicense the model.

### Neutral

- Analysis, cohort manifests, and language discipline stay in this repo.
- A later ADR may add a thin batch wrapper over `che render`; not required
  to be self-contained.

## Status of implementation

Package + `che` CLI + `scripts/import-weights.sh` + protocol/README pointing
at `che doctor` / `che render --audio`. No experiment results in this ADR.
