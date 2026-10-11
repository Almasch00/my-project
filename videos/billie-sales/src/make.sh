#!/bin/bash
# Regenerate compositions, then re-apply the voiceover carve to the music bed.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/build.py
node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music --voice vo >/dev/null
echo "built + carved"
