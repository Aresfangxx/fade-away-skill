# Promote-to-Wiki Module

Load this only when either:

- The current session produced an explicit `➡️ 下一步` and `bound_topic` is `None`.
- The user accepted a Task Candidate Trigger prompt from `SKILL.md`.

## Time Zone Rule

Use the configured vault time zone (`GMT+8` / `Asia/Hong_Kong`) for all dates, `HH:MM` values,
frontmatter `updated:` timestamps, session links, and `_Index.md` rows. All
placeholders in this module are vault-time-derived values. Prefer `TZ=Asia/Hong_Kong date`
when checking the current timestamp.

## Step 1 - Propose Binding

Read `<VAULT_ROOT>/00 Tasks/_Index.md`. Suggest binding to an existing topic
only when the match is clear. Otherwise default to a new kebab-case filename.

Skip this step when `SKILL.md` already showed a Task Candidate prompt and the user
accepted A or B. In that case, use the accepted topic choice directly.

Output exactly this shape:

```markdown
📌 这个 session 看起来是 **<short inferred topic>**。绑到哪？
- **A.** 现有 [[<existing-topic-filename>]]
- **B.** 新建 `<suggested-kebab-name>.md`
- **C.** 不绑（这个 session 不进 wiki）
```

If the index has no body rows, omit option A.

## Step 2 - Wait For User

Interpret replies:

- `A`, `嗯`, `好`, `用现有的` -> use option A, only if option A was shown.
- `B`, `新建`, `新的` -> create the suggested file, unless the user supplies another
  valid filename.
- `C`, `不用`, `跳过` -> set `bind_skipped = True`; do not ask again this session.

If the reply is ambiguous, ask one clarification question. Do not write topic/index
files before the user chooses A or B.

## Step 3 - Write Topic Page

For a new page, write `<VAULT_ROOT>/00 Tasks/<topic>.md`:

```markdown
---
updated: <vault-time ISO 8601 timestamp, preferably with +08:00>
status: in-progress
---

# <Chinese title>

## 📍 现状
<one concise paragraph synthesizing the session so far; include ⚠️ inline if needed.>

## ➡️ 下一步
- <latest explicit next action, or candidate continuation>

## 🕐 Sessions
- <YYYY-MM-DD> <HH:MM> → [[<YYYY-MM-DD>#HH:MM]]
```

For an existing page, modify only:

1. Frontmatter `updated:`.
2. `## 📍 现状` body.
3. `## ➡️ 下一步` body.
4. `## 🕐 Sessions`, appending the vault-time-date session line only if that vault-time date is absent.

Do not touch other sections.

For Task Candidate binding without an explicit `➡️ 下一步`, infer one concrete
continuation from the active entry. If no defensible continuation exists, use:

```markdown
- 下一步待用户确认。
```

## Step 4 - Update Index

Read `<VAULT_ROOT>/00 Tasks/_Index.md`. Remove any existing row for this
topic, then insert the fresh row immediately after the `|---|---|---|` separator.

Before writing the row, sanitize next-step text:

1. Collapse all CR/LF whitespace to one space.
2. Trim leading/trailing whitespace.
3. Escape literal pipe characters as `\|`.

Row format:

```markdown
| [[<topic>]] | YYYY-MM-DD HH:MM | <escaped one-line next-step> |
```

Update frontmatter `updated:` to the same vault-time ISO timestamp used by the topic page.
Read the index back after writing and verify this topic appears exactly once and each
body row has three table cells.

## Step 5 - Link Journal Entry

In the daily journal at
`<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/<YYYY-MM-DD>.md`
(date's own month + its ISO week), locate the current session header by
`current_entry_start` and `current_entry_title`. Append the topic link:

```markdown
### HH:MM ▶️ <task-title> → [[00 Tasks/<topic>]]
```

Do not choose the most recent `###` blindly if the session has switched topics.
Refine the title only if the current context makes a clearly better short Chinese
title obvious.

## Step 6 - Set State

Set `bound_topic = <topic>` and `bind_skipped = False` for the rest of the session.
Future explicit `➡️ 下一步` updates go through the main SKILL.md bound-topic flow.
