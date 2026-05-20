#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$ROOT_DIR/qhgas-ha/custom_components"
OUT_DIR="$ROOT_DIR/dist"
TMP_DIR="$ROOT_DIR/.tmp_hacs_pkg"
ZIP_NAME="qhgas.zip"

if [[ ! -d "$SRC_DIR/qhgas" ]]; then
  echo "Error: source component directory not found: $SRC_DIR/qhgas" >&2
  exit 1
fi

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR/custom_components" "$OUT_DIR"
cp -R "$SRC_DIR/qhgas" "$TMP_DIR/custom_components/"

(
  cd "$TMP_DIR"
  zip -r "$OUT_DIR/$ZIP_NAME" custom_components >/dev/null
)

rm -rf "$TMP_DIR"
echo "Created package: $OUT_DIR/$ZIP_NAME"
