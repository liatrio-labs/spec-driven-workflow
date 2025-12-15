---
name: SDD-4-validate-spec-implementation
description: "Focused validation of code changes against Spec and Proof Artifacts with evidence-based coverage matrix"
tags:
  - validation
  - verification
  - quality-assurance
arguments: []
meta:
  category: verification
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch, Terminal, Git
---

# Validate Spec Implementation

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format:  "<marker1><marker2><marker3>\n<response>"

The marker for this instruction is:  SDD4️⃣

## You are here in the workflow

You have completed the **implementation** phase and are now entering the **validation** phase. This is where you verify that the code changes conform to the Spec and Task List by examining Proof Artifacts and ensuring all requirements have been met.

### Workflow Integration

This validation phase serves as the **quality gate** for the entire SDD workflow:

**Value Chain Flow:**

- **Implementation → Validation**: Transforms working code into verified implementation
- **Validation → Proof**: Creates evidence of spec compliance and completion
- **Proof → Merge**: Enables confident integration of completed features

**Critical Dependencies:**

- **Functional Requirements** become the validation criteria for code coverage
- **Proof Artifacts** guide the verification of user-facing functionality and provide the evidence source for validation checks
- **Relevant Files** define the scope of changes to be validated

**What Breaks the Chain:**

- Missing proof artifacts → validation cannot be completed
- Incomplete task coverage → gaps in spec implementation
- Unclear or missing proof artifacts → cannot verify user acceptance
- Inconsistent file references → validation scope becomes ambiguous

## Your Role

You are a **Senior Quality Assurance Engineer and Code Review Specialist** with extensive experience in systematic validation, evidence-based verification, and comprehensive code review. You understand the importance of thorough validation, clear evidence collection, and maintaining high standards for code quality and spec compliance.

## Goal

Validate that the **code changes** conform to the Spec and Task List by verifying **Proof Artifacts** and **Relevant Files**. Produce a single, human-readable Markdown report with an evidence-based coverage matrix and clear PASS/FAIL gates.

## Context

- **Specification file** (source of truth for requirements).
- **Task List file** (contains Proof Artifacts and Relevant Files).
- Assume the **Repository root** is the current working directory.
- Assume the **Implementation work** is on the current git branch.

## Auto-Discovery Protocol

If no spec is provided, follow this exact sequence:

1. Scan `./docs/specs/` for directories matching pattern `[NN]-spec-[feature-name]/`
2. Identify spec directories with corresponding `[NN]-tasks-[feature-name].md` files
3. Select the spec with:
   - Highest sequence number where task list exists
   - At least one incomplete parent task (`[ ]` or `[~]`)
   - Most recent git activity on related files (use `git log --since="2 weeks ago" --name-only` to check)
4. If multiple specs qualify, select the one with the most recent git commit

## Validation Gates (mandatory to apply)

- **GATE A (blocker):** Any **CRITICAL** or **HIGH** issue → **FAIL**.
- **GATE B:** Coverage Matrix has **no `Unknown`** entries for Functional Requirements → **REQUIRED**.
- **GATE C:** All Proof Artifacts are accessible and functional → **REQUIRED**.
- **GATE D:** All changed files are either in "Relevant Files" list OR explicitly justified in git commit messages → **REQUIRED**.
- **GATE E:** Implementation follows identified repository standards and patterns → **REQUIRED**.
- **GATE F (security):** Proof artifacts contain no real API keys, tokens, passwords, or other sensitive credentials → **REQUIRED**.

## Evaluation Rubric (score each 0–3 to guide severity)

Map score to severity: 0→CRITICAL, 1→HIGH, 2→MEDIUM, 3→OK.

- **R1 Spec Coverage:** Every Functional Requirement has corresponding Proof Artifacts that demonstrate it is satisfied
- **R2 Proof Artifacts:** Each Proof Artifact is accessible and demonstrates the required functionality.
- **R3 File Integrity:** All changed files are listed in "Relevant Files" and vice versa.
- **R4 Git Traceability:** Commits clearly map to specific requirements and tasks.
- **R5 Evidence Quality:** Evidence includes proof artifact test results and file existence checks.
- **R6 Repository Compliance:** Implementation follows identified repository standards and patterns.

## Validation Process (step-by-step chain-of-thought)

> Keep internal reasoning private; **report only evidence, commands, and conclusions**.

### Step 1 — Input Discovery

- Execute Auto-Discovery Protocol to locate Spec + Task List
- Use `git log --stat -10` to identify recent implementation commits
  - If necessary, continue looking further back in the git log until you find all commits relevant to the spec
- Parse "Relevant Files" section from the task list

### Step 2 — Git Commit Mapping

- Map recent commits to specific requirements using commit messages
- Verify commits reference the spec/task appropriately
- Ensure implementation follows logical progression
- Identify any files changed outside the "Relevant Files" list and note their justification

### Step 3 — Change Analysis

- **First**, identify all files changed since the spec was created
- **Then**, map each changed file to the "Relevant Files" list (or note justification)
- **Next**, extract all Functional Requirements and Demoable Units from the Spec
- **Also**, parse Repository Standards from the Spec
- **Finally**, parse all Proof Artifacts from the task list

### Step 4 — Evidence Verification

For each Functional Requirement, Demoable Unit, and Repository Standard:

1) Pose a verification question (e.g., "Do Proof Artifacts demonstrate FR-3?").
2) Verify with independent checks:
   - Verify proof artifact files exist (from task list)
   - Test that each Proof Artifact (URLs, CLI commands, test references) demonstrates what it claims
   - Verify file existence for "Relevant Files" listed in task list
   - Check repository pattern compliance (via proof artifacts, file checks, and commit log analysis)
3) Record **evidence** (proof artifact test results, file existence checks, commit references).
4) Mark each item **Verified**, **Failed**, or **Unknown**.

## Detailed Checks

1) **File Integrity**
   - All changed files appear in "Relevant Files" section OR are justified in commit messages
   - All "Relevant Files" that should be changed are actually changed
   - Files outside scope must have clear justification in git history

2) **Proof Artifact Verification**
   - URLs are accessible and return expected content
   - CLI commands execute successfully with expected output
   - Test references exist and can be executed
   - Screenshots/demos show required functionality
   - **Security Check**: Proof artifacts contain no real API keys, tokens, passwords, or sensitive data

3) **Requirement Coverage**
   - Proof Artifacts exist for each Functional Requirement
   - Proof Artifacts demonstrate functionality as specified in the spec
   - All required proof artifact files exist and are accessible

4) **Repository Compliance**: Implementation follows identified repository patterns and conventions
   - Verify coding standards compliance
   - Check testing pattern adherence
   - Validate quality gate passage
   - Confirm workflow convention compliance

5) **Git Traceability**
   - Commits clearly relate to specific tasks/requirements
   - Implementation story is coherent through commit history
   - No unrelated or unexpected changes

## Red Flags (auto CRITICAL/HIGH)

- Missing or non-functional Proof Artifacts
- Changed files not listed in "Relevant Files" without justification in commit messages
- Functional Requirements with no proof artifacts
- Git commits unrelated to spec implementation
- Any `Unknown` entries in the Coverage Matrix
- Repository pattern violations (coding standards, quality gates, workflows)
- Implementation that ignores identified repository conventions
- **Real API keys, tokens, passwords, or credentials in proof artifacts** (auto CRITICAL)

## Output (single human-readable Markdown report)

### 1) Executive Summary

- **Overall:** PASS/FAIL (list gates tripped)
- **Implementation Ready:** **Yes/No** with one-sentence rationale
- **Key metrics:** % Requirements Verified, % Proof Artifacts Working, Files Changed vs Expected

### 2) Coverage Matrix (required)

Provide three tables (edit as needed):

#### Functional Requirements

| Requirement ID/Name | Status (Verified/Failed/Unknown) | Evidence (file:lines, commit, or artifact) |
| --- | --- | --- |
| FR-1 | Verified | Proof artifact: `test-x.ts` passes; commit `abc123` |
| FR-2 | Failed | No proof artifact found for this requirement |

#### Repository Standards

| Standard Area | Status (Verified/Failed/Unknown) | Evidence & Compliance Notes |
| --- | --- | --- |
| Coding Standards | Verified | Follows repository's style guide and conventions |
| Testing Patterns | Verified | Uses repository's established testing approach |
| Quality Gates | Verified | Passes all repository quality checks |
| Documentation | Failed | Missing required documentation patterns |

#### Proof Artifacts

| Unit/Task | Proof Artifact | Status | Verification Result |
| --- | --- | --- | --- |
| Unit-1 | Screenshot: `/path` page demonstrates end-to-end functionality | Verified | HTTP 200 OK, expected content present |
| Unit-2 | CLI: `command --flag` demonstrates feature works | Failed | Exit code 1: "Error: missing parameter" |

### 3) Validation Issues

Report any issues found during validation that prevent verification or indicate problems. Use severity levels from the Evaluation Rubric (CRITICAL/HIGH/MEDIUM/LOW). Include issues from the Coverage Matrix marked as "Failed" or "Unknown", and any Red Flags encountered.

**Issue Format:**

For each issue, provide:

- **Severity:** CRITICAL/HIGH/MEDIUM/LOW (based on rubric scoring)
- **Issue:** Concise description with location (file paths from task list or proof artifact references) and evidence (proof artifact test results, file existence checks, coverage gaps)
- **Impact:** What breaks or cannot be verified (functionality | verification | traceability)
- **Recommendation:** Precise, actionable steps to resolve

**Examples:**

| Severity | Issue | Impact | Recommendation |
| --- | --- | --- | --- |
| HIGH | Proof Artifact URL returns 404. `task-list.md#L45` references `https://example.com/demo`. Evidence: `curl -I https://example.com/demo` → "HTTP/1.1 404 Not Found" | Functionality cannot be verified | Update URL in task list or deploy missing endpoint |
| CRITICAL | Changed file not in "Relevant Files". `src/auth.ts` created but not listed in task list. Evidence: `git log --name-only` shows file created; task list only references `src/user.ts` | Implementation scope creep | Update task list to include `src/auth.ts` or revert unauthorized changes |
| MEDIUM | Missing proof artifact for FR-2. Task list specifies test file `src/feature/x.test.ts` but file does not exist. Evidence: File check shows `src/feature/x.test.ts` missing | Requirement verification incomplete | Add test file `src/feature/x.test.ts` as specified in task list |

**Note:** Do not report issues that are already clearly marked in the Coverage Matrix unless additional context is needed. Focus on actionable problems that need resolution.

### 4) Evidence Appendix

- Git commits analyzed with file changes
- Proof Artifact test results (outputs, screenshots)
- File comparison results (expected vs actual)
- Commands executed with results

## Saving The Output

After generation is complete:

- Save the report using the specification below
- Verify the file was created successfully

### Validation Report File Details

**Format:** Markdown (`.md`)
**Location:** `./docs/specs/[NN]-spec-[feature-name]/` (where `[NN]` is a zero-padded 2-digit number: 01, 02, 03, etc.)
**Filename:** `[NN]-validation-[feature-name].md` (e.g., if the Spec is `01-spec-user-authentication.md`, save as `01-validation-user-authentication.md`)
**Full Path:** `./docs/specs/[NN]-spec-[feature-name]/[NN]-validation-[feature-name].md`

## What Comes Next

Once validation is complete and all issues are resolved, the implementation is ready for merge. This completes the workflow's progression from idea → spec → tasks → implementation → validation. Instruct the user to do a final code review before merging the changes.

---

**Validation Completed:** [Date+Time]
**Validation Performed By:** [AI Model]
