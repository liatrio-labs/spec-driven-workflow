# Migrate Spec-Driven Development from slash-command prompts to the `sdd` skill

> **Stable link for sharing:** use <https://github.com/liatrio-labs/spec-driven-workflow/blob/main/MIGRATION.md>. Avoid sharing links to temporary PR branches because those branch links may stop working after the PR is merged and the branch is deleted.

If you previously installed Spec-Driven Development (SDD) as four slash-command prompts, you can now install it as one agent skill:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code
```

After restarting your agent, use:

```text
/sdd
```

The skill replaces the need to remember four separate `/SDD-*` commands. Existing project artifacts under `docs/specs/` do not need to be moved or converted.

## Who this guide is for

Use this guide if you installed SDD with the older prompt-based flow, usually with a command like this:

```bash
uvx --from git+https://github.com/liatrio-labs/slash-command-manager \
  slash-man generate \
  --github-repo liatrio-labs/spec-driven-workflow \
  --github-branch main \
  --github-path prompts/
```

That install created separate commands such as:

```text
/SDD-1-generate-spec
/SDD-2-generate-task-list-from-spec
/SDD-3-manage-tasks
/SDD-4-validate-spec-implementation
```

The prompt-based install still works as a fallback for agents that do not support skills. For agents that do support skills, use the `sdd` skill instead.

## What changes after migration

Before migration, you picked the phase command yourself:

```text
/SDD-1-generate-spec
/SDD-2-generate-task-list-from-spec
/SDD-3-manage-tasks
/SDD-4-validate-spec-implementation
```

After migration, you invoke one skill:

```text
/sdd
```

The skill checks the repository, looks at `docs/specs/`, and decides which SDD phase applies.

```text
Old prompt command                         New skill invocation
----------------------------------------   -----------------------------------------
/SDD-1-generate-spec                       /sdd Start SDD for a new feature.
/SDD-2-generate-task-list-from-spec        /sdd Continue SDD with task planning.
/SDD-3-manage-tasks                        /sdd Continue SDD with implementation.
/SDD-4-validate-spec-implementation        /sdd Continue SDD with validation.
```

You do not need to use those exact phrases. They are examples. The important part is that `/sdd` is the entry point.

## Why the skill install is preferred

The skill install is simpler for day-to-day use:

- one entry point instead of four commands,
- less chance of running the wrong phase,
- better continuation after starting a fresh agent session,
- automatic routing based on artifacts already in the repo,
- the same Markdown outputs under `docs/specs/`.

The workflow is still intentionally explicit. The `sdd` skill is something you invoke when you want to run SDD; it is not meant to trigger automatically in the background.

## Before you migrate

If you are in the middle of an SDD run, checkpoint your work first.

From the project repository:

```bash
git status --short
```

If you have uncommitted SDD artifacts, commit or otherwise save them before changing your setup:

```bash
git add docs/specs
git commit -m "docs: checkpoint SDD artifacts"
```

If your team does not want checkpoint commits, use your normal backup or branch workflow. The key point is simple: do not leave active specs, tasks, or proof artifacts only in untracked local files.

## Install the `sdd` skill

### Claude Code

For Claude Code, run:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code
```

For a non-interactive install:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code --yes
```

If the installer reports symlink or permission problems, retry with `--copy`:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code --copy
```

### Other agents

If you use another supported agent, change the `-a` target. For example:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a cursor
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a codex
```

You can install to more than one agent at once:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a cursor -a codex
```

## Update an existing `sdd` skill install

If you already installed the `sdd` skill and want the latest published version, run:

```bash
npx skills update sdd --yes
```

The `skills` CLI also supports scope-specific updates:

```bash
# Update only project-scoped skills
npx skills update sdd --project --yes

# Update only globally installed skills
npx skills update sdd --global --yes
```

Restart your agent after updating so it reloads the refreshed skill files.

## Restart and verify

Restart your agent after installing the skill.

For Claude Code:

```bash
claude
```

Inside Claude Code, list installed skills:

```text
/skills
```

Confirm that `sdd` appears in the list.

Then open a repository where you use SDD and run:

```text
/sdd
```

A healthy first response should tell you:

- the detected SDD phase,
- the selected spec directory, if one exists,
- what artifact state it found under `docs/specs/`,
- what to do next.

## Continue an existing SDD run

No artifact migration is required.

The skill uses the same SDD artifact structure as the prompt workflow:

```text
docs/specs/
└── 01-spec-feature-name/
    ├── 01-spec-feature-name.md
    ├── 01-questions-1-feature-name.md        # optional
    ├── 01-tasks-feature-name.md
    ├── 01-audit-feature-name.md
    ├── 01-proofs/
    │   └── 01-task-01-proofs.md
    └── 01-validation-feature-name.md
```

To continue work that started under the old prompts:

1. open a fresh agent session in the project repository,
2. invoke `/sdd`,
3. let the skill inspect `docs/specs/`,
4. follow the phase it reports.

If more than one active spec exists, the skill should ask which one to continue.

## Clean up the old prompt commands

Cleanup is optional. You can leave the old prompt commands installed while you verify the new skill. Remove them only after `/sdd` works.

There are two cleanup options:

1. use `slash-man cleanup` to remove generated slash-command-manager files,
2. manually remove only the old SDD prompt files from your agent command directory.

### Option 1: use `slash-man cleanup`

Start with a dry run:

```bash
uvx --from git+https://github.com/liatrio-labs/slash-command-manager \
  slash-man cleanup \
  --dry-run \
  --agent claude-code \
  --yes
```

Review the files it plans to delete. This matters because `slash-man cleanup` can remove other files generated by Slash Command Manager, not only SDD prompts.

If the dry run only lists files you want to remove, run:

```bash
uvx --from git+https://github.com/liatrio-labs/slash-command-manager \
  slash-man cleanup \
  --agent claude-code \
  --yes
```

To clean another agent, change the `--agent` value:

```bash
uvx --from git+https://github.com/liatrio-labs/slash-command-manager \
  slash-man cleanup \
  --dry-run \
  --agent cursor \
  --yes
```

Useful cleanup flags:

```text
--dry-run          Show what would be deleted without deleting files
--agent, -a        Limit cleanup to one agent; can be repeated
--yes, -y          Skip confirmation prompts
--target-path, -t  Search under a specific directory instead of your home directory
--no-backups       Do not remove backup files
```

### Option 2: manually remove only the SDD prompt files

If you only want to remove the old SDD prompts and keep other generated slash commands, manually delete the SDD files.

Look for these filenames:

```text
SDD-1-generate-spec.md
SDD-2-generate-task-list-from-spec.md
SDD-3-manage-tasks.md
SDD-4-validate-spec-implementation.md
```

There may also be timestamped backup files, for example:

```text
SDD-1-generate-spec.md.20260317-175041.bak
```

Common prompt install locations:

```text
Claude Code:       ~/.claude/commands
Cursor:            ~/.cursor/commands
Windsurf:          ~/.codeium/windsurf/global_workflows
Codex CLI:         ~/.codex/prompts
Gemini CLI:        ~/.gemini/commands
VS Code Linux:     ~/.config/Code/User/prompts
VS Code macOS:     ~/Library/Application Support/Code/User/prompts
VS Code Windows:   %APPDATA%\Code\User\prompts
OpenCode CLI:      ~/.config/opencode/command
Amazon Q:          ~/.aws/amazonq/prompts
Kiro CLI:          ~/.kiro/prompts
Kiro IDE:          ~/.kiro/steering
```

For Claude Code on macOS/Linux, a cautious manual cleanup looks like this:

```bash
mkdir -p ~/.claude/commands/archive-sdd-prompts
mv ~/.claude/commands/SDD-1-generate-spec.md* ~/.claude/commands/archive-sdd-prompts/ 2>/dev/null || true
mv ~/.claude/commands/SDD-2-generate-task-list-from-spec.md* ~/.claude/commands/archive-sdd-prompts/ 2>/dev/null || true
mv ~/.claude/commands/SDD-3-manage-tasks.md* ~/.claude/commands/archive-sdd-prompts/ 2>/dev/null || true
mv ~/.claude/commands/SDD-4-validate-spec-implementation.md* ~/.claude/commands/archive-sdd-prompts/ 2>/dev/null || true
```

This archives the files instead of deleting them. After restarting Claude Code and confirming the old `/SDD-*` commands no longer appear, you can delete the archive if you no longer need it.

## Recommended rollout for teams

For a team or class environment:

1. Update onboarding docs to show the `npx skills add ... --skill sdd` command as the default.
2. Tell users that the slash-command prompt install is now fallback-only.
3. Have users restart their agent after installing the skill.
4. Ask users to verify with `/skills` before the first SDD exercise.
5. During exercises, tell users to invoke `/sdd` instead of choosing `/SDD-*` commands.
6. Leave cleanup of old prompt files as a separate optional step after verification.

Avoid asking users to remove old prompts before the skill is verified. That creates unnecessary recovery work if their agent or environment has a skill-loading issue.

## Troubleshooting

### `npx: command not found`

Install Node.js/npm, then verify:

```bash
node --version
npm --version
npx --version
```

### The `sdd` skill does not appear

Try these in order:

1. restart the agent completely,
2. run the agent's skill listing command, such as `/skills`,
3. reinstall with `--yes`,
4. retry with `--copy` if the installer reports symlink or permission errors.

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code --yes
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code --copy
```

### The old `/SDD-*` commands still show up

The old prompt files probably still exist in your agent command directory.

Use one of the cleanup options above, then restart the agent.

### The skill chooses the wrong phase

First confirm you are running the agent from the repository root. Then inspect the SDD artifacts:

```bash
find docs/specs -maxdepth 3 -type f | sort
```

Common causes:

- multiple active specs exist,
- the task file exists but the audit file is missing,
- generated files were renamed outside the expected `[NN]-...` pattern,
- the agent session was opened outside the project repository.

If needed, provide the spec name when invoking the skill:

```text
/sdd Continue the 02-spec-checkout-flow spec with validation.
```

### The agent skips checkpoints or stops showing SDD markers

The SDD workflow uses markers such as `SDD1️⃣`, `SDD2️⃣`, `SDD3️⃣`, and `SDD4️⃣` to make context problems easier to spot.

If markers disappear, or the agent starts skipping required stop-and-wait checkpoints, start a fresh session from the repository root and invoke `/sdd` again.

## Quick reference

Recommended Claude Code install:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code
```

Non-interactive install:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code --yes
```

Permission/symlink fallback:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd -a claude-code --copy
```

Update an existing `sdd` skill install:

```bash
npx skills update sdd --yes
```

Verify inside Claude Code:

```text
/skills
```

Start or continue SDD:

```text
/sdd
```

Old prompt install, fallback only:

```bash
uvx --from git+https://github.com/liatrio-labs/slash-command-manager \
  slash-man generate \
  --github-repo liatrio-labs/spec-driven-workflow \
  --github-branch main \
  --github-path prompts/
```

Dry-run cleanup of old generated prompt commands:

```bash
uvx --from git+https://github.com/liatrio-labs/slash-command-manager \
  slash-man cleanup \
  --dry-run \
  --agent claude-code \
  --yes
```

## Source links

- SDD repository: <https://github.com/liatrio-labs/spec-driven-workflow>
- SDD README quickstart: <https://github.com/liatrio-labs/spec-driven-workflow#tldr--quickstart>
- SDD Playbook: <https://liatrio-labs.github.io/spec-driven-workflow/index.html>
- Forge SDD install docs: <https://liatrio-labs.github.io/forge-immersive-ai-mastery-program/docs/introduction/1.3-install-sdd-workflow>
- Slash Command Manager: <https://github.com/liatrio-labs/slash-command-manager>
