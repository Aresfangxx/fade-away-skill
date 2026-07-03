# Task Auto-Bind Trigger

Use this module after the per-turn save when an unbound journal entry lacks an
explicit `➡️ 下一步`.

Default to creating or binding a `00 Tasks` topic for task-like sessions. Do not
prompt first. Skip only trivial one-off Q&A, greetings, dashboard/lint-only
reports, pure clarification, or sessions with no task nature.

## Skip

Skip this check when:

- `bound_topic` is set.
- `bind_skipped = True`, `task_auto_bind_checked = True`, or
  `task_auto_bind_skipped = True`.
- The turn is dashboard-only, lint-report-only, weekly-index-only, or pure
  clarification.

Also skip and set `task_auto_bind_skipped = True` when the entry is clearly:

- A casual greeting or social exchange.
- A simple answerable question with no file/action/project continuation.
- A one-off translation, rewrite, calculation, lookup, or explanation that ends
  with the answer.
- A status/dashboard/lint/weekly report where the user did not ask to fix or
  continue work.

## Auto-Bind Signals

Create or bind a topic immediately when any signal is true:

- The user asks to build, fix, debug, implement, refactor, write, revise,
  create, update, install, configure, deploy, test, review, analyze, or maintain
  a named artifact, project, workflow, or document.
- The work creates, edits, configures, or validates a durable artifact: plugin,
  config, script, source file, document, deck, report, exported file, deployed
  service, or verified local runtime behavior.
- The entry has at least 2 saved progress lines and a concrete continuation.
- The entry shows a feedback/debug loop such as `用户反馈` -> `复现` -> `修复` ->
  `验证`.
- The user says a task should already exist or complains that task creation is
  too passive.

## Binding Target

Read `<VAULT_ROOT>/00 Tasks/_Index.md`, including the active table and
the graveyard section.

- If one existing topic clearly matches, bind it.
- If the only clear match is under FADE, ask whether to un-fade it or create a
  derivative new topic; do not bind the FADE path directly.
- Otherwise infer a short kebab-case topic filename from the durable artifact,
  project, or goal. Before creating it, confirm no same-name page exists under
  `<VAULT_ROOT>/00 Tasks/FADE/**/`.
- Ask one short clarification question only when multiple existing topics match
  equally or no defensible topic name can be inferred.

Then read `references/promote-to-wiki.md` and follow the write/index/link rules
with the target treated as already accepted. Start at its write step; do not
show A/B/C choices.

For the topic/index next-step, infer one concrete continuation from the active
entry. If no defensible continuation exists, use:

```markdown
- 下一步待用户确认。
```

Set `bound_topic = <topic>` and `task_auto_bind_checked = True`.
