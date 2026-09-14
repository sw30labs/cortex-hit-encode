#!/usr/bin/env python3
"""Figure: permutation null for cohort v2 primary test (same recipe as v0).

Re-runs the frozen within-pair sign-flip permutation (same seed/count as
phase4_v2.py) and plots the null distribution of the paired mean difference
with the observed statistic marked. No invented numbers: everything is
recomputed from runs/v2 receipts + predictions.npy on disk.
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUNS_VOL = Path("/Volumes/DATA/cortex-hit-encode/runs/v2")
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "analysis"))

from phase4_v2 import ROI_NAMES, N_PERM, endpoint, roi_vertex_mask  # noqa: E402

RNG = np.random.default_rng(20260914)


def main() -> int:
    mask, _, _ = roi_vertex_mask()
    pairs = {}
    for p in sorted(RUNS_VOL.glob("*/receipt.json")):
        r = json.loads(p.read_text())
        if r.get("status") != "ok":
            continue
        pred = Path(r["output_paths"]["predictions"])
        if not pred.exists():
            continue
        pairs.setdefault(r["pair_id"], {})[r["label"]] = endpoint(
            np.load(pred), mask)
    complete = [v for v in pairs.values() if "hit" in v and "nonhit" in v]
    hit = np.array([v["hit"] for v in complete])
    non = np.array([v["nonhit"] for v in complete])
    d = hit - non
    obs = float(d.mean())
    null = np.array([
        float(np.mean(d * RNG.choice([-1.0, 1.0], size=len(d))))
        for _ in range(N_PERM)])
    p = (float(np.sum(np.abs(null) >= abs(obs))) + 1) / (N_PERM + 1)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.hist(null, bins=60, color="#888", edgecolor="none")
    ax.axvline(obs, color="crimson", lw=2,
               label=f"observed diff = {obs:.4f}\nperm p = {p:.3f}")
    ax.axvline(0, color="k", lw=1, ls="--")
    ax.set_xlabel("paired mean diff (hit − nonhit), auditory ROI energy")
    ax.set_ylabel("permutation draws")
    ax.set_title(f"cohort v2 null — {len(complete)} pairs, "
                 f"{N_PERM:,} sign-flips")
    ax.legend(frameon=False)
    fig.tight_layout()
    out = ROOT / "analysis" / "null-dist-v2.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out} (obs={obs:.6f}, p={p:.4f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
