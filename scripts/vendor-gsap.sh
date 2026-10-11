#!/bin/bash
# Copy GSAP into a HyperFrames project and point its HTML at the local copy.
# usage: scripts/vendor-gsap.sh <project-dir>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$1"
mkdir -p "$DIR/vendor"
cp "$ROOT/node_modules/gsap/dist/gsap.min.js" "$DIR/vendor/gsap.min.js"
find "$DIR" -name '*.html' -not -path '*/node_modules/*' -print0 |
  xargs -0 -r sed -i -E 's#https://cdn\.jsdelivr\.net/npm/gsap@[0-9.]+/dist/gsap\.min\.js#vendor/gsap.min.js#g'
