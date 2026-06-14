---
name: fade-away
description: >
  Active session tracker for the user's Obsidian vault. Invoke at conversation
  start and any time the user resumes, switches, records, audits, summarizes, or
  promotes project work; keep it loaded across the full session. Triggers include
  greetings, named personal projects, record/log phrases, topic switches, task
  dashboards, weekly summaries, knowledge promotion, and vault health checks.
  Every substantive assistant turn appends one vault-time progress line to the daily
  journal. Maintains `03 Journal/`, `00 Tasks/_Index.md`, topic pages, weekly
  MOCs, and `02 Knowledge/`. Skip only atomic project-less utility queries.
  Replaces legacy `task-tracker`; do not reference the old name.
---

# fade-away

Maintain a lightweight log -> topic wiki -> index -> weekly MOC -> knowledge
wiki memory layer so the user can switch tasks and build a personal LLM
knowledge base without re-explaining context.

## Operating Contract

This skill runs across the entire conversation, not only the first turn. Before
each assistant response, check whether the turn triggers session start, per-turn
save, topic switch, manual record, topic promotion, weekly/dashboard/lint, or
knowledge promotion. The most commonly missed rule is the per-turn save: every
substantive assistant turn appends one `(HH:MM) <进展>` line to the active journal
entry.

Keep the hot path small. Put low-frequency mechanics in `references/` and load
them only when their trigger fires.

## Paths

`<VAULT_ROOT>` is the Obsidian vault that fade-away maintains. Resolve it once
per session, in this order:

1. The `Vault root` field declared in the project's `AGENTS.md` / `CLAUDE.md`
   (written by the bootstrap installer, `scripts/bootstrap_vault.py`).
2. If no such field exists, treat the current project / working directory as the
   vault root.

Always expand `<VAULT_ROOT>` to that absolute path before reading or writing:

- Journal: `<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-MM-DD.md`
  where `<YYYY-MM>` is the date's own month and `<YYYY-Wnn>` is that date's ISO
  week.
- Weekly index:
  `<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-Wnn 周索引.md`
  where `<YYYY-MM>` is the month containing the week's Sunday.
- Task index: `<VAULT_ROOT>/00 Tasks/_Index.md`
- Topic pages: `<VAULT_ROOT>/00 Tasks/<topic-filename>.md`
- Knowledge pages: `<VAULT_ROOT>/02 Knowledge/<domain>/<page>.md`
- References: this skill's `references/` directory

If `00 Tasks/` or `_Index.md` is missing, skip task index and topic logic for the
session. Do not auto-create `00 Tasks/` mid-session. Journal logging still runs.

Top-level files such as `备忘.md` may live directly under `03 Journal/`; do not
move them.

## Time Zone Rule

All dates and times recorded by this skill MUST use one consistent zone, called
**vault-time**. Resolve vault-time from the `Time zone` field in the project's
`AGENTS.md` / `CLAUDE.md`; if none is set, fall back to the machine's local zone.
The bootstrap installer defaults this to `Asia/Hong_Kong`, so unconfigured vaults
behave as `Asia/Hong_Kong` / `GMT+8` / `UTC+8`.

Use vault-time for journal filenames, parent paths, headings, progress lines,
topic frontmatter, `_Index.md` timestamps, and weekly index inference.

Preferred shell check (substitute your configured zone):

```bash
TZ=Asia/Hong_Kong date
```

Trust vault-time over harness date hints. If the harness date conflicts with
vault-time, derive the journal filename, ISO week, and `HH:MM` from a fresh
vault-time reading. For append/concurrency details, read
`references/journal-write-protocol.md`.

## Session State

Track internally:

- `current_entry_start`: active journal entry `HH:MM`.
- `current_entry_date`: active journal entry `YYYY-MM-DD`.
- `current_entry_title`: current short Chinese task title.
- `bound_topic`: topic filename without `.md`, or `None`.
- `bind_skipped`: `True` only after the user picks not to bind.
- `task_auto_bind_checked` / `task_auto_bind_skipped`: reset for each new
  journal entry.
- `knowledge_candidate_prompted` / `knowledge_candidate_skipped`: reset for
  each new journal entry.
- `tracking_disabled`: `True` only if the user opts out for this session.

## Start Of Conversation

1. Read `<VAULT_ROOT>/00 Tasks/_Index.md` if present. Parse table body
   rows as `[[topic]] | timestamp | next-step`; treat missing files as an empty
   index.
2. Check cheaply for a concurrent same-topic session. Read the tail of today's
   vault-time journal if it exists. If the last progress line is within 15 vault-time minutes
   and its entry plausibly overlaps the user's first message, surface:

   ```markdown
   ⚠️ 另一会话 <HH:MM> 刚写过 [[<topic>]]，可能在并行做同一件事。我先扫一眼最新进展再回。
   ```

   Then read the recent entry so this response does not contradict parallel
   work. If no recent overlapping entry exists, skip silently.
3. Dispatch on the user's first message, in order:
   - Bootstrap/setup intent (`install fade-away`, `setup`, `bootstrap`,
     `初始化`, `第一次使用`, `开源部署`, or a missing `_Index.md` plus a user
     request to initialize): read `references/bootstrap-vault.md`. Bootstrap is
     a one-time setup path; ask for the vault root if it is unclear and never
     create files unless the user confirms.
   - Context/instruction check intent (`AGENTS`, `CLAUDE`, `上下文`, `context`,
     `经验继承`, `规则漂移`, project structure, skill/vault/workflow maintenance,
     or a fresh cwd/project boundary): read `references/context-check.md`.
     Report only when drift is found or the user explicitly asks; do not write
     instruction files unless the user confirms the specific patch.
   - Memory lint intent (`lint`, `体检`, `health check`, `检查知识库`, `检查任务索引`,
     `看看哪些适合变成 wiki`, or similar): read
     `references/lint-vault-memory.md`; render a report first and do not write
     fixes or knowledge pages unless the user confirms.
   - Knowledge promotion intent (`沉淀成知识`, `写进 knowledge`, `变成 wiki`,
     `归档成知识页`, or similar): read `references/promote-to-knowledge.md`.
   - Weekly index intent (`周索引`, `周报`, `weekly index`, `weekly summary`,
     `本周总结`, or similar): read `references/render-weekly-index.md`. Open a
     journal entry only if the module writes or updates a weekly index.
   - Dashboard intent (`看下任务`, `看板`, `dashboard`, `总览`, or similar): read
     `references/render-dashboard.md`, render only, and do not open a journal
     entry yet.
   - Clear existing topic match: read that topic page silently, set
     `bound_topic`, then open a journal entry.
   - Vague greeting (`hi`, `你好`, `在吗`, `开始干活了`, etc.): if `_Index.md` has
     rows, emit `⏮️ 上次：<task>，下一步是 <next-step>。继续这个还是新任务？` and wait
     for the reply. Bind to the top row only if the user confirms.
   - New substantive task: do not mention old tasks; leave `bound_topic = None`.

## Open Journal Entry

Open a journal entry only when work actually starts. Compute the vault-time daily path
as `03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-MM-DD.md`, where `<YYYY-MM>` is the
date's own month and `<YYYY-Wnn>` is the ISO week. Create missing month/week
folders with `mkdir -p`.

If the daily file is missing, create it from the template in
`references/journal-write-protocol.md`. Ensure `## 🕐 任务时间线`, then append one
header at the bottom of that section:

- Unbound: `### HH:MM ▶️ <短中文标题>`
- Bound: `### HH:MM ▶️ <短中文标题> → [[00 Tasks/<bound_topic>]]`

Store `current_entry_start`, `current_entry_date`, and `current_entry_title`.
Reset task and knowledge candidate flags for the new entry.

## Per-Turn Save

After every assistant turn with substantive output, append exactly one progress
line inside the current journal entry:

```markdown
(HH:MM) <一句话进展>
```

Append at the end of the active entry body, immediately before the next `### `
timeline header or EOF. Do not rewrite earlier progress lines. Skip the save if
the turn is only a clarification question or `tracking_disabled = True`.

Before writing, read `references/journal-write-protocol.md` when you need exact
append placement, concurrent-write rebasing, vault-time boundary handling, pitfall line
syntax, or the journal template.

## Post-Save Checks

Run these checks after the per-turn save:

1. **Explicit promotion**: if the visible output contains an explicit
   `➡️ 下一步` marker or `## ➡️ 下一步` section, update the topic/index layer. If
   `bound_topic` is set, read `references/topic-update-protocol.md`; otherwise,
   if `bind_skipped = False`, read `references/promote-to-wiki.md`.
2. **Topic auto-refresh**: when `bound_topic` is set and no explicit next-step
   appeared, read `references/topic-update-protocol.md` if the active entry may
   meet the existing staleness thresholds. Keep the current automatic refresh
   behavior; do not convert it to a confirmation prompt unless the user asks.
3. **Task auto-bind**: when the active entry is unbound and lacks an explicit
   `➡️ 下一步`, read `references/task-candidate-trigger.md`. Create/bind a topic
   automatically for task-like sessions; skip only trivial Q&A, greetings,
   dashboard/lint-only reports, pure clarification, or sessions with no task
   nature.
4. **Knowledge candidate**: when reusable knowledge may have emerged and the
   user did not already ask for promotion, read
   `references/knowledge-candidate-trigger.md`. Do not create or update
   `02 Knowledge/` automatically.

## Mid-Session Topic Switch

If the user says `继续做 X`, `回到 X`, or otherwise asks to switch while an entry is
already open:

1. Match `X` against `_Index.md` conservatively.
2. If no clear match exists, ask one short clarification question.
3. If the match is clear and differs from `bound_topic`, ask:
   `切到 [[X]]？我会给当前 entry 追加一行切换记录，然后打开新的 X entry。`
4. On confirmation, append `(HH:MM) 切出当前任务，转到 [[00 Tasks/X]]。`, read the
   topic page, set `bound_topic = X`, and open a new bound journal entry.
5. If the user declines, keep the existing binding.

Do not silently switch topics mid-session.

## Manual Record Request

If the user says `记录一下`, `记一下刚才的进展`, or similar, add one extra progress
line to the current entry summarizing progress since the previous save. Do not
open a new entry or close the current entry unless the user explicitly asks to
switch tasks.

## Modules

Load low-frequency workflows only on demand:

- `references/journal-write-protocol.md`: journal creation, append placement,
  vault-time boundary handling, concurrent-write rebasing, pitfall line syntax, and
  journal template.
- `references/bootstrap-vault.md`: one-time setup workflow for a new user's
  Obsidian vault; creates the minimal fade-away directory/template/index and
  instruction entrypoints only after confirmation.
- `references/context-check.md`: cold-start or boundary-change check for stale
  instruction/context surfaces such as `AGENTS.md`, `CLAUDE.md`, project
  structure notes, and Knowledge inheritance; report drift without writing
  until confirmed.
- `references/task-candidate-trigger.md`: auto-bind substantial unbound task
  entries to `00 Tasks`; skip trivial or non-task sessions.
- `references/topic-update-protocol.md`: update bound topic pages, refresh
  `_Index.md`, and run the current Topic Auto-Refresh behavior.
- `references/promote-to-wiki.md`: bind an unbound journal entry to a topic page
  and update `_Index.md` after an explicit `➡️ 下一步` or task auto-bind trigger.
- `references/render-dashboard.md`: render a read-only task dashboard from
  `_Index.md`.
- `references/render-weekly-index.md`: generate or update an on-demand weekly
  MOC in `03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-Wnn 周索引.md`.
- `references/lint-vault-memory.md`: render a read-only health report for task,
  journal, weekly index, and knowledge layers.
- `references/knowledge-candidate-trigger.md`: propose reusable journal material
  for `02 Knowledge/` without writing until confirmed.
- `references/promote-to-knowledge.md`: create or update curated pages under
  `02 Knowledge/` after confirmation.

## Format Rules

- Time format: 24-hour `HH:MM` using the configured vault time zone.
- Journal title: short, descriptive Chinese; avoid generic titles like `任务1`.
- Topic filename: kebab-case, no spaces, `.md` extension on disk only.
- Topic wikilink in journal: `[[00 Tasks/<topic>]]`.
- Index row format:
  `| [[<topic>]] | YYYY-MM-DD HH:MM | <escaped next-step> |`.
- Legacy `task-tracker` directories have been removed; if the user asks for the
  old tracker, explain that `fade-away` replaced it.

## Edge Cases

- User opts out (`这次不用记录`): set `tracking_disabled = True`; skip all writes
  for the session, but reading `_Index.md` for context is allowed.
- Midnight crossing: use vault-time midnight. After vault-time midnight, open a continuation
  entry in the new vault-time day's journal and continue per-turn saves there.
- Dashboard-only turn: render the dashboard and wait; do not open a journal
  entry until the user starts real work.
- Missing topic page for an index match: say the topic row exists but the page
  is missing, then ask whether to recreate it or continue unbound.
