# Fade-Out Protocol

Load this module only for archive/fade-out requests (`归档`, `淡出`, `收进 FADE`)
or when dashboard/lint rendering nominates stale/completed tasks. This module is
confirmation-gated: render candidates first, then execute only after the user
clearly confirms.

## Fade-Out Conditions

Nominate a topic when either condition is true:

- Its active `_Index.md` row is more than 10 vault-time calendar days old.
- The topic frontmatter has `status: completed`, or its index next-step starts
  with `—（已完成）`.

Do not silently move files. Dashboard/lint may report candidates, but file moves
and link rewrites require explicit confirmation.

## Archive Operation

After confirmation, perform all three steps:

1. Move the topic file from `<VAULT_ROOT>/00 Tasks/<topic>.md` to
   `<VAULT_ROOT>/00 Tasks/FADE/<branch>/<topic>.md`.
2. Move its `_Index.md` row out of the active table and into the graveyard
   section. The graveyard uses list items, not active table rows.
3. Run `rg` over journals and weekly indexes for path-style wikilinks pointing
   at the old path and rewrite them explicitly. A filesystem move bypasses
   Obsidian's automatic link update, so this scan is required.

Preserve existing topic content, frontmatter, sessions, and source links.

## Revive / Derivative Work

- If an unfinished faded task resumes, un-fade it: move the topic back to
  `<VAULT_ROOT>/00 Tasks/`, then insert a fresh active-table row at the
  top of `_Index.md`.
- If a completed task leads to derivative work, create a new topic instead of
  reviving the completed page.

## FADE Format

`00 Tasks/FADE/` contains branch folders plus optional merged pages. `_原始页/`
keeps pre-merge source pages. `type: fade-merged` marks a valid merged history
page. Links from the graveyard may use `[[FADE/<branch>/<topic>]]`; active table
rows must not.
