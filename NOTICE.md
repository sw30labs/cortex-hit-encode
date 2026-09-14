# Notice

## TRIBE v2

TRIBE v2 model and weights are subject to **CC-BY-NC-4.0** (research / non-commercial). See upstream:

- https://github.com/facebookresearch/tribev2
- https://huggingface.co/facebook/tribev2

This experiment repo does not redistribute those weights. Copy or hardlink them
from an existing cache (`scripts/import-weights.sh`).

## VideoCortex (vendored instrument)

Encode / render / doctor / fetch instrument vendored from
https://github.com/sw30labs/videocortex @ `b34589552925338491cee8aee7087722be21c7d9`
(MIT, Nicolas Cravino). VideoCortex remains an upstream *reference* only; this
repo does not depend on a sibling checkout at runtime and does not modify that
tree. The command deck (`serve` / web) is not vendored.

Pin: `cortex_hit_encode.VENDOR_COMMIT`.

## Frozen feature extractors

TRIBE v2 stacks four frozen encoders. Each carries its own terms (same table as
VideoCortex `NOTICE.md`):

| modality | repo | note |
|---|---|---|
| text | `meta-llama/Llama-3.2-3B` | **Gated.** Llama 3.2 Community License — accept on HuggingFace. |
| image | `facebook/dinov2-large` | Apache-2.0 |
| audio | `facebook/w2v-bert-2.0` | MIT |
| video | `facebook/vjepa2-vitg-fpc64-256` | See the model card |

## Attribution (TRIBE)

> d'Ascoli, S., Rapin, J., Benchetrit, Y., Brooks, T., Begany, K., Raugel, J.,
> Banville, H., & King, J.-R. (2026). *A foundation model of vision, audition,
> and language for in-silico neuroscience.* arXiv:2605.04326

## Stimuli

Audio/video used in runs must be rights-cleared by the operator. Do not commit
copyrighted media to git. Manifests may store hashes and rights basis only.
