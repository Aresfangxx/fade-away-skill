# Knowledge-Retrieval-Trigger Module

Load this from `SKILL.md` before substantive work when the current request may
depend on durable context in `<VAULT_ROOT>/02 Knowledge/`. This module is
read-only.

This is an inventory-first retrieval gate. Do not hard-code current Knowledge
folders as the routing model. `02 Knowledge/` is expected to grow. Each run must
first inspect the current directory and Markdown metadata, then decide which
files to read from that live structure.

## Purpose

`00 Tasks/_Index.md`, topic pages, and recent journals recover short-term task
state. `02 Knowledge/` recovers long-term methods, project facts, personal
preferences, decision frameworks, writing conventions, and anti-patterns. A
substantive answer should use both layers when the request plausibly depends on
both.

## When To Run

Run this gate for:

- Named projects, domains, people, products, or methods.
- Requests for context, "what am I doing", strategy, decisions, tradeoffs,
  prioritization, reviews, writing style, or diagnosis.
- Continuations of older work where `_Index.md` gives only the next step but not
  the reusable method or factual source.
- Any task where prior rules, templates, evidence maps, personal preferences, or
  domain source-of-truth pages would materially change the answer.

Skip this gate for:

- Vague greetings that are waiting for the user's confirmation.
- Dashboard, lint, and weekly-index rendering unless the module itself asks for
  Knowledge.
- Pure journal bookkeeping, manual record requests, or topic/index maintenance.
- Atomic utility tasks with no project or reusable-method dimension.
- Sensitive folders/files unless the user explicitly asks for them.

## Retrieval Model

Use a three-stage pipeline:

1. **Inventory** - list the live Knowledge tree and Markdown metadata.
2. **Rank** - score candidate files from paths, names, headings, aliases, tags,
   type/status, and source-of-truth markers.
3. **Read** - open only the highest-value Markdown pages, usually 1-3 files.

Full-body search is a fallback, not the primary routing method.

## Step 1 - Build Query Signals

Extract 2-8 signals from:

- the user's request;
- matched topic title and `_Index.md` next-step;
- current project folder or mentioned file path;
- explicit skill/tool names;
- requested output type, such as `deck`, `slides`, `docx`, `PDF`, `review`,
  `决策`, `排错`, `写作`, `尽调`.

Include both literal words and obvious variants. Do not rely on a fixed synonym
table; infer from the current request and the live Knowledge inventory.

## Step 2 - Inventory The Live Knowledge Tree

Always start with current structure. Substitute the resolved absolute vault root
for `<VAULT_ROOT>`:

```bash
rg --files "<VAULT_ROOT>/02 Knowledge"
find "<VAULT_ROOT>/02 Knowledge" -maxdepth 2 -type d | sort
rg -n "^(title|aliases|tags|domain|type|status|canonical):|^# " "<VAULT_ROOT>/02 Knowledge"
```

From this inventory, derive:

- top-level domains from folder names;
- candidate pages whose filename, H1, `title`, or `aliases` match the query;
- candidate pages whose `tags` or `domain` match the query;
- navigation pages from `type: moc`, filenames containing `知识地图`, `MOC`, or
  `index`;
- source-of-truth pages from filenames or tags containing `口径`, `事实源`,
  `source-of-truth`, `single-source-of-truth`, `SSOT`;
- canonical pages from `status: canonical`; deprioritize `status: superseded`
  unless the user asks for an archived version.

The inventory is the router. If a new folder or page appears, it must be
eligible without editing this module.

## Step 3 - Rank Candidate Files

Rank candidates with this priority:

1. Exact match in filename, H1, `title`, or `aliases`.
2. Strong match between query signals and the top-level folder or subfolder
   names.
3. `tags` / `domain` match.
4. Navigation page (`type: moc`, `知识地图`, `MOC`, `index`) for broad domain
   requests.
5. Source-of-truth page for factual questions in that domain.
6. Method/template pages (`架构`, `流程`, `规范`, `规则`, `模板`) for production,
   writing, implementation, or review tasks.
7. `status: canonical` over `status: superseded`.
8. Full-body match inside a selected domain only when metadata is insufficient.

For broad domains, read the navigation/MOC page first, then one source-of-truth
or method page selected from that navigation. For narrow requests, read the
direct page first and follow at most one Knowledge-to-Knowledge link.

## Step 4 - Read Budget

Read the smallest useful set:

- Usually 1-3 Markdown pages.
- Avoid PDFs, images, generated HTML, and binary assets unless explicitly asked.
- Follow at most one Knowledge-to-Knowledge hop unless the task requires a
  formal audit.
- If no file is defensible after inventory + metadata ranking, continue from
  the task/journal layer instead of broad-scanning the vault.

## Step 5 - Body Search Fallback

Use full-content search only after inventory and metadata routing fail, or when
looking for a specific phrase inside a selected candidate domain:

```bash
rg -n "<specific phrase>|<rare keyword>" "<VAULT_ROOT>/02 Knowledge/<selected-domain-or-file>"
```

Do not run broad body searches as the primary strategy when paths,
frontmatter, aliases, tags, navigation pages, or source-of-truth pages already
provide a route.

## How To Use The Result

- Let Knowledge change the answer's assumptions, not just appear as a citation.
- If Knowledge conflicts with a recent journal or topic page, state the conflict
  and prefer the most authoritative source for that kind of fact:
  - current task state -> topic page / `_Index.md` / latest journal
  - durable methods and preferences -> `02 Knowledge/`
  - project facts with a source-of-truth page -> that source-of-truth page
- If no relevant Knowledge is found after inventory-first routing, continue from
  the task/journal layer and do not mention the absence unless it matters.
- Set `knowledge_context_checked = True` after the gate runs or is intentionally
  skipped.

## Anti-Patterns

- Reading `_Index.md` and today's journal, then claiming to know the user's
  broader context.
- Treating Knowledge as an archive only for humans rather than an active
  retrieval layer for the agent.
- Hard-coding current folder names as the only routing map.
- Running broad full-content search before checking live inventory, filenames,
  headings, frontmatter, aliases, tags, navigation pages, and source-of-truth
  pages.
- Opening many old pages when one navigation page plus one source-of-truth or
  method page would answer the request.
- Using stale Knowledge to override a newer explicit user correction.
