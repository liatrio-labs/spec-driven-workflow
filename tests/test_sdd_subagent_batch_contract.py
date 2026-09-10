from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "skill" / "SKILL.md"
PHASE_3 = ROOT / "skill" / "references" / "sdd-3-manage-tasks.md"


def test_router_requires_phase_reference_context_when_delegating():
    text = SKILL_MD.read_text().lower()

    assert "whenever you delegate sdd work to a subagent" in text
    assert "read the relevant sdd phase reference file before beginning" in text


def test_phase_3_documents_batch_subagent_loop():
    phase_3 = PHASE_3.read_text().lower()

    assert "batch mode with subagents" in phase_3
    assert "implement → review → remediate → repeat" in phase_3
    assert "separate subagents for each loop part" in phase_3
    assert "read `skill/references/sdd-3-manage-tasks.md`" in phase_3
    assert "git status --short" in phase_3
    assert "git log --oneline -1" in phase_3
    assert "report that all sdd-3 tasks are complete" in phase_3
