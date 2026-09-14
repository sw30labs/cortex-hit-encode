# Report v2 — cortex-hit-encode round 2 (full tracks, user-labeled cohort)

Date: 2026-09-14 (same-day freeze → encode → analysis; exploratory round 2)
Instrument: `che` 0.1.0 (vendored VideoCortex commit b345895, TRIBE v2 local cache, MPS, torch 2.6.0)
Cohort: `stimuli/manifests/cohort-v2.csv`, freeze commit `c396d13`, addendum in `docs/protocol.md`
Receipts: `/Volumes/DATA/cortex-hit-encode/runs/v2/<id>/receipt.json` (22/22 status=ok)
Stimulus hashes: `stimuli/manifests/hashes-v2.json` (media on /Volumes/DATA, not in git)
Numbers machine-generated: `analysis/results-v2.json`, `analysis/phase4_v2.py`
Figure: `analysis/null-dist-v2.png` (`analysis/plot_null_v2.py` — recomputes the
test from disk; reproduces obs/p exactly)

## Question

Same frozen question as v0: do hit-labeled tracks produce a different
predicted average-subject cortical response (TRIBE v2 encoding) than matched
non-hits from the same artists? Round 2 upgrades the stimuli: **full tracks
instead of 30 s previews**, and a fame-labeled cohort you curated by hand.

## Method (as frozen in docs/protocol.md, v2 addendum)

- 11 within-artist pairs (22 stimuli), Argentine rock, 9 artists
  (Soda Stereo ×2, Sumo ×2, Charly García, Fito Páez, Redondos,
  Indio/WOS, Skay Beilinson, Attaque 77, Enanitos Verdes).
- Hit definition v2: `user-labeled-v2-folders` (your 24hits/24nonhits
  assignment), with YouTube view_count per source recorded as popularity
  evidence. Not a chart definition.
- Exclusions held at freeze: 34-min epic ("El cielo puede esperar"),
  Cerati "Cosas Imposibles" (labeled nonhit, 56M views — pairing it would
  poison a pair), unpaired extras, orphans without metadata.
- Media: user-supplied full-track WAVs; `trim_policy = full_track`
  (durations 134–322 s). Loudness: same −16 LUFS two-pass policy;
  `lufs_post` carried as covariate.
- Endpoint, test, lag mode, ROI list: **identical to v0** (frozen —
  mean |x| over 573 Destrieux auditory ROI vertices; within-pair sign-flip
  permutation, 20,000 draws; unadjusted + adjusted for lufs_post, duration).

## Result

| Quantity | v2 (full tracks) | v0 (30 s previews) |
|---|---|---|
| n pairs | 11 | 14 |
| mean endpoint, hits | 0.1338 | 0.1784 |
| mean endpoint, non-hits | 0.1363 | 0.1915 |
| paired diff (hit − nonhit) | −0.00246 | −0.0131 |
| dz | −0.055 | −0.21 |
| permutation p (unadjusted) | 0.841 | 0.448 |
| permutation p (covariate-adjusted) | 0.842 | 0.544 |
| pairs where hit > nonhit | 4 / 11 | 6 / 14 |

Direction again nominally *opposite* the H1 prediction (hits slightly lower)
and even closer to zero than in v0. The endpoint also shows a general level
shift for full tracks (means ~0.134 vs ~0.178) — expected: TRIBE mean ROI
energy averages over TRs, and full tracks include long quiet/structural
 stretches absent from a 30 s hook-of-the-song preview.

## Call (pre-registered rules, docs/hypothesis.md)

- **H1: not supported. H0 stands, again.** Same call as v0, now on a second,
  better-powered stimulus class. Per call rule 1: stop product mythology.
- **H2: not reached** (nothing to explain away).
- **H3: not separately testable here** — all pairs within-artist; consistent
  with H3 but indistinguishable from H0.

## Limitations (honest list)

1. n=11 pairs: only a large effect (|dz| ≳ 0.9) would be detectable. The
   observed dz (−0.055) is essentially zero — more pairs at *this endpoint*
   would not rescue it (same conclusion as v0, from an independent cohort).
2. Hit label = user folder assignment + YouTube views, not chart history;
   views are biased by upload age/channel (recorded at freeze).
3. "QUEMARÁS" pair spans two artists (WOS ft. Indio vs an Indio deep cut) —
   kept but flagged at freeze.
4. TRIBE predicts an *average subject* fitted on continuous natural
   stimulation; produced full tracks remain off-distribution, and the
   duration/structure confound (loud quiet sections) rides on the endpoint —
   which is exactly what the covariate adjustment handles, and it changed
   nothing (0.841 → 0.842).
5. Same-day freeze→analyze; exploratory.

## What this does not mean

Two independent rounds (14 pairs of previews; 11 pairs of full tracks),
different labels, different media, same frozen endpoint and test — both null,
both with a point estimate on the wrong side of zero. This does not prove
hit-label acoustics are undefinable; it does say that *this* instrument at
*this* endpoint finds no hit/non-hit separation in either direction. No
hit-probability, forecasting, or mind-reading claims.

## What would actually change the picture

Not more pairs at this endpoint (dz ≈ 0 already). If this line of work
continues, the informative moves are a different readout (e.g.
encoding-prediction *error* against real fMRI, or brain-encoding similarity
to observed responses) — not another round of label-matched averages.
