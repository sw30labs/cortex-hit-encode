# Report v0 — cortex-hit-encode pilot

Date: 2026-09-14 (same-day freeze → encode → analysis; exploratory pilot)
Instrument: `che` 0.1.0 (vendored VideoCortex commit b345895, TRIBE v2 local cache, MPS, torch 2.6.0)
Cohort: `stimuli/manifests/cohort-v0.csv`, freeze commit `30e6d8b`
Receipts: `/Volumes/DATA/cortex-hit-encode/runs/v0/<id>/receipt.json` (28/28 status=ok)
Stimulus hashes: `stimuli/manifests/hashes-v0.json`
Numbers machine-generated: `analysis/results-v0.json`, `analysis/phase4.py`
Figure: `analysis/null-dist-v0.png`

## Question

Do hit-labeled tracks produce a different predicted average-subject cortical
response (TRIBE v2 encoding) than matched non-hits from the same artists?
This is an encoding-separation test. It says nothing about what any
individual listener thinks, and it is not a hit predictor.

## Method (as frozen in docs/protocol.md)

- 14 within-artist pairs (28 stimuli), Argentine-rock canon, 8 artists
  (Soda Stereo, Los Redondos, Sumo, Fito Páez, Charly García, Indio Solari,
  Babasónicos; Virus dropped — catalog too thin on the source).
- Hit definition `deezer-rank-top2-vs-deepcut`: top-2 by Deezer popularity
  rank vs lowest-rank deep cut from the same artist pull (api.deezer.com,
  retrieved 2026-09-14T09:11:40Z). Popularity-proxy label, pre-registered.
- Media: official Deezer 30s preview assets (rights basis recorded per row).
  All stimuli 30 s (trim policy trivially satisfied).
- Loudness: two-pass EBU R128 loudnorm toward −16 LUFS; peak-limiter capped
  true peak left post files at −19.2…−20.2 LUFS uniformly; achieved
  `lufs_post` carried as covariate.
- Endpoint (frozen): `mean_auditory_roi_energy` — mean |x| over L/R Destrieux
  `G temp sup-G T transv`, `G temp sup-Plan tempo`, `G temp sup-Lateral`
  (573 fsaverage5 vertices), averaged across TRs.
- Test (frozen): two-sided within-pair sign-flip permutation, 20,000 draws,
  unadjusted and adjusted for lufs_post + duration.

## Result

| Quantity | Value |
|---|---|
| mean endpoint, hits | 0.1784 |
| mean endpoint, non-hits | 0.1915 |
| paired diff (hit − nonhit) | −0.0131 |
| dz | −0.21 |
| permutation p (unadjusted) | 0.448 |
| permutation p (covariate-adjusted) | 0.544 |
| pairs where hit > nonhit | 6 / 14 |

The point estimate points the *opposite* way from the H1 prediction (hits
slightly lower, not higher) and is indistinguishable from the permutation
null in either direction.

## Call (pre-registered rules, docs/hypothesis.md)

- **H1: not supported. H0 stands.** The primary test does not beat the
  permutation null. Per call rule 1: stop product mythology.
- **H2: not reached** (no separation left to explain away).
- **H3: not separately testable here.** Every pair is within-artist, so the
  primary test *is* the within-artist slice; its null result is consistent
  with H3 (fame-proxy reading) but cannot separate H3 from H0.

## Limitations (honest list)

1. 30-second previews only — no song structure, no dynamics beyond 30 s.
2. TRIBE predicts an *average subject* fitted mostly on continuous natural
   stimulation; produced music clips are off-distribution for it.
3. Hit label is a 2026 streaming-popularity proxy, not chart history.
4. All pairs within-artist: strongest matching, but H1/H3 slices overlap by
   construction (recorded at freeze).
5. Loudness normalization was true-peak-limited, leaving all files ~3–4 dB
   below target; residuals are uniform and carried as a covariate.
6. N=14 pairs → a true small effect (|dz| < ~0.8) would be missed. The dz
   here (−0.21) is far too small to rescue with more power at this endpoint.
7. Same-day freeze→analyze means minimal cooling-off; treat as exploratory.

## What this does not mean

This does not imply hit labels have no acoustic correlate, that prediction
is impossible from longer windows or other endpoints, or anything about
chart outcomes, causality, or any individual brain. Language ban list
observed: no hit-probability, forecasting, or mind-reading claims.
