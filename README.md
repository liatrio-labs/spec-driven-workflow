<div align="center">
    <img src="./misc/header.png" alt="Spec Driven Development header" width="400"/>
    <h1>🧭 Spec-Driven Development Workflow</h1>
    <h3><em>Build predictable software with a repeatable AI-guided workflow.</em></h3>
</div>

<p align="center">
    <strong>Spec-driven development tools for collaborating with AI agents to deliver reliable outcomes.</strong>
</p>

<p align="center">
    <a href="https://github.com/liatrio-labs/spec-driven-workflow/actions/workflows/ci.yml"><img src="https://github.com/liatrio-labs/spec-driven-workflow/actions/workflows/ci.yml/badge.svg" alt="CI Status"/></a>
    <a href="https://github.com/liatrio-labs/spec-driven-workflow/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"/></a>
    <a href="https://github.com/liatrio-labs/spec-driven-workflow/stargazers"><img src="https://img.shields.io/github/stars/liatrio-labs/spec-driven-workflow?style=social" alt="GitHub stars"/></a>
    <a href="docs/operations.md"><img src="https://img.shields.io/badge/docs-Operations-blue" alt="Documentation"/></a>
</p>

## TLDR

1. Install the workflow prompts as slash commands in all your [local AI tools](#supported-ai-tools):

    ```bash
    # Use Slash Command Manager (new location)
    uvx --from git+https://github.com/liatrio-labs/slash-command-manager slash-man generate --yes
    ```

2. In your AI tool of choice, use `/generate-spec` with your idea:

    ```text
    /generate-spec I want to add user authentication to my app
    ```

    → AI asks clarifying questions → You provide answers → Spec created in `tasks/0001-spec-user-auth.md`

3. Continue the flow:

    - Run `/generate-task-list-from-spec` → Task list created in `tasks/tasks-0001-spec-user-auth.md`
    - Use `/manage-tasks` → Execute tasks one-by-one with proof artifacts

4. **SHIP IT** 🚢💨

## ⚠️ Migration Notice: Generator and MCP Functionality Moved

**Important:** The slash command generator and MCP server functionality have been extracted into a separate repository: **[Slash Command Manager](https://github.com/liatrio-labs/slash-command-manager)**.

### What Changed

- **Old CLI entry point:** `sdd-commands` (from `spec-driven-workflow`)
- **New CLI entry point:** `slash-man` (from `slash-command-manager`)
- **Old MCP server:** `spec-driven-workflow-mcp`
- **New MCP server:** `slash-command-manager-mcp`

### Quick Migration Steps

#### 1. Install Slash Command Manager

```bash
# Via uvx (recommended)
uvx --from git+https://github.com/liatrio-labs/slash-command-manager slash-man generate --yes

# Or from source
git clone https://github.com/liatrio-labs/slash-command-manager.git
cd slash-command-manager
pip install -e .
slash-man generate --yes
```

#### 2. Update Your Scripts and CI/CD

Replace any references to `sdd-commands` with `slash-man`:

```bash
# Old
sdd-commands generate --yes

# New
slash-man generate --yes
```

If you were installing from the old repository:

```bash
# Old
uvx --from git+https://github.com/liatrio-labs/spec-driven-workflow sdd-commands generate --yes

# New
uvx --from git+https://github.com/liatrio-labs/slash-command-manager slash-man generate --yes
```

#### 3. MCP Server Configuration

If you use the MCP server, update your configuration:

```bash
# Old
uvx --from git+https://github.com/liatrio-labs/spec-driven-workflow spec-driven-workflow-mcp

# New
uvx --from git+https://github.com/liatrio-labs/slash-command-manager slash-command-manager-mcp
```

### Backward Compatibility

**⚠️ Breaking Changes:**

- The `sdd-commands` CLI entry point is no longer available from this repository
- The `spec-driven-workflow-mcp` server entry point is no longer available from this repository
- Package dependencies (`fastmcp`, `questionary`, `typer`, etc.) are no longer included in `spec-driven-workflow`

**✅ No Breaking Changes:**

- The SDD workflow prompts (`prompts/`) remain unchanged and continue to work as before
- Generated slash command files are compatible with both old and new versions
- All functionality is preserved, just in a separate package

### This Repository Now Focuses On

- **SDD workflow prompts** (`prompts/`) — The three core prompts for spec-driven development
- **Documentation and workflow guidance** — Usage patterns, best practices, and examples
- **Reference materials** — Example specs, task lists, and workflow documentation

The generator CLI and MCP server are now maintained in the [Slash Command Manager](https://github.com/liatrio-labs/slash-command-manager) repository with independent versioning and release cycles.

## Highlights

- **Prompt-first workflow:** Use curated prompts to go from idea → spec → task list → implementation-ready backlog.
- **Predictable delivery:** Every step emphasizes demoable slices, proof artifacts, and collaboration with junior developers in mind.
- **Bonus MCP tooling:** Optionally pair the workflow with an MCP server for automation inside modern AI clients.

## Why Spec-Driven Development?

Spec-Driven Development (SDD) keeps AI collaborators and human developers aligned around a shared source of truth. This repository packages a lightweight, prompt-centric workflow that turns an idea into a reviewed specification, an actionable plan, and a disciplined execution loop. By centering on markdown artifacts instead of tooling, the workflow travels with you—across projects, models, and collaboration environments.

MCP technology remains available as an optional integration, but the heart of the project is the trio of prompts that guide teams from idea to demoable outcomes with consistent artifacts.

## Guiding Principles

- **Clarify intent before delivery:** The spec prompt enforces clarifying questions so requirements are explicit and junior-friendly.
- **Ship demoable slices:** Every stage pushes toward thin, end-to-end increments with clear demo criteria and proof artifacts.
- **Make work transparent:** Tasks live in versioned markdown files so stakeholders can review, comment, and adjust scope anytime.
- **Progress one slice at a time:** The management prompt enforces single-threaded execution to reduce churn and unfinished work-in-progress.
- **Stay automation ready:** While SDD works with plain Markdown, the prompts are structured for MCP, IDE agents, or other AI integrations.

## Prompt Workflow

All prompts live in `prompts/` and are designed for use inside your preferred AI assistant.

1. **`generate-spec`** (`prompts/generate-spec.md`): Ask clarifying questions, then author a junior-friendly spec with demoable slices.
2. **`generate-task-list-from-spec`** (`prompts/generate-task-list-from-spec.md`): Transform the approved spec into actionable parent tasks and sub-tasks with proof artifacts.
3. **`manage-tasks`** (`prompts/manage-tasks.md`): Coordinate execution, update task status, and record outcomes as you deliver value.

Each prompt writes Markdown outputs into `tasks/`, giving you a lightweight backlog that is easy to review, share, and implement.

## How does it work?

The workflow is driven by Markdown prompts that function as reusable playbooks for the AI agent. Reference the prompts directly, or invoke them via supported tooling, to keep the AI focused on structured outcomes. Users can manage context with their existing workflows (GitHub CLI, Atlassian MCP, etc.), and optionally let the MCP server automate portions of the process.

## Workflow Overview

Three prompts in `/prompts` define the full lifecycle. Use them sequentially to move from concept to completed work.

### Stage 1 — Generate the Spec ([prompts/generate-spec.md](./prompts/generate-spec.md))

- Directs the AI assistant to use clarifying questions with the user before writing a Markdown spec.
- Produces `/tasks/000X-spec-<feature>.md` with goals, demoable units of work, functional/non-goals, metrics, and open questions.

### Stage 2 — Generate the Task List ([prompts/generate-task-list-from-spec.md](./prompts/generate-task-list-from-spec.md))

- Reads the approved spec, inspects the repo for context, and drafts parent tasks first.
- On confirmation from the user, expands each parent task into sequenced subtasks with demo criteria, proof artifacts, and relevant files.
- Outputs `/tasks/tasks-000X-spec-<feature>.md` ready for implementation.

### Stage 3 — Manage Tasks ([prompts/manage-tasks.md](./prompts/manage-tasks.md))

- Enforces disciplined execution: mark in-progress immediately, finish one subtask before starting the next, and log artifacts as you go.
- Bakes in commit hygiene, validation steps, and communication rituals so handoffs stay tight.

### Detailed SDD Workflow Diagram

```mermaid
sequenceDiagram
  participant U as User
  participant GS as 1. generate-spec
  participant SPEC as 0001-spec-<feature>.md
  participant GT as 2. generate-task-list-from-spec
  participant TL as tasks-0001-spec-<feature>.md
  participant MT as 3. manage-tasks
  participant CODE as Code / Docs / Tests

  U->>GS: Provide Feature/Task
  GS->>CODE: Analyze codebase
  CODE-->>GS: Context findings
  GS->>U: Clarifications
  U-->>GS: Incorporate Clarifications
  GS->>SPEC: Write Spec (tasks/)
  SPEC-->>U: Review
  U-->>GS: Incorporate Review
  GS->>SPEC: Finalize Spec

  U->>GT: Provide Spec reference
  GT->>SPEC: Read Spec
  GT->>CODE: Analyze codebase
  CODE-->>GT: Context findings
  GT-->>U: Phase 1: parent tasks
  U-->>GT: Generate sub tasks
  GT-->>CODE: Identify Relevant Files
  GT->>TL: Phase 2: sub-tasks (write) (tasks/)

  U->>MT: Work tasks
  MT->>TL: Update statuses
  MT->>CODE: Implement changes
  CODE-->>U: Demo/changes for review
  U-->>MT: Feedback on changes
  MT->>CODE: Iterate changes
```

## Core Artifacts

- **Specs:** `000X-spec-<feature>.md` — canonical requirements, demo slices, and success metrics.
- **Task Lists:** `tasks-000X-spec-<feature>.md` — parent/subtask checklist with relevant files and proof artifacts.
- **Status Keys:** `[ ]` not started, `[~]` in progress, `[x]` complete, mirroring the manage-tasks guidance.
- **Proof Artifacts:** URLs, CLI commands, screenshots, or tests captured per task to demonstrate working software.

## Hands-On Usage

The SDD workflow can be used in three ways, from simplest to most automated:

### Option 1: Manual Copy-Paste (No Tooling Required)

1. **Kick off a spec:** Copy or reference `prompts/generate-spec.md` inside your preferred AI chat. Provide the feature idea, answer the clarifying questions, and review the generated spec before saving it under `/tasks`.
2. **Plan the work:** Point the assistant to the new spec and walk through `prompts/generate-task-list-from-spec.md`. Approve parent tasks first, then request the detailed subtasks and relevant files. Commit the result to `/tasks`.
3. **Execute with discipline:** Follow `prompts/manage-tasks.md` while implementing. Update statuses as you work, attach proof artifacts, and pause for reviews at each demoable slice.

### Option 2: Native Slash Commands (Recommended)

#### Supported AI Tools

The slash command generator currently supports the following AI coding assistants:

| AI Tool      | Command Install Location                         |
|--------------|--------------------------------------------------|
| Claude Code  | `~/.claude/commands`                             |
| Codex CLI    | `~/.codex/prompts`                               |
| Cursor       | `~/.cursor/commands`                             |
| Gemini CLI   | `~/.gemini/commands`                             |
| VS Code      | `~/.config/Code/User/prompts`                    |
| Windsurf     | `~/.codeium/windsurf/global_workflows`           |

For full setup and agent-specific details, see the [Slash Command Manager documentation](https://github.com/liatrio-labs/slash-command-manager).

#### Slash Command Installation

Generate slash commands for your AI coding assistant using Slash Command Manager:

```bash
# Via uvx (recommended)
uvx --from git+https://github.com/liatrio-labs/slash-command-manager slash-man generate --yes

# Or install locally
git clone https://github.com/liatrio-labs/slash-command-manager.git
cd slash-command-manager
pip install -e .
slash-man generate --yes
```

This will auto-detect your configured AI assistants (Claude Code, Cursor, Windsurf, etc.) and generate command files in your home directory.

**Note**: Once available on PyPI, you'll be able to run `uvx slash-command-manager slash-man generate --yes` for a one-liner installation.

See the [Slash Command Manager README](https://github.com/liatrio-labs/slash-command-manager) for details.

### Option 3: MCP Server (Advanced)

Run the prompts as an MCP server for programmatic access. This option is most useful for custom integrations and tools that support MCP.

**Installation and Usage:**

```bash
# Via uvx (recommended)
uvx --from git+https://github.com/liatrio-labs/slash-command-manager slash-command-manager-mcp

# Or install locally
git clone https://github.com/liatrio-labs/slash-command-manager.git
cd slash-command-manager
pip install -e .
python server.py
```

> Note: MCP prompt support is not uniformly supported across AI tools. See [docs/mcp-prompt-support.md](./docs/mcp-prompt-support.md) for details.
>
> **Migration:** The MCP server has been moved to [Slash Command Manager](https://github.com/liatrio-labs/slash-command-manager). This repository retains the prompts for reference, but the server implementation is now in the separate repository.

### Workflow Essentials

1. Open `prompts/generate-spec.md` inside your AI assistant and follow the instructions to produce a new spec in `tasks/`.
2. Point the assistant at the generated spec and run `prompts/generate-task-list-from-spec.md` to create the implementation backlog.
3. Use `prompts/manage-tasks.md` while executing work to keep status, demo criteria, and proof artifacts up to date.

### Installation

```bash
# Clone the repository
git clone https://github.com/liatrio-labs/spec-driven-workflow.git
cd spec-driven-workflow

# Install dependencies
uv sync
```

### Run the MCP Server

The MCP server has been moved to the [Slash Command Manager](https://github.com/liatrio-labs/slash-command-manager) repository. See that repository's documentation for installation and usage instructions.

See [docs/operations.md](docs/operations.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for advanced configuration, deployment, and contribution guidelines.

## References

| Reference | Description | Link |
| --- | --- | --- |
| AI Dev Tasks | Foundational example of an SDD workflow expressed entirely in Markdown. | <https://github.com/snarktank/ai-dev-tasks> |
| MCP | Standard protocol for AI agent interoperability, used here as an optional integration layer. | <https://modelcontextprotocol.io/docs/getting-started/intro> |
| FastMCP | Python tooling for building MCP servers and clients that power this repo's automation. | <https://github.com/jlowin/fastmcp> |

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
