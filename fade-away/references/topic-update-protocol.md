# Topic Update Protocol

Use this module when a bound topic needs to be updated after an explicit
`➡️ 下一步`, or when Topic Auto-Refresh may need to fold journal progress back
into the topic page.

## Explicit Next-Step Update

When `bound_topic` is set and the visible output contains an explicit
`➡️ 下一步` marker or `## ➡️ 下一步` section:

1. Read `<VAULT_ROOT>/00 Tasks/<bound_topic>.md`.
2. Update only these regions:
   - Frontmatter `updated:` -> current vault-time ISO 8601 timestamp, including
     `+08:00` when possible.
   - `## 📍 现状` -> concise synthesis of previous status plus this turn's
     progress; include blockers inline with `⚠️` if relevant.
   - `## ➡️ 下一步` -> the latest explicit next action.
   - `## 🕐 Sessions` -> append
     `- YYYY-MM-DD HH:MM → [[YYYY-MM-DD#HH:MM]]` using the vault-time date/time, only
     if that vault-time date is not already listed. Drop any `03 Journal/` prefix;
     Obsidian resolves the link by basename.
3. Update `_Index.md`: follow the concurrent-write rules in
   `journal-write-protocol.md`, remove any existing active-table row for this
   topic, and insert a fresh row at the top of the table body.
4. Sanitize the index next-step before writing: collapse newlines to spaces,
   trim whitespace, escape literal `|` as `\|`, and compress it to one
   next-action sentence, <= ~120 characters. When the topic page lists multiple
   items, write only the top-priority action plus `（余 N 项见 topic 页）`.
5. Read `_Index.md` back after writing. Confirm the topic has exactly one row
   and the Markdown table still has three columns per body row.

## Topic Auto-Refresh

The Promotion Trigger fires only on an explicit `➡️ 下一步`. Long sessions may
accumulate many progress lines without that marker, leaving the bound topic's
`## 📍 现状` stale even though the journal has the latest truth.

When `bound_topic` is set and either staleness threshold defined in SKILL.md
Post-Save Check #2 holds after the per-turn save, refresh the topic page even
without an explicit next-step. Count `(HH:MM)` lines under the current entry
header whose timestamps are newer than the topic frontmatter `updated:`.

Skip the refresh when the turn is pure clarification, dashboard-only, lint-only,
or weekly-index-only.
Skip the refresh and ask `这些进展像是另一个任务，要切 entry 吗？` when the new
progress lines clearly belong to a different project or deliverable than the
bound topic.

The refresh follows the explicit update rules with these adjustments:

- `## ➡️ 下一步` is not overwritten unless the active entry contains a fresh
  explicit marker. If the existing next-step is still valid, leave it; if it is
  clearly obsolete, append `⚠️ 待用户确认是否仍然有效` rather than guess.
- Pitfall lines (`(HH:MM) ❌ ...`) from the active entry are aggregated into
  `## 🪤 踩过的坑` on the topic page. Create the section if missing, one bullet
  per pitfall: `- <YYYY-MM-DD> <一句死路根因>`. Deduplicate by trimmed message.
- Do not touch `_Index.md` unless `📍 现状` actually changed. The index row's
  next-step is meaningful only when there is a new next-step.
