---
name: validate-spec-implementation-v3
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

# Validate Spec Implementation (v3 — focused evidence-based)

## Goal

Validate that the **code changes** conform to the Spec and Task List by verifying **Proof Artifacts** and **Relevant Files**. Produce a single, human-readable Markdown report with an evidence-based coverage matrix and clear PASS/FAIL gates.

## Context

- **Specification file** (source of truth for requirements).
- **Task List file** (contains Demo Criteria, Proof Artifacts, and Relevant Files).
- Assume the **Repository root** is the current working directory.
- Assume the **Implementation work** is on the current git branch.

## Auto-Discovery Protocol

If no spec is provided, follow this exact sequence:

1. Scan `./docs/specs/` for directories matching pattern `[n]-spec-[feature-name]/`
2. Identify spec directories with corresponding `[n]-tasks-[feature-name].md` files
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

## Evaluation Rubric (score each 0–3 to guide severity)

Map score to severity: 0→CRITICAL, 1→HIGH, 2→MEDIUM, 3→OK.

- **R1 Spec Coverage:** Every Functional Requirement is traceable to code changes.
- **R2 Proof Artifacts:** Each Proof Artifact is accessible and demonstrates the required functionality.
- **R3 File Integrity:** All changed files are listed in "Relevant Files" and vice versa.
- **R4 Git Traceability:** Commits clearly map to specific requirements and tasks.
- **R5 Evidence Quality:** Evidence includes specific file paths, line numbers, and artifact outputs.

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
- **Finally**, parse all Proof Artifacts from the task list

### Step 4 — Evidence Verification

For each Functional Requirement and Demoable Unit:

1) Pose a verification question (e.g., "Is FR-3 implemented in the changed files?").
2) Verify with independent checks:
   - Search changed files for requirement implementation (glob/grep)
   - Test each Proof Artifact (URLs, CLI commands, test references)
   - Verify file content matches requirement specifications
3) Record **evidence** (file paths + line ranges, artifact outputs, commit references).
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

3) **Requirement Implementation**
   - Functional requirements are present in changed code
   - Demo Criteria are satisfied by the implementation
   - Code structure follows spec specifications

4) **Git Traceability**
   - Commits clearly relate to specific tasks/requirements
   - Implementation story is coherent through commit history
   - No unrelated or unexpected changes

## Red Flags (auto CRITICAL/HIGH)

- Missing or non-functional Proof Artifacts
- Changed files not listed in "Relevant Files" without justification in commit messages
- Functional Requirements with no implementation evidence
- Git commits unrelated to spec implementation
- Any `Unknown` entries in the Coverage Matrix

## Output (single human-readable Markdown report)

### 1) Executive Summary

- **Overall:** PASS/FAIL (list gates tripped)
- **Implementation Ready:** **Yes/No** with one-sentence rationale
- **Key metrics:** % Requirements Verified, % Proof Artifacts Working, Files Changed vs Expected

### 2) Coverage Matrix (required)

Provide two tables (edit as needed):

#### Functional Requirements

| Requirement ID/Name | Status (Verified/Failed/Unknown) | Evidence (file:lines, commit, or artifact) |
| --- | --- | --- |
| FR-1 | Verified | `src/feature/x.ts#L10-L58`; commit `abc123` |
| FR-2 | Failed | No implementation found in changed files |

#### Proof Artifacts

| Demo Unit | Proof Artifact | Status | Evidence & Output |
| --- | --- | --- | --- |
| Demo-1 | URL: https://... | Verified | Returns "200 OK" with expected content |
| Demo-2 | CLI: command | Failed | Exit code 1: "Error: missing parameter" |

### 3) Issues (use rubric → severity)

For each issue:

- **Severity:** CRITICAL/HIGH/MEDIUM/LOW
- **What & Where:** concise description + concrete paths/lines
- **Evidence:** minimal diff or command output
- **Root Cause:** spec | task | implementation
- **Impact:** functionality | demo | traceability
- **Recommendation:** precise, actionable steps

> **Few‑shot exemplars**
>
> - *HIGH* — Proof Artifact URL returns 404. Evidence: `curl -I https://example.com/demo` → "HTTP/1.1 404 Not Found". **Impact:** Demo criteria cannot be verified. **Fix:** Update URL or deploy missing endpoint.
> - *CRITICAL* — Changed file `src/auth.ts` not in "Relevant Files". Evidence: `git diff` shows new file but task list only references `src/user.ts`. **Impact:** Implementation scope creep. **Fix:** Update task list or revert changes.
> - *Reject (too vague)* — "Some files are missing."

### 4) Evidence Appendix

- Git commits analyzed with file changes
- Proof Artifact test results (outputs, screenshots)
- File comparison results (expected vs actual)
- Commands executed with results

---

**Validation Completed:** [Date+Time]
**Validation Performed By:** [AI Model]
