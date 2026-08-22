import pytest
from pathlib import Path
import json
import shutil
import tempfile
import sys
import os

# Add the script to the path so we can import it
script_dir = Path(__file__).parent.parent / "skill" / "scripts"
sys.path.append(str(script_dir))
import importlib
assess = importlib.import_module("assess-sdd-state")

@pytest.fixture
def workspace():
    """Create a temporary workspace directory structure."""
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace_path = Path(temp_dir)
        yield workspace_path

# A minimal audit report that actually records a passing verdict. An empty or
# verdict-less audit file is not a passing gate, so fixtures that need the
# workflow to advance past Phase 2 must supply a real verdict.
PASSING_AUDIT = """# 01-audit-auth.md

## Executive Summary

- Overall Status: PASS
- Required Gate Failures: 0
"""


def test_no_specs_dir(workspace):
    """Test S1_START: Empty Workspace"""
    result = assess.main(base_path=workspace)
    assert result["specs_directory_exists"] is False
    assert result["recommendation"].startswith("Phase 1:")

def test_empty_specs_dir(workspace):
    """Test S1_START: Specs dir exists but is empty."""
    docs_specs = workspace / "docs" / "specs"
    docs_specs.mkdir(parents=True)

    result = assess.main(base_path=workspace)
    assert result["specs_directory_exists"] is True
    assert result["recommendation"].startswith("Phase 1:")

def test_phase_2_start(workspace):
    """Test S2_START: Spec exists, tasks file missing"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    # Create the spec file
    (feature_dir / "01-spec-auth.md").touch()

    result = assess.main(base_path=workspace)
    assert len(result["active_specs"]) == 1
    spec = result["active_specs"][0]

    assert spec["files_found"]["spec"] is True
    assert spec["files_found"]["tasks"] is False
    assert spec["phase"] == 2
    assert result["recommendation"].startswith("Phase 2:")

def test_phase_3_start(workspace):
    """Test S3_START: All required files exist, and tasks are incomplete"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-audit-auth.md").write_text(PASSING_AUDIT)

    with open(feature_dir / "01-tasks-auth.md", "w") as f:
        f.write("# Tasks\n- [ ] Task 1\n- [x] Task 2")

    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    assert spec["files_found"]["spec"] is True
    assert spec["files_found"]["tasks"] is True
    assert spec["files_found"]["audit"] is True
    assert spec["phase"] == 3
    assert result["recommendation"].startswith("Phase 3:")

def test_phase_4_start_selects_completed_unvalidated_spec(workspace):
    """Test S4_START: completed tasks with missing validation route to Phase 4."""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-audit-auth.md").write_text(PASSING_AUDIT)

    with open(feature_dir / "01-tasks-auth.md", "w") as f:
        f.write("# Tasks\n- [x] Task 1\n- [x] Task 2")


    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    assert spec["files_found"]["validation"] is False
    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_START"
    assert spec["action_required"] == "Validate Implementation (Phase 4)"
    assert result["recommendation"].startswith("Phase 4:")
def test_S1_QUESTIONS(workspace):
    """Test S1_QUESTIONS: Directory exists and questions file exists, but spec is missing"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    # Missing spec
    (feature_dir / "01-questions-1-auth.md").touch()

    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    assert spec["files_found"]["spec"] is False
    assert spec["files_found"]["questions"] is True
    assert spec["phase"] == 1
    assert "QUESTIONS" in spec["detailed_state"]

def test_S2_PARENTS_DONE(workspace):
    """Test S2_PARENTS_DONE: Tasks file exists but has TBD markers instead of sub-tasks"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    (feature_dir / "01-spec-auth.md").touch()

    with open(feature_dir / "01-tasks-auth.md", "w") as f:
        f.write("# Tasks\n## TBD")

    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_PARENTS_DONE"

def test_S2_AUDIT_FAILED(workspace):
    """Test S2_AUDIT_FAILED: Audit file exists but contains a FAIL statement"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-tasks-auth.md").touch()

    with open(feature_dir / "01-audit-auth.md", "w") as f:
        f.write("# Audit\n- GATE A: **FAIL**")

    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_FAILED"

def test_S4_FAILED(workspace):
    """Test S4_FAILED: Validation report exists but contains FAIL gates"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-audit-auth.md").write_text(PASSING_AUDIT)

    with open(feature_dir / "01-tasks-auth.md", "w") as f:
        f.write("# Tasks\n- [x] Task 1")


    validation_dir = docs_specs / "01-validation-auth"
    validation_dir.mkdir(parents=True, exist_ok=True)

    with open(feature_dir / "01-validation-auth.md", "w") as f:
        f.write("# Validation\n- GATE A: **FAIL**")

    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_FAILED"

def test_S4_COMPLETE(workspace):
    """Test S4_COMPLETE: Validation report exists and passes all gates"""
    docs_specs = workspace / "docs" / "specs"
    feature_dir = docs_specs / "01-spec-auth"
    feature_dir.mkdir(parents=True)

    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-audit-auth.md").write_text(PASSING_AUDIT)

    with open(feature_dir / "01-tasks-auth.md", "w") as f:
        f.write("# Tasks\n- [x] Task 1")

    with open(feature_dir / "01-validation-auth.md", "w") as f:
        f.write("# Validation\n- All gates: PASS")

    result = assess.main(base_path=workspace)
    spec = result["active_specs"][0]

    # Ideally, if it's fully complete, the script should recommend Phase 1 for a *new* spec
    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_COMPLETE"


# ---------------------------------------------------------------------------
# Authoritative-verdict regression tests
#
# The assessor must decide PASS/FAIL from the report's authoritative
# "Overall Status:" (audit) / "Overall:" (validation) line, NOT by scanning
# the whole file for the token FAIL. Otherwise a report that failed on run 1
# and passed on run 2 -- whose Re-Audit Delta retains "FAIL -> PASS" history --
# or prose that merely mentions the word FAIL is mis-read as a failure, trapping
# the workflow in the failure state.
# ---------------------------------------------------------------------------

# A realistic passing re-audit: Executive Summary says PASS, but the retained
# Re-Audit Delta history still contains the word FAIL.
AUDIT_FAIL_THEN_PASS = """# 01-audit-auth.md

## Executive Summary

- Overall Status: PASS
- Required Gate Failures: 0
- Flagged Risks: 0

## Re-Audit Delta (Runs 2+)

- Changed gate statuses since previous run: Requirement-to-test traceability FAIL -> PASS
- Still-failing REQUIRED gates: none
"""

# A passing audit whose prose merely mentions the word FAIL.
AUDIT_PASS_FAIL_WORD_IN_BODY = """# 01-audit-auth.md

## Executive Summary

- Overall Status: PASS
- Required Gate Failures: 0

## Notes

All required gates pass; none returned FAIL.
"""

# A genuine failure with an authoritative FAIL verdict (regression guard).
AUDIT_GENUINE_FAIL = """# 01-audit-auth.md

## Executive Summary

- Overall Status: FAIL
- Required Gate Failures: 1

## Gateboard

| Gate | Status | Why it failed (<=10 words) | Exact fix target |
| --- | --- | --- | --- |
| Requirement-to-test traceability | FAIL | FR-2 has no mapped test artifact | `## Tasks > 2.0` |
"""


def _spec_with_audit(workspace, audit_body, tasks_body):
    """Create a workspace whose single spec has spec/tasks/audit files."""
    feature_dir = workspace / "docs" / "specs" / "01-spec-auth"
    feature_dir.mkdir(parents=True)
    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-tasks-auth.md").write_text(tasks_body)
    (feature_dir / "01-audit-auth.md").write_text(audit_body)
    return feature_dir


def test_audit_fail_then_pass_history_is_not_failed(workspace):
    """RED before fix: PASS audit with retained FAIL->PASS history must not trap in Phase 2."""
    _spec_with_audit(workspace, AUDIT_FAIL_THEN_PASS, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["detailed_state"] != "S2_AUDIT_FAILED"
    assert spec["phase"] == 3
    assert spec["detailed_state"] == "S3_MIDFLIGHT"


def test_audit_pass_with_fail_word_in_body_is_not_failed(workspace):
    """RED before fix: PASS audit that merely mentions the word FAIL must not trap in Phase 2."""
    _spec_with_audit(workspace, AUDIT_PASS_FAIL_WORD_IN_BODY, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["detailed_state"] != "S2_AUDIT_FAILED"
    assert spec["phase"] == 3
    assert spec["detailed_state"] == "S3_MIDFLIGHT"


def test_audit_overall_fail_still_traps(workspace):
    """Regression guard: an authoritative Overall Status: FAIL still routes to S2_AUDIT_FAILED."""
    _spec_with_audit(workspace, AUDIT_GENUINE_FAIL, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_FAILED"


def test_audit_non_status_overall_pass_does_not_bypass_failed_gate(workspace):
    """Only a documented status label may bypass the fallback gate scan."""
    body = "## Overall discussion: PASS\n\n- GATE A: FAIL\n"
    _spec_with_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_FAILED"


def test_audit_non_status_overall_fail_does_not_override_current_pass(workspace):
    """Historical prose cannot override the documented current audit status."""
    body = "## Overall notes: FAIL on run 1\n\n- Overall Status: PASS\n"
    _spec_with_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 3
    assert spec["detailed_state"] == "S3_MIDFLIGHT"


def _spec_with_validation(workspace, validation_body):
    """Create a workspace whose single spec is complete through validation."""
    feature_dir = workspace / "docs" / "specs" / "01-spec-auth"
    feature_dir.mkdir(parents=True)
    (feature_dir / "01-spec-auth.md").touch()
    (feature_dir / "01-audit-auth.md").write_text("- Overall Status: PASS")
    (feature_dir / "01-tasks-auth.md").write_text("# Tasks\n- [x] Task 1")
    (feature_dir / "01-validation-auth.md").write_text(validation_body)
    return feature_dir


def test_validation_fail_then_pass_history_is_complete(workspace):
    """RED before fix: PASS validation with retained FAIL history must read as S4_COMPLETE."""
    body = "## Summary\n\n- **Overall:** PASS (GATE A was FAIL on run 1, fixed on run 2)\n"
    _spec_with_validation(workspace, body)

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_COMPLETE"


def test_validation_pass_with_fail_word_in_body_is_complete(workspace):
    """RED before fix: PASS validation that merely mentions FAIL must read as S4_COMPLETE."""
    body = "## Summary\n\n- **Overall:** PASS\n\nNo gate returned FAIL.\n"
    _spec_with_validation(workspace, body)

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_COMPLETE"


# ---------------------------------------------------------------------------
# Fail-closed gate regression tests
#
# The planning audit is the workflow's only barrier between planning and
# implementation. Absence of a verdict is not a passing verdict: every report
# the assessor cannot read as an explicit PASS must hold the spec in Phase 2.
# ---------------------------------------------------------------------------

def _spec_through_audit(workspace, audit_body, tasks_body, sequence="01", feature="auth"):
    """Create one spec directory with spec, tasks, and audit files."""
    feature_dir = workspace / "docs" / "specs" / f"{sequence}-spec-{feature}"
    feature_dir.mkdir(parents=True)
    (feature_dir / f"{sequence}-spec-{feature}.md").write_text("# Spec\n")
    (feature_dir / f"{sequence}-tasks-{feature}.md").write_text(tasks_body)
    (feature_dir / f"{sequence}-audit-{feature}.md").write_text(audit_body)
    return feature_dir


def test_empty_audit_file_does_not_open_the_gate(workspace):
    """An audit file truncated by an interrupted session is not a passing gate."""
    _spec_through_audit(workspace, "", "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_UNVERIFIED"
    assert any("empty" in blocker for blocker in spec["blockers"])


def test_unfilled_pass_slash_fail_placeholder_does_not_open_the_gate(workspace):
    """The literal template line `Overall Status: PASS/FAIL` records no verdict."""
    body = (
        "## Executive Summary\n\n"
        "- Overall Status: PASS/FAIL\n"
        "- Required Gate Failures: 3\n"
    )
    _spec_through_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_UNVERIFIED"


def test_unfilled_placeholder_with_failing_gateboard_reads_as_failed(workspace):
    """A placeholder verdict falls through to the gateboard, which says FAIL."""
    body = (
        "## Executive Summary\n\n"
        "- Overall Status: PASS/FAIL\n\n"
        "## Gateboard\n\n"
        "| Gate | Status |\n| --- | --- |\n"
        "| Requirement-to-test traceability | FAIL |\n"
    )
    _spec_through_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_FAILED"


def test_audit_whose_failure_is_only_in_prose_does_not_open_the_gate(workspace):
    """Lowercase prose is not a verdict, so the gate stays closed rather than open."""
    body = "# Audit\n\nResult: two required gates failed and must be remediated.\n"
    _spec_through_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_UNVERIFIED"


@pytest.mark.skipif(
    hasattr(os, "geteuid") and os.geteuid() == 0,
    reason="root can read files regardless of mode bits",
)
def test_unreadable_audit_does_not_open_the_gate(workspace):
    """A read error must surface as a blocker, not be swallowed into a pass."""
    feature_dir = _spec_through_audit(
        workspace, "- Overall Status: FAIL\n", "# Tasks\n- [ ] Task 1"
    )
    audit_path = feature_dir / "01-audit-auth.md"
    audit_path.chmod(0o000)
    try:
        spec = assess.main(base_path=workspace)["active_specs"][0]
    finally:
        audit_path.chmod(0o644)

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_UNVERIFIED"
    assert any("unreadable" in blocker for blocker in spec["blockers"])


def test_pass_fail_column_legend_does_not_trap_a_passing_audit(workspace):
    """A `Status (PASS/FAIL)` column header is a legend, not a failing gate."""
    body = (
        "# Audit\n\n"
        "| Gate | Status (PASS/FAIL) |\n| --- | --- |\n"
        "| Requirement-to-test traceability | PASS |\n"
        "| Proof artifact verifiability | PASS |\n"
    )
    _spec_through_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["detailed_state"] == "S3_MIDFLIGHT"
    assert spec["phase"] == 3


def test_bare_verdict_after_a_colon_line_is_not_a_status_value(workspace):
    """A qualifying prefix must share the token's line, not precede it."""
    body = "# Audit\n\n## Notes:\n\nPASS\n"
    _spec_through_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_UNVERIFIED"


def test_bare_verdict_after_a_table_row_is_not_a_status_value(workspace):
    """A token on its own line cannot inherit the pipe of the row above it."""
    body = "# Audit\n\n| Gate | Status |\n| --- | --- |\n\nPASS\n"
    _spec_through_audit(workspace, body, "# Tasks\n- [ ] Task 1")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 2
    assert spec["detailed_state"] == "S2_AUDIT_UNVERIFIED"


# ---------------------------------------------------------------------------
# Content-scan precision: markdown prose and fenced examples are not state
# ---------------------------------------------------------------------------

def test_tbd_inside_a_subtask_does_not_revert_to_parents_only(workspace):
    """The word TBD in a sub-task must not erase generated sub-tasks."""
    docs_specs = workspace / "docs" / "specs" / "01-spec-auth"
    docs_specs.mkdir(parents=True)
    (docs_specs / "01-spec-auth.md").write_text("# Spec\n")
    (docs_specs / "01-tasks-auth.md").write_text(
        "### [x] 1.0 Parent\n\n#### 1.0 Tasks\n\n- [x] 1.1 Replace the TBD placeholder in config\n"
    )

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["detailed_state"] == "S2_SUBTASKS_DONE"
    assert spec["action_required"] == "Generate Planning Audit (Phase 2)"


def test_bare_tbd_line_still_detects_parents_only(workspace):
    """Regression guard: the template's bare TBD line still means parents-only."""
    docs_specs = workspace / "docs" / "specs" / "01-spec-auth"
    docs_specs.mkdir(parents=True)
    (docs_specs / "01-spec-auth.md").write_text("# Spec\n")
    (docs_specs / "01-tasks-auth.md").write_text(
        "### [ ] 1.0 Parent\n\n#### 1.0 Tasks\n\nTBD\n"
    )

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["detailed_state"] == "S2_PARENTS_DONE"


def test_checkbox_inside_a_code_fence_is_not_an_incomplete_task(workspace):
    """A fenced template example must not strand a finished spec in Phase 3."""
    tasks = (
        "### [x] 1.0 Parent\n\n#### 1.0 Tasks\n\n- [x] 1.1 done\n\n"
        "Sub-task format:\n\n```markdown\n- [ ] N.N description\n```\n"
    )
    feature_dir = _spec_through_audit(workspace, PASSING_AUDIT, tasks)

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_START"


def test_heading_style_incomplete_parent_task_is_detected(workspace):
    """Regression guard: `### [ ] 1.0` is a real unchecked task, fences aside."""
    _spec_through_audit(workspace, PASSING_AUDIT, "### [ ] 1.0 Parent\n\n- [ ] 1.1 todo\n")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 3
    assert spec["detailed_state"] == "S3_MIDFLIGHT"


def test_unclosed_fence_does_not_hide_incomplete_tasks(workspace):
    """A truncated task file must not look finished.

    Dropping every line after an unterminated fence would hide real unchecked
    boxes, so an unterminated fence is not treated as a block at all.
    """
    tasks = (
        "### [x] 1.0 Parent\n\n- [x] 1.1 done\n\n"
        "```markdown\n- [ ] 2.1 still open\n### [ ] 2.0 Parent two\n"
    )
    _spec_through_audit(workspace, PASSING_AUDIT, tasks)

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 3
    assert spec["detailed_state"] == "S3_MIDFLIGHT"


# ---------------------------------------------------------------------------
# Selection order
# ---------------------------------------------------------------------------

def test_highest_sequence_wins_within_the_same_phase(workspace):
    """Two specs in the same phase: the newest sequence is the active one."""
    for sequence, feature in (("01", "older"), ("02", "newer")):
        _spec_through_audit(
            workspace, PASSING_AUDIT, "# Tasks\n- [ ] Task 1", sequence, feature
        )

    result = assess.main(base_path=workspace)

    assert "Sequence 02" in result["recommendation"]
    assert "newer" in result["recommendation"]


def test_validation_without_a_verdict_is_not_complete(workspace):
    """A validation report with no readable verdict does not close the workflow."""
    feature_dir = _spec_through_audit(workspace, PASSING_AUDIT, "# Tasks\n- [x] Task 1")
    (feature_dir / "01-validation-auth.md").write_text("# Validation\n\nLooks good to me.\n")

    spec = assess.main(base_path=workspace)["active_specs"][0]

    assert spec["phase"] == 4
    assert spec["detailed_state"] == "S4_UNVERIFIED"
