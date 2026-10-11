#!/bin/bash
# Trim "Micrah - The Event" to the video length and sit it well below the voiceover.
# Fade in, a lift for the end card after the VO ends (66.4s), fade out at 69s.
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i assets/music-src-micrah-the-event.mp3 -t 69 \
  -af "volume=-17dB,volume='if(gte(t,66.4),1.8,1)':eval=frame,afade=t=in:st=0:d=0.6,afade=t=out:st=66.6:d=2.4,aresample=48000" \
  -ac 2 assets/music.wav
echo "music ready"
