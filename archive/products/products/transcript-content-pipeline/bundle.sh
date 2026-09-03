#!/usr/bin/env bash
# Build the public product download: ONE versioned zip a customer downloads.
#
# Unzipping it gives:
#   transcript-content-pipeline/
#     START-HERE.html                          # setup guide
#     transcript-content-pipeline-skill.zip    # <- the file they upload to Claude
#     examples/                                # sample transcript, .vtt, brand-docs
#     README.md
#
# The inner skill zip keeps SKILL.md at its root so Claude's uploader accepts
# it; the outer zip carries the human-facing docs and examples.
#
# Usage:
#   ./bundle.sh                      # -> ./dist/transcript-content-pipeline-v1.0.zip
#   VERSION=1.1 ./bundle.sh          # set the version
#   VERSION=1.1 ./bundle.sh ~/Desktop  # also copy the product zip there

set -euo pipefail

NAME="transcript-content-pipeline"
VERSION="${VERSION:-1.0}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$ROOT_DIR/dist"
STAGE="$DIST_DIR/.bundle/$NAME"
PRODUCT_ZIP="$DIST_DIR/$NAME-v$VERSION.zip"

# 1. Build the inner skill zip (uploadable, SKILL.md at root)
"$ROOT_DIR/package.sh" >/dev/null
SKILL_ZIP="$DIST_DIR/$NAME.zip"

# 2. Stage the product contents (inside dist so writes persist in sandboxes)
rm -rf "$DIST_DIR/.bundle"
mkdir -p "$STAGE"
cp "$ROOT_DIR/START-HERE.html" "$STAGE/"
cp "$ROOT_DIR/README.md" "$STAGE/"
[[ -f "$ROOT_DIR/LICENSE" ]] && cp "$ROOT_DIR/LICENSE" "$STAGE/"
cp "$SKILL_ZIP" "$STAGE/$NAME-skill.zip"
cp -R "$ROOT_DIR/examples" "$STAGE/examples"

# 3. Zip the product
rm -f "$PRODUCT_ZIP"
( cd "$DIST_DIR/.bundle" && zip -rq "$PRODUCT_ZIP" "$NAME" -x '*.DS_Store' '*/__pycache__/*' )
rm -rf "$DIST_DIR/.bundle"

# 4. Optional copy to a destination
OUT="$PRODUCT_ZIP"
if [[ -n "${1:-}" ]]; then
  DEST="$1"
  [[ "$DEST" == *.zip ]] || DEST="$DEST/$NAME-v$VERSION.zip"
  mkdir -p "$(dirname "$DEST")"
  cp "$PRODUCT_ZIP" "$DEST"
  OUT="$DEST"
fi

echo "Built product package (v$VERSION) -> $OUT"
unzip -l "$OUT"
