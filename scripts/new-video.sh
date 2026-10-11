#!/bin/bash
# Scaffold a HyperFrames project under videos/<name> that works offline from the CDN:
# GSAP is copied from node_modules into the project because cdn.jsdelivr.net is
# blocked in Claude Code cloud sessions.
#
# usage: npm run new-video -- <name> [extra `hyperframes init` flags]
#   e.g. npm run new-video -- my-recut --resolution portrait --video ~/footage.mp4 --skip-transcribe
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: npm run new-video -- <name> [hyperframes init flags]" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="$1"
shift

cd "$ROOT/videos"
npx hyperframes init "$NAME" --non-interactive "$@"
"$ROOT/scripts/vendor-gsap.sh" "$ROOT/videos/$NAME"
echo "Created videos/$NAME"
