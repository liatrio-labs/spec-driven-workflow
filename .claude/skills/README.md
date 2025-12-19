# Claude Code Skills for Spec-Driven Development

This directory contains Agent Skills for Claude Code that implement the Spec-Driven Development (SDD) workflow.

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

These skills are designed for use with Claude Code. To install:

```bash
# Copy to user skills directory (available in all projects)
mkdir -p ~/.claude/skills
cp -r .claude/skills/* ~/.claude/skills/

# Or copy to project-specific location (available only in this project)
# Skills are already in .claude/skills/ for this project
```

## How Skills Work

Claude Code automatically discovers and can invoke these skills when they're relevant to your workflow. Each skill:

- Contains YAML frontmatter with metadata (name, description, tags)
- Includes detailed instructions and context markers
- Provides workflow integration guidance
- Implements validation and quality checks

## Learn More

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [SDD Workflow Overview](https://github.com/liatrio-labs/spec-driven-workflow)
- [SDD Playbook](https://liatrio-labs.github.io/spec-driven-workflow/)
