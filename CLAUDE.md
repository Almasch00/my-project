# my-project — video editing with HyperFrames

Videos are built with [HyperFrames](https://github.com/heygen-com/hyperframes): HTML + CSS + GSAP compositions rendered to MP4.
Start any video task with the `/hyperframes` skill (it routes to `/talking-head-recut`, `/embedded-captions`, etc.).

## Layout
- `videos/<name>/` — one HyperFrames project per video (`index.html`, `hyperframes.json`, media).
- `scripts/new-video.sh` — scaffold a project: `npm run new-video -- <name> --resolution portrait [--video file.mp4 --skip-transcribe]`.
- `scripts/vendor-gsap.sh <dir>` — copy GSAP into a project and rewrite CDN URLs to `vendor/gsap.min.js`.
- `.claude/hooks/session-start.sh` — cloud-session setup (npm install, skills, browser path).

## Commands (run inside `videos/<name>/`)
- `npx hyperframes lint` / `npx hyperframes check` — validate before rendering.
- `npx hyperframes render -o renders/out.mp4` — render (outputs are gitignored).
- `npx hyperframes snapshot` — still frames for visual review.

## Cloud-session constraints
- `cdn.jsdelivr.net` is blocked: never load GSAP or other libs from a CDN; use `vendor/` copies (from `node_modules`).
- Hugging Face is blocked: whisper transcription, Kokoro TTS and MusicGen are unavailable. Use `--skip-transcribe` and supply transcripts/word timings yourself.
- Chrome: `HYPERFRAMES_BROWSER_PATH` points at the pre-installed Playwright headless shell; don't run `hyperframes browser ensure`.
- Fonts: use local files with `@font-face` (Inter is installed at `/usr/share/fonts/opentype/inter/`; copy the file into the project).
- Don't commit raw footage or renders of people unless the user explicitly asks.
