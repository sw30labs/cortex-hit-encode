# Hypotheses — cortex-hit-encode

Date: 2026-09-14  
Instrument: `che` (vendored VideoCortex encode path) + TRIBE v2 (encoding, average subject)  
Sibling craft work (out of band): artist-twin `insight/hit_patterns.py` (lyric structure only)

## Motivation

Commercial “hits” are labeled after social markets act. Encoding models predict how an **average** cortex responds to a stimulus. The interesting question is whether hit **labels**, after careful matching, still separate predicted maps — i.e. whether there is a measurable encoding fingerprint associated with hit-labeled songs in a genre — **without** claiming that fingerprint causes charts.

## Primary hypothesis

**H1 (encode separation).**  
Among genre-, language-, and era-matched stimuli, tracks meeting a pre-registered **hit label** criterion produce systematically different predicted average-subject cortical response patterns under TRIBE v2 / `che` than matched non-hits — especially in auditory / temporal / language-adjacent ROIs and in temporal dynamics of regional energy — **after** controlling for loudness, duration, and (where available) vocal presence / cut-rate confounds.

v0 operational gate (same name as plan + protocol): **`mean_auditory_roi_energy`** — mean `|x|` over a frozen Destrieux auditory ROI set, averaged across TRs; permutation test of the hit − non-hit difference.

Operationalization of “hit label” is fixed in the cohort sheet before analysis (examples: national chart peak ≤ N, certification, or streams threshold). One definition per pilot; no peeking.

## Null and alternatives

**H0 (no separation).** After matching and confound regression, hit vs non-hit labels do **not** separate encode summaries better than a permutation null (label shuffle within matched pairs or within cohort).

**H2 (confound).** Any *remaining* separation after the **standard** v0 loudness-normalize (all stimuli, same LUFS target) collapses when stimuli are duration-matched more tightly, matched to a stricter LUFS residual, or reduced to instrumental stems — i.e. the effect is leftover production energy / density, not a hit-label fingerprint. H2 is a sensitivity, not the Phase 2 prep step.

**H3 (fame proxy).** Within-artist hit vs deep-cut pairs show little or no separation once artist and era are held fixed — suggesting catalog fame / production era, not a general hit circuit. H3 is a secondary slice; it can be supported even if H1 holds on the broader matched cohort.

**H4 (craft bridge — deferred, non-causal).** Even if H1 fails, encode diffs between *high vs low lyric hit-shaped craft scores* (artist-twin Insight) may still separate maps. That would support craft priors, still not chart forecasts. **Out of scope for pilot v0** unless H1 is inconclusive and time remains.

## Predictions if H1 is supported

1. Higher **`mean_auditory_roi_energy`** (mean `|x|` in the frozen auditory ROI set) for hit-labeled tracks vs matched non-hits.
2. Secondary: multivariate distance on the ROI vector, or more sustained time-courses, may also separate — not the v0 gate.
3. Effect survives the loudness + duration covariates; shrinks but does not vanish under H2-style controls (or we accept H2).

## How to call H0 / H1 / H2 / H3

Same rules as [experiment-plan.md](experiment-plan.md) and [protocol.md](protocol.md):

1. Primary test not above the permutation null → **H0**. Stop product mythology.
2. Primary test above null, but H2 controls kill the difference → **H2**. Do not market as a hit fingerprint.
3. Primary test above null, H2 survives, within-artist slice null → **H1** on the matched cohort; **H3** as a fame/era caveat.
4. Primary + H2 survive and within-artist also separates → **H1**; **H3** not supported.
5. Encode failures / TRIBE lag misuse / mixed lag modes → invalid run. Fix protocol; do not interpret.

## Falsifiers

- No separation after the pre-registered primary test → H0.
- Separation vanishes under H2 controls → H2.
- Within-artist pairs null → H3 (caveat or alternative, per the call rules above).
- Invalid encodes → no hypothesis call.

## What success does *not* mean

Supporting H1 does **not** authorize:

- decoding songs from desired activation maps;
- claiming high probability of commercial success (`hit_probability`, “likely a hit,” “% chance,” Billboard / chart forecast, “ensure a hit”);
- mind-reading or “this is what someone is thinking”;
- hard-gating artist-twin generation on cortex scores.

It authorizes: “interesting encoding difference in this cohort under this instrument.”

Language: [non-goals.md](non-goals.md).

## Pre-registration discipline

Complete the Phase 1 freeze in [protocol.md](protocol.md) **before** the first real encode batch:

1. Freeze cohort inclusion rules and one `hit_definition_id` in `stimuli/manifests/cohort-v0.csv` (copy from the example).
2. Freeze the **same** primary endpoint + test in [experiment-plan.md](experiment-plan.md) **and** [protocol.md](protocol.md): `mean_auditory_roi_energy`, permutation of the hit − non-hit difference.
3. Freeze the Destrieux auditory ROI label list (confirm names against the `che overlay` atlas).
4. Record `che` / vendored VideoCortex commit + TRIBE weight hashes in each `runs/.../receipt.json` (see `runs/receipt.example.json`).
