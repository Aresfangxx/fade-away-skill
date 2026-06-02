# Task Candidate Trigger

Use this module after the per-turn save when an unbound journal entry appears
resumable but the visible output does not contain an explicit `➡️ 下一步`.

Do not create or update any topic automatically.

## Skip

Skip this check when:

- `bound_topic` is set.
- `bind_skipped = True`, `task_candidate_prompted = True`, or
  `task_candidate_skipped = True`.
- The turn is dashboard-only, lint-report-only, weekly-index-only, or pure
  clarification.

## Prompt Signals

Prompt once when the active entry satisfies at least two signals:

- The active entry has at least 3 saved progress lines.
- The same vault-time day contains another entry with the same project keyword, such
  as `ERP`, `MRP`, `CRM`, `MobileApp`, `DataPipeline`, `Codex`, or another obvious
  project name.
- The work produced a concrete deliverable: `PDF`, `HTML`, `DOCX`, `PPTX`,
  script, test pass, QA screenshot, report, exported file, or deployed/running
  UI.
- The entry shows iterative continuation language: `继续`, `重导`, `QA`,
  `用户反馈`, `修正`, `复查`, `口径`, `待确认`, or equivalent.
- The entry or current work clearly matches a topic keyword in `_Index.md`.
- There is a concrete continuation implied by the work, but no formal
  `➡️ 下一步` marker was emitted.

## Prompt

Output exactly one concise prompt:

```markdown
📌 这个 entry 看起来已经是可续接任务。要绑到 `00 Tasks` 吗？
- **A.** 现有 [[<matched-topic>]]
- **B.** 新建 `<suggested-topic>.md`
- **C.** 只留 journal
```

Omit option A if there is no clear existing topic match. Then set
`task_candidate_prompted = True`.

## User Reply

- `A`, `嗯`, `好`, `用现有的` -> bind to option A, only if option A was shown.
- `B`, `新建`, `新的` -> create the suggested topic, unless the user supplies
  another valid kebab-case filename.
- `C`, `不用`, `跳过`, `只留 journal` -> set `task_candidate_skipped = True`;
  do not ask again for the active entry.

For A/B, read `references/promote-to-wiki.md` and follow its write/index/link
rules with the candidate prompt treated as already accepted. If no explicit next
action exists, set the topic/index next-step to a one-line concrete continuation
inferred from the active entry; if none is defensible, use
`下一步待用户确认。`.
