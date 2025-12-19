# GitHub Copilot Skills for Spec-Driven Development

This directory contains Agent Skills for GitHub Copilot that implement the Spec-Driven Development (SDD) workflow.

## Available Skills

### sdd-1-generate-spec

Generate a comprehensive specification for a feature with workflow guidance and scope validation.

**When to use:** Starting a new feature or enhancement; need to transform an initial idea into a structured specification.

### sdd-2-generate-task-list

Convert a specification into an actionable task list with demoable units and detailed subtasks.

**When to use:** After creating a specification; need to break down the work into implementable tasks.

### sdd-3-manage-tasks

Execute structured task implementation with built-in verification and progress tracking.

**When to use:** During implementation; need guided execution with checkpoints and proof artifacts.

### sdd-4-validate-implementation

Validate implementation against the specification using proof artifacts and evidence-based coverage.

**When to use:** After completing implementation; need to verify all requirements are met before shipping.

## Installation

These skills are automatically available when you use this repository with GitHub Copilot.

**To use in your own projects:**

```bash
# From the spec-driven-workflow repository root, copy skills to your project
mkdir -p /path/to/your/project/.github
cp -r .github/skills /path/to/your/project/.github/

# Or add to organization-wide skills
# Place in {org}/.github/skills/ or {org}/.github-private/skills/
```

## How Skills Work

GitHub Copilot agents automatically discover and can invoke these skills when they're relevant to your workflow. Each skill:

- Contains YAML frontmatter with metadata (name, description, tags)
- Includes detailed instructions and context markers
- Provides workflow integration guidance
- Implements validation and quality checks

Skills are accessible in:

- VS Code with GitHub Copilot
- Agent HQ for multi-agent orchestration
- GitHub Copilot CLI
- Coding agent workflows

## Learn More

- [GitHub Copilot Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [SDD Workflow Overview](https://github.com/liatrio-labs/spec-driven-workflow)
- [SDD Playbook](https://liatrio-labs.github.io/spec-driven-workflow/)
