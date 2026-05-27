---
name: sdd
description: "Execute the Liatrio Spec-Driven Development (SDD) workflow when explicitly invoked by the user. NOTE: this skill is NOT intended to be dynamically loaded or automatically triggered; it should only ever be explicitly called by the user."
---

# Spec-Driven Workflow Orchestrator

You are the orchestrator for the Spec-Driven Development (SDD) workflow. Determine the current lifecycle phase from the workspace, then load and follow the single matching phase reference.

## Skill Contract

This skill manages one SDD phase per invocation unless the loaded phase explicitly requires a smaller checkpoint. It must:

1. Assess workspace state before routing.
2. Select exactly one active spec and one phase reference.
3. Load only that phase reference.
4. Execute the phase instructions or stop at a required approval gate.
5. Tell the user the selected spec, detected state, current phase, chosen phase reference path, created or updated artifacts, and next recommended natural-language request.

If multiple active specs exist and the user request does not clearly identify one, ask the user which spec to continue before modifying files. If the selection is unambiguous, state why that spec was selected.

## State Assessment

Before routing, run the bundled assessor script while the current working directory is the target repository/workspace root:

```bash
python3 {{skill_dir}}/scripts/assess-sdd-state.py .
```

`{{skill_dir}}` locates bundled skill assets only; SDD artifacts are assessed from the workspace path argument (`.` in the command above). The script outputs JSON describing active specs and a recommended phase. Use that output as the default source of truth for routing.

Use manual inspection only if the script cannot run. When falling back manually, state that fallback explicitly, inspect `./docs/specs/`, and apply the same phase rules below.

## Phase Rules

- **Phase 1 — Spec Generation**
  - **Condition:** The user requested a new feature, but no matching `[NN]-spec-[feature-name]/` directory exists, or the spec directory exists but the spec document is incomplete or missing.
  - **Action:** Gather context and write the formal specification.

- **Phase 2 — Task List Generation and Audit**
  - **Condition:** `[NN]-spec-[feature-name].md` exists and is complete, but `[NN]-tasks-[feature-name].md` is missing, or the mandatory `[NN]-audit-[feature-name].md` planning audit has not been generated and passed.
  - **Action:** Translate the spec into parent/sub-tasks, define Proof Artifacts, and run the mandatory planning audit gate.

- **Phase 3 — Task Implementation**
  - **Condition:** The spec, task list, and a passing planning audit report all exist, and there are incomplete tasks marked with `[ ]` or `[~]` in the task list.
  - **Action:** Execute the task list, implement the code, and generate the required Proof Artifacts.

- **Phase 4 — Validation**
  - **Condition:** Implementation tasks are marked complete and the user asks to validate the work, or the assessor discovers an active spec where implementation appears finished and validation is missing or failing.
  - **Action:** Evaluate the codebase and Proof Artifacts against the spec requirements using strict pass/fail quality gates.

## Reference Routing

After determining the phase, read only the corresponding bundled reference file:

- **If Phase 1 applies:** `{{skill_dir}}/references/sdd-1-generate-spec.md`
- **If Phase 2 applies:** `{{skill_dir}}/references/sdd-2-generate-task-list-from-spec.md`
- **If Phase 3 applies:** `{{skill_dir}}/references/sdd-3-manage-tasks.md`
- **If Phase 4 applies:** `{{skill_dir}}/references/sdd-4-validate-spec-implementation.md`

Always defer to the detailed instructions, constraints, and anti-patterns in the chosen reference file.

## User-Facing Reporting

When beginning or handing off work, state the phase and selected spec in plain language:

```markdown
Current SDD phase: Phase N — <phase name>
Selected spec: `docs/specs/NN-spec-feature/` (or `none yet — new spec will be created` when no spec exists)
Phase reference: `<chosen bundled phase reference path>`
Detected state: <state summary from assessor or manual fallback>
Selection reason: <why this spec/phase was selected>
```

When a phase creates or updates files, include:

- created or updated artifact paths
- any approval gate reached
- validation or audit outcome, when applicable
- a `How to Continue the SDD Workflow` handoff using this exact spacing pattern:

```markdown
## How to Continue the SDD Workflow

Likely next phase action: <what the skill will do next, or that the current workflow is complete>

To continue the workflow in this chat, reply with:

`<suggested natural-language reply>`

You can also continue in a new chat if you want to keep context lean; the SDD skill will reassess repository state from the persisted concrete artifact set for the current phase, such as spec, task, audit, proof, or validation artifacts.
```

Use a blank line between every distinct part of the handoff: heading, likely next phase action, same-chat instruction, suggested reply, and new-chat option. Suggested replies include:

- `Continue SDD with task planning.`
- `Generate the sub-tasks.`
- `Continue SDD with implementation.`
- `Continue SDD with validation.`
- `Start SDD for a new feature.`

Do not label the handoff as a generic next-request section. Do not put the suggested reply before the likely next phase action. Do not compress the handoff into adjacent lines. Do not refer users to slash-style phase invocations, bundled reference filenames, or direct phase command names for continuation. The skill router reassesses workspace state on the next invocation and loads the correct reference.
