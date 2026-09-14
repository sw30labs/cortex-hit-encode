# Non-goals

Binding until a new ADR supersedes.

1. **No decoder** — will not build activation → audio/lyrics/video synthesis in this repo.
2. **No artist-twin generate wiring** — no LangGraph nodes, album gates, or YuE2 prompt injection from cortex scores.
3. **No hit probability product** — no `hit_probability`, “likely a hit,” “% chance,” Billboard forecast, chart forecast, “ensure a hit,” or any chart-forecast UI.
4. **No mass scraping** — no Billboard/YouTube/Spotify harvesters as a feature; user-supplied rights-cleared media only.
5. **No claiming personal neural readout** — no mind-reading, no “this is what someone is thinking”; average-subject predictions only.
6. **No vendoring TRIBE weights** — depend on VideoCortex / upstream HF under NC terms.
7. **No Karpathy Autoresearch mega-loop** in v0 — fixed pilot cohort, pre-registered tests, one report.
8. **No H4 in v0** — lyric *hit-shaped craft* bridge stays deferred (see [hypothesis.md](hypothesis.md)).

## Language (canonical)

Same list as the README. Use it in papers, UX, and run notes.

**Say:** *hit-labeled cohort*, *encode separation*, *predicted cortical response*, *predicted average-subject maps*. *hit-shaped craft* only if bridging later (H4, deferred).

**Never:** `hit_probability`, “likely a hit,” “% chance,” Billboard forecast, chart forecast, “ensure a hit,” “this is what someone is thinking,” mind-reading, decoder claims.
