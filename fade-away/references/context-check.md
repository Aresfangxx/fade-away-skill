# Context Check

Use this module for cold-start, cwd/project-boundary, and instruction-surface
maintenance checks. It keeps agent-facing context files aligned without adding
work to the per-turn hot path.

## Trigger

Read this module only when one of these is true:

- The session is starting in a project whose instruction surfaces may matter.
- The user switches cwd, resumes a different project, or asks to inspect project
  structure.
- The user mentions `AGENTS.md`, `CLAUDE.md`, context, inheritance, rules,
  drift, skill maintenance, vault maintenance, or workflow maintenance.
- A turn changed `fade-away`, a relevant `02 Knowledge` page, project structure,
  or durable project conventions.

Do not run this check after every progress save, ordinary code edit, simple
question, or continuous work inside an already-bound topic.

## Instruction Surfaces

Check only surfaces that plausibly affect the current workspace:

- Current project root: `AGENTS.md`, `CLAUDE.md`, `README.md`, `HANDOFF.md`, or
  equivalent local instruction files.
- Vault root when cwd is under `<VAULT_ROOT>`: `<VAULT_ROOT>/AGENTS.md`.
- Active topic page and `<VAULT_ROOT>/00 Tasks/_Index.md` when a topic
  is bound.
- Matching `02 Knowledge` pages when the current task already depends on them.
- `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` fade-away / Task Tracker
  designation sections when maintaining this workflow.
- Canonical Knowledge pages describing the workflow, especially
  `<VAULT_ROOT>/02 Knowledge/AI 工作流/fade-away-记忆架构.md`, when a turn
  changes `fade-away` behavior.
- `<VAULT_ROOT>/04 Templates/Daily Note.md` because Obsidian's Daily
  Notes core plugin reads it via `.obsidian/daily-notes.json`.
- Skill mirrors when maintaining a skill, especially `.agents` and `.claude`
  copies that should stay behaviorally aligned. Run `scripts/sync_check.sh`
  from the skill directory when present.

Prefer exact files near the current cwd over broad vault scans.

## Drift Signals

Report a drift candidate when you find concrete evidence such as:

- A root instruction file references missing, renamed, or deprecated paths.
- A project convention changed but the local `AGENTS.md` / `CLAUDE.md` still
  describes the old structure.
- A Knowledge page or task topic now contains a durable workflow rule that the
  instruction surface still omits.
- `.agents` and `.claude` skill mirrors differ in behavior, not just in
  mirror-specific self-description.
- A skill or workflow's behavior has changed, but the canonical Knowledge page
  describing it still documents the old behavior.
- Live skill has behavior-level changes not yet ported to the public repo
  checkout, which is a semantic port: local time-zone wording -> vault-time and
  absolute paths -> `<VAULT_ROOT>`, not a byte mirror.
- A user-facing next step depends on context that future sessions would not
  discover from the current instruction surfaces.

Ignore harmless differences such as formatting-only changes or intentionally
local project rules.

## Output Contract

Stay quiet when no meaningful drift is found, unless the user explicitly asked
for a report.

When drift is found, show a concise report:

```markdown
**Context Check**
- Surface: `<path>`
- Drift: <what is stale or missing>
- Suggested patch: <one sentence>
- Risk: <why this should or should not be written now>
```

Do not update `AGENTS.md`, `CLAUDE.md`, Knowledge pages, topic pages, or skill
files automatically. Ask for confirmation or wait for a direct instruction such
as "go", "apply", or "按你的建议做".

After confirmed writes, keep changes narrow:

- Preserve project-local rules over global defaults.
- Put global behavior in the vault root instruction file; put project-specific
  conventions in that project's root instruction file.
- Keep `AGENTS.md` and `CLAUDE.md` behaviorally aligned when both exist, while
  allowing tool-specific wording.
- Do not rewrite unrelated sections.
