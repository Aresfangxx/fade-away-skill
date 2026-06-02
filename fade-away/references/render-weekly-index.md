# Render-Weekly-Index Module

Load this only when the user asks for a weekly index, weekly summary, weekly MOC, or
weekly report. This is a cold module; never run it during normal greeting, resume,
per-turn save, or dashboard flows.

## Output Path

Create or update:

```markdown
<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-Wnn 周索引.md
```

`<YYYY-MM>` is the month containing the week's **Sunday** (so `2026-W18 周索引.md`,
whose Sunday is `2026-05-03`, lives under `03 Journal/2026-05/2026-W18/`).

Use ISO week numbering. Weeks run Monday through Sunday. Run `mkdir -p` on the
parent path if the month or week folder does not yet exist.

## Time Zone Rule

Resolve `本周`, `上周`, the most recently completed week, `created:` dates, journal
filenames, and journal save times using the configured vault time zone (`GMT+8` /
`Asia/Hong_Kong`). Do not use the machine local timezone if it differs.

## Step 1 - Resolve Target Week

Infer the target week conservatively:

- If the user gives an ISO week (`2026-W18`) or date range, use that.
- If the user says `本周`, use the current vault-time ISO week, even if incomplete.
- If the user says `上周`, use the previous vault-time ISO week.
- If the user simply asks to generate a weekly index, use the most recently completed
  ISO week. On vault-time Monday, this is the week that ended the previous vault-time day.

If the target cannot be inferred, ask one short clarification question.

## Step 2 - Read Source Journals

Read daily journal files for each date in the target Monday-Sunday range. Each
daily file lives at `<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-MM-DD.md`,
where `<YYYY-MM>` is that date's own month. A week that spans two months therefore
has its dailies split across **two** `<YYYY-MM>/<YYYY-Wnn>/` folders — read both.

- Existing daily files are source material.
- Missing daily files should be represented as empty days in the daily table.
- Do not create missing daily journal files.
- Prefer the `## 🕐 任务时间线` section, but use other sections if they contain useful
  context.

Also read the most recent existing `YYYY-Wnn 周索引.md` before the target week, if
available, and reuse its broad format unless the user requests a different format.

## Step 3 - Synthesize

Create a weekly MOC, not a transcript. Compress daily entries into:

- One short weekly headline paragraph.
- A daily journal table covering all seven days.
- 2-5 main threads, each with concrete deliverables, status, and links back to daily
  journals or project pages.
- Optional side threads for one-off tasks.
- A Mermaid overview when relationships are useful.
- `下周看点` with open questions, follow-ups, or continuation points.

Preserve important caveats marked with `⚠️`, unresolved confirmations, and explicit
next actions. Avoid inventing status not supported by the daily journals.

## Step 4 - Write Safely

If the weekly index file does not exist, create it with this frontmatter. Use the vault-time current date for `created:`:

```markdown
---
created: "YYYY-MM-DD"
type: journal-moc
week: YYYY-Wnn
range: "YYYY-MM-DD ~ YYYY-MM-DD"
tags: [journal, moc, weekly-index]
---
```

Add topic-specific tags only when they are obvious from the week, such as
`api-gateway`, `data-pipeline`, or `research-notes`.

If the weekly index already exists:

- Read it first.
- Preserve useful manual additions when possible.
- Update only stale synthesized sections, unless the user asks for a full rewrite.

Do not delete any daily journals or existing weekly index files.

## Step 5 - Journal The Action

If a weekly index was created or materially updated, append one progress line to the
current journal entry if one is open. If no entry is open, open a short entry in
the current vault-time daily journal:

```markdown
### HH:MM ▶️ <YYYY-Wnn> 周索引生成
(HH:MM) 读取 <range> 的日记并生成/更新 `YYYY-Wnn 周索引.md`。
```

Do not update `00 Tasks/_Index.md` unless the assistant's visible response includes
an explicit `➡️ 下一步` and the normal promotion rules apply.
