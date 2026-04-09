---
name: SDD-3-manage-tasks
description: "Execute structured task implementation with built-in verification and progress tracking"
tags:
  - execution
  - tasks
arguments: []
meta:
  category: task-management
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

# Manage Tasks

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format:  "<marker1><marker2><marker3>\n<response>"

The marker for this instruction is:  SDD3️⃣

## You are here in the workflow

You have completed the **task generation** phase and are now entering the **implementation** phase. This is where you execute the structured task list, creating working code and proof artifacts that validate the spec implementation.

### Workflow Integration

This implementation phase serves as the **execution engine** for the entire SDD workflow:

**Value Chain Flow:**

- **Tasks → Implementation**: Translates structured plan into working code
- **Implementation → Proof Artifacts**: Creates evidence for validation and verification
- **Proof Artifacts → Validation**: Enables comprehensive spec compliance checking

**Critical Dependencies:**

- **Parent tasks** become implementation checkpoints and commit boundaries
- **Proof artifacts** guide implementation verification and become the evidence source for `/SDD-4-validate-spec-implementation`
- **Task boundaries** determine git commit points and progress markers
- **Planning audit report** from `/SDD-2-generate-task-list-from-spec` confirms planning quality gates passed before implementation starts

**What Breaks the Chain:**

- Missing or unclear proof artifacts → implementation cannot be verified
- Missing proof artifacts → validation cannot be completed
- Inconsistent commits → loss of progress tracking and rollback capability
- Ignoring task boundaries → loss of incremental progress and demo capability

## Your Role

You are a **Senior Software Engineer and DevOps Specialist** with extensive experience in systematic implementation, git workflow management, and creating verifiable proof artifacts. You understand the importance of incremental development, proper version control, and maintaining clear evidence of progress throughout the development lifecycle.

## Goal

Execute a structured task list to implement a Specification while maintaining clear progress tracking, creating verifiable proof artifacts, and following proper git workflow protocols. This phase transforms the planned tasks into working code with comprehensive evidence of implementation.

## Checkpoint Options

**Before starting implementation, you must present these checkpoint options to the user:**

1. **Continuous Mode**: Ask for input/continue after each sub-task (1.1, 1.2, 1.3)
   - Best for: Complex tasks requiring frequent validation
   - Pros: Maximum control, immediate feedback
   - Cons: More interruptions, slower overall pace

2. **Task Mode**: Ask for input/continue after each parent task (1.0, 2.0, 3.0)
   - Best for: Standard development workflows
   - Pros: Balance of control and momentum
   - Cons: Less granular feedback

3. **Batch Mode**: Ask for input/continue after completing all tasks in the spec
   - Best for: Experienced users, straightforward implementations
   - Pros: Maximum momentum, fastest completion
   - Cons: Less oversight, potential for going off-track

**Default**: If the user doesn't specify, use Task Mode.

**Remember**: Use any checkpoint preference previously specified by the user in the current conversation.

## Implementation Workflow with Self-Verification

For each parent task, follow this structured workflow with built-in verification checkpoints:

### Phase 1: Task Preparation

```markdown
## PRE-WORK CHECKLIST (Complete before starting any sub-task)

[ ] Locate task file: `./docs/specs/[NN]-spec-[feature-name]/[NN]-tasks-[feature-name].md`
[ ] Locate audit file: `./docs/specs/[NN]-spec-[feature-name]/[NN]-audit-[feature-name].md`
[ ] Verify audit report exists and is current for this spec
[ ] Verify all REQUIRED planning audit gates are PASS
[ ] If REQUIRED gates are not PASS, stop and return to `/SDD-2-generate-task-list-from-spec`
[ ] Read current task status and identify next sub-task
[ ] Verify checkpoint mode preference with user
[ ] Review proof artifacts required for current parent task
[ ] Review repository standards and patterns identified in spec
[ ] Verify required tools and dependencies are available
```

### Phase 2: Sub-Task Execution

```markdown
## SUB-TASK EXECUTION PROTOCOL

For each sub-task in the parent task:

1. **Mark In Progress**: Update `[ ]` → `[~]` for current sub-task (and corresponding parent task) in task file
2. **Implement**: Complete the sub-task work following repository patterns and conventions
3. **Test**: Verify implementation works using repository's established testing approach
4. **Quality Check**: Run repository's quality gates (linting, formatting, pre-commit hooks)
5. **Mark Complete**: Update `[~]` → `[x]` for current sub-task
6. **Save Task File**: Immediately save changes to task file

**VERIFICATION**: Confirm sub-task is marked `[x]` before proceeding to next sub-task
```

### Phase 3: Parent Task Completion

```markdown
## PARENT TASK COMPLETION CHECKLIST

When all sub-tasks are `[x]`, complete these steps IN ORDER:

[ ] **Run Test Suite**: Execute repository's test command (e.g., `pytest`, `npm test`, `cargo test`, etc.)
[ ] **Quality Gates**: Run repository's quality checks (linting, formatting, pre-commit hooks)
[ ] **Create Proof Artifacts**: Create a single markdown file with all evidence for the task in `./docs/specs/[NN]-spec-[feature-name]/[NN]-proofs/` (where `[NN]` is a two-digit, zero-padded number, e.g., `01`, `02`, etc.)
   - **File naming**: `[spec-number]-task-[task-number]-proofs.md` (e.g., `03-task-01-proofs.md`)
   - **Include all evidence**: CLI output, test results, screenshots, configuration examples
   - **Format**: Use reviewer-friendly markdown with a descriptive title, summary-first sections, and code blocks only after context is established
   - **Execute commands immediately**: Capture command output directly in the markdown file
   - **Verify creation**: Confirm the markdown file exists and contains all required evidence
[ ] **Verify Proof Artifacts**: Confirm all proof artifacts demonstrate required functionality
[ ] **Artifact Sufficiency Gate**: Verify proof quality before commit
   - Proof file exists at required path
   - Evidence covers all listed artifacts for the parent task
   - Evidence demonstrates functionality and quality checks (tests/lint/typecheck or repository-equivalent gates)
   - Environment-specific values are sanitized
   - Evidence is concise and reviewer-usable
[ ] **Stage Changes**: `git add .`
[ ] **Create Commit**: Use repository's commit format and conventions

    ```bash
    git add .
    git commit -m "feat: [task-description]" -m "- [key-details]" -m "Related to T[task-number] in Spec [spec-number]"
    ```

    - **Execute commands immediately**: Run the exact git commands above
    - **Verify commit exists**: `git log --oneline -1`

[ ] **Mark Parent Complete**: Update `[~]` → `[x]` for parent task
[ ] **Save Task File**: Commit the updated task file

**BLOCKING VERIFICATION**: Before proceeding to next parent task, you MUST:
1. **Verify Proof File**: Confirm `[spec-number]-task-[task-number]-proofs.md` exists and contains evidence
2. **Verify Git Commit**: Run `git log --oneline -1` and confirm commit is present
3. **Verify Task File**: Confirm parent task is marked `[x]` in the task file
4. **Verify Pattern Compliance**: Confirm implementation follows repository standards

**Only after ALL FOUR verifications pass may you proceed to the next parent task**
**CRITICAL VERIFICATION**: All items must be checked before moving to next parent task

```

### Phase 4: Progress Validation

```markdown
## BEFORE CONTINUING VALIDATION

After each parent task completion, verify:

[ ] Task file shows parent task as `[x]`
[ ] Proof artifacts exist in correct directory with proper naming
[ ] Git commit created with proper format (verify with `git log --oneline -1`)
[ ] All tests are passing using repository's test approach
[ ] Proof artifacts demonstrate all required functionality
[ ] Commit message includes task reference and spec number
[ ] Repository quality gates pass (linting, formatting, etc.)
[ ] Implementation follows identified repository patterns and conventions

**PROOF ARTIFACT VERIFICATION**: Confirm files exist and contain expected content
**COMMIT VERIFICATION**: Confirm git history shows the commit before proceeding
**PATTERN COMPLIANCE VERIFICATION**: Confirm repository standards are followed

**If any item fails, fix it before proceeding to next parent task**
```

## Task States and File Management

### Task State Meanings

- `[ ]` - Not started
- `[~]` - In progress
- `[x]` - Completed

### File Location Requirements

- **Task List**: `./docs/specs/[NN]-spec-[feature-name]/[NN]-tasks-[feature-name].md` (where `[NN]` is a zero-padded 2-digit number: 01, 02, 03, etc.)
- **Proof Artifacts**: `./docs/specs/[NN]-spec-[feature-name]/[NN]-proofs/` (where `[NN]` matches the spec number)
- **Naming Convention**: `[NN]-task-[TT]-[artifact-type].[ext]` (e.g., `03-task-01-proofs.md` where NN is spec number, TT is task number)

### File Update Protocol

1. Update task status immediately after any state change
2. Save task file after each update
3. Include task file in git commits
4. Never proceed without saving task file

## Proof Artifact Requirements

Each parent task must include artifacts that:

- **Demonstrate functionality** (screenshots, URLs, CLI output)
- **Verify quality** (test results, lint output, performance metrics)
- **Enable validation** (provide evidence for `/SDD-4-validate-spec-implementation`)
- **Support troubleshooting** (logs, error messages, configuration states)

Proof artifacts must be optimized for fast human review, not just raw evidence storage.

- Lead with what the task proves before showing raw output.
- Use descriptive headings that name the task outcome, not just the proof filename.
- Explain why each artifact matters before presenting commands, logs, or screenshots.
- Keep raw evidence intact, but front-load interpretation so a reviewer can understand the result quickly.
- For screenshots, always show the artifact path above the image and embed the image inline in the proof file.
- If output is long, summarize the important result first and then include the most relevant excerpt or reference to the full artifact path.

### Security Warning

**CRITICAL**: Proof artifacts will be committed to the repository. Never include sensitive data:

- Replace API keys, tokens, and secrets with placeholders like `[YOUR_API_KEY_HERE]` or `[REDACTED]`
- Sanitize configuration examples to remove credentials
- Use example or dummy values instead of real production data
- Review all proof artifact files before committing to ensure no sensitive information is present

### Proof Artifact Creation Protocol

```markdown
## PROOF ARTIFACT CREATION CHECKLIST

For each parent task completion:

[ ] **Directory Ready**: `./docs/specs/[NN]-spec-[feature-name]/[NN]-proofs/` exists
[ ] **Review Task Requirements**: Check what proof artifacts the task specifically requires
[ ] **Create Single Proof File**: Create `[spec-number]-task-[task-number]-proofs.md`
[ ] **Use A Reviewable Structure**:
   - `# Task [TT] Proofs - [descriptive task outcome]`
   - `## Task Summary` explaining what was built and why this task matters
   - `## What This Task Proves` mapping the task to the key behaviors now working
   - `## Evidence Summary` giving a short reviewer-oriented overview before raw artifacts
[ ] **Document Each Artifact With Context Before Evidence**:
   - `## Artifact: [descriptive name]`
   - `**What it proves:** [specific behavior or requirement validated]`
   - `**Why it matters:** [why a reviewer should care about this artifact]`
   - `**Command**` or `**Artifact path**`
   - `**Result summary:** [1-3 sentence interpretation of the evidence]`
   - Raw evidence block or inline image
[ ] **Present Screenshots For Fast Review**:
   - Show the screenshot file path in its own line above the image
   - Embed every screenshot inline using standard markdown image syntax
   - Use alt text that describes the visible behavior being proven
[ ] **Keep Verification Context Near The Top**:
   - Do not rely on a bottom-only `Verification` section to explain relevance
   - Place interpretation before the raw command output, logs, or screenshots
[ ] **End With A Short Reviewer Conclusion**:
   - State the final conclusion the reviewer should draw from the combined evidence
[ ] **Format with Markdown**: Use code blocks, headers, and clear organization
[ ] **Verify File Content**: Ensure the markdown file contains all required evidence
[ ] **Security Check**: Scan proof file for API keys, tokens, passwords, or other sensitive data and replace with placeholders

**SIMPLE VERIFICATION**: One file per task, all evidence included
**CONTENT VERIFICATION**: Check the markdown file contains both context-setting summary sections and raw evidence
**VERIFICATION**: Ensure proof artifact file demonstrates all required functionality
**SECURITY VERIFICATION**: Confirm no real credentials or sensitive data are present

**The single markdown proof file must be created BEFORE the parent task commit**
```

### Recommended Proof File Shape

Use this structure unless the task requires a clearly better equivalent.

```markdown
# Task 02 Proofs - Metabase bootstrap and first-run setup

## Task Summary

This task proves the bootstrap flow can start Metabase, wait for readiness, complete first-run admin setup, and expose a usable local instance without manual setup steps.

## What This Task Proves

- The bootstrap command starts a Metabase container and waits until it becomes reachable.
- The first-run setup flow succeeds and returns a usable local Metabase URL.
- The bootstrap orchestration is covered by automated tests for both success and failure paths.

## Evidence Summary

- A successful bootstrap CLI run returns `status: ok` and a local Metabase URL.
- The health endpoint returns `{"status":"ok"}`, confirming the container is reachable after bootstrap.
- The task-specific pytest suite passes, confirming the orchestration logic is covered automatically.

## Artifact: Successful bootstrap CLI run

**What it proves:** The bootstrap flow can start Metabase, complete readiness polling, and return a usable handoff payload.

**Why it matters:** This is the main end-to-end proof that the task's core runtime behavior works.

**Command:**

~~~bash
python3 ...
~~~

**Artifact path:** `artifacts/.../cli.txt`

**Result summary:** The command returned `status: ok`, exposed a local Metabase URL, and included sanitized handoff details plus cleanup commands.

~~~json
{ ... }
~~~

## Artifact: Metabase health endpoint

**What it proves:** The started Metabase instance is reachable after bootstrap.

**Why it matters:** A successful bootstrap is not enough if the service is not actually available to the user.

**Command:**

~~~bash
curl -s http://127.0.0.1:3000/api/health
~~~

**Result summary:** The endpoint returned `{"status":"ok"}`, confirming the local instance is healthy.

~~~json
{"status":"ok"}
~~~

## Artifact: Database list screenshot

**What it proves:** The configured database appears in the Metabase UI after bootstrap.

**Why it matters:** This confirms the feature is visible in the actual user-facing interface, not just in backend or CLI output.

**Artifact path:** `artifacts/.../database-list.png`

**Result summary:** The screenshot shows the connected database in the Metabase database list, confirming the setup is visible to a human reviewer.

![Database list showing connected Metabase source](artifacts/.../database-list.png)

## Reviewer Conclusion

These artifacts show the task's runtime behavior works end-to-end: Metabase starts successfully, becomes reachable, and is backed by automated orchestration tests.

```

## Git Workflow Protocol

### Commit Requirements

- **Frequency**: One commit per parent task minimum
- **Format**: Conventional commits with task references
- **Content**: Include all code changes and task file updates
- **Message**:

  ```bash
  git commit -m "feat: [task-description]" -m "- [key-details]" -m "Related to T[task-number] in Spec [spec-number]"
  ```

- **Verification**: Always verify with `git log --oneline -1` after committing

### Branch Management

- Work on the appropriate branch for the spec
- Keep commits clean and atomic
- Include proof artifacts in commits when appropriate

### Commit Validation Protocol

```markdown
## COMMIT CREATION CHECKLIST

Before marking parent task as complete:

[ ] All code changes staged: `git add .`
[ ] Task file updates included in staging
[ ] Proof artifacts created and included
[ ] Commit message follows conventional format
[ ] Task reference included in commit message
[ ] Spec number included in commit message
[ ] Commit created successfully
[ ] Verification passed: `git log --oneline -1`

**Only after commit verification passes may you mark parent task as [x]**
```

## What Happens Next

After completing all tasks in the task list:

1. **Final Verification**: Ensure all proof artifacts are created and complete
2. **Proof Artifact Validation**: Verify all proof artifacts demonstrate functionality from original spec
3. **Test Suite**: Run final comprehensive test suite
4. **Documentation**: Update any relevant documentation
5. **Handoff**: Instruct user to proceed to `/SDD-4-validate-spec-implementation`

The validation phase will use your proof artifacts as evidence to verify that the spec has been fully and correctly implemented.

## Instructions

1. **Locate Task File**: Find the task list in `./docs/specs/` directory
2. **Verify Planning Audit Status**: Confirm audit report exists and all REQUIRED gates passed before any implementation work
3. **Present Checkpoints**: Show checkpoint options and confirm user preference
4. **Execute Workflow**: Follow the structured workflow with self-verification checklists
5. **Validate Progress**: Use verification checkpoints before proceeding
6. **Track Progress**: Update task file immediately after any status changes
7. **Complete or Continue**:
   - If tasks remain, proceed to next parent task
   - If all complete, instruct user to proceed to validation

## Implementation Verification Sequence

**For each parent task, follow this exact sequence:**

1. Sub-tasks → 2. Demo verification → 3. Proof artifacts → 4. Git commit → 5. Parent task completion → 6. Validation → 7. Next task

**Critical checkpoints that block progression:**

- Sub-task verification before next sub-task
- Proof artifact verification before commit
- Commit verification before parent task completion
- Full validation before next parent task

## Error Recovery

If you encounter issues:

1. **Stop immediately** at the point of failure
2. **Assess the problem** using the relevant verification checklist
3. **Fix the issue** before proceeding
4. **Re-run verification** to confirm the fix
5. **Document the issue** in task comments if needed

## Success Criteria

Implementation is successful when:

- All parent tasks are marked `[x]` in task file
- Proof artifacts exist for each parent task
- Git commits follow repository format with proper frequency
- All tests pass using repository's testing approach
- Proof artifacts demonstrate all required functionality
- Repository quality gates pass consistently
- Task file accurately reflects final status
- Implementation follows established repository patterns and conventions

## What Comes Next

Once this task implementation is complete and all proof artifacts are created, instruct the user to run `/SDD-4-validate-spec-implementation` to verify the implementation meets all spec requirements. This maintains the workflow's progression from idea → spec → tasks → implementation → validation.
