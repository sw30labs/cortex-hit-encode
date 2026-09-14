# Experiment plan — cortex-hit-encode

Version: 0.1 (design)  
Date: 2026-09-14

## Goal

Test **H1** (encode separation of hit-labeled vs matched non-hit stimuli) with VideoCortex / TRIBE v2, with pre-registered confounds and falsifiers. Produce a short report: support / fail to support / confound-explained.

## Phases

### Phase 0 — Design (this PR / docs) ✅

- Hypothesis, ADR, protocol, repo skeleton.
- No model download required.

### Phase 1 — Cohort lock

1. Pick genre/language band for pilot (default suggestion: rock-español / Argentine rock “Indio-adjacent” *as an example*, not a brand requirement).
2. Define **hit label** in writing (one of):
   - chart peak threshold, or
   - certification, or
   - streams/plays threshold on a named source with date.
3. Select ≥8 hits + ≥8 non-hits with matching rules (era ± years, language, approximate tempo/energy band if known).
4. Prefer **within-artist** pairs for a secondary H3 slice if catalog allows.
5. Fill `stimuli/manifests/cohort-v0.csv` with: id, path, label, artist, year, rights_basis, duration_s, loudness_lufs_target, notes.
6. Freeze the CSV (commit hash) before first encode.

### Phase 2 — Stimulus prep

1. Rights-cleared local files only (user-supplied). Store under a local data root; gitignore binaries.
2. Normalize loudness to a fixed LUFS target; record pre/post LUFS.
3. Trim policy: full track vs fixed first N seconds — **pick one** for v0 and stick to it (recommend fixed window + full-track sensitivity later).
4. Audio-primary for v0; add video only if rights-ok and VideoCortex path is stable for that modality mix.
5. Compute content hashes; write sidecar JSON next to each file.

### Phase 3 — Encode

1. Pin VideoCortex commit + TRIBE weight revisions via `videocortex doctor` / run receipts.
2. Lag mode: document `stimulus` vs `scanner`; default match VideoCortex stimulus-aligned reading.
3. Batch render; store outputs under `runs/<cohort>/<stimulus_id>/` (or pointers if huge).
4. Failures: log and exclude with reason; do not silently impute.

### Phase 4 — Analysis

**Pre-register primary endpoint (v0 proposal — edit before Phase 1 freeze):**

- Feature: mean predicted energy in a small auditory ROI set (names from Destrieux / VideoCortex labels — finalize against actual overlay atlas).
- Test: paired or unmatched permutation test of hit vs non-hit on that scalar (or Mahalanobis on ROI vector).
- Covariates: loudness, duration; report adjusted and unadjusted.

**Secondary:**

- Time-course correlation / peak latency summaries.
- H2: re-run after stricter loudness match or instrumental-only if available.
- H3: within-artist subset.

**Reporting:**

- Effect size + null distribution plot.
- Explicit “does not imply chart causality” paragraph.

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
| Lag / TR misuse | Follow VideoCortex lag docs; one mode per cohort |
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
