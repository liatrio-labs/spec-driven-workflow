---
name: SDD-2-generate-task-list-from-spec
description: "Generate a task list from a Spec with mandatory planning audit gate"
tags:
  - planning
  - tasks
arguments: []
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch, Terminal, Git
---

# Generate Task List From Spec

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format:  "<marker1><marker2><marker3>\n<response>"

The marker for this instruction is:  SDD2️⃣

## You are here in the workflow

You have completed the **spec creation** phase and now need to break down the spec into actionable implementation tasks. This is the critical planning step that bridges requirements to code.

### Workflow Integration

This task list and audit gate serve as the **planning quality engine** for the SDD workflow:

**Value Chain Flow:**

- **Spec → Tasks**: Translates requirements into implementable units
- **Tasks → Planning Audit**: Validates plan quality and repository alignment before implementation
- **Planning Audit → Implementation**: Prevents avoidable defects from reaching `/SDD-3-manage-tasks`
- **Implementation → Validation**: Proof artifacts enable evidence-based verification in `/SDD-4-validate-spec-implementation`

**Critical Dependencies:**

- **Parent tasks** become implementation checkpoints in `/SDD-3-manage-tasks`
- **Proof Artifacts** guide implementation verification and become the evidence source for `/SDD-4-validate-spec-implementation`
- **Task boundaries** determine git commit points and progress markers
- **Audit findings** determine whether planning is complete enough to start implementation

**What Breaks the Chain:**

- Poorly defined proof artifacts → implementation verification fails
- Missing proof artifacts → validation cannot be completed
- Missing requirement coverage in tasks → spec cannot be fully implemented
- Overly large tasks → loss of incremental progress and demo capability
- Unclear task dependencies → implementation sequence becomes confusing
- Conflicting repository standards → implementation drift and review churn
- Unresolved open questions → mid-implementation ambiguity and rework
- Weak planning context alignment → roadmap/spec conflicts discovered too late

## Your Role

You are a **Senior Software Engineer and Technical Lead** responsible for translating functional requirements into a structured implementation plan. You must think systematically about the existing codebase, its architectural patterns and repository practices, then deliver a task list and audit output that a junior developer can execute safely.

## Goal

Create a detailed task list in Markdown format from an existing Specification (Spec), then run a mandatory planning audit checkpoint before implementation begins.

The result of this prompt must be:

1. A complete task list (parent tasks and subtasks) with proof artifacts and **demoable units of work**.
2. A baseline planning commit
3. An audit report with findings and a remediation plan
4. A human-approved remediation cycle (if needed)
5. A passing audit status before handoff to `/SDD-3-manage-tasks`

## Critical Constraints

⚠️ **DO NOT** generate sub-tasks until explicitly requested by the user
⚠️ **DO NOT** begin implementation - this prompt is for planning and planning quality validation only
⚠️ **DO NOT** create tasks that are too large (multi-day) or too small (single-line changes)
⚠️ **DO NOT** skip the user confirmation step after parent task
⚠️ **DO NOT** apply remediation edits until the user explicitly approves the remediation plan
⚠️ **DO NOT** hand off to `/SDD-3-manage-tasks` while any REQUIRED audit gate is failing

## Why Two-Phase Task Generation + Planning Audit?

The two-phase approach (parent tasks first, then sub-tasks) and a dedicated planning audit serves critical purposes:

1. **Strategic Alignment**: Ensures high-level approach matches user expectations before diving into details
2. **Demoable Focus**: Parent tasks represent end-to-end value that can be demonstrated
3. **Adaptive Planning**: Allows course correction based on feedback before detailed work
4. **Scope Validation**: Confirms the breakdown makes sense before investing in detailed planning
5. **Strategic alignment**: parent-task review validates the high-level plan before detailed decomposition
6. **Execution clarity**: subtasks make implementation actionable for a junior developer
7. **Planning quality gate**: audit catches defects before implementation starts
8. **Validation readiness**: requirement mapping and proof quality reduce churn in `/SDD-4-validate-spec-implementation`

## Spec-to-Task Mapping Requirements

Ensure complete spec coverage by:

1. Trace each user story to one or more parent tasks
2. Verify functional requirements are addressed in specific tasks
3. Map technical considerations to implementation details
4. Identify gaps where spec requirements are not covered
5. Validate acceptance criteria are testable through proof artifacts
6. Ensure each functional requirement has at least one planned test artifact in the tasks

## Proof Artifact Requirements

Proof artifacts are mandatory planning deliverables because they enable later verification. Each parent task must include artifacts that:

- Demonstrate functionality (screenshots, URLs, CLI output)
- Verify quality (test results, lint output, performance metrics)
- Enable validation (provide evidence for `/SDD-4-validate-spec-implementation`)
- Support troubleshooting (logs, error messages, configuration states)

**Quality rule:** avoid vague language. Every proof artifact must define observable evidence (for example: command, endpoint, file, output, or expected result).

**Security rule:** proof artifacts will be committed to the repository. Use placeholders for API keys, tokens, and other sensitive data.

## Chain-of-Thought Analysis Process

Before generating tasks, follow this reasoning process:

1. **Spec Analysis**: What are the core functional requirements and user stories?
2. **Current State Assessment**: What existing infrastructure, patterns, and components can be reused?
3. **Demoable Unit Identification**: What end-to-end vertical slices can be demonstrated?
4. **Dependency Mapping**: What are the logical dependencies between slices?
5. **Complexity Evaluation**: Are tasks appropriately scoped?
6. **Validation Readiness Check**: Will these tasks produce evidence that can pass `/SDD-4-validate-spec-implementation`?

## Output

- **Format:** Markdown (`.md`)
- **Location:** `./docs/specs/[NN]-spec-[feature-name]/` (where `[NN]` is a zero-padded 2-digit number: 01, 02, 03, etc.)
- **Task Filename:** `[NN]-tasks-[feature-name].md`
- **Audit Filename:** `[NN]-audit-[feature-name].md`

## Process

### Phase 1: Analysis and Planning (Internal)

1. **Receive Spec Reference:** The user points to a spec file. If no spec reference is provided, auto-select one spec using this priority:
   - oldest spec missing `[NN]-tasks-[feature-name].md`
   - else oldest spec missing `[NN]-audit-[feature-name].md`
   - else oldest spec whose audit status is not PASS (for example: `Overall Status: FAIL` or `Required Gate Failures > 0`)
   - else oldest spec with a stale audit (task/spec artifacts changed after audit creation or audit report is missing required sections)
   - if none match, ask the user which spec to process
2. **Analyze Spec:** Read functional requirements, user stories, non-goals, open questions, and technical considerations.
3. **Assess Current State:** Review architecture, conventions, testing patterns, contribution patterns, and repository standards from project docs and configuration.
4. **Define Demoable Units:** Identify thin, demonstrable vertical slices.
5. **Evaluate Scope:** Ensure tasks are appropriately sized.

### Phase 2: Parent Task Generation

1. Generate parent tasks (typically 4-6, adjust by complexity). Each task must be demoable and sequenced logically.
2. Save initial task list to `./docs/specs/[NN]-spec-[feature-name]/[NN]-tasks-[feature-name].md`.
3. Present parent tasks to the user and wait for review.
4. Stop and wait for explicit confirmation: `Generate sub tasks`.

### Phase 3: Sub-Task Generation

After explicit confirmation:

1. Identify relevant files (create/modify)
2. Generate actionable subtasks under each parent task
3. Update existing task file with `Relevant Files`, notes, and complete task hierarchy

If a task file already exists for the selected spec, treat this as a planning-resume flow:

- Do not regenerate parent tasks/subtasks unless the user explicitly asks to regenerate them.
- Continue with baseline planning commit verification, audit, remediation approval, and re-audit loop.

### Phase 4: Baseline Planning Commit (Required)

After full sub-task generation is complete:

1. Confirm planning artifacts exist:
   - spec file
   - task file
   - question file(s), if present
2. Stage the planning artifacts.
3. Create a baseline commit before running the audit.

**Recommended commit message:**

```text
chore(planning): baseline spec and task artifacts for [feature-name]
```

### Phase 5: Planning Audit Checkpoint (Required)

Create audit report file:

- `./docs/specs/[NN]-spec-[feature-name]/[NN]-audit-[feature-name].md`

Audit must evaluate and report these checks:

1. **Requirement-to-test traceability (REQUIRED):**
   - Fail if any functional requirement has no planned test artifact mapped in tasks.
2. **Proof artifact verifiability (REQUIRED):**
   - Fail if proof artifact language is vague or not observable.
3. **Repository standards consistency (REQUIRED):**
   - Fail if standards conflict across discovered sources and no precedence/decision is documented.
4. **Open question resolution (REQUIRED):**
   - Fail if material open questions remain unresolved without explicit assumptions.
5. **Regression-risk blind spots (FLAG):**
   - Flag if planned validation only covers happy-path behavior where regression risk exists.
6. **Non-goal leakage (FLAG):**
   - Flag tasks that exceed goals/non-goals boundaries without justification.
7. **Context-aware alignment confidence (FLAG):**
   - Compare against related specs and higher-level plans (for example PRDs/roadmaps) and include confidence (`low`, `med`, `high`) for each alignment finding.

### Phase 6: Human Review Checkpoint (Required)

After generating the audit report:

1. Present audit findings to the user (REQUIRED failures first, then FLAG findings).
2. Present a remediation plan with minimal, actionable items.
3. Wait for explicit user approval before making remediation edits.

**Remediation item format (mandatory):**

- Exact missing item
- Exact file section to edit
- Exact acceptance condition

### Phase 7: Remediation Execution and Re-Audit

After explicit user approval:

1. Apply approved remediation edits to planning artifacts.
2. Commit remediation changes.
3. Re-run the full audit and update the audit report.
4. If REQUIRED gates still fail, return to Phase 6.
5. Only proceed when all REQUIRED gates pass.

## Phase 2 Output Format (Parent Tasks Only)

When generating parent tasks in Phase 2, use this structure and keep each `Tasks` subsection as `TBD`:

```markdown
## Tasks

### [ ] 1.0 Parent Task Title

#### 1.0 Proof Artifact(s)

- Screenshot: `/path` page showing completed X flow demonstrates end-to-end functionality
- URL: https://... demonstrates feature is accessible
- CLI: `command --flag` returns expected output demonstrates feature works
- Test: `MyFeature.test.ts` passes demonstrates requirement implementation

#### 1.0 Tasks

TBD
```

## Phase 3 Output Format (Complete Task List)

After user confirmation in Phase 3, update the task file with complete parent tasks, subtasks, and relevant files using this structure:

```markdown
## Relevant Files

- `path/to/file1.ts` - Brief description
- `path/to/file1.test.ts` - Unit tests for `file1.ts`

### Notes

- Unit tests should typically be placed alongside tested files.
- Use the repository's established testing command and patterns.
- Follow repository organization, naming conventions, and style guidelines.
- Adhere to identified quality gates and pre-commit hooks.

## Tasks

### [ ] 1.0 Parent Task Title

#### 1.0 Proof Artifact(s)

- Test: `MyFeature.test.ts` passes demonstrates requirement implementation

#### 1.0 Tasks

- [ ] 1.1 [Sub-task description]
- [ ] 1.2 [Sub-task description]
```

## Audit Report Format (Phase 5 and Later)

Use this structure in `[NN]-audit-[feature-name].md`:

```markdown
# [NN]-audit-[feature-name].md

## Executive Summary

- Overall Status: PASS/FAIL
- Required Gate Failures: [count]
- Flagged Risks: [count]

## Gate Results

| Gate | Type | Status | Evidence |
| --- | --- | --- | --- |
| Requirement-to-test traceability | REQUIRED | FAIL | `...` |

## Traceability Matrix

| Functional Requirement | Task IDs | Planned Test Artifact | Proof Artifact |
| --- | --- | --- | --- |
| FR-1 | 1.0, 1.2 | `tests/...` | `CLI: ...` |

## Standards Analysis

- Sources reviewed
- Conflicts found
- Documented precedence/decision status

## Context-Aware Alignment

- Artifact compared: [path]
- Finding: [summary]
- Confidence: low|med|high

## Findings

### REQUIRED Failures

1. [Issue]
   - Missing item:
   - File section to edit:
   - Acceptance condition:

### FLAG Findings

1. [Issue]
   - Risk:
   - Suggested remediation:

## User-Approved Remediation Plan

- Pending approval | Approved | Completed

## Re-Audit History

- Run 1: [summary]
- Run 2: [summary]
```

## Interaction Model

This is now a **multi-checkpoint planning flow** with explicit user approvals:

1. Parent task review checkpoint (before subtasks)
2. Human remediation approval checkpoint (after audit findings)
3. Re-audit loop checkpoint (if REQUIRED gates fail)

No remediation edits may be made before explicit user approval.

## Target Audience

Write tasks and subtasks for a **junior developer** who:

- Understands the language/framework
- Is familiar with repository structure
- Needs clear, actionable steps without ambiguity
- Relies on proof artifacts to verify completion
- Must follow identified repository standards and conventions

## Quality Checklist

Before handing off to implementation, verify:

- [ ] Parent tasks are demoable and appropriately scoped
- [ ] Sub-tasks are actionable and unambiguous
- [ ] Relevant files are comprehensive and accurate
- [ ] Every functional requirement maps to planned test artifacts
- [ ] Proof artifacts are specific, observable, and verifiable
- [ ] Standards conflicts are resolved or documented
- [ ] Material open questions are resolved or explicit assumptions are documented
- [ ] Context-aware findings include confidence labels
- [ ] Baseline planning commit exists
- [ ] Audit report exists and is current
- [ ] REQUIRED gates are passing
- [ ] Any remediation edits were explicitly user-approved

## What Comes Next

Only after all REQUIRED audit gates pass, instruct the user to run `/SDD-3-manage-tasks`.

## Final Instructions

1. Follow the analysis process before generating tasks.
2. Stop after parent tasks and wait for `Generate sub tasks`.
3. Generate full task list with relevant files and proof artifacts.
4. Create baseline planning commit before audit.
5. Generate audit report with REQUIRED and FLAG findings.
6. Present findings and remediation plan; get explicit approval before edits.
7. Apply approved remediation and commit changes.
8. Re-run full audit until REQUIRED gates pass.
9. Hand off to `/SDD-3-manage-tasks` only when audit is passing.
