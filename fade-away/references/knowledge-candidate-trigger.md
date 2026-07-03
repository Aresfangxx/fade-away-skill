# Knowledge-Candidate-Trigger Module

Load this only from `SKILL.md` after a per-turn journal save when the active entry
may contain reusable knowledge. This module proposes candidates; it must not write
`02 Knowledge/` by itself.

## Time Zone Rule

Use the configured vault time zone for any journal source links,
candidate timestamps, and later handoff to `promote-to-knowledge.md`.

## Purpose

Surface reusable knowledge while keeping the hot path quiet. The goal is a
half-active layer: propose good candidates before they disappear into journals,
but require user confirmation before any knowledge page is created or updated.

## Step 1 - Check Candidate Quality

Prompt only when the active entry has at least one strong signal:

- A reusable method, workflow, checklist, or decision framework.
- A stable distinction that prevents recurring confusion.
- A cross-project operating model or architecture pattern.
- An explanation the user is likely to ask for again.
- A pattern repeated across more than one saved progress line, session, or task.
- A design/product/writing decision with enough context to preserve problem,
  tradeoffs, decision logic, reusable principles, and anti-patterns.

Do not prompt for:

- Routine task status or "done today" logs.
- Narrow file-change summaries.
- One-off implementation details with no reusable pattern.
- A final answer summary that lacks source context or rationale.
- Material that should first be handled by `lint-vault-memory.md`.
- Sensitive operational details that should not be promoted broadly.

If quality is unclear, do nothing. Avoid noisy prompts.

## Step 2 - Choose Suggested Destination

Suggest a destination only when it is defensible from the active entry:

List the live top-level folders under `<VAULT_ROOT>/02 Knowledge/` (one
`ls`) and suggest a destination from them. Propose a new folder only when none
fits the candidate.

Use a short Chinese title and a concise kebab-case or readable Chinese filename
that matches existing `02 Knowledge/` style. If the domain is unclear, omit the
path and ask whether to decide the destination during promotion.

## Step 3 - Prompt Once

Output one concise prompt:

```markdown
💡 这段可能适合沉淀成 Knowledge：<candidate-title>。要处理吗？
- **A.** 写入/更新 `<suggested-path>`
- **B.** 只留 journal
```

If no path is defensible, use:

```markdown
💡 这段可能适合沉淀成 Knowledge：<candidate-title>。要处理吗？
- **A.** 进入 Knowledge promotion，先确认合适路径
- **B.** 只留 journal
```

Then set `knowledge_candidate_prompted = True`.

## Step 4 - Handle User Reply

- `A`, `好`, `写`, `沉淀`, `更新 knowledge` -> read
  `references/promote-to-knowledge.md` and follow it. Treat the candidate title,
  suggested path, active journal entry, and current conversation as source hints,
  not as sufficient evidence by themselves.
- `B`, `不用`, `跳过`, `只留 journal` -> set
  `knowledge_candidate_skipped = True`; do not ask again for the active entry.

If the reply is ambiguous, ask one short clarification question. Do not write a
knowledge page until the user clearly chooses promotion.

## Step 5 - Handoff Rules

When handing off to `promote-to-knowledge.md`:

- Read the whole active journal entry, not only the latest progress line.
- Check for related topic pages, weekly indexes, or existing knowledge pages.
- Require the Knowledge-Grade Gate from `promote-to-knowledge.md`.
- If the material cannot meet the gate, explain the gap instead of creating a
  shallow page.
