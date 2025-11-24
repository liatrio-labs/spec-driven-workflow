# Contributing to Spec-Driven Development (SDD) Workflow

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

### Recommended: Secret Scanning Pre-commit Hooks

To prevent accidental commits of API keys, tokens, or other sensitive data (especially in proof artifacts), consider adding secret scanning to your pre-commit configuration:

#### Option 1: gitleaks (recommended)

```yaml
# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0 # Update to the latest version (run `pre-commit autoupdate`)
    hooks:
      - id: gitleaks
```

#### Option 2: truffleHog

```yaml
# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0 # Update to the latest version (run `pre-commit autoupdate`)
    hooks:
      - id: trufflehog
        args: ['--trace', 'filesystem', '.']
```

#### Option 3: detect-secrets

```yaml
# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0 # Update to the latest version (run `pre-commit autoupdate`)
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

After adding a secret scanner, run `pre-commit install` again to activate it. The scanner will automatically check files before each commit and block commits containing potential secrets.

See the [pre-commit hooks documentation](https://pre-commit.com/hooks.html) for more secret scanning options.

> ⚠️ **Note:** To keep your hooks current with the latest versions, periodically run `pre-commit autoupdate`.

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
- Fix Markdown formatting issues
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
- **PR titles must follow Conventional Commits format** (e.g., `feat: add new feature`). This is enforced by an automated check.
- PR description template:

```markdown
## Why?

## What Changed?

## Additional Notes
```

- Ensure all checks pass (pre-commit) before requesting review.
- Reference related issues where applicable.

### PR Title Format

PR titles are validated automatically and must follow this format:

```text
<type>(<optional scope>): <description>
```

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Examples:**

- `feat(auth): add login button to navigation`
- `fix: resolve race condition in async handler`
- `docs: update installation instructions`
- `chore: bump dependencies and run pre-commit`

The description should:

- Start with a lowercase letter
- Be concise and descriptive
- Use imperative mood (e.g., "add" not "added" or "adds")

**Breaking changes:** Add `!` after the type (e.g., `feat!: drop Python 3.10 support`)

If the automated check fails, update your PR title and it will re-run automatically.

## Issue Templates

Use the GitHub issue templates under `.github/ISSUE_TEMPLATE/` for bug reports, feature requests, and questions. These templates prompt for summary, context/repro, and related prompt/workflow information.

## Code of Conduct

We strive to maintain a welcoming and respectful community. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) to understand our community standards and expectations.

If you have any concerns, please contact the Liatrio Maintainers team (`@liatrio-labs/liatrio-labs-maintainers`) or use GitHub's private reporting form for this repository.

## References

- `README.md` — overview and quick start
- `.pre-commit-config.yaml` — linting and formatting hooks
- `.github/ISSUE_TEMPLATE/` — issue forms
