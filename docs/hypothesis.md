# Hypotheses — cortex-hit-encode

Date: 2026-09-14  
Instrument: VideoCortex + TRIBE v2 (encoding, average subject)  
Sibling craft work (out of band): artist-twin `insight/hit_patterns.py` (lyric structure only)

## Motivation

Commercial “hits” are labeled after social markets act. Encoding models predict how an **average** cortex responds to a stimulus. The interesting question is whether hit **labels**, after careful matching, still separate predicted maps — i.e. whether there is a measurable encoding fingerprint associated with hit-labeled songs in a genre — **without** claiming that fingerprint causes charts.

## Primary hypothesis

**H1 (encode separation).**  
Among genre-, language-, and era-matched stimuli, tracks meeting a pre-registered **hit label** criterion produce systematically different predicted average-subject cortical response patterns under TRIBE v2 / VideoCortex than matched non-hits — especially in auditory / temporal / language-adjacent ROIs and in temporal dynamics of regional energy — **after** controlling for loudness, duration, and (where available) vocal presence / cut-rate confounds.

Operationalization of “hit label” is fixed in the cohort sheet before analysis (examples: national chart peak ≤ N, certification, or streams threshold). One definition per pilot; no peeking.

## Null and alternatives

**H0.** After matching and confound regression, hit vs non-hit labels do **not** separate encode summaries better than a permutation null (label shuffle within matched pairs or within cohort).

**H2 (confound).** Any apparent separation collapses when stimuli are loudness-normalized, duration-matched more tightly, or reduced to instrumental stems — i.e. the effect is production energy / density, not “hitness.”

**H3 (fame proxy).** Within-artist hit vs deep-cut pairs show little or no separation once artist and era are held fixed — suggesting catalog fame/production era, not a general hit circuit.

**H4 (craft bridge — deferred, non-causal).** Even if H1 fails, encode diffs between *high vs low lyric hit-shaped craft scores* (artist-twin Insight) may still separate maps. That would support craft priors, still not chart forecasts. **Out of scope for pilot v0** unless H1 is inconclusive and time remains.

## Predictions if H1 is supported

1. Higher mean energy and/or more sustained time-courses in pre-registered auditory ROIs for hits vs controls.
2. Multivariate distance (e.g. track-level ROI feature vectors) separates classes above permutation chance.
3. Effect survives loudness covariate; shrinks but does not vanish under H2-style controls (or we accept H2).

## Falsifiers

- No separation after pre-registered tests → report H0; stop product mythology.
- Separation vanishes under loudness/duration controls → support H2; do not market as hit fingerprint.
- Within-artist pairs null → support H3.
- Encode failures / TRIBE lag misuse / mismatched lag modes invalidate the run — fix protocol, do not interpret.

## What success does *not* mean

Supporting H1 does **not** authorize:

- decoding songs from desired activation maps;
- claiming high probability of commercial success;
- hard-gating artist-twin generation on cortex scores.

It authorizes: “interesting encoding difference in this cohort under this instrument.”

## Pre-registration discipline

Before the first real encode batch:

1. Freeze cohort inclusion rules and hit definition in `stimuli/manifests/cohort-v0.yaml` (or csv).
2. Freeze primary ROI list and primary test in `docs/experiment-plan.md`.
3. Record VideoCortex / TRIBE commit + weight hashes in each run receipt.
