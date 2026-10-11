#!/bin/bash
# Prepare a Claude Code cloud session for HyperFrames video editing.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# HyperFrames CLI + GSAP (local copies; the jsdelivr CDN is blocked here)
npm install --no-audit --no-fund

# Use the pre-installed Chromium instead of downloading Chrome
BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
if [ ! -x "$BROWSER" ]; then
  BROWSER="$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1 || true)"
fi
if [ -n "${BROWSER:-}" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export HYPERFRAMES_BROWSER_PATH=\"$BROWSER\"" >> "$CLAUDE_ENV_FILE"
fi

# Agent skills (~/.claude/skills): core set + the talking-head workflows.
# Non-fatal so a GitHub hiccup never blocks the session.
npx hyperframes skills update talking-head-recut embedded-captions >/dev/null 2>&1 ||
  echo "warning: hyperframes skills update failed; run it manually" >&2

# Re-vendor GSAP into any existing projects (vendor/ is gitignored)
for d in videos/*/; do
  [ -f "$d/index.html" ] && scripts/vendor-gsap.sh "$d"
done
exit 0
