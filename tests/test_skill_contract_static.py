from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCE_DIR = SKILL_DIR / "references"


def read_skill_payload() -> str:
    return "\n".join(path.read_text() for path in [SKILL_MD, *sorted(REFERENCE_DIR.glob("*.md"))])


def test_skill_frontmatter_has_production_name_and_description():
    text = SKILL_MD.read_text()

    assert text.startswith("---\n")
    assert re.search(r"^name: sdd$", text, re.MULTILINE)
    assert re.search(r"^description: \".+\"$", text, re.MULTILINE)
    assert "sdd-skill-poc" not in text


def test_router_requires_workspace_root_assessor_invocation():
    text = SKILL_MD.read_text()

    assert "Before routing, run the bundled assessor script while the current working directory is the target repository/workspace root" in text
    assert "python {{skill_dir}}/scripts/assess-sdd-state.py ." in text
    assert "SDD artifacts are assessed from the workspace path argument (`.`" in text


def test_all_router_phase_reference_paths_exist():
    text = SKILL_MD.read_text()
    referenced_paths = re.findall(r"`\{\{skill_dir\}\}/(references/[^`]+\.md)`", text)

    assert referenced_paths == [
        "references/sdd-1-generate-spec.md",
        "references/sdd-2-generate-task-list-from-spec.md",
        "references/sdd-3-manage-tasks.md",
        "references/sdd-4-validate-spec-implementation.md",
    ]

    for referenced_path in referenced_paths:
        assert (SKILL_DIR / referenced_path).is_file()


def test_skill_payload_does_not_use_legacy_slash_commands_for_continuation():
    payload = read_skill_payload()

    forbidden_continuation_patterns = [
        r"`/SDD-[^`]+`",
        r"reply with:\s*\n\s*`/SDD-",
        r"continue .*?/SDD-",
    ]

    for pattern in forbidden_continuation_patterns:
        assert not re.search(pattern, payload, re.IGNORECASE)


def test_phase_3_requires_first_run_git_and_workspace_hygiene():
    phase_3 = (REFERENCE_DIR / "sdd-3-manage-tasks.md").read_text().lower()

    assert "first-run" in phase_3
    assert "git status" in phase_3
    assert "workspace" in phase_3
    assert "dirty" in phase_3
