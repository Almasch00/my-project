---
workflow: general-video
flow: automation
storyboard: no
message: "Billie keeps your Odoo reorder rules right, automatically — book a 20-minute stock check"
destination: youtube
aspect: 1920x1080
language: en
length: 66s
audience: Odoo users running inventory/procurement (SMB operations, purchasing, finance)
---

## Intent

Sales video for **Billie**, Bay Forward's AI procurement agent that works inside Odoo.
Follow the same ideas and style direction as the reference "Lisa (v.1.1)" sales video:
same subtitle style, same text transitions and animation language, motion graphics throughout.
About 1 minute, driven by the supplied voiceover.

## Assets

- assets/vo.mp3 — ElevenLabs voiceover (Kristen, warm corporate), 66.4s; drives the timeline.
- assets/billie.png — red/white robot; use as the Billie logo/mascot.
- assets/bayforward.svg — Bay Forward logo (navy, for light backgrounds).
- assets/bayforward-white.svg — Bay Forward logo (white, for dark backgrounds).
- assets/odoo.png — original Odoo logo (supplied by user); replaces the earlier glyph everywhere.
- assets/music-src-micrah-the-event.mp3 — "Micrah - The Event" (supplied by user); music bed, kept low (src/prepare_music.sh).
- assets/footage/warehouse-floor.mp4 (hook only) — Intel sample-videos (github.com/intel-iot-devkit/sample-videos), CC BY 4.0; credit required.
- Reference (not shipped): Lisa_v.1.1_1.mp4 — style source.

## Customizations

- Subtitles in the same style as the Lisa video (white bold sans on dark-grey rounded per-line boxes, bottom centre).
- Text transitions/animations styled like Lisa: rolling blurred word carousel, card collapse-to-line, curved ribbon swoosh ("Meet / Billie"), toggle, blue split-screen pill list, "runs on Odoo" reveal, gradient big-letter logo close.
- Subtle SFX on transitions; music bed = user's "Micrah - The Event", low and carved under the VO (synthesized bed removed).
- Footage from free sources: Unsplash/Pexels/Pixabay are blocked in this environment, so CC BY 4.0 clips from Intel sample-videos are used (hook background only; overstock scene keeps its motion graphics per user).
- End CTA: "Book a 20-minute stock check" with info@bayforward.be in small text.

## Notes

- Swap footage by replacing files in assets/footage/ (same names) and running src/make.sh.
- Network: no CDN, no Hugging Face — all assets local.
