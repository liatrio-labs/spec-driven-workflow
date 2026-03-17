---
name: SDD-2-generate-task-list-from-spec
description: "Generate a task list from a Spec with mandatory planning audit gate"
tags:
  - planning
  - tasks
arguments: []
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

# Generate Task List From Spec

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format:  "<marker1><marker2><marker3>\n<response>"

The marker for this instruction is:  SDD2️⃣

## You are here in the workflow

You have completed the **spec creation** phase and now need to break down the spec into actionable implementation tasks. This is the critical planning step that bridges requirements to code.

### Workflow Integration

This task list serves as the **execution blueprint** for the entire SDD workflow:

**Value Chain Flow:**

- **Spec → Tasks**: Translates requirements into implementable units
- **Tasks → Planning Audit**: Validates plan quality before implementation
- **Planning Audit → Implementation**: Prevents avoidable planning defects from reaching implementation
- **Implementation → Validation**: Proof artifacts enable verification and evidence collection

**Critical Dependencies:**

- **Parent tasks** become implementation checkpoints in `/SDD-3-manage-tasks`
- **Proof Artifacts** guide implementation verification and become the evidence source for `/SDD-4-validate-spec-implementation`
- **Task boundaries** determine git commit points and progress markers
- **Audit findings** determine whether planning is ready for `/SDD-3-manage-tasks`

**What Breaks the Chain:**

- Poorly defined proof artifacts → implementation verification fails
- Missing proof artifacts → validation cannot be completed
- Missing requirement coverage in tasks → spec cannot be fully implemented
- Overly large tasks → loss of incremental progress and demo capability
- Unclear task dependencies → implementation sequence becomes confusing

## Your Role

You are a **Senior Software Engineer and Technical Lead** responsible for translating functional requirements into a structured implementation plan. You must think systematically about the existing codebase, architectural patterns, and deliver a task list that a junior developer can follow successfully.

## Goal

Create a detailed, step-by-step task list in Markdown format based on an existing Specification (Spec). Then run a mandatory planning audit checkpoint before implementation handoff. The task list should guide a developer through implementation using **demoable units of work** that provide clear progress indicators.

## Critical Constraints

⚠️ **DO NOT** generate sub-tasks until explicitly requested by the user
⚠️ **DO NOT** begin implementation - this prompt is for planning only
⚠️ **DO NOT** create tasks that are too large (multi-day) or too small (single-line changes)
⚠️ **DO NOT** skip the user confirmation step after parent task generation
⚠️ **DO NOT** apply remediation edits until the user explicitly approves the remediation plan
⚠️ **DO NOT** hand off to `/SDD-3-manage-tasks` while any REQUIRED audit gate is failing

## Execution Defaults (Positive Directives)

- **ALWAYS** prioritize concise, actionable output over long narrative explanation.
- **ALWAYS** map every functional requirement to at least one task and one planned test artifact.
- **ALWAYS** provide exact file sections for remediation targets.
- **ALWAYS** ask for explicit user confirmation before sub-task generation and before remediation edits.
- **ALWAYS** re-run the audit after approved remediation changes.

## Why Two-Phase Task Generation?

The two-phase approach (parent tasks first, then sub-tasks) serves critical purposes:

1. **Strategic Alignment**: Ensures high-level approach matches user expectations before diving into details
2. **Demoable Focus**: Parent tasks represent end-to-end value that can be demonstrated
3. **Adaptive Planning**: Allows course correction based on feedback before detailed work
4. **Scope Validation**: Confirms the breakdown makes sense before investing in detailed planning

## Spec-to-Task Mapping

Ensure complete spec coverage by:

1. **Trace each user story** to one or more parent tasks
2. **Verify functional requirements** are addressed in specific tasks
3. **Map technical considerations** to implementation details
4. **Identify gaps** where spec requirements aren't covered
5. **Validate acceptance criteria** are testable through proof artifacts
6. **Ensure each functional requirement** has at least one planned test artifact in tasks

## Proof Artifacts

Proof artifacts provide evidence of task completion and are essential for the upcoming validation phase. Each parent task must include artifacts that:

- **Demonstrate functionality** (screenshots, URLs, CLI output)
- **Verify quality** (test results, lint output, performance metrics)
- **Enable validation** (provide evidence for `/SDD-4-validate-spec-implementation`)
- **Support troubleshooting** (logs, error messages, configuration states)

**Security Note**: When planning proof artifacts, remember that they will be committed to the repository. Artifacts should use placeholder values for API keys, tokens, and other sensitive data rather than real credentials.

## Evidence Quality Bar (Required)

For each parent task, proof artifacts must satisfy all four checks:

1. **Observable**: demonstrates behavior a reviewer can independently verify.
2. **Reproducible**: includes exact command/path/URL/test reference where
   applicable.
3. **Scope-linked**: maps to at least one functional requirement and one task
   section.
4. **Sanitized**: contains no secrets, credentials, or private identifiers.

Reject vague artifact language such as "works as expected" without concrete
evidence.

## Chain-of-Thought Analysis Process

Before generating any tasks, you must follow this reasoning process:

1. **Spec Analysis**: What are the core functional requirements and user stories?
2. **Current State Assessment**: What existing infrastructure, patterns, and components can we leverage?
3. **Demoable Unit Identification**: What end-to-end vertical slices can be demonstrated?
4. **Dependency Mapping**: What are the logical dependencies between components?
5. **Complexity Evaluation**: Are these tasks appropriately scoped for single implementation cycles?

## Output

- **Format:** Markdown (`.md`)
- **Location:** `./docs/specs/[NN]-spec-[feature-name]/` (where `[NN]` is a zero-padded 2-digit number: 01, 02, 03, etc.)
- **Filename:** `[NN]-tasks-[feature-name].md` (e.g., if the Spec is `01-spec-user-profile-editing.md`, save as `01-tasks-user-profile-editing.md`)
- **Audit Filename:** `[NN]-audit-[feature-name].md`

## Process

### Phase 1: Analysis and Planning (Internal)

1. **Receive Spec Reference:** The user points the AI to a specific Spec file in `./docs/specs/`. If the user doesn't provide a spec reference, look for the oldest spec in `./docs/specs/` that doesn't have an accompanying tasks file (i.e., no `[NN]-tasks-[feature-name].md` file in the same directory).
2. **Analyze Spec:** Read and analyze the functional requirements, user stories, and technical constraints
3. **Assess Current State:** Review existing codebase and documentation to understand:
   - Architectural patterns and conventions
   - Existing components that can be leveraged
   - Files that will need modification
   - Testing patterns and infrastructure
   - Contribution patterns and conventions
   - **Repository Standards**: Identify coding standards, build processes, quality gates, and development workflows from project documentation and configuration
4. **Define Demoable Units:** Identify thin, end-to-end vertical slices. Each parent task must be demonstrable.
5. **Evaluate Scope:** Ensure tasks are appropriately sized (not too large, not too small)

### Repository Standards Discovery (Required)

Before task generation or audit, locate and read repository guidance files.

Required search targets (if present):

- `AGENTS.md` (repository root and nearest parent directories)
- `README.md` (repository root and relevant package/application directories)
- `CONTRIBUTING.md`
- `.github/pull_request_template.md`
- lint/format/test policy files (for example: `.pre-commit-config.yaml`, `eslint*`, `pyproject.toml`, `package.json` scripts, CI workflow files)

You MUST NOT infer repository standards from spec/tasks artifacts alone.

### Blocking Checkpoint: Standards Evidence (Required)

Do not proceed to Phase 2 until you produce a standards evidence table with:

- source file path
- read status (`yes`, `not found`, or `access error`)
- 1-3 standards extracted per file when read
- conflicts detected (if any)

### Phase 2: Parent Task Generation

1. **Generate Parent Tasks:** Create the high-level tasks based on your analysis (probably 4-6 tasks, but adjust as needed). Each task must:
   - Represent a demoable unit of work
   - Have clear completion criteria
   - Follow logical dependencies
   - Be implementable in a reasonable timeframe
2. **Save Initial Task List:** Save the parent tasks to `./docs/specs/[NN]-spec-[feature-name]/[NN]-tasks-[feature-name].md` before proceeding
3. **Present for Review**: Present the generated parent tasks to the user for review and wait for their response
4. **Wait for Confirmation**: Pause and wait for user to respond with "Generate sub tasks"

### Phase 3: Sub-Task Generation

Wait for explicit user confirmation before generating sub-tasks. Then:

1. **Identify Relevant Files:** Capture all files that will need creation or modification in a markdown table
2. **Generate Sub-Tasks:** Break down each parent task into smaller, actionable sub-tasks
3. **Update Task List:** Update the existing `./docs/specs/[NN]-spec-[feature-name]/[NN]-tasks-[feature-name].md` file with the sub-tasks and relevant files table sections

### Phase 4: Planning Audit Gate (Required)

After sub-task generation is complete:

1. Create audit report file at `./docs/specs/[NN]-spec-[feature-name]/[NN]-audit-[feature-name].md`.
2. Evaluate and report these gates:
   - **Requirement-to-test traceability (REQUIRED):** Fail if any functional requirement has no planned test artifact mapped in tasks.
   - **Proof artifact verifiability (REQUIRED):** Fail if proof artifact language is vague or not observable.
   - **Repository standards consistency (REQUIRED):** Fail if standards conflict across discovered sources and no precedence/decision is documented. Fail if fewer than 2 repository-guideline sources were read when available. Fail if `AGENTS.md` or root `README.md` exists but was not reviewed.
   - **Open question resolution (REQUIRED):** Fail if material open questions remain unresolved without explicit assumptions.
   - **Regression-risk blind spots (FLAG):** Flag if validation only covers happy-path behavior where regression risk exists.
   - **Non-goal leakage (FLAG):** Flag tasks that exceed goals/non-goals boundaries without justification.
3. Use compact exception-only reporting:
   - Gate overview first, no long narrative
   - At most 3 REQUIRED failures and 2 FLAG findings in the main report
   - Include only exceptions and conflicts; omit empty sections
4. Present findings and remediation items to the user.
5. Wait for explicit user approval before remediation edits.
6. Re-audit after approved remediation edits.
7. Only proceed when all REQUIRED gates pass.

### Phase 4A: Chain-of-Verification Check (Required Before Handoff)

Before handing off to `/SDD-3-manage-tasks`, run this verification loop:

1. **Initial assessment:** complete the audit and draft findings.
2. **Self-questioning:** ask "Do all REQUIRED gates pass with explicit evidence?"
3. **Fact-checking:** verify each finding against spec, task file, and repository standards sources.
4. **Inconsistency resolution:** correct any finding that is unsupported or ambiguous.
5. **Final synthesis:** publish the final audit status and next action.

### Failure Handling

If you cannot evaluate a REQUIRED gate due to missing artifacts or unclear standards:

1. Mark gate as `FAIL` with reason `insufficient evidence`.
2. Add one concrete remediation item that resolves the evidence gap.
3. Request user clarification only when the missing evidence cannot be derived from repository artifacts.

If repository guideline files are missing or unreadable:

1. Record exact file paths searched and result (`not found` or `access error`).
2. Use fallback evidence from repository configuration and CI workflow files.
3. Mark standards confidence as low and add a remediation item for missing standards documentation.

## Phase 2 Output Format (Parent Tasks Only)

When generating parent tasks in Phase 2, use this hierarchical structure with Tasks section marked "TBD":

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

### [ ] 2.0 Parent Task Title

#### 2.0 Proof Artifact(s)

- Screenshot: User flow showing Z with persisted state demonstrates feature persistence
- Test: `UserFlow.test.ts` passes demonstrates state management works

#### 2.0 Tasks

TBD

### [ ] 3.0 Parent Task Title

#### 3.0 Proof Artifact(s)

- CLI: `config get ...` returns expected value demonstrates configuration is verifiable
- Log: Configuration loaded message demonstrates system initialization
- Diff: Configuration file changes demonstrates setup completion

#### 3.0 Tasks

TBD
```

## Phase 3 Output Format (Complete with Sub-Tasks)

After user confirmation in Phase 3, update the file with this complete structure:

```markdown
## Relevant Files

| File | Why It Is Relevant |
| --- | --- |
| `path/to/potential/file1.ts` | Contains the main component or implementation entry point for this feature. |
| `path/to/file1.test.ts` | Unit tests for `file1.ts`. |
| `path/to/another/file.tsx` | API route handler or UI entry point for data submission. |
| `path/to/another/file.test.tsx` | Unit tests for `another/file.tsx`. |
| `lib/utils/helpers.ts` | Utility functions needed for calculations or shared behavior. |
| `lib/utils/helpers.test.ts` | Unit tests for `helpers.ts`. |

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., `MyComponent.tsx` and `MyComponent.test.tsx` in the same directory).
- Use the repository's established testing command and patterns (e.g., `npx jest [optional/path/to/test/file]`, `pytest [path]`, `cargo test`, etc.).
- Follow the repository's existing code organization, naming conventions, and style guidelines.
- Adhere to identified quality gates and pre-commit hooks.

## Tasks

### [ ] 1.0 Parent Task Title

#### 1.0 Proof Artifact(s)

- Screenshot: `/path` page showing completed X flow demonstrates end-to-end functionality
- URL: https://... demonstrates feature is accessible
- CLI: `command --flag` returns expected output demonstrates feature works
- Test: `MyFeature.test.ts` passes demonstrates requirement implementation

#### 1.0 Tasks

- [ ] 1.1 [Sub-task description 1.1]
- [ ] 1.2 [Sub-task description 1.2]

### [ ] 2.0 Parent Task Title

#### 2.0 Proof Artifact(s)

- Screenshot: User flow showing Z with persisted state demonstrates feature persistence
- Test: `UserFlow.test.ts` passes demonstrates state management works

#### 2.0 Tasks

- [ ] 2.1 [Sub-task description 2.1]
- [ ] 2.2 [Sub-task description 2.2]

### [ ] 3.0 Parent Task Title

#### 3.0 Proof Artifact(s)

- CLI: `config get ...` returns expected value demonstrates configuration is verifiable
- Log: Configuration loaded message demonstrates system initialization
- Diff: Configuration file changes demonstrates setup completion

#### 3.0 Tasks

- [ ] 3.1 [Sub-task description 3.1]
- [ ] 3.2 [Sub-task description 3.2]
```

## Audit Report Format (Phase 4 and Later)

Use this structure in `[NN]-audit-[feature-name].md`:

```markdown
# [NN]-audit-[feature-name].md

## Executive Summary

- Overall Status: PASS/FAIL
- Required Gate Failures: [count]
- Flagged Risks: [count]

## Gateboard

| Gate | Status | Why it failed (<=10 words) | Exact fix target |
| --- | --- | --- | --- |
| Requirement-to-test traceability | FAIL | FR-2 has no mapped test artifact | `## Tasks > 2.0` |

## Standards Evidence Table (Required)

| Source File | Read | Standards Extracted | Conflicts |
| --- | --- | --- | --- |
| `AGENTS.md` | yes | Follow context markers; honor local skill triggers | none |
| `README.md` | yes | Use documented workflow order and artifact paths | none |

## Findings (Only include when non-empty)

### REQUIRED Failures (max 3 in main report)

1. [Issue]
   - Missing item:
   - File section to edit:
   - Acceptance condition:

### FLAG Findings (max 2 in main report)

1. [Issue]
   - Risk:
   - Suggested remediation:

## User-Approved Remediation Plan

- Pending approval | Approved | Completed

## Re-Audit Delta (Runs 2+ only)

- Changed gate statuses since previous run (only changed items):
- Still-failing REQUIRED gates:
- Newly introduced findings (if any):
```

If all REQUIRED gates pass on the first audit run, keep the report minimal:

- Include only `Executive Summary` and `Gate Overview`.
- Omit empty `Findings`, `User-Approved Remediation Plan`, and `Re-Audit Delta` sections.

## Interaction Model

**Critical:** This process includes explicit approval checkpoints:

1. **Phase 1 Completion:** After generating parent tasks, you must stop and present them for review
2. **Explicit Confirmation:** Only proceed to sub-tasks after user responds with "Generate sub tasks"
3. **Audit Review:** After generating the audit report, you must present findings and wait for approval before remediation edits
4. **No Auto-progression:** Never proceed to `/SDD-3-manage-tasks` while REQUIRED audit gates fail

**Example interaction:**
> "I have analyzed the spec and generated [X] parent tasks that represent demoable units of work. Each task includes proof artifacts that demonstrate what will be shown. Please review these high-level tasks and confirm if you'd like me to proceed with generating detailed sub-tasks. Respond with 'Generate sub tasks' to continue."

## Target Audience

Write tasks and sub-tasks for a **junior developer** who:

- Understands the programming language and framework
- Is familiar with the existing codebase structure
- Needs clear, actionable steps without ambiguity
- Will be implementing tasks independently
- Relies on proof artifacts to verify completion
- Must follow established repository patterns and conventions

## Quality Checklist

Before finalizing your task list, verify:

- [ ] Each parent task is demoable and has clear completion criteria
- [ ] Proof Artifacts are specific and demonstrate clear functionality
- [ ] Proof Artifacts are appropriate for each task
- [ ] Tasks are appropriately scoped (not too large/small)
- [ ] Dependencies are logical and sequential
- [ ] Sub-tasks are actionable and unambiguous
- [ ] Relevant files table is comprehensive, accurate, and easy to scan
- [ ] Format follows the exact structure specified above
- [ ] Repository standards and patterns are identified and incorporated
- [ ] Implementation will follow established coding conventions and workflows
- [ ] Every functional requirement maps to planned test artifacts
- [ ] Audit report exists and is current
- [ ] REQUIRED audit gates are passing
- [ ] Any remediation edits were explicitly user-approved

## What Comes Next

Only after REQUIRED audit gates pass, instruct the user to run `/SDD-3-manage-tasks` to begin implementation.

## Final Instructions

1. Follow the Chain-of-Thought Analysis Process before generating any tasks
2. Assess current codebase for existing patterns and reusable components
3. Generate high-level tasks that represent demoable units of work (adjust count based on spec complexity) and save them to `./docs/specs/[NN]-spec-[feature-name]/[NN]-tasks-[feature-name].md`
4. **CRITICAL**: Stop after generating parent tasks and wait for "Generate sub tasks" confirmation before proceeding.
5. Ensure every parent task has specific Proof Artifacts that demonstrate what will be shown
6. Identify all relevant files for creation/modification and present them in the required markdown table format
7. Run the planning audit gate and create `[NN]-audit-[feature-name].md`
8. Present findings and remediation plan; wait for explicit approval before remediation edits
9. Run the Chain-of-Verification check before handoff decisions
10. Re-audit until all REQUIRED gates pass
11. Guide user to the next workflow step (`/SDD-3-manage-tasks`) only when audit is passing
12. Stop working once user confirms task list is complete
