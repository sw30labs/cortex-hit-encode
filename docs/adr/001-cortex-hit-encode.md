# ADR 001: Standalone cortex-hit-encode experiment

Date: 2026-09-14  
Status: Accepted  
Owner: Nicolas Cravino / sw30labs

## Problem

Artist-twin already ships **Insight** craft diagnostics (`hit_patterns`, `chart_brief`): hit-*shaped* lyric structure, explicitly not a chart forecast. Separately, VideoCortex exposes TRIBE v2 as an **encoding** instrument (stimulus → predicted average-subject fMRI).

A tempting product story is: run cortex encodes on hits, find shared activations, invert them, and drive lyrics→music until the brain “lights up like a hit.”

That story mixes three different claims:

1. Encoding comparison is feasible with today’s VideoCortex.
2. Inverse / decode (activation → stimulus) is available in this stack.
3. Optimizing predicted cortex ⇒ commercial hit.

(1) is interesting research. (2) is false for VideoCortex as shipped (encoding ≠ decoding). (3) contradicts the hit-science literature already cited in artist-twin Insight (social influence, weak acoustic predictors).

We needed a place to pursue (1) without contaminating artist-twin’s generate graphs or overselling (2)/(3).

## Decision

Create a **new public repo** `sw30labs/cortex-hit-encode` as a **standalone encoding comparative experiment**:

- Use VideoCortex / TRIBE v2 **as-is** (encoding, average subject, haemodynamic lag).
- Curate rights-cleared hit vs matched non-hit stimuli; batch-encode; analyze ROI / dynamics differences with confound controls and permutation tests.
- Keep **all generate wiring out**: no LangGraph nodes in artist-twin, no album admission gates, no YuE2 prompt injection from cortex scores in v0.
- Keep language discipline identical to Insight and [docs/non-goals.md](../non-goals.md): no `hit_probability`, “likely a hit,” “% chance,” Billboard / chart forecast, “ensure a hit,” mind-reading, or decoder claims.
- Optional future: feed **descriptive** encode findings into human-readable craft checklists only — separate ADR if/when earned.

## Consequences

### Positive

- Clear scientific object: H1 encode separation vs H0 / H2 / H3 (H4 deferred). Primary v0 endpoint: `mean_auditory_roi_energy`.
- No false product promise inside Compose Track/Album.
- Reuses an instrument Nic already invested in (VideoCortex).
- Cool, publishable, wiki-friendly under Miscellaneous Research.

### Negative / costs

- Requires rights-cleared stimulus labor; cannot casually scrape catalogs.
- TRIBE NC license constrains commercial packaging of the *model*; experiment remains research-framed.
- Average-subject, TR-scale maps are coarse; null results are likely and must be publishable as wins for honesty.
- Dual maintenance: VideoCortex upgrades may change encode numbers — pin versions in run receipts.

### Neutral

- artist-twin Insight craft path remains the shift-left candidate for *lyric form*; this repo does not replace it.

## Non-goals (binding)

See [docs/non-goals.md](../non-goals.md). In particular: no decoder loop, no Billboard scrapers as product, no auto-wiring into generate.

## Ethics and rights

- Stimulus files stay off git by default; manifests record hashes + rights basis.
- No claim that predicted maps are a specific listener’s experience.
- Results reported as instrument predictions, not neural truth.

## Related work

- VideoCortex README: encoding ≠ decoding.
- artist-twin `insight/hit_patterns.py`: craft, not forecast.
- Swarm 2026-09-14: commercial “ensure a hit” rejected; craft advisory optional elsewhere.

## Status of implementation

Design docs in this repo, plus a Phase 1 freeze checklist, `runs/receipt.example.json`, and an analysis outline. The encode instrument is now vendored here (`che`); see [ADR 002](002-self-contained-instrument.md). Pilot encodes deferred until cohort + rights + `che doctor` are green. No results yet.
