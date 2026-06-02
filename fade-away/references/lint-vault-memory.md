# Lint-Vault-Memory Module

Load this only when the user asks to lint, audit, health-check, or inspect the
memory layer, including requests like "哪些适合变成 wiki". This module is read-only by
default. It produces a report first and must not modify files unless the user
explicitly confirms a follow-up fix or promotion.

## Time Zone Rule

Use the configured vault time zone (`GMT+8` / `Asia/Hong_Kong`) for default scan windows, `today`,
`yesterday`, week boundaries, and any journal entries opened after fixes.

## Scope

Inspect these layers when present:

- `<VAULT_ROOT>/00 Tasks/_Index.md`
- `<VAULT_ROOT>/00 Tasks/*.md`
- `<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-MM-DD.md`
  (`<YYYY-MM>` = date's own month)
- `<VAULT_ROOT>/03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-Wnn 周索引.md`
  (`<YYYY-MM>` = Sunday's month)
- `<VAULT_ROOT>/02 Knowledge/**/*.md`

Use a narrow time window unless the user asks for a full audit:

- Default for knowledge-promotion candidates: the latest 7-14 days of daily journals
  plus the latest weekly index.
- Default for structural checks: all `_Index.md` rows and all topic pages.
- For large scans, say what window was used.

## Checks

### Index Integrity

- `_Index.md` rows pointing to missing topic pages.
- Topic pages missing from `_Index.md` while still active.
- Duplicate topic rows.
- Malformed table rows, including unescaped literal `|` in next-step cells.
- Topic statuses that conflict with dashboard visibility.

### Journal-Topic Consistency

- Journal entries with `→ [[00 Tasks/<topic>]]` that are missing from the topic's
  `## 🕐 Sessions`.
- Topic sessions pointing to missing journal files or anchors.
- Explicit `➡️ 下一步` lines in bound journal entries that did not update topic
  `## ➡️ 下一步`.

### Weekly Index Consistency

- Latest weekly index missing existing daily journals in its date range.
- Weekly index mentioning a main thread that has no topic page or knowledge page
  candidate.
- `下周看点` items that contradict topic next-steps or completed status.

### Knowledge Layer Gaps

Identify journal or weekly-index material that should be promoted to `02 Knowledge`
when it meets at least one criterion:

- Reusable method, workflow, checklist, or decision framework.
- Explanation the user is likely to ask again.
- Cross-project concept, architecture, or operating model.
- Repeated pattern appearing in multiple sessions.
- Stable distinction that prevents future confusion.

Do not recommend promotion for one-off status updates, file names alone, transient
implementation details, or narrow "done today" logs unless they reveal a reusable
process.

### Knowledge Page Quality

For existing pages under `02 Knowledge`, check content quality as well as structure.
Do not stop at frontmatter, source presence, or API visibility.

Flag these issues:

- `P1 not knowledge-grade`: the page is mostly a chat recap, task status summary,
  or final-answer summary, and does not preserve reusable judgment.
- `P1 missing rationale`: the page states rules but omits the original problem,
  decision logic, tradeoffs, or why the conclusion matters.
- `P2 weak provenance`: sources point to generic pages, ordinary progress lines,
  or the latest assistant answer rather than the actual journal entry, spec, plan,
  task page, document, or source file that supports the claim.
- `P2 missing boundaries`: the page lacks applicability, non-applicability, or
  anti-patterns, making it hard to reuse safely.
- `P3 readability cleanup`: long lines, duplicate sections, weak headings, or
  formatting that makes the page harder to scan.

For design/product/workflow knowledge, require the page to include the reasoning
chain:

- original problem / design intent
- key tradeoffs
- decision logic
- reusable principles
- applicability boundaries
- anti-patterns
- provenance

If a design knowledge page only records a final UI tweak or final decision, report
it as `P1 not knowledge-grade` even when its frontmatter and links are valid.

## Report Format

Render a concise report:

```markdown
## Memory Lint Report

Scope: <files/date range scanned>

### Index Issues
- [P1/P2/P3] <issue> — <source link>

### Stale Or Conflicting Tasks
- ...

### Journal / Topic Link Gaps
- ...

### Weekly Index Gaps
- ...

### Knowledge Wiki Candidates
| Priority | Candidate | Why it should become wiki | Suggested path | Sources |
|---|---|---|---|---|
| P1 | <title> | <reusable value> | `02 Knowledge/<domain>/<page>.md` | [[...]], [[...]] |

### Knowledge Page Quality Issues
- [P1/P2/P3] <page> — <issue> — <source/evidence>

### Suggested Next Actions
- <action>
```

Priority guidance:

- `P1`: high reuse, repeated topic, or prevents recurring confusion.
- `P2`: useful pattern but not urgent.
- `P3`: optional cleanup or weak candidate.

For existing knowledge pages, use:

- `P1`: not knowledge-grade, missing rationale, or likely to mislead future reuse.
- `P2`: weak provenance or missing applicability boundaries.
- `P3`: readability, formatting, or minor source-anchor cleanup.

If no issues or candidates are found, say that clearly and include the scan scope.

## Follow-Up Rules

- Do not create knowledge pages from the report automatically.
- If the user confirms a candidate, read `references/promote-to-knowledge.md`.
- If the user asks to fix index/topic issues, make the smallest safe edits and read
  back the changed files.
- If changes are made, append one progress line to the current journal entry, or open
  a short journal entry if none is active.
