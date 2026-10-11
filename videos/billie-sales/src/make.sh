#!/bin/bash
# Regenerate compositions + SFX. Music was removed at the user's request (v5);
# to bring it back: re-add the <audio id="music"> line in src/build.py, run
# src/prepare_music.sh, then carve:
#   node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music --voice vo
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/build.py
python3 -I src/audio_synth.py assets >/dev/null   # sfx.wav
echo "built"
