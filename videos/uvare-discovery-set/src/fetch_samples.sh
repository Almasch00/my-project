#!/bin/bash
# Fetch the FluidR3_GM note samples (MIT licence) used by compose_music.py.
set -euo pipefail
DEST="${1:?usage: fetch_samples.sh <dir>}"
BASE=https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/FluidR3_GM
NOTES="C Db D Eb E F Gb G Ab A Bb B"
for inst in acoustic_grand_piano string_ensemble_1 pad_2_warm celesta; do
  mkdir -p "$DEST/$inst"
  for o in 1 2 3 4 5 6 7; do for nn in $NOTES; do
    f="$DEST/$inst/$nn$o.mp3"; [ -s "$f" ] || curl -sf -o "$f" "$BASE/$inst-mp3/$nn$o.mp3" || rm -f "$f"
  done; done
done
