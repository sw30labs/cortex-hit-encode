# Pilot protocol — cohort v0

Checklist for the first real batch. Complete the **Phase 1 freeze** before any encode.

Hypotheses and call rules: [hypothesis.md](hypothesis.md).  
Primary endpoint name (same as [experiment-plan.md](experiment-plan.md)): **`mean_auditory_roi_energy`**.  
Language: [non-goals.md](non-goals.md).

## Freeze (Phase 1 — do this first)

Nothing below is a result. These are the knobs that must stop moving before Phase 3.

- [ ] Ban list read (README + [non-goals.md](non-goals.md))
- [ ] One `hit_definition_id` from `stimuli/manifests/hit-definitions.md`, with chart/territory/source + retrieval date written in cohort notes
- [ ] Matching rules written: genre band, language, era window (**±5 years** unless you record another), optional tempo/energy band
- [ ] ≥8 hit-labeled + ≥8 matched non-hit rows in `stimuli/manifests/cohort-v0.csv` (from the example)
- [ ] Optional H3: ≥4 within-artist pairs (`pair_id` shared); if fewer, H3 is underpowered — say so, do not peek later
- [ ] Trim policy **one of:** `fixed_window_30s` (recommended) | `full_track` — write it here: `____________`
- [ ] LUFS target written (recommended **−16 LUFS** integrated): `____________`
- [ ] Lag mode **one of:** `stimulus` (recommended) | `scanner` — write it here: `____________`
- [ ] Primary endpoint name frozen as `mean_auditory_roi_energy` (do not rename in the report)
- [ ] Primary test frozen: two-sided permutation of the hit − non-hit difference on that scalar (shuffle within `pair_id` if present, else within cohort); unadjusted + loudness/duration-adjusted
- [ ] Auditory ROI list frozen — exact `che` / Destrieux strings, confirmed against the overlay. Suggested cluster to confirm: L/R `G temp sup/G T transv`, `G temp sup/Plan tempo`, `G temp sup/Lateral`. Write the frozen list: `____________`
- [ ] `stimuli/manifests/cohort-v0.csv` committed; record that commit SHA: `____________`

Do not start encodes until every box above is checked.

## 0. Preconditions

- [ ] `che doctor` green on the machine that will encode (`che doctor --offline` after weights are local)
- [ ] TRIBE weights imported with `scripts/import-weights.sh` from an existing VideoCortex / HF cache — do not re-download; do not modify VideoCortex
- [ ] `HF_HOME` / `HUGGINGFACE_HUB_CACHE` pointed at a **private** data root (not a VideoCortex tree)
- [ ] Local stimulus root created (e.g. `/Volumes/DATA/cortex-hit-encode/stimuli`) — **not** committed

## 1. Cohort (example band)

**Example (replace if you prefer another band):** rock-español / Argentine rock, roughly Indio-adjacent catalog for familiarity — still requires **rights-cleared** audio you control or license.

### Suggested CSV columns

`id,label,artist,title,year,language,genre_tags,rights_basis,rights_notes,local_relpath,duration_s,lufs_pre,lufs_post,hit_definition_id,pair_id,notes`

`label` is `hit` or `nonhit` only.

## 2. Prep (Phase 2)

- [ ] Copy files into local data root mirroring `local_relpath`
- [ ] Loudness normalize to the **frozen** LUFS target; fill `lufs_pre` / `lufs_post`
- [ ] Apply the frozen trim policy only
- [ ] Hash each file (`sha256`); store in `stimuli/manifests/hashes-v0.json`

## 3. Encode (Phase 3)

For each stimulus:

- [ ] `che render --audio …` (or `--video` only if freeze said so). Exact flags in `runs/<cohort>/<stimulus_id>/receipt.json` — see `runs/receipt.example.json`
- [ ] Read / overlay time alignment uses the frozen lag mode (`stimulus` vs `scanner` is a `che overlay` read, not a second encode). Do not mix modes in one cohort.
- [ ] Point receipt at `manifest.json`, `predictions.npy`, contact sheet / overlay paths
- [ ] Record `che` / `cortex_hit_encode` version + vendored VideoCortex commit (`VENDOR_COMMIT`) + TRIBE weight revision in the receipt
- [ ] On failure: `status=failed`, reason, do not analyze

## 4. Analysis gate (Phase 4)

- [ ] Every analyzed row has `status=ok` and a receipt
- [ ] Compute **`mean_auditory_roi_energy`** only on the frozen ROI list
- [ ] Run the pre-registered permutation test (outline: [analysis/README.md](../analysis/README.md); script stub: `analysis/compare_encodes.py`)
- [ ] H2 sensitivity and H3 within-artist slice if the freeze said they were in scope
- [ ] Write `analysis/report-v0.md` with an H0 / H1 / H2 / H3 call — no invented numbers, no generate wiring

## 5. Stop rules

- Stop generate-wiring discussions until the report exists.
- Stop if rights are unclear for any stimulus — drop it, do not “just use YouTube.”
- Stop if lag modes or trim/LUFS policy drifted mid-batch — fix and re-encode; do not interpret a mixed run.
