# Analysis (Phase 4 outline)

No results live here yet. Do not add a report until real receipts exist.

**Primary endpoint:** `mean_auditory_roi_energy`  
**Primary test:** two-sided permutation of the hit − non-hit difference  
Same names as [docs/experiment-plan.md](../docs/experiment-plan.md) and [docs/protocol.md](../docs/protocol.md).

## Inputs

- Frozen `stimuli/manifests/cohort-v0.csv`
- One `runs/<cohort>/<id>/receipt.json` per stimulus (`status=ok` only)
- `che` `predictions.npy` (`n_TR × 20484` fsaverage5) plus the Destrieux map the instrument already uses

## Steps (Karpathy-simple)

1. Load cohort labels + `pair_id` + `lufs_post` + `duration_s`.
2. For each ok receipt, load predictions; mean `|x|` over the **frozen** auditory ROI vertices; average across TRs → one scalar, `mean_auditory_roi_energy`.
3. Unadjusted permutation test (shuffle labels within `pair_id` if present, else within cohort).
4. Repeat after residualizing on loudness + duration.
5. H2 slice if you froze one (stricter LUFS / duration / instrumental).
6. H3 slice: rows that share a `pair_id` and the same artist.
7. Write `analysis/report-v0.md`: effect size, null plot, H0/H1/H2/H3 call, ban-list paragraph. No `hit_probability`. No generate wiring.

Stub: `compare_encodes.py` (exits until receipts exist; does not print fake p-values).
