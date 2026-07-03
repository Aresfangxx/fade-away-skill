# Promote-To-Knowledge Module

Load this only when the user explicitly asks to create, update, or promote a durable
knowledge wiki page under `<VAULT_ROOT>/02 Knowledge/`.

## Time Zone Rule

Use the configured vault time zone for `created:`, `updated:`,
journal source links, and journal save entries.

## Purpose

Promote reusable knowledge from journal logs, task pages, weekly indexes, project
files, or the current conversation into a stable wiki page. Use this for methods,
frameworks, durable distinctions, operating models, and repeatedly useful answers.

Do not promote routine task status, narrow file-change summaries, or one-off
implementation logs unless they reveal a reusable pattern.

## Knowledge-Grade Gate

Before writing or updating a page, decide whether the source material is
knowledge-grade. A page is knowledge-grade only if it preserves reusable judgment,
not merely a summary of the latest chat.

Minimum bar:

- It names the original problem or confusion that made the knowledge necessary.
- It explains the reasoning, tradeoffs, or decision logic, not only the final rule.
- It separates durable principles from task-specific facts.
- It states where the pattern applies and where it does not.
- It includes provenance that points to the actual source material, not just the
  most recent assistant answer.

If the draft cannot meet this bar from available context, stop and read the
source files first. If the sources are unavailable or ambiguous, ask one concise
clarifying question instead of writing a shallow page.

Treat "chat recap disguised as knowledge" as a failure mode. Do not deliver a
knowledge page whose main content is only "what we just decided" without the
context that makes the decision reusable.

### Design / Product Knowledge

For UI, product, writing, narrative, workflow, or other design-oriented knowledge,
the page must include this reasoning chain unless the user asks for a different
format:

```markdown
## 设计初衷 / Problem
## 关键取舍 / Tradeoffs
## 设计逻辑 / Decision Logic
## 可复用原则 / Reusable Principles
## 适用 / 不适用场景
## 反模式
## 来源记录
```

Do not promote only the final visual tweak. For design knowledge, read the
brainstorming notes, specs, plans, task pages, or other durable design artifacts
that explain why the design exists.

## Destination

Default root:

```markdown
<VAULT_ROOT>/02 Knowledge/
```

List the live top-level folders under `<VAULT_ROOT>/02 Knowledge/` and
choose the smallest fitting domain from the current structure. Propose a new
folder only when none fits.

If `02 Knowledge/` is empty in a fresh vault/bootstrap scenario, use these
initial domains:

- `AI 工作流/`
- `文档生产/`
- `个人方法论/`
- `项目管理/`
- `技术排错/`

If no domain is obvious, ask one short clarification question or place the page at
`02 Knowledge/<title>.md`.

## Page Template

Use this structure unless the user asks for a different format. Use vault-time dates for both fields:

```markdown
---
type: knowledge
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
sources:
  - "[[<YYYY-MM-DD>#HH:MM]]"
---

# <标题>

## 核心结论

## 适用场景

## 判断框架 / 操作模式

## 例子

## 来源记录
```

Adapt section names to the topic, but keep source provenance.

## Promotion Workflow

1. Identify source material:
   - Current conversation, if the user says "把刚才这个沉淀".
   - Lint report candidate sources.
   - Journal entries, weekly indexes, topic pages, or project files named by user.
2. Read the original sources before drafting:
   - For a journal source, read the whole relevant entry, not just one progress line.
   - For a design or implementation decision, read the spec/plan/task page when
     one exists.
   - For a current-conversation source, still check whether there are existing
     files that contain earlier context.
3. Check whether a similar knowledge page already exists under `02 Knowledge/`.
   - If yes, update it instead of creating a duplicate.
   - Preserve useful manual content.
4. Write a concise synthesis:
   - Start with the durable conclusion.
   - Include the original problem, decision logic, and tradeoffs when relevant.
   - Separate reusable principle from specific examples.
   - Keep task/project facts as examples, not as the whole page.
5. Add provenance:
   - Include journal links, topic links, weekly-index links, or source file links.
   - If a claim is inferred rather than directly sourced, mark it as synthesis.
6. Read the page back and verify:
   - Frontmatter is present.
   - Sources are present.
   - Source links point to real headings/files where possible.
   - The page is not just a task log.
   - The page is not just a chat recap.
   - Design/product pages contain initial intent, tradeoffs, decision logic,
     reusable principles, and anti-patterns.

## Optional Indexing

If a domain folder develops more than 5 pages, suggest creating an `_Index.md` in
that domain. Do not create the domain index unless the user agrees.

## Journal Save

After creating or materially updating a knowledge page, append one progress line to
the current journal entry, or open a short entry if none is active:

```markdown
### HH:MM ▶️ Knowledge wiki 沉淀
(HH:MM) 将 <topic> 沉淀为 `02 Knowledge/<path>.md`，保留来源链接。
```
