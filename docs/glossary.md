# SDD glossary

This glossary defines install and workflow terms used by the Spec-Driven Development (SDD) project.

## Agent skill

An installable folder of instructions, references, and helper scripts that an AI agent can load as a reusable capability. For SDD, the recommended install is the `sdd` skill from this repository.

## `sdd` skill

The single recommended SDD entry point for skill-capable agents. Users invoke it intentionally, for example with `/sdd`, and the skill inspects `docs/specs/` to choose the right workflow phase.

## Prompt file

A Markdown instruction file under `prompts/`. Prompt files remain available for assistants that do not support skills or for teams that deliberately want separate phase prompts.

## Slash command prompt

A prompt file installed into an agent-specific command directory so it can be selected from an agent chat UI. The older SDD install exposed four separate slash commands: `/SDD-1-generate-spec`, `/SDD-2-generate-task-list-from-spec`, `/SDD-3-manage-tasks`, and `/SDD-4-validate-spec-implementation`.

## Slash Command Manager

The `slash-man` CLI from [`liatrio-labs/slash-command-manager`](https://github.com/liatrio-labs/slash-command-manager). It can install SDD prompt files into supported agent command directories and can clean up generated prompt files with `slash-man cleanup`.

## Skill-first install

The recommended SDD install path for agents that support skills:

```bash
npx skills add liatrio-labs/spec-driven-workflow --skill sdd
```

## Prompt-based install

The fallback install path that downloads `prompts/` and installs them as separate slash commands, usually with `slash-man generate`. Use this only when the target agent does not support skills or when a team specifically wants separate phase commands.

## SDD artifacts

The Markdown files created by SDD in a project repository, usually under `docs/specs/[NN]-spec-[feature-name]/`. These include specs, questions files, task lists, audit reports, proof artifacts, and validation reports.

## Migration guide

Instructions for moving from the prompt-based slash-command install to the skill-first install are in [`MIGRATION.md`](../MIGRATION.md).
