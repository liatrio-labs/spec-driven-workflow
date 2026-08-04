#!/usr/bin/env python3
import os
import re
from pathlib import Path
import json

import sys

def get_specs_dir(base_path=None):
    """Locate the specs directory starting from the current location or provided base_path."""
    current = Path(base_path) if base_path else Path.cwd()
    specs_dir = current / "docs" / "specs"
    return specs_dir

def assess_spec_dir(spec_path):
    """
    Assess a single spec directory to determine its state in the SDD workflow.
    """
    spec_dir = Path(spec_path)
    feature_name_match = re.match(r'^([0-9]{2})-spec-(.*)$', spec_dir.name)

    if not feature_name_match:
        return {"status": "invalid_name", "path": str(spec_dir)}

    seq_num = feature_name_match.group(1)
    feature_name = feature_name_match.group(2)

    files = list(spec_dir.glob("*.md"))
    file_names = [f.name for f in files]

    spec_file = f"{seq_num}-spec-{feature_name}.md"
    tasks_file = f"{seq_num}-tasks-{feature_name}.md"
    audit_file = f"{seq_num}-audit-{feature_name}.md"
    validation_file = f"{seq_num}-validation-{feature_name}.md"

    # Check for any questions file matching the pattern [NN]-questions-[N]-[feature].md
    has_questions = any(re.match(rf'^{seq_num}-questions-\d+-{re.escape(feature_name)}\.md$', name) for name in file_names)

    state = {
        "sequence": seq_num,
        "feature": feature_name,
        "directory": str(spec_dir),
        "files_found": {
            "spec": spec_file in file_names,
            "tasks": tasks_file in file_names,
            "audit": audit_file in file_names,
            "validation": validation_file in file_names,
            "questions": has_questions
        },
        "phase": 0,
        "detailed_state": "",
        "action_required": ""
    }

    # Logic matching SKILL.md state assessment
    if not state["files_found"]["spec"]:
        state["phase"] = 1
        if state["files_found"]["questions"]:
            state["detailed_state"] = "S1_QUESTIONS"
            state["action_required"] = "Answer Clarification Questions (Phase 1)"
        else:
            state["detailed_state"] = "S1_START"
            state["action_required"] = "Generate Spec (Phase 1)"
    elif not state["files_found"]["tasks"]:
        state["phase"] = 2
        state["detailed_state"] = "S2_START"
        state["action_required"] = "Generate Task List (Phase 2)"
    elif not state["files_found"]["audit"]:
        state["phase"] = 2

        # Check if tasks are parents only (TBD marker)
        tasks_path = spec_dir / tasks_file
        has_tbd = False
        try:
            with open(tasks_path, 'r', encoding='utf-8') as f:
                if re.search(r'## TBD|\bTBD\b', f.read()):
                    has_tbd = True
        except Exception:
            pass

        if has_tbd:
            state["detailed_state"] = "S2_PARENTS_DONE"
            state["action_required"] = "Review Parent Tasks & Generate Sub-tasks (Phase 2)"
        else:
            state["detailed_state"] = "S2_SUBTASKS_DONE"
            state["action_required"] = "Generate Planning Audit (Phase 2)"
    else:
        # Check audit gates for FAIL
        audit_path = spec_dir / audit_file
        audit_failed = False
        try:
            with open(audit_path, 'r', encoding='utf-8') as f:
                if re.search(r'\*\*FAIL\*\*|\bFAIL\b', f.read()):
                    audit_failed = True
        except Exception:
            pass

        if audit_failed:
            state["phase"] = 2
            state["detailed_state"] = "S2_AUDIT_FAILED"
            state["action_required"] = "Fix Planning Audit Failures (Phase 2)"
            return state # Return early to trap it in Phase 2
        else:
            state["detailed_state"] = "S2_COMPLETE"

        # Check task completion
        tasks_path = spec_dir / tasks_file
        incomplete_tasks = False
        try:
            with open(tasks_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for incomplete markdown checkboxes
                if re.search(r'\[\s\]', content) or re.search(r'\[~\]', content):
                    incomplete_tasks = True
        except Exception:
            pass

        if incomplete_tasks:
            state["phase"] = 3
            state["action_required"] = "Implement Tasks (Phase 3)"
            # At this point, we could probably detect midflight vs start, but both are Phase 3
            state["detailed_state"] = "S3_MIDFLIGHT"
        elif not state["files_found"]["validation"]:
            state["phase"] = 4
            state["detailed_state"] = "S4_START"
            state["action_required"] = "Validate Implementation (Phase 4)"
        else:
            state["phase"] = 4

            # Check validation for FAIL
            val_path = spec_dir / validation_file
            val_failed = False
            try:
                with open(val_path, 'r', encoding='utf-8') as f:
                    if re.search(r'\*\*FAIL\*\*|\bFAIL\b', f.read()):
                        val_failed = True
            except Exception:
                pass

            if val_failed:
                state["detailed_state"] = "S4_FAILED"
                state["action_required"] = "Fix Validation Failures (Phase 4)"
            else:
                state["detailed_state"] = "S4_COMPLETE"
                state["action_required"] = "Validation Complete. Start next feature (Phase 1)"

    return state

def main(base_path=None):
    specs_dir = get_specs_dir(base_path)

    result = {
        "specs_directory_exists": specs_dir.exists(),
        "specs_directory": str(specs_dir),
        "active_specs": [],
        "recommendation": ""
    }

    if not specs_dir.exists():
        result["recommendation"] = "Phase 1: No specs directory found. A new feature specification is required."
        return result

    spec_dirs = [d for d in specs_dir.iterdir() if d.is_dir() and re.match(r'^[0-9]{2}-spec-', d.name)]

    if not spec_dirs:
        result["recommendation"] = "Phase 1: Specs directory exists but is empty. A new feature specification is required."
        return result

    for d in sorted(spec_dirs):
        result["active_specs"].append(assess_spec_dir(d))

    # Find the most advanced incomplete spec
    # A spec in Phase 3 is actively being worked on.
    # A spec in Phase 2 needs planning.
    # Phase 4 means it's done but might need final validation.

    # Phase 4 complete means the spec is essentially in Phase 4 but the *next flow* is Phase 1
    # However, keeping it as Phase 4 in the script output means the Orchestrator reads S4_COMPLETE
    # and S4_COMPLETE triggers S1_START per our flow diagram.

    active = sorted(
        [s for s in result["active_specs"] if s.get("phase", 0) in [1, 2, 3, 4]],
        key=lambda x: (x["phase"], -int(x["sequence"])), # Prioritize highest phase, then highest sequence
        reverse=True
    )

    if active:
        # Prioritize any incomplete phases over a completed phase 4
        incomplete = [s for s in active if s.get("phase", 0) < 4 or s.get("detailed_state") == "S4_FAILED" or s.get("detailed_state") == "S4_START"]

        if incomplete:
            target = incomplete[0]
            result["recommendation"] = f"Phase {target['phase']}: {target['action_required']} for feature '{target['feature']}' (Sequence {target['sequence']})"
        else:
            # Everything is S4_COMPLETE
            target = active[0]
            result["recommendation"] = f"Phase 4 (Complete): {target['action_required']} for feature '{target['feature']}' (Sequence {target['sequence']}). OR start Phase 1 for a new feature."
    else:
        result["recommendation"] = "Phase 1: No valid specs found. A new feature specification is required."

    return result

if __name__ == "__main__":
    result = main(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps(result, indent=2))
