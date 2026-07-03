# Journal Write Protocol

Use this module when creating a daily journal, appending progress, handling vault-time
date ambiguity, recording pitfall lines, or rebasing around concurrent writes.

## vault-time Boundary

All journal paths and `HH:MM` lines use the configured vault time zone.
Harness/system date hints may reflect the local machine timezone and can lag
vault-time near midnight. If there is any conflict, run:

```bash
TZ=<IANA_TIME_ZONE> date
```

Then derive the journal filename, ISO week, weekly index path, and progress-line
time from that vault-time result.

When the week is unknown, derive ISO week with:

```bash
TZ=<IANA_TIME_ZONE> date -j -f "%Y-%m-%d" "<YYYY-MM-DD>" "+%G-W%V"
```

## Journal Directory Layout

Daily journals and weekly indices live in nested month/week folders under
`03 Journal/`. The two layers are computed independently:

- Daily file: place under the date's own month folder:
  `03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-MM-DD.md`.
- Weekly index: place under the month containing the week's Sunday:
  `03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-Wnn 周索引.md`.
- A week spanning two months may therefore have a `<YYYY-Wnn>/` folder in both
  month folders. The weekly index lives only with the Sunday side.

Examples:

- `2026-04-15` -> `03 Journal/2026-04/2026-W16/2026-04-15.md`
- `2026-04-29` -> `03 Journal/2026-04/2026-W18/2026-04-29.md`
- `2026-05-02` -> `03 Journal/2026-05/2026-W18/2026-05-02.md`
- `2026-W18 周索引` -> `03 Journal/2026-05/2026-W18/2026-W18 周索引.md`
  because Sunday `2026-05-03` falls in May.

## Journal Template

Create missing daily journals with:

```markdown
---
created: "YYYY-MM-DD"
type: journal
---

# YYYY-MM-DD 星期X

## 🕐 任务时间线
```

**Four template sources must stay in sync**:

1. Claude side: `~/.claude/skills/fade-away/references/journal-write-protocol.md`.
2. Codex side: `~/.agents/skills/fade-away/references/journal-write-protocol.md`.
3. Obsidian Daily Notes template: `<VAULT_ROOT>/04 Templates/Daily Note.md`.
4. Bootstrap script template: `scripts/bootstrap_vault.py`.

When you change the template body, update all four. Sync mechanics and
verification live in `references/context-check.md`.

## Append Placement

Progress lines default to:

```markdown
(HH:MM) <一句话进展>
```

Append the line at the end of the active entry body, immediately before the next
`### ` timeline header. Locate the active entry by matching the complete stored
header line: `### HH:MM ▶️ <current_entry_title>` plus the topic suffix when
present. Time alone is not a safe anchor. Do not insert repeatedly right under
the header. Do not rewrite earlier progress lines.

Fall back to end-of-file only after confirming the active entry is the final
`### ` block in the file. After the edit, verify the new line sits between the
target header and its next `### ` sibling; if another header intervenes, re-read
and rebase. If the stored header is unavailable, run State Recovery in
`SKILL.md`; never blindly anchor to the last `### ` block, which may belong to a
parallel session.

## Concurrent Writes

The user may run multiple sessions that append to the same daily journal. Avoid
clobbering other sessions:

1. Re-read the journal tail immediately before each edit, usually the last
   ~50 lines.
2. Use the literal last progress line you observed, plus enough surrounding
   context to be unique, as the edit anchor.
3. If the edit reports that the file changed since read, re-read and rebase.
   Another session may have appended under your entry or opened a new sibling
   `### ` entry below it.
4. Recompute the insertion point under your own active entry. Your line belongs
   under your entry, not under a newer sibling header.
5. Bash append is the last-resort fallback. Use it only after confirming your
   active entry is the final `### ` block in the file. If a newer entry sits
   below yours, shell append misattributes the line.
6. Parallel subagents must not append to the journal themselves and must not
   open sibling entries. The main thread owns journal writes and records on
   their behalf.

### `_Index.md`

`_Index.md` updates are also concurrent writes. Before editing, re-read
`<VAULT_ROOT>/00 Tasks/_Index.md` immediately. Only perform line-level
edits anchored by a unique complete old row or by the unique table separator
row; never rewrite the whole table from a stale copy.

If an edit conflicts, re-read the latest table and replay only this topic's
single-row upsert. After writing, verify these invariants:

- Every other topic row that existed immediately before the write still exists.
- No other topic row moved backward in timestamp or content.
- Row count did not decrease unless this is an explicitly confirmed fade-out
  move.

Concurrent new rows from other sessions are legal. A fade-out move is a separate
lint/dashboard-confirmed operation and is exempt from the non-decrease invariant.

## Pitfall Lines

Most progress lines describe forward motion. When a turn discovers a dead end,
prefix the line with `❌`:

```markdown
(HH:MM) ❌ <死路> — <根因或观察>
```

Pitfall lines follow the normal append rules. Topic Auto-Refresh aggregates them
into the bound topic's `## 🪤 踩过的坑` section through
`topic-update-protocol.md`.
