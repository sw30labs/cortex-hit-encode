# Pilot protocol — cohort v0

Checklist for the first real batch. Complete Phase 1 freeze before encodes.

## 0. Preconditions

- [ ] VideoCortex `doctor` green on the machine that will encode
- [ ] TRIBE weights available under NC research use
- [ ] This repo docs read; ban list acknowledged
- [ ] Local data root created (e.g. `/Volumes/DATA/cortex-hit-encode/stimuli`) — **not** committed

## 1. Cohort (example band)

**Example (replace if you prefer another band):** rock-español / Argentine rock, roughly Indio-adjacent catalog for familiarity — still requires **rights-cleared** audio you control or license.

- [ ] List ≥8 hit-labeled tracks with frozen hit definition
- [ ] List ≥8 matched non-hits
- [ ] Optional: ≥4 within-artist hit/deep-cut pairs for H3
- [ ] Commit `stimuli/manifests/cohort-v0.csv`

### Suggested CSV columns

`id,label,artist,title,year,language,genre_tags,rights_basis,rights_notes,local_relpath,duration_s,lufs_pre,lufs_post,hit_definition_id,pair_id,notes`

## 2. Prep

- [ ] Copy files into local data root mirroring `local_relpath`
- [ ] Loudness normalize to agreed LUFS; fill lufs_* columns
- [ ] Hash each file (`sha256`); store in `stimuli/manifests/hashes-v0.json`
- [ ] Trim policy recorded in manifest `notes` or global `docs/experiment-plan.md` freeze line

## 3. Encode

For each stimulus:

- [ ] `videocortex render …` (exact flags recorded in `runs/.../receipt.json`)
- [ ] Confirm lag mode
- [ ] Save contact sheet / ROI export paths in receipt
- [ ] On failure: `status=failed`, reason, do not analyze

## 4. Analysis gate

- [ ] Primary ROI list frozen
- [ ] Run permutation test script (to be added in Phase 4)
- [ ] Write `analysis/report-v0.md` with H0/H1/H2/H3 call

## 5. Stop rules

- Stop generate-wiring discussions until report exists.
- Stop if rights unclear for any stimulus — drop it, do not “just use YouTube.”
