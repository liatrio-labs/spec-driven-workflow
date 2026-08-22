#!/usr/bin/env python3
import re
from pathlib import Path
import json

import sys

# Verdicts. A report that yields UNVERIFIED has no trustworthy verdict and must
# not be treated as a passing gate.
PASS = "PASS"
FAIL = "FAIL"
UNVERIFIED = "UNVERIFIED"

_FENCE = re.compile(r'^\s*(?:```|~~~)')

_AUTHORITATIVE_STATUS = re.compile(
    r'^\s*(?:[-*+]\s*)?(?:\*\*)?overall(?:\s+status)?(?:\*\*)?\s*:'
    r'\s*(?:\*\*)?\s*(PASS|FAIL)\b',
    re.IGNORECASE | re.MULTILINE,
)

_ANY_VERDICT_TOKEN = re.compile(r'\b(PASS|FAIL)\b', re.IGNORECASE)

# A verdict token is only a status *value* when it sits where a value goes: after
# a colon, inside a table cell, or wrapped in bold. Bare prose ("no gate returned
# FAIL", "all required gates pass") is not a verdict.
_STATUS_VALUE_PREFIXES = (":", "|", "**")


def _strip_code_fences(text):
    """Drop fenced code blocks so template examples cannot be read as state.

    Task files legitimately contain fenced examples such as::

        ```markdown
        - [ ] N.N description
        ```

    Counting those as real unchecked boxes strands a finished spec in Phase 3
    forever, so every content scan runs on the stripped text.

    A fence that is opened and never closed is not treated as a block: its lines
    are restored, because a truncated task file must not be able to hide
    unfinished work behind a missing closing fence.
    """
    kept = []
    pending = None  # lines held inside a fence that has not closed yet
    for line in text.splitlines():
        if _FENCE.match(line):
            pending = [] if pending is None else None
            continue
        if pending is None:
            kept.append(line)
        else:
            pending.append(line)
    if pending:
        # The final fence never closed, so it does not delimit a block. Restoring
        # its lines keeps a truncated task file from hiding real task state:
        # dropping them would make an unfinished spec look finished.
        kept.extend(pending)
    return "\n".join(kept)


def _is_placeholder(text, match):
    """True when the captured verdict is the unfilled `PASS/FAIL` template.

    The documented report template ships the literal line
    ``- Overall Status: PASS/FAIL``. Read naively that parses as PASS, so an
    audit whose verdict was never filled in reads as a passing gate. Treat the
    slash form as "no verdict recorded" instead.
    """
    return text[match.end():match.end() + 1] == "/" or text[max(0, match.start() - 1):match.start()] == "/"


def _status_value_tokens(text):
    """Yield PASS/FAIL tokens that appear in a status-value position.

    The qualifying prefix must sit on the *same line* as the token. Scanning
    backwards across newlines would let a bare ``PASS`` inherit the colon, pipe,
    or bold marker of an earlier line, so prose such as::

        ## Notes:

        PASS

    would be read as a verdict and open the planning gate.
    """
    for match in _ANY_VERDICT_TOKEN.finditer(text):
        if _is_placeholder(text, match):
            continue
        line_start = text.rfind("\n", 0, match.start()) + 1
        before = text[line_start:match.start()].rstrip()
        if before.endswith(_STATUS_VALUE_PREFIXES):
            yield match.group(1).upper()


def _report_verdict(text):
    r"""Return PASS, FAIL, or UNVERIFIED for an audit/validation report.

    The report's Executive Summary carries the verdict on an
    ``Overall Status: PASS/FAIL`` line (audits) or ``Overall: PASS/FAIL`` line
    (validations). That line is authoritative; retained run history elsewhere in
    the report (e.g. a Re-Audit Delta noting ``FAIL -> PASS``) or prose that
    merely mentions the word FAIL must not flip the verdict.

    The authoritative-line regex accepts optional indentation, a Markdown list
    marker, and bold formatting around ``Overall`` / ``Overall Status`` and the
    verdict. It deliberately requires a colon followed immediately by the
    captured verdict, so prose such as ``Overall notes: FAIL on run 1`` cannot
    override an explicit current status.

    Regex anatomy (``^`` / ``$`` apply per line; matching is case-insensitive)::

    ^\s*
    │ │
    │ └─ Allow leading whitespace
    └── Start at the beginning of a line
    (?:[-*+]\s*)?
    │
    └─ Optional Markdown list marker:
    "- ", "* ", or "+ "
    (?:\*\*)?
    │
    └─ Optional opening bold marker: "**"
    overall
    │
    └─ Require the literal label "overall"
    (?:\s+status)?
    │
    └─ Optionally allow the word "status":
    "Overall"         ✓
    "Overall Status"  ✓
    (?:\*\*)?\s*:
    │       │       │
    │       │       └─ Require a colon
    │       └───────── Allow whitespace before it
    └───────────────── Optional closing bold marker
    \s*(?:\*\*)?\s*(PASS|FAIL)\b
    │    │              │          │
    │    │              │          └─ Prevent matches like "FAILED"
    │    │              └──────────── Capture the verdict
    │    └─────────────────────────── Allow bold verdicts: "**PASS**"
    └──────────────────────────────── Allow spaces after ":"

    Strategy:
      1. Return the first authoritative status line's verdict. A parenthetical
         note such as ``PASS (was FAIL on run 1)`` therefore stays PASS. An
         unfilled ``PASS/FAIL`` placeholder is skipped, not read as PASS.
      2. Otherwise scan for verdict tokens in status-value position (after a
         colon, in a table cell, or bolded): any FAIL wins, else PASS. Bare
         prose is ignored, and the ``(PASS/FAIL)`` column legend is ignored.
      3. Otherwise return UNVERIFIED. Callers must treat that as "gate not
         satisfied", never as a pass.
    """
    body = _strip_code_fences(text)

    for match in _AUTHORITATIVE_STATUS.finditer(body):
        if not _is_placeholder(body, match):
            return match.group(1).upper()

    tokens = set(_status_value_tokens(body))
    if FAIL in tokens:
        return FAIL
    if PASS in tokens:
        return PASS
    return UNVERIFIED


def _read_report_verdict(path):
    """Read one report and return (verdict, error).

    An unreadable or empty report is UNVERIFIED with a reason, never a silent
    pass. `error` is None on a clean read.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return UNVERIFIED, f"{path.name}: not found"
    except OSError as exc:
        return UNVERIFIED, f"{path.name}: unreadable ({exc.strerror})"
    except UnicodeDecodeError:
        return UNVERIFIED, f"{path.name}: not valid UTF-8"

    if not text.strip():
        return UNVERIFIED, f"{path.name}: file is empty"

    verdict = _report_verdict(text)
    if verdict is UNVERIFIED:
        return verdict, f"{path.name}: no authoritative 'Overall Status: PASS' line found"
    return verdict, None


def _read_text(path):
    """Read a task file, returning (text, error)."""
    try:
        return path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return "", f"{path.name}: not found"
    except OSError as exc:
        return "", f"{path.name}: unreadable ({exc.strerror})"
    except UnicodeDecodeError:
        return "", f"{path.name}: not valid UTF-8"


def _is_parents_only(tasks_text):
    """True when sub-tasks are still placeholders.

    The Phase 2 template writes a bare ``TBD`` line under each parent task's
    Tasks heading. Requiring the whole line to be TBD keeps a sub-task that
    merely mentions the word ("replace the TBD placeholder in config") from
    reverting a fully planned spec back to parent-tasks-only.
    """
    return any(
        line.strip().lstrip("#").strip() == "TBD"
        for line in _strip_code_fences(tasks_text).splitlines()
    )


_CHECKBOX = re.compile(r'^\s*(?:[-*+]\s+|#{1,6}\s+)?\[([ x~])\]', re.IGNORECASE)


def _has_incomplete_tasks(tasks_text):
    """True when any real checkbox is still `[ ]` or `[~]` (fences excluded)."""
    for line in _strip_code_fences(tasks_text).splitlines():
        match = _CHECKBOX.match(line)
        if match and match.group(1).lower() in (" ", "~"):
            return True
    return False


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
        "action_required": "",
        "blockers": []
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
        return state

    if not state["files_found"]["tasks"]:
        state["phase"] = 2
        state["detailed_state"] = "S2_START"
        state["action_required"] = "Generate Task List (Phase 2)"
        return state

    tasks_text, tasks_error = _read_text(spec_dir / tasks_file)
    if tasks_error:
        state["phase"] = 2
        state["detailed_state"] = "S2_TASKS_UNREADABLE"
        state["action_required"] = "Repair the task list before continuing (Phase 2)"
        state["blockers"].append(tasks_error)
        return state

    if not state["files_found"]["audit"]:
        state["phase"] = 2
        if _is_parents_only(tasks_text):
            state["detailed_state"] = "S2_PARENTS_DONE"
            state["action_required"] = "Review Parent Tasks & Generate Sub-tasks (Phase 2)"
        else:
            state["detailed_state"] = "S2_SUBTASKS_DONE"
            state["action_required"] = "Generate Planning Audit (Phase 2)"
        return state

    # The planning audit is a gate: it opens only on an explicit PASS verdict.
    audit_verdict, audit_error = _read_report_verdict(spec_dir / audit_file)
    if audit_verdict == FAIL:
        state["phase"] = 2
        state["detailed_state"] = "S2_AUDIT_FAILED"
        state["action_required"] = "Fix Planning Audit Failures (Phase 2)"
        return state
    if audit_verdict != PASS:
        state["phase"] = 2
        state["detailed_state"] = "S2_AUDIT_UNVERIFIED"
        state["action_required"] = (
            "Planning audit verdict could not be verified; re-run the audit and record "
            "'Overall Status: PASS' before implementation (Phase 2)"
        )
        state["blockers"].append(audit_error)
        return state

    state["detailed_state"] = "S2_COMPLETE"

    if _has_incomplete_tasks(tasks_text):
        state["phase"] = 3
        state["detailed_state"] = "S3_MIDFLIGHT"
        state["action_required"] = "Implement Tasks (Phase 3)"
        return state

    if not state["files_found"]["validation"]:
        state["phase"] = 4
        state["detailed_state"] = "S4_START"
        state["action_required"] = "Validate Implementation (Phase 4)"
        return state

    state["phase"] = 4
    validation_verdict, validation_error = _read_report_verdict(spec_dir / validation_file)
    if validation_verdict == PASS:
        state["detailed_state"] = "S4_COMPLETE"
        state["action_required"] = "Validation Complete. Start next feature (Phase 1)"
    elif validation_verdict == FAIL:
        state["detailed_state"] = "S4_FAILED"
        state["action_required"] = "Fix Validation Failures (Phase 4)"
    else:
        state["detailed_state"] = "S4_UNVERIFIED"
        state["action_required"] = (
            "Validation verdict could not be verified; re-run validation and record "
            "'Overall: PASS' (Phase 4)"
        )
        state["blockers"].append(validation_error)

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
        key=lambda x: (x["phase"], int(x["sequence"])), # Prioritize highest phase, then highest sequence
        reverse=True
    )

    if active:
        # Prioritize any incomplete phases over a completed phase 4
        incomplete = [s for s in active if s.get("phase", 0) < 4 or s.get("detailed_state") != "S4_COMPLETE"]

        if incomplete:
            target = incomplete[0]
            result["recommendation"] = f"Phase {target['phase']}: {target['action_required']} for feature '{target['feature']}' (Sequence {target['sequence']})"
            if target.get("blockers"):
                result["recommendation"] += f" | blockers: {'; '.join(target['blockers'])}"
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
