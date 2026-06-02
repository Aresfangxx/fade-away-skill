# Bootstrap Vault

Use this module only for first-run setup of a new fade-away Obsidian vault. This
is not a daily startup check and not a drift checker.

## Trigger

Read this module when the user explicitly asks to install, set up, initialize,
bootstrap, or open-source-deploy `fade-away`, or when the current workspace lacks
the core vault files and the user asks to initialize them.

Do not run this module during ordinary greetings, per-turn saves, normal topic
work, dashboard rendering, linting, or context drift checks.

## Inputs

Before creating files, identify:

- Vault root: ask when unclear. Prefer an absolute path. For portable/open-source
  installs, support `FADE_AWAY_VAULT_ROOT`.
- Agent surfaces: whether to create `AGENTS.md`, `CLAUDE.md`, or both.
- Time zone: default `Asia/Hong_Kong` only for this user's vault; for a public
  install, ask or preserve the user's local preference.

If the target path already contains notes, treat it as an existing vault. Never
delete, move, or overwrite existing files.

## Minimal Structure

Create only the minimum needed for fade-away to run:

```text
<vault>/
├── 00 Tasks/
│   └── _Index.md
├── 02 Knowledge/
├── 03 Journal/
├── 04 Templates/
│   └── Daily Note.md
├── AGENTS.md
└── CLAUDE.md (optional)
```

`01 Note/` is optional. Create it only if the user wants a general notes inbox.

## Setup Steps

1. Show the target vault root and files that will be created.
2. Ask for confirmation unless the user already gave a direct command such as
   "go", "apply", or "create it".
3. Prefer `scripts/bootstrap_vault.py` for deterministic setup.
4. After setup, verify the created files exist and render a short summary.
5. Do not open a normal journal entry unless the user starts substantive work
   inside the new vault.

## Script

Run from the skill directory:

```bash
python3 scripts/bootstrap_vault.py --vault-root "/absolute/path/to/vault"
```

Useful options:

- `--agent-surface agents` creates `AGENTS.md` only.
- `--agent-surface claude` creates `CLAUDE.md` only.
- `--agent-surface both` creates both.
- `--timezone Asia/Hong_Kong` sets the timezone text in generated instructions.
- `--dry-run` prints actions without writing.

The script is idempotent: it creates missing directories and files, and skips
existing files.

## Generated Content Rules

Keep generated instruction files thin:

- Point agents to `fade-away` as the session tracker.
- Record the vault root and timezone.
- Explain the minimal directory structure.
- State that existing files must not be deleted or overwritten.

Do not copy the full `fade-away` skill into `AGENTS.md` or `CLAUDE.md`.
Instruction files are routing surfaces, not full manuals.
