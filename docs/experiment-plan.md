# Experiment plan — cortex-hit-encode

Version: 0.2 (design; endpoint named)  
Date: 2026-09-14

## Goal

Test **H1** (encode separation of hit-labeled vs matched non-hit stimuli) with VideoCortex / TRIBE v2, with pre-registered confounds and falsifiers. Produce a short report: support / fail to support / confound-explained.

## Hypotheses (same names everywhere)

| ID | Name | Claim |
|---|---|---|
| **H1** | encode separation | After matching + standard confound controls, hit-labeled tracks produce systematically different predicted average-subject maps than matched non-hits. |
| **H0** | no separation | After matching + confound regression, labels do not beat a permutation null. |
| **H2** | confound | Remaining separation collapses under *stricter* production-energy controls (tighter LUFS residual, tighter duration, or instrumental stems). Not the same as the standard Phase 2 LUFS normalize. |
| **H3** | fame proxy | Within-artist hit vs deep-cut pairs show little or no separation (fame / era, not a general hit circuit). Secondary slice. |
| **H4** | craft bridge | Deferred. Out of scope for v0. |

Full wording and call rules: [hypothesis.md](hypothesis.md).

**Primary endpoint (v0) — same name as [protocol.md](protocol.md):** `mean_auditory_roi_energy`  
Mean absolute predicted signal (`|x|`) over a frozen Destrieux auditory ROI set, averaged across TRs; one scalar per stimulus.

**Primary test (v0):** two-sided permutation test of the hit − non-hit difference on that scalar (shuffle labels within `pair_id` when present; otherwise shuffle within cohort). Report unadjusted and covariate-adjusted (loudness, duration).

## Phases

### Phase 0 — Design (docs) ✅

- Hypothesis, ADR, protocol, repo skeleton.
- No model download required.

### Phase 0.5 — Self-contained instrument ✅

- Vendored `che` CLI (ADR 002). Copy weights with `scripts/import-weights.sh`.
- Still no experiment results; still no sibling VideoCortex runtime dependency.

### Phase 1 — Cohort lock + freeze

Do not start Phase 3 encodes until the freeze checklist in [protocol.md](protocol.md) is checked.

1. Pick genre/language band for pilot (default suggestion: rock-español / Argentine rock “Indio-adjacent” *as an example*, not a brand requirement).
2. Define **hit label** in writing — one `hit_definition_id` from `stimuli/manifests/hit-definitions.md` (chart peak, certification, or streams/plays on a named source with date).
3. Select ≥8 hits + ≥8 non-hits with matching rules (language, genre band, era **±5 years** default, approximate tempo/energy band if known).
4. Prefer **within-artist** pairs for a secondary H3 slice if catalog allows (≥4 pairs if possible).
5. Fill `stimuli/manifests/cohort-v0.csv` from the example: id, label, artist, title, year, language, genre_tags, rights_basis, local_relpath, duration_s, lufs_*, hit_definition_id, pair_id, notes.
6. Freeze (commit) the CSV **and** the items on the protocol freeze checklist (trim policy, LUFS target, lag mode, ROI list, primary endpoint name) before first encode.

### Phase 2 — Stimulus prep

1. Rights-cleared local files only (user-supplied). Store under a local data root; gitignore binaries.
2. Normalize loudness to the **frozen** LUFS target (recommend **−16 LUFS** integrated); record pre/post LUFS. This is standard prep, not the H2 test.
3. Trim policy: **pick one** at freeze and stick to it. Recommend `fixed_window_30s` from the start of the file; full-track as a later sensitivity, not the v0 gate.
4. Audio-primary for v0 (`che render --audio …`); add video only if rights-ok and the encode path is stable for that modality mix.
5. Compute content hashes (`sha256`); write `stimuli/manifests/hashes-v0.json`.

### Phase 3 — Encode

1. Pin `che` / `cortex_hit_encode` version + vendored VideoCortex commit (`VENDOR_COMMIT`) + TRIBE weight revisions via `che doctor` / each `receipt.json`.
2. Lag mode: **one mode per cohort**. Default `stimulus` (`che overlay` / stimulus-aligned reading of the already-encoded series). Do not mix with `scanner`. This is a read convention, not a second model.
3. Batch render; store outputs or pointers under `runs/<cohort>/<stimulus_id>/` with a `receipt.json` (schema: `runs/receipt.example.json`). Large binaries stay gitignored.
4. Failures: `status=failed`, reason, exclude from analysis; do not silently impute.

### Phase 4 — Analysis

**Primary endpoint (v0) — locked name; ROI *labels* still filled at Phase 1 freeze:**

- **Name:** `mean_auditory_roi_energy`
- **Feature:** mean `|x|` in a small Destrieux auditory ROI set (`che` / nilearn surface atlas). Confirm exact label strings against the overlay before freeze. Suggested cluster to confirm: L/R `G temp sup/G T transv`, `G temp sup/Plan tempo`, `G temp sup/Lateral`.
- **Test:** two-sided permutation of the hit − non-hit difference on that scalar (within-`pair_id` shuffle when pairs exist; else cohort shuffle).
- **Covariates:** loudness (`lufs_post` or residual to target), duration; report adjusted and unadjusted.

**Secondary (not the gate):**

- Time-course / peak-latency summaries; Mahalanobis on the ROI vector.
- H2: stricter LUFS residual, tighter duration, or instrumental-only if available.
- H3: within-artist (`pair_id`) subset.

Script outline: [analysis/README.md](../analysis/README.md). Do not invent numbers.

**Reporting:**

- Effect size + null distribution plot.
- Explicit H0/H1/H2/H3 call using the rules in [hypothesis.md](hypothesis.md).
- Explicit “does not imply chart causality” paragraph. Ban list: [non-goals.md](non-goals.md).

### Phase 5 — Write-up

- `analysis/report-v0.md` (or HTML plate).
- Optional wiki blurb under Miscellaneous Research — after results, not before.

## Success criteria

| Outcome | Criteria |
|---|---|
| Scientific success | Pre-registered test completed; H0/H1/H2/H3 called honestly |
| Engineering success | Reproducible receipts: cohort hash, tool versions, stimulus hashes |
| Product success | **None claimed.** No generate wiring. |

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Rights / takedown | Local-only media; manifests without URLs to piracy |
| Confound loudness | LUFS normalize; covariate; H2 sensitivity |
| Small N | Pilot = exploratory; label as underpowered; no hype |
| Average subject mismatch to niche genre | State limitation; don’t over-generalize |
| Lag / TR misuse | Follow `che overlay --lag-mode` docs; one mode per cohort |
| Scope creep into decoder | Hard non-goal; reject PRs that add inverse |

## Effort sketch

| Phase | Rough effort |
|---|---|
| Cohort + rights | human days (bottleneck) |
| Prep + encode 16 tracks | hours–day depending on GPU/MPS |
| Analysis v0 | hours–day |
| Generate wiring | **not scheduled** |

## Relationship to artist-twin shift-left

If H1 is interesting, a **later** ADR may propose human-readable craft notes. Soft advisory in generate remains a separate decision (see swarm 2026-09-14). This repo does not implement it.
