#!/usr/bin/env python3
"""Bootstrap a minimal fade-away Obsidian vault.

Creates only missing files. Existing files are never overwritten.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


TASK_INDEX = """---
type: task-index
updated: {timestamp}
---

# 任务索引

> fade-away 自动维护。手动改动可能在后续 save 时被覆盖。

| 任务 | 最近 | ➡️ 下一步 |
| --- | --- | --- |
"""


DAILY_TEMPLATE = """---
created: "{{date}}"
type: journal
---

# {{date}} {{weekday}}

## 🕐 任务时间线
"""


AGENTS_TEMPLATE = """# Project Vault

This vault is configured for the `fade-away` session tracker.

## fade-away

- Vault root: `{vault_root}`
- Time zone: `{timezone}`
- On conversation start, read `00 Tasks/_Index.md` before deciding whether to
  resume a topic, show a dashboard, or start new work.
- When substantive work starts, create or append to the current daily journal
  under `03 Journal/`.
- After each substantive assistant turn, append one short progress line to the
  active journal entry.
- Update task/topic/index state only through the `fade-away` workflow.

## Vault Structure

```text
00 Tasks/       task index and topic pages
02 Knowledge/   durable knowledge pages
03 Journal/     daily journals and weekly indices
04 Templates/   Obsidian templates
```

Do not delete, move, rename, or overwrite existing vault files unless the user
explicitly asks for that specific action.
"""


CLAUDE_TEMPLATE = """# Project Vault

Use `fade-away` as the session tracker for this vault.

- Vault root: `{vault_root}`
- Time zone: `{timezone}`
- Read `00 Tasks/_Index.md` at conversation start.
- Write substantive progress to `03 Journal/`.
- Keep `AGENTS.md` and `CLAUDE.md` behaviorally aligned when updating
  instruction surfaces.

Do not delete, move, rename, or overwrite existing vault files unless the user
explicitly asks for that specific action.
"""


def write_if_missing(path: Path, content: str, dry_run: bool) -> str:
    if path.exists():
        return f"skip existing file: {path}"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return f"create file: {path}"


def mkdir(path: Path, dry_run: bool) -> str:
    if path.exists():
        return f"skip existing dir: {path}"
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)
    return f"create dir: {path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a fade-away vault")
    parser.add_argument("--vault-root", required=True, help="Absolute vault root path")
    parser.add_argument(
        "--agent-surface",
        choices=["agents", "claude", "both", "none"],
        default="both",
        help="Instruction files to create",
    )
    parser.add_argument("--timezone", default="Asia/Hong_Kong")
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault_root).expanduser()
    if args.timestamp:
        timestamp = args.timestamp
    else:
        try:
            timestamp = datetime.now(ZoneInfo(args.timezone)).isoformat(timespec="seconds")
        except ZoneInfoNotFoundError:
            timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    actions: list[str] = []

    for rel in ["00 Tasks", "02 Knowledge", "03 Journal", "04 Templates"]:
        actions.append(mkdir(vault / rel, args.dry_run))

    actions.append(
        write_if_missing(
            vault / "00 Tasks" / "_Index.md",
            TASK_INDEX.format(timestamp=timestamp),
            args.dry_run,
        )
    )
    actions.append(write_if_missing(vault / "04 Templates" / "Daily Note.md", DAILY_TEMPLATE, args.dry_run))

    if args.agent_surface in {"agents", "both"}:
        actions.append(
            write_if_missing(
                vault / "AGENTS.md",
                AGENTS_TEMPLATE.format(vault_root=str(vault), timezone=args.timezone),
                args.dry_run,
            )
        )
    if args.agent_surface in {"claude", "both"}:
        actions.append(
            write_if_missing(
                vault / "CLAUDE.md",
                CLAUDE_TEMPLATE.format(vault_root=str(vault), timezone=args.timezone),
                args.dry_run,
            )
        )

    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
