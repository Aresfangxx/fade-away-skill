#!/bin/sh
# Fade-away skill installer.
# Downloads the `fade-away/` skill folder into your agent's skills directory.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Aresfangxx/Fade-away/main/install.sh | sh
#
# Override the install location with FADE_AWAY_SKILL_DIR, e.g. for Codex:
#   curl -fsSL .../install.sh | FADE_AWAY_SKILL_DIR="$HOME/.agents/skills/fade-away" sh
#
# After installing, open your agent and say "setup fade-away" (or "初始化")
# to initialize your vault — no manual script run needed.

set -e

REPO_URL="https://github.com/Aresfangxx/Fade-away"
TARBALL_URL="$REPO_URL/archive/refs/heads/main.tar.gz"
DEST="${FADE_AWAY_SKILL_DIR:-$HOME/.claude/skills/fade-away}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Fade-away → installing skill to: $DEST"

if command -v git >/dev/null 2>&1; then
  git clone --depth 1 "$REPO_URL" "$TMP/repo" >/dev/null 2>&1
  SRC="$TMP/repo/fade-away"
elif command -v curl >/dev/null 2>&1; then
  curl -fsSL "$TARBALL_URL" | tar -xz -C "$TMP"
  SRC="$TMP/Fade-away-main/fade-away"
else
  echo "Error: need either git or curl installed." >&2
  exit 1
fi

if [ ! -d "$SRC" ]; then
  echo "Error: could not locate the skill folder after download." >&2
  exit 1
fi

mkdir -p "$DEST"
cp -R "$SRC/." "$DEST/"

echo "✓ Installed."
echo ""
echo "Next step — open Claude Code or Codex and say:"
echo "    setup fade-away"
echo "The skill will ask for your vault location and initialize it for you."
