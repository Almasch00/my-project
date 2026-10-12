---
workflow: general-video
flow: automation
storyboard: no
message: "Uvaré's Discovery Set: a luxurious way to find your signature scent"
destination: Instagram Reels / TikTok
aspect: "9:16"
length: 18s
---

# Uvaré — Discovery Set tester reel

## Intent
User: "edit them according to my references … full independence … output should match the luxury and premium level of my references. Use royalty free luxury premium music."
References (Pinterest): 924152786041626021, 294422894412501621, 1071786411316965412.

## Assets
- Raw shots: Google Drive folder `Uvare` (10vvnXchu2lCVlWrY-3zGlRCo_fQsUQ3V). Used IMG_1179, 1205, 1176, 1208, 1209.
  Skipped IMG_1207 (0.7s, hand in frame) and IMG_1162.HEIC (still).
- Logo: `assets/uvare-logo-original.png` (user supplied) → `assets/uvare-logo-ivory.png`.
- Reference: user-supplied Salt & Stone tester reel (Pinterest is unreachable from the cloud session).
- Music: original 110 BPM groove, `src/compose_groove.py` (FluidR3_GM samples, MIT + synthesised drums) → `assets/music.wav`.

## Notes
- v1 (warm grade, slow dissolves, serif captions) rejected: "too yellow and brown", not like the reference.
- v2 follows the reference: neutral/cool near-monochrome grade matched by measurement, 11 hard cuts on the
  beat of a 110 BPM groove, close punch-ins and tilts, no captions, clean white end card with the black logo.
- Footage is not committed: rebuild with `python3 -I src/grade_match.py <raw_dir> footage`.
