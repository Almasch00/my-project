---
workflow: general-video
flow: automation
storyboard: no
message: "Uvaré's Discovery Set: a luxurious way to find your signature scent"
destination: Instagram Reels / TikTok
aspect: "9:16"
length: 24s
---

# Uvaré — Discovery Set tester reel

## Intent
User: "edit them according to my references … full independence … output should match the luxury and premium level of my references. Use royalty free luxury premium music."
References (Pinterest): 924152786041626021, 294422894412501621, 1071786411316965412.

## Assets
- Raw shots: Google Drive folder `Uvare` (10vvnXchu2lCVlWrY-3zGlRCo_fQsUQ3V). Used IMG_1179, 1205, 1176, 1208, 1209.
  Skipped IMG_1207 (0.7s, hand in frame) and IMG_1162.HEIC (still).
- Logo: `assets/uvare-logo-original.png` (user supplied) → `assets/uvare-logo-ivory.png`.
- Music: original score, `src/compose_music.py` (FluidR3_GM samples, MIT) → `assets/music.wav`.

## Notes
- Cuts on bar lines of a 72 BPM score (bar = 3.333s), 0.6s dissolves with warm light bloom.
- Footage is not committed: rebuild with `bash src/prep_footage.sh <raw_dir>`.
