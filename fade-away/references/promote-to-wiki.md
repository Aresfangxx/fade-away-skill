# Promote-to-Wiki Module

Load this only when either:

- The current session produced an explicit `➡️ 下一步` and `bound_topic` is `None`.
- The Task Auto-Bind Trigger selected a target topic.

## Time Zone Rule

Use the configured vault time zone for all dates, `HH:MM` values,
frontmatter `updated:` timestamps, session links, and `_Index.md` rows. All
placeholders in this module are vault-time-derived values. Prefer `TZ=<IANA_TIME_ZONE> date`
when checking the current timestamp.

## Step 1 - Select Binding Target

Read `<VAULT_ROOT>/00 Tasks/_Index.md`, including both the active table
and the graveyard section. Before creating a new page, confirm no same-name page
already exists under `<VAULT_ROOT>/00 Tasks/FADE/**/`.

Skip this step when `task-candidate-trigger.md` selected an existing or inferred
topic. In that case, use that topic directly and continue with Step 3.

For an unbound explicit `➡️ 下一步` with no selected topic, bind directly whenever
the target is defensible: use a clear active topic match if one exists. If the
only match is under FADE, ask whether to un-fade it or create a derivative new
topic; do not bind the FADE path directly. Otherwise create an inferred
kebab-case topic from the durable artifact, project, or goal. Ask one short
clarification question only when multiple topics match equally or no defensible
topic name can be inferred.

When clarification is genuinely required, output exactly this shape:

```markdown
📌 这个 session 看起来是 **<short inferred topic>**。绑到哪？
- **A.** 现有 [[<existing-topic-filename>]]
- **B.** 新建 `<suggested-kebab-name>.md`
- **C.** 不绑（这个任务不进 wiki）
```

If the index has no body rows, omit option A.

## Step 2 - Handle Clarification Reply

Run this step only when Step 1 asked the user to choose a binding target. For
task auto-bind or a defensible explicit next-step target, skip directly to Step
3.

Interpret replies:

- `A`, `嗯`, `好`, `用现有的` -> use option A, only if option A was shown.
- `B`, `新建`, `新的` -> create the suggested file, unless the user supplies another
  valid filename.
- `C`, `不用`, `跳过` -> set `bind_skipped = True`; do not ask again for this entry.

If the reply is ambiguous, ask one clarification question. Do not write
topic/index files before the user chooses A or B.

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

For Task Auto-Bind binding without an explicit `➡️ 下一步`, infer one concrete
continuation from the active entry. If no defensible continuation exists, use:

```markdown
- 下一步待用户确认。
```

## Step 4 - Update Index

Read `<VAULT_ROOT>/00 Tasks/_Index.md` immediately before editing. Follow
the `_Index.md` concurrent-write rules in `journal-write-protocol.md`. Remove any
existing active-table row for this topic, then insert the fresh row immediately
after the table separator row (`|---|` alignment row; dash count may vary).

Before writing the row, sanitize next-step text:

1. Collapse all CR/LF whitespace to one space.
2. Trim leading/trailing whitespace.
3. Escape literal pipe characters as `\|`.
4. Compress the index next-step cell to one next-action sentence, <= ~120
   characters. When the topic page lists multiple items, write only the
   top-priority action plus `（余 N 项见 topic 页）`.

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

Set `bound_topic = <topic>` and `bind_skipped = False`.
Future explicit `➡️ 下一步` updates go through the main SKILL.md bound-topic flow.
