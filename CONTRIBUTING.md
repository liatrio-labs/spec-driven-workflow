# Contributing to Spec Driven Development (SDD) Workflow

Thanks for your interest in contributing! This guide explains how to set up your environment, follow our style and commit conventions, run linters, and submit pull requests.

## Overview

This repository provides prompts that enable a spec‑driven development workflow. Contributions generally fall into one of these areas:

- Documentation improvements
- Prompt and workflow improvements
- Examples and use cases

Please open an issue first for significant changes to discuss the approach.

## Getting Started

1. Fork and clone the repository.
2. Ensure you have Python 3.12+ installed (for pre-commit hooks).
3. Set up the development environment:

```bash
pip install pre-commit
pre-commit install
```

## Development Setup

- Install pre-commit hooks once with `pre-commit install`.
- Keep changes small and focused; prefer incremental PRs.
- All prompts are plain Markdown files in the `prompts/` directory.

### Common Commands

```bash
# Run full pre-commit checks across the repo
pre-commit run --all-files

# Run markdown linting only
pre-commit run markdownlint-fix --all-files
```

## Style and Quality

- Markdown is linted using markdownlint (via pre-commit). Keep lines reasonably short and headings well structured.
- YAML files are validated for syntax errors.
- Commit messages must follow Conventional Commits specification (enforced via commitlint).
- Keep documentation consistent with `README.md`.

## Testing

Before submitting a PR, run:

```bash
# Run all pre-commit checks
pre-commit run --all-files
```

This will:

- Check YAML syntax
- Fix markdown formatting issues
- Validate commit message format (on commit)

## Branching and Commit Conventions

### Branch Naming

Use short, descriptive branch names with a category prefix:

- `feat/<short-topic>`
- `fix/<short-topic>`
- `docs/<short-topic>`
- `chore/<short-topic>`
- `refactor/<short-topic>`

Examples:

- `feat/new-prompt`
- `docs/usage-examples`
- `fix/prompt-typo`

### Conventional Commits

We follow the Conventional Commits specification. Examples:

- `feat: add new validation prompt`
- `fix: correct typo in generate-spec prompt`
- `docs: add usage examples`
- `chore: update markdownlint config`

If a change is breaking, include `!` (e.g., `feat!: restructure prompt format`).

Semantic versioning and releases are automated in CI using `python-semantic-release`. Contributors only need to follow Conventional Commits; no manual tagging is required.

## Pull Requests

- Keep PRs focused and well scoped.
- Use a conventional title (e.g., `feat: add new prompt`).
- PR description template:

```markdown
## Why?

## What Changed?

## Additional Notes
```

- Ensure all checks pass (pre-commit) before requesting review.
- Reference related issues where applicable.

## Issue Templates

Use the GitHub issue templates under `.github/ISSUE_TEMPLATE/` for bug reports, feature requests, and questions. These templates prompt for summary, context/repro, and related prompt/workflow information.

## Code of Conduct (Placeholder)

We strive to maintain a welcoming and respectful community. A formal Code of Conduct will be added or linked here in a future update. In the meantime, please be considerate and professional in all interactions.

If you have any concerns, please open an issue or contact the maintainers.

## References

- `README.md` — overview and quick start
- `.pre-commit-config.yaml` — linting and formatting hooks
- `.github/ISSUE_TEMPLATE/` — issue forms
