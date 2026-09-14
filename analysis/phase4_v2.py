#!/usr/bin/env python3
"""Phase 4 analysis — cohort v2.

Primary endpoint (frozen): mean_auditory_roi_energy
  = mean |x| over the frozen Destrieux auditory ROI vertices, averaged over TRs.
Primary test (frozen): two-sided permutation of the hit - non-hit difference,
  shuffling labels within pair_id (all pairs present); unadjusted and
  covariate-adjusted (lufs_post, duration_s).

Writes analysis/results-v2.json. No invented numbers: everything here is
computed from runs/.../receipt.json + predictions.npy on disk.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUNS_VOL = Path("/Volumes/DATA/cortex-hit-encode/runs/v2")
sys.path.insert(0, str(ROOT / "src"))

ROI_NAMES = ["G temp sup-G T transv", "G temp sup-Plan tempo", "G temp sup-Lateral"]
N_PERM = 20000
RNG = np.random.default_rng(20260914)


def roi_vertex_mask():
    from cortex_hit_encode.regions import load_region_labels

    region_id, names = load_region_labels()
    want = {n for n in ROI_NAMES}
    ids = [i for i, (_hemi, name) in enumerate(names) if name in want]
    if not ids:
        raise SystemExit("frozen ROI labels not found in atlas")
    mask = np.isin(region_id, ids)
    labels = [f"{'L' if h=='left' else 'R'} {n}" for h, n in names if n in want]
    return mask, labels, int(mask.sum())


def endpoint(pred: np.ndarray, mask: np.ndarray) -> float:
    # mean |x| over ROI vertices, per TR, then averaged over TRs
    return float(np.abs(pred[:, mask]).mean())


def paired_stat(vals_hit: np.ndarray, vals_non: np.ndarray) -> float:
    return float(np.mean(vals_hit - vals_non))


def paired_perm_p(vals_hit, vals_non, n_perm=N_PERM):
    obs = paired_stat(vals_hit, vals_non)
    d = vals_hit - vals_non
    n = len(d)
    count = 0
    for _ in range(n_perm):
        signs = RNG.choice([-1.0, 1.0], size=n)
        if abs(float(np.mean(d * signs))) >= abs(obs) - 1e-12:
            count += 1
    return obs, (count + 1) / (n_perm + 1)


def adjusted_endpoint(e, lufs, dur, coef):
    # residualise the endpoint on standardized covariates (frozen adjustment)
    X = np.column_stack([np.ones_like(e), (lufs - lufs.mean()) / lufs.std(),
                         (dur - dur.mean()) / dur.std()])
    y = e - X @ coef
    return y


def fit_coef(e, lufs, dur):
    X = np.column_stack([np.ones_like(e), (lufs - lufs.mean()) / lufs.std(),
                         (dur - dur.mean()) / dur.std()])
    coef, *_ = np.linalg.lstsq(X, e, rcond=None)
    return coef


def main() -> int:
    receipts = []
    for p in sorted(RUNS_VOL.glob("*/receipt.json")):
        r = json.loads(p.read_text())
        if r.get("status") == "ok":
            r["_dir"] = p.parent
            receipts.append(r)
    if not receipts:
        print("no ok receipts", file=sys.stderr)
        return 2

    mask, roi_labels, n_v = roi_vertex_mask()
    print(f"ROI vertices: {n_v} across {len(roi_labels)} labels: {roi_labels}")

    recs = []
    for r in receipts:
        pred_path = Path(r["output_paths"]["predictions"])
        if not pred_path.exists():
            print(f"skip {r['stimulus_id']}: predictions missing", file=sys.stderr)
            r["status"] = "failed"
            continue
        preds = np.load(pred_path)
        r["energy"] = endpoint(preds, mask)
        r["lufs"] = float(r["lufs_post"])
        r["dur"] = float(r["duration_s"])
        recs.append(r)

    # group by pair_id (hit/nonhit)
    pairs = {}
    for r in recs:
        pairs.setdefault(r["pair_id"], {})[r["label"]] = r
    complete = [v for v in pairs.values() if "hit" in v and "nonhit" in v]
    print(f"ok={len(recs)} complete pairs={len(complete)}")

    hit = np.array([v["hit"]["energy"] for v in complete])
    non = np.array([v["nonhit"]["energy"] for v in complete])
    lufs = np.array([v["hit"]["lufs"] + v["nonhit"]["lufs"] for v in complete]) / 2
    dur = np.array([v["hit"]["dur"] + v["nonhit"]["dur"] for v in complete]) / 2

    obs_u, p_u = paired_perm_p(hit, non)
    e_all = np.concatenate([hit, non])
    lu = np.concatenate([
        np.array([v["hit"]["lufs"] for v in complete]),
        np.array([v["nonhit"]["lufs"] for v in complete])])
    du = np.concatenate([
        np.array([v["hit"]["dur"] for v in complete]),
        np.array([v["nonhit"]["dur"] for v in complete])])
    coef = fit_coef(e_all, lu, du)
    adj = adjusted_endpoint(e_all, lu, du, coef)
    obs_a, p_a = paired_perm_p(adj[: len(complete)], adj[len(complete):])

    hits_won = int((hit > non).sum())

    summary = {
        "n_pairs": len(complete),
        "roi_labels": roi_labels,
        "roi_vertices": n_v,
        "mean_hit": float(hit.mean()), "mean_nonhit": float(non.mean()),
        "unadjusted_diff": obs_u, "unadjusted_p": p_u,
        "adjusted_diff": obs_a, "adjusted_p": p_a,
        "hits_higher_count": hits_won,
        "effect_dz": obs_u / float(np.std(hit - non, ddof=1)),
        "per_stimulus": [
            {"pair": pid, "hit_id": v["hit"]["stimulus_id"],
             "nonhit_id": v["nonhit"]["stimulus_id"],
             "hit_energy": v["hit"]["energy"], "nonhit_energy": v["nonhit"]["energy"]}
            for pid, v in sorted(complete and
                                 {v["hit"]["pair_id"]: v for v in complete}.items())],
    }
    out = ROOT / "analysis" / "results-v2.json"
    out.write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "per_stimulus"}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
