# Conclusion — cortex-hit-encode (research closed)

Date: 2026-09-14
Decision: **Close the research line. H0 stands; H1 not supported in two
independent rounds.** Per pre-registered call rule 1 (docs/hypothesis.md):
stop product mythology. No round 3 at this endpoint.

## What we ran

| Round | Cohort | Stimuli | Endpoint + test (frozen, identical) | Result |
|---|---|---|---|---|
| v0 | cohort-v0, freeze `30e6d8b` — 14 within-artist pairs, Deezer-rank hit definition | 30 s official previews, 8 Argentine-rock artists | `mean_auditory_roi_energy`; within-pair sign-flip permutation, 20k draws | dz = −0.21, p = 0.448 (adj 0.544), hits > nonhits in 6/14 |
| v2 | cohort-v2, freeze `c396d13` — 11 within-artist pairs, user-labeled folders + YouTube view evidence | full tracks (134–322 s), user-supplied WAVs, 9 artists | same | dz = −0.055, p = 0.841 (adj 0.842), hits > nonhits in 4/11 |

Both rounds: 28/28 and 22/22 encodes `status=ok`, receipts on
/Volumes/DATA, hashes + manifests in git, protocol frozen **before**
analysis each time (addenda recorded in docs/protocol.md). Reports:
`analysis/report-v0.md`, `analysis/report-v2.md`. Numbers:
`analysis/results-v0.json`, `analysis/results-v2.json` (machine-generated;
figures independently recomputed from disk and match).

## The finding, in one paragraph

An encoding model that predicts how an average human cortex responds to
sound found **no difference** between a band's famous hits and their obscure
deep cuts from the same catalog — not with 30-second clips, and not with full
tracks. If anything the trend ran very slightly the *other* way (hits marginally
lower auditory-ROI energy), shrinking toward zero in the better round. Two
independent cohorts, two label sources, two media types, one frozen readout:
a consistent, unambiguous null.

## Assumptions we relied upon (and what closes if they're wrong)

The conclusion is only as strong as these. Each was recorded at freeze;
none was tested by this experiment itself:

1. **Instrument validity.** TRIBE v2's predicted *average-subject* response
   is a meaningful stand-in for how human cortex differentiates produced
   music. TRIBE was fitted mostly on continuous naturalistic stimulation;
   commercial tracks are off-distribution. If the model's auditory-ROI
   output is simply insensitive to whatever differs between these songs,
   our null says "the meter doesn't move," not "nothing differs."
2. **Endpoint sufficiency.** `mean_auditory_roi_energy` (mean |x| over 573
   Destrieux auditory vertices, averaged over TRs) captures the kind of
   difference H1 predicted. H1 also named temporal *dynamics* and
   multivariate patterns as secondary; we never tested those. A null at the
   mean-energy gate does not falsify every possible encode-level signature.
3. **Label validity.** "Hit" was a popularity proxy both times (Deezer rank
   in v0; user folder assignment + YouTube views in v2 — views biased by
   upload age/channel). If hit status is not substantially carried by
   acoustic/perceptual properties of the recording at all (promotion,
   culture, timing, lyric semantics beyond what the encoder represents),
   the experiment was asking the cortex a question it cannot answer.
4. **Matching is not confound-free.** Within-artist pairing controls artist,
   language, era, production style aggressively — arguably too aggressively:
   it also removes much of the between-song variance H1 needs. Loudness
   normalized to a shared policy; residuals carried as covariates (they
   changed nothing: 0.841 → 0.842).
5. **Average-subject generalization.** One predicted cortex, not many. No
   claim here touches any individual listener.
6. **Statistical power.** 14 and 11 within-artist pairs detect large effects
   only. But both point estimates sat on the wrong side of zero with
   |dz| ≤ 0.21 — no plausible power at this endpoint rescues that.

Assumptions 1–3 are the load-bearing ones. Rejecting any one of them
reopens a *different* experiment (different instrument, readout, or label
theory), not this one.

## Call against the pre-registered rules

- **H1 (encode separation): not supported.** Call rule 1 fired both rounds.
- **H2 (confound): not reached** — there was no separation left to explain away.
- **H3 (fame proxy): unfalsifiable here** — every pair was within-artist, so
  the primary test *was* the within-artist slice; its null is consistent
  with H3 but cannot separate H3 from H0.
- **H4 (craft bridge): never triggered** (required H1-supporting or
  inconclusive ground; conditions not met).

## What we are NOT claiming (language ban enforced)

No hit prediction, no chart forecasting, no `hit_probability`, no
mind-reading, no decoder claims, no artist-twin gating on cortex scores
(docs/non-goals.md). "The instrument found no separation in this cohort" is
the entire claim.

## What closing looks like

- The `che` instrument stays: it is self-contained, tested, and reusable
  (`che doctor`, `che render`), and both cohort manifests, hashes, receipts
  and analysis scripts are reproducible. The instrument outlives the thesis.
- If the question ever reopens, the informative directions are a different
  readout (encoding-prediction *error* against real fMRI; inter-subject
  correlation on produced music) or a different label theory — not another
  round of label-matched mean-energy comparisons. We said this explicitly in
  report-v2 and we hold to it.
- Media policy unchanged: audio stays on /Volumes/DATA and out of git
  (docs/local-data.md).

## Verdict

The thesis was: *hitness leaves a fingerprint in predicted auditory cortex
encoding.* Under a pre-registered endpoint, pre-registered test, two
cohorts, and better data each round — the fingerprint never appeared.
Falsified at the tested operationalization. Closed cleanly, in the open.
