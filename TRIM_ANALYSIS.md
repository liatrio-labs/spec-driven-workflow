# Repository Trim Analysis

## Overview

This repository should be trimmed to focus solely on the prompts and workflow documentation. The Python utility (`slash_commands/`) and MCP server (`mcp_server/`, `server.py`) have been extracted to another repository.

## What Should STAY

### Core Content

- ✅ **`prompts/`** - All prompt files (the core content)
  - `generate-spec.md`
  - `generate-task-list-from-spec.md`
  - `manage-tasks.md`
  - `validate-spec-implementation.md`

### Documentation

- ✅ **`README.md`** - Needs updating to remove MCP/server references, but keep workflow documentation
- ✅ **`LICENSE`** - Keep
- ✅ **`CHANGELOG.md`** - Keep for historical reference
- ✅ **`misc/header.png`** - Keep if referenced in README

### Optional (Consider Keeping)

- ⚠️ **`docs/archive/`** - Historical documentation, might be useful
- ⚠️ **`docs/workspace-examples/`** - Examples might be useful
- ⚠️ **`tasks/`** - Example specs/tasks could serve as documentation examples
- ⚠️ **`.markdownlint.yaml`** - Useful for maintaining markdown quality

## What Should be REMOVED

### Python Utility Code

- ❌ **`slash_commands/`** - Entire directory (extracted to another repo)
- ❌ **`mcp_server/`** - Entire directory (extracted to another repo)
- ❌ **`server.py`** - MCP server entrypoint (extracted)
- ❌ **`__version__.py`** - Version management for Python package
- ❌ **`pyproject.toml`** - Python package configuration (or heavily simplified if keeping minimal tooling)
- ❌ **`uv.lock`** - Dependency lock file
- ❌ **`tests/`** - Test suite for Python utilities
- ❌ **`dist/`** - Python package build artifacts
- ❌ **`htmlcov/`** - Test coverage HTML reports
- ❌ **`coverage.xml`** - Test coverage data
- ❌ **`__pycache__/`** - Python bytecode cache directories

### Utility-Specific Documentation

- ❌ **`docs/operations.md`** - MCP server operations guide
- ❌ **`docs/slash-command-generator.md`** - Slash command generator documentation
- ⚠️ **`docs/mcp-prompt-support.md`** - MCP prompt support matrix (consider keeping if useful for users, but update to note utilities are elsewhere)

### Development Configuration

- ❌ **`.pre-commit-config.yaml`** - Pre-commit hooks (includes Python linting/tests, not needed without Python code)
- ❌ **`CONTRIBUTING.md`** - Needs complete rewrite to remove Python dev setup
- ❌ **`.github/workflows/ci.yml`** - CI workflow that runs Python tests and linting
- ❌ **`.github/workflows/release.yml`** - Semantic release workflow for Python package
- ⚠️ **`.github/workflows/claude.yml`** - AI assistant integration (Claude Code) for issues/PRs - **Keep if you want AI help on this repo, remove if not needed**
- ⚠️ **`.github/workflows/opencode-gpt-5-codex.yml`** - AI assistant integration (OpenCode) for issues/PRs - **Keep if you want AI help on this repo, remove if not needed**
- ⚠️ **`.github/chainguard/`** - Check if this is related to Python package security
- ✅ **`.github/ISSUE_TEMPLATE/`** - Keep (useful for prompt/workflow issues)
- ✅ **`.github/pull_request_template.md`** - Keep (useful for contributions)

### Temporary/Output Directories

- ❌ **`temp/`** - Temporary files directory
- ❌ **`output/`** - Output directory
- ❌ **`scripts/`** - Empty scripts directory
- ⚠️ **`prompt_evals/`** - Evaluation files (consider removing unless they're useful documentation)

## Potential Gaps / Things to Consider

### 1. README Updates Needed

The README currently contains:

- Installation instructions for Python utilities (`uv sync`, `uvx sdd-generate-commands`)
- MCP server setup and usage instructions
- References to `docs/operations.md` and `docs/slash-command-generator.md`

**Action Required**: Update README to focus on:

- How to use the prompts directly (copy-paste method)
- Workflow overview
- Links to the other repository for utilities (if applicable)

### 2. Documentation Structure

Consider creating a simple `docs/USAGE.md` or updating README with:

- How to use prompts in different AI tools
- Workflow examples
- Best practices

### 3. Version Management

If removing `pyproject.toml` and `__version__.py`, consider:

- How to track prompt versions?
- Should there be a simple version file or tag-based versioning?

### 4. CI/CD

- Check for `.github/workflows/` - if it exists, update or remove CI that tests Python code
- Keep only workflows that validate markdown/docs if any

### 5. Package Metadata

If completely removing Python packaging:

- Consider a simple `package.json` or `package.yaml` for metadata?
- Or just rely on git tags and README for versioning

### 6. Example Content

- `tasks/` directory contains example specs/tasks - these could be valuable as documentation examples
- Consider moving to `docs/examples/` or keeping in `tasks/` as examples

### 7. Archive Content

- `docs/archive/` might contain useful historical context
- Consider keeping if it documents workflow evolution

## Recommended Cleanup Steps

1. **Remove Python code directories**

   ```bash
   rm -rf slash_commands/ mcp_server/ __pycache__/
   rm server.py __version__.py
   ```

2. **Remove build/test artifacts**

   ```bash
   rm -rf dist/ htmlcov/ tests/ __pycache__/
   rm coverage.xml uv.lock
   ```

3. **Remove utility-specific docs**

   ```bash
   rm docs/operations.md docs/slash-command-generator.md
   ```

4. **Remove temporary directories**

   ```bash
   rm -rf temp/ output/ scripts/
   ```

5. **Update configuration files**
   - Remove or simplify `pyproject.toml` (or remove entirely)
   - Remove `.pre-commit-config.yaml` (or keep minimal markdown linting)
   - Update `CONTRIBUTING.md` to remove Python dev setup

6. **Update README**
   - Remove installation instructions for utilities
   - Remove MCP server references
   - Add note about utilities being in separate repository
   - Focus on prompt usage and workflow

7. **Consider keeping**
   - `.markdownlint.yaml` for markdown quality
   - `tasks/` as examples (or move to `docs/examples/`)
   - `docs/archive/` if historically valuable

## Questions to Answer

1. **Where are the utilities now?** Should README link to the new repository?
   1. ***The utility for downloading and installing the prompts is in /home/damien/Liatrio/repos/slash-command-manager - find the github link for it and add a note to the README linking to it. Note should be near the top.
2. **Versioning strategy?** How should prompt versions be tracked without Python packaging?
   1. ***Workflow will stay versioned, but the versioning process needs to be updated to mirror the process used/outlined in /home/damien/Liatrio/repos/open-source-template.
3. **CI/CD?** Should there be any CI for markdown validation or just manual?
   - Current CI runs Python tests - needs to be removed or replaced with markdown linting
   - Semantic release workflow won't work without Python package - needs removal or alternative
   - ***Update CI to run markdown linters. Maybe just needs to run the pre-commit checks? do some research
4. **Examples?** Keep `tasks/` as examples or move/remove?
   1. ***Remove
5. **Archive?** Keep `docs/archive/` for historical reference?
   1. ***Remove
6. **Other workflows?** `.github/workflows/claude.yml` and `opencode-gpt-5-codex.yml` are AI assistant integrations for issues/PRs - keep if you want AI help on this repo
   1. ***Remove
7. **Pre-commit?** Keep minimal markdown linting or remove entirely?
   1. *** Keep miminal

### Additional Notes

Do not remove /temp - that has WIP notes and stuff that I need, it's gitignored anyway.
