#!/usr/bin/env bash
# Copy or hardlink TRIBE / encoder weights from an existing VideoCortex or
# HuggingFace cache into this experiment's *private* data root.
#
# Never downloads. Never writes into a VideoCortex checkout.
# Prefer hardlinks when source and dest are on the same filesystem.
#
# Usage:
#   scripts/import-weights.sh --from /path/to/videocortex-or-hf-cache
#   scripts/import-weights.sh --hf-src ~/.cache/huggingface/hub \
#       --feature-src /path/to/videocortex/.videocortex-cache
#
# Destinations (override as needed):
#   HF hub:  $HUGGINGFACE_HUB_CACHE  or  $HF_HOME/hub  or  ~/.cache/huggingface/hub
#   Features: $CORTEX_HIT_ENCODE_CACHE  or  ./.che-cache
set -euo pipefail

REQUIRED_REPOS=(
  "facebook/tribev2"
  "facebook/w2v-bert-2.0"
  "facebook/dinov2-large"
  "meta-llama/Llama-3.2-3B"
  "facebook/vjepa2-vitg-fpc64-256"
)

FROM=""
HF_SRC=""
HF_DEST=""
FEATURE_SRC=""
FEATURE_DEST=""
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: scripts/import-weights.sh [options]

  --from DIR            Search this tree for HF hub model dirs and an optional
                        .videocortex-cache / .che-cache feature cache
  --hf-src DIR          Explicit HF hub cache (contains models--* directories)
  --hf-dest DIR         Destination hub cache (default: $HUGGINGFACE_HUB_CACHE
                        or $HF_HOME/hub or ~/.cache/huggingface/hub)
  --feature-src DIR     Optional VideoCortex feature cache to import
  --feature-dest DIR    Destination feature cache (default:
                        $CORTEX_HIT_ENCODE_CACHE or ./.che-cache)
  --dry-run             Print the plan; do not copy
  -h, --help            Show this help

Never calls HuggingFace. If a required source is missing, exits 1.
Do not modify VideoCortex — this script only *reads* it.
EOF
}

die() { echo "ERROR: $*" >&2; exit 1; }

hub_dirname() {
  # facebook/tribev2 -> models--facebook--tribev2
  local repo="$1"
  echo "models--${repo//\//--}"
}

default_hf_dest() {
  if [ -n "${HUGGINGFACE_HUB_CACHE:-}" ]; then
    echo "$HUGGINGFACE_HUB_CACHE"
  elif [ -n "${HF_HOME:-}" ]; then
    echo "$HF_HOME/hub"
  else
    echo "$HOME/.cache/huggingface/hub"
  fi
}

default_feature_dest() {
  if [ -n "${CORTEX_HIT_ENCODE_CACHE:-}" ]; then
    echo "$CORTEX_HIT_ENCODE_CACHE"
  else
    echo "$(pwd)/.che-cache"
  fi
}

same_filesystem() {
  local src="$1" dest_parent="$2"
  local src_dev dest_dev
  src_dev=$(stat -c '%d' "$src" 2>/dev/null || stat -f '%d' "$src")
  dest_dev=$(stat -c '%d' "$dest_parent" 2>/dev/null || stat -f '%d' "$dest_parent")
  [ "$src_dev" = "$dest_dev" ]
}

copy_or_hardlink() {
  local src="$1" dest="$2"
  if [ -e "$dest" ]; then
    echo "  exists   $dest"
    return 0
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "  would   $src -> $dest"
    return 0
  fi
  mkdir -p "$(dirname "$dest")"
  if same_filesystem "$src" "$(dirname "$dest")"; then
    if cp -al "$src" "$dest" 2>/dev/null; then
      echo "  hardlink $src -> $dest"
      return 0
    fi
    if command -v rsync >/dev/null 2>&1; then
      mkdir -p "$dest"
      if rsync -a --link-dest="$src" "$src"/ "$dest"/; then
        echo "  hardlink $src -> $dest"
        return 0
      fi
    fi
  fi
  cp -a "$src" "$dest"
  echo "  copied   $src -> $dest"
}

dir_nonempty() {
  [ -d "$1" ] && [ -n "$(find "$1" -mindepth 1 -maxdepth 1 2>/dev/null | head -n 1)" ]
}

human_size() {
  if [ ! -e "$1" ]; then
    echo "missing"
    return
  fi
  du -sh "$1" 2>/dev/null | awk '{print $1}'
}

find_hub_root() {
  local root="$1"
  local probe="models--facebook--tribev2"
  local cand
  for cand in \
    "$root" \
    "$root/hub" \
    "$root/huggingface/hub" \
    "$root/.cache/huggingface/hub" \
    "$root/hub/hub"
  do
    if [ -d "$cand/$probe" ]; then
      echo "$cand"
      return 0
    fi
  done
  return 1
}

find_feature_cache() {
  local root="$1"
  local cand
  for cand in \
    "$root/.videocortex-cache" \
    "$root/.che-cache" \
    "$root"
  do
    if dir_nonempty "$cand" && { [ "$(basename "$cand")" = ".videocortex-cache" ] \
      || [ "$(basename "$cand")" = ".che-cache" ]; }; then
      echo "$cand"
      return 0
    fi
  done
  return 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --from) FROM="${2:-}"; shift 2 ;;
    --hf-src) HF_SRC="${2:-}"; shift 2 ;;
    --hf-dest) HF_DEST="${2:-}"; shift 2 ;;
    --feature-src) FEATURE_SRC="${2:-}"; shift 2 ;;
    --feature-dest) FEATURE_DEST="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

if [ -z "$HF_SRC" ]; then
  if [ -z "$FROM" ]; then
    die "pass --from DIR and/or --hf-src DIR (a local cache; this script does not download)"
  fi
  if ! HF_SRC=$(find_hub_root "$FROM"); then
    die "no HF hub model dirs under $FROM (looked for models--facebook--tribev2). Pass --hf-src."
  fi
fi

[ -d "$HF_SRC" ] || die "HF source is not a directory: $HF_SRC"

if [ -z "$FEATURE_SRC" ] && [ -n "$FROM" ]; then
  FEATURE_SRC=$(find_feature_cache "$FROM" || true)
fi

if [ -z "$HF_DEST" ]; then
  HF_DEST=$(default_hf_dest)
fi
if [ -z "$FEATURE_DEST" ]; then
  FEATURE_DEST=$(default_feature_dest)
fi

case "$HF_DEST" in
  *videocortex*|*VideoCortex*)
    die "HF dest $HF_DEST looks like a VideoCortex path. Point HF_HOME / HUGGINGFACE_HUB_CACHE at a private data root."
    ;;
esac

echo "import-weights (never downloads; never writes into VideoCortex)"
echo "  HF src : $HF_SRC"
echo "  HF dest: $HF_DEST"
if [ -n "$FEATURE_SRC" ]; then
  echo "  feat src: $FEATURE_SRC"
  echo "  feat dest: $FEATURE_DEST"
else
  echo "  feat src: (none — feature cache is optional; will recompute on first encode)"
fi
if [ "$DRY_RUN" -eq 1 ]; then
  echo "  mode   : dry-run"
fi
echo

missing=0
for repo in "${REQUIRED_REPOS[@]}"; do
  name=$(hub_dirname "$repo")
  src="$HF_SRC/$name"
  if ! dir_nonempty "$src"; then
    echo "  MISSING $repo  ($src)"
    missing=1
  else
    echo "  found   $repo  ($(human_size "$src"))"
  fi
done

if [ "$missing" -ne 0 ]; then
  die "required model dirs missing under $HF_SRC — will not download. Copy them here first."
fi

echo
echo "importing hub models -> $HF_DEST"
if [ "$DRY_RUN" -eq 0 ]; then
  mkdir -p "$HF_DEST"
fi
for repo in "${REQUIRED_REPOS[@]}"; do
  name=$(hub_dirname "$repo")
  copy_or_hardlink "$HF_SRC/$name" "$HF_DEST/$name"
done

if [ -n "$FEATURE_SRC" ]; then
  echo
  echo "importing feature cache -> $FEATURE_DEST"
  if [ "$FEATURE_SRC" = "$FEATURE_DEST" ]; then
    echo "  already at destination"
  else
    copy_or_hardlink "$FEATURE_SRC" "$FEATURE_DEST"
  fi
fi

echo
if [ "$DRY_RUN" -eq 1 ]; then
  echo "verify (dry-run): sources present; dest not written"
  echo
  echo "done (dry-run)."
  exit 0
fi

echo "verify"
fail=0
for repo in "${REQUIRED_REPOS[@]}"; do
  name=$(hub_dirname "$repo")
  dest="$HF_DEST/$name"
  size=$(human_size "$dest")
  if dir_nonempty "$dest"; then
    echo "  ok      $repo  $size"
  else
    echo "  FAIL    $repo  ($dest)"
    fail=1
  fi
done
if [ -n "$FEATURE_SRC" ]; then
  if dir_nonempty "$FEATURE_DEST"; then
    echo "  ok      feature cache  $(human_size "$FEATURE_DEST")"
  else
    echo "  FAIL    feature cache  ($FEATURE_DEST)"
    fail=1
  fi
fi

if [ "$fail" -ne 0 ]; then
  die "verification failed"
fi

echo
echo "done. Point HF_HOME / HUGGINGFACE_HUB_CACHE at the private dest, then:"
echo "  che doctor --offline"
echo "  che render --audio path/to/stimulus.wav"
