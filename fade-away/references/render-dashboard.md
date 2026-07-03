# Render-Dashboard Module

Load this only when the user asks for a task overview. Do not modify files.

## Time Zone Rule

Interpret `_Index.md` timestamps and relative labels using the configured vault time zone. `今天` and `昨天` are vault-time calendar dates.

## Step 1 - Read Index

Read `<VAULT_ROOT>/00 Tasks/_Index.md`.

If the file is missing or the table has no body rows, output:

```markdown
📭 当前没有进行中的任务。
```

Stop and wait for the user's next message. Do not open a journal entry.

## Step 2 - Parse Rows

Parse rows in this format:

```markdown
| [[topic]] | YYYY-MM-DD HH:MM | next-step |
```

Treat escaped `\|` inside next-step as literal `|`. Ignore malformed rows and, if any
are ignored, add a short `⚠️` line after the dashboard naming the malformed topic or
row text.

## Step 3 - Categorize

Compute calendar days since the timestamp using vault-time calendar dates:

| Days since | Tier |
|---|---|
| 0-7 | 🔥 活跃 |
| 8-30 | 💤 休眠 |
| >30 | 🗄️ 长睡 |

Relative time:

- Same vault-time date: `今天 HH:MM`
- 1 day ago: `昨天 HH:MM`
- 2+ days: `<N> 天前`

## Step 4 - Render

Output:

```markdown
🔥 活跃（7 天内）
- [[<topic>]] — <relative-time> — <next-step>

💤 休眠（8-30 天）
- （无）

🗄️ 长睡（>30 天）
- （无）
```

For empty tiers, use `- （无）`. Keep topic order from `_Index.md` within each tier.

If an active row is more than 10 vault-time calendar days old or its next-step starts
with `—（已完成）`, add a short read-only fade-out candidate note after the
dashboard. Do not move files; confirmed archive operations use
`references/fade-out-protocol.md`.

## Step 5 - Wait

After rendering, wait. The next user message should go through normal fade-away
conversation-start handling and open a journal entry only if work begins.
