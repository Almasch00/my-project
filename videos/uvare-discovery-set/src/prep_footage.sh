#!/bin/bash
# Rebuild footage/ from the raw iPhone clips (Drive folder "Uvare").
# HLG HDR MOVs are tone-mapped to SDR; every shot is rotated/scaled to 1080x1920
# and given the same warm, soft-highlight luxury grade.
# usage: bash src/prep_footage.sh <raw_dir>
set -euo pipefail
RAW="${1:?usage: prep_footage.sh <raw_dir>}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/footage"
mkdir -p "$OUT"
GRADE="eq=contrast=1.07:saturation=0.9:gamma=0.97,colorbalance=rs=0.02:bs=-0.03:rm=0.03:gm=0.005:bm=-0.03:rh=0.02:bh=-0.04,curves=master='0/0.02 0.25/0.21 0.75/0.76 1/0.94'"
ENC=(-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 30 -g 15 -an -movflags +faststart -color_primaries bt709 -color_trc bt709 -colorspace bt709)
HDR="zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
for f in IMG_1176 IMG_1179; do
  ffmpeg -v error -y -i "$RAW/$f.MOV" -vf "$HDR,scale=1080:1920:flags=lanczos,$GRADE" "${ENC[@]}" "$OUT/${f,,}.mp4"
done
for f in IMG_1205 IMG_1208 IMG_1209; do
  ffmpeg -v error -y -i "$RAW/$f.MP4" -vf "scale=1080:1920:flags=lanczos:in_range=pc:out_range=tv,$GRADE" "${ENC[@]}" "$OUT/${f,,}.mp4"
done
