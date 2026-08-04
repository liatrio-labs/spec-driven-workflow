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
    (feature_dir / "01-audit-auth.md").touch()

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
    (feature_dir / "01-audit-auth.md").touch()

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
    (feature_dir / "01-audit-auth.md").touch()

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
    (feature_dir / "01-audit-auth.md").touch()

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
