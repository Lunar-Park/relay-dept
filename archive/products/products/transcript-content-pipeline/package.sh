#!/usr/bin/env bash
# Package the Transcript -> Content Pipeline skill into an uploadable zip.
#
# Produces a zip whose root contains the `transcript-content-pipeline/` folder
# with SKILL.md at its root (required by Claude's Skills uploader).
#
# Usage:
#   ./package.sh                 # writes ./dist/transcript-content-pipeline.zip
#   ./package.sh ~/Desktop       # writes the zip into the given directory
#   ./package.sh ~/Desktop/x.zip # writes the zip to the given file path

set -euo pipefail

SKILL_NAME="transcript-content-pipeline"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$ROOT_DIR/skill"

# Always build inside the project dir. Some sandboxed environments discard
# writes made outside the working tree (e.g. directly to ~/Desktop or a temp
# dir), so we stage + zip here, then copy to the destination at the end.
DIST_DIR="$ROOT_DIR/dist"
STAGE="$DIST_DIR/.stage"
BUILT_ZIP="$DIST_DIR/$SKILL_NAME.zip"

rm -rf "$STAGE"
mkdir -p "$STAGE/$SKILL_NAME"
cp -R "$SKILL_SRC"/. "$STAGE/$SKILL_NAME/"

# Build the zip (SKILL.md ends up at the folder root)
rm -f "$BUILT_ZIP"
( cd "$STAGE" && zip -rq "$BUILT_ZIP" "$SKILL_NAME" -x '*.DS_Store' '*/__pycache__/*' )
rm -rf "$STAGE"

# Resolve and copy to the requested destination (default: leave in ./dist)
DEST_ARG="${1:-}"
OUT_ZIP="$BUILT_ZIP"
if [[ -n "$DEST_ARG" ]]; then
  if [[ "$DEST_ARG" == *.zip ]]; then
    OUT_ZIP="$DEST_ARG"
  else
    OUT_ZIP="$DEST_ARG/$SKILL_NAME.zip"
  fi
  mkdir -p "$(dirname "$OUT_ZIP")"
  cp "$BUILT_ZIP" "$OUT_ZIP"
fi

echo "Packaged skill -> $OUT_ZIP"
unzip -l "$OUT_ZIP"
