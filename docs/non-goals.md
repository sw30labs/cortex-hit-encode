# Non-goals

Binding until a new ADR supersedes.

1. **No decoder** — will not build activation → audio/lyrics/video synthesis in this repo.
2. **No artist-twin generate wiring** — no LangGraph nodes, album gates, or YuE2 prompt injection from cortex scores.
3. **No hit probability product** — no `hit_probability`, chart forecast UI, or “ensure a hit” copy.
4. **No mass scraping** — no Billboard/YouTube/Spotify harvesters as a feature; user-supplied rights-cleared media only.
5. **No claiming personal neural readout** — average-subject predictions only.
6. **No vendoring TRIBE weights** — depend on VideoCortex / upstream HF under NC terms.
7. **No Karpathy Autoresearch mega-loop** in v0 — fixed pilot cohort, pre-registered tests, one report.
