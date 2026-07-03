#!/usr/bin/env bash
set -euo pipefail

AGENTS_DIR="${FADE_AWAY_AGENTS_SKILL_DIR:-$HOME/.agents/skills/fade-away}"
CLAUDE_DIR="${FADE_AWAY_CLAUDE_SKILL_DIR:-$HOME/.claude/skills/fade-away}"

diff -r "$AGENTS_DIR" "$CLAUDE_DIR"
