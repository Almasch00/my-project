#!/bin/bash
# Regenerate compositions + audio, then re-apply the voiceover carve to the music bed.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/build.py
python3 -I src/audio_synth.py assets >/dev/null   # sfx.wav
src/prepare_music.sh                               # music.wav from Micrah - The Event
node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music --voice vo >/dev/null
echo "built + carved"
