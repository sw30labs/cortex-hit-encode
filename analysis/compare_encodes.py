#!/usr/bin/env python3
"""Phase 4 outline. Not a results generator.

Primary endpoint: mean_auditory_roi_energy
Primary test: permutation of the hit − non-hit difference

Run after Phase 3 receipts exist. Exits 2 if none are found.
Does not invent p-values or write report-v0.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
PRIMARY_ENDPOINT = "mean_auditory_roi_energy"


def find_receipts(runs_dir: Path) -> list[Path]:
    skip = {runs_dir / "receipt.example.json"}
    found = []
    for path in sorted(runs_dir.rglob("receipt.json")):
        if path in skip:
            continue
        found.append(path)
    return found


def load_receipt(path: Path) -> dict:
    data = json.loads(path.read_text())
    if data.get("primary_endpoint") not in (None, PRIMARY_ENDPOINT):
        raise SystemExit(
            f"{path}: primary_endpoint must be {PRIMARY_ENDPOINT!r}"
        )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--runs",
        type=Path,
        default=RUNS,
        help="runs/ directory (default: repo runs/)",
    )
    args = parser.parse_args(argv)

    receipts = find_receipts(args.runs)
    if not receipts:
        print(
            "No receipt.json files under",
            args.runs,
            file=sys.stderr,
        )
        print(
            "Complete Phase 1 freeze + Phase 3 encodes before analysis.",
            file=sys.stderr,
        )
        return 2

    ok = 0
    failed = 0
    for path in receipts:
        rec = load_receipt(path)
        status = rec.get("status")
        if status == "ok":
            ok += 1
        else:
            failed += 1
            print(f"skip {path}: status={status!r}", file=sys.stderr)

    print(f"receipts={len(receipts)} ok={ok} failed={failed}")
    print(
        "Next (not implemented here): compute "
        f"{PRIMARY_ENDPOINT}, permutation test, write analysis/report-v0.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
