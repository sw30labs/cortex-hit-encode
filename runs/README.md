# Runs

Encode outputs stay **local**. Gitignores `runs/**` except this README and the example receipt.

Layout (v0):

```
runs/<cohort>/<stimulus_id>/
  receipt.json       # this repo's metadata (required)
  manifest.json      # VideoCortex run manifest (pointer or copy)
  predictions.npy    # usually gitignored; hash it in the receipt
```

Copy `receipt.example.json` per stimulus. Fill real hashes and paths after Phase 3. The example is a **schema**, not a completed run.
