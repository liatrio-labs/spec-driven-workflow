"""Helper tools for the Spec-Driven Development MCP server.

This module provides tools for:
- Listing workspace artifacts (specs, tasks)
- Creating spec stubs
- Summarizing diffs between versions
"""

from typing import Literal

from fastmcp import Context

from .config import config


def _list_directory_artifacts(artifact_dir, artifact_label: str) -> list[str]:
    """Helper to list artifacts in a directory.

    Args:
        artifact_dir: Directory to search for artifacts
        artifact_label: Label for the artifact type

    Returns:
        List of formatted result strings
    """
    results = []
    if artifact_dir.exists():
        artifacts = sorted(artifact_dir.glob("*.md"))
        if artifacts:
            results.append(f"{artifact_label} ({len(artifacts)}):")
            for artifact in artifacts:
                results.append(f"  - {artifact.name}")
        else:
            results.append(f"{artifact_label}: (none)")
    else:
        results.append(f"{artifact_label}: (directory not found)")
    return results


def list_artifacts(
    ctx: Context,
    artifact_type: Literal["specs", "tasks", "all"] = "all",
) -> str:
    """List artifacts in the workspace.

    Args:
        ctx: MCP context
        artifact_type: Type of artifacts to list (specs, tasks, or all)

    Returns:
        Formatted string listing the artifacts found
    """
    workspace = config.workspace_root
    results = []

    if artifact_type in ("specs", "all"):
        results.extend(_list_directory_artifacts(workspace / "specs", "Specs"))

    if artifact_type in ("tasks", "all"):
        results.extend(_list_directory_artifacts(workspace / "tasks", "Tasks"))

    if not results:
        return "No artifacts found."

    return "\n".join(results)


def create_spec_stub(
    ctx: Context,
    feature_name: str,
    spec_number: int | None = None,
) -> str:
    """Create a spec stub file in the workspace.

    Args:
        ctx: MCP context
        feature_name: Name of the feature (used in filename)
        spec_number: Optional spec number (auto-incremented if not provided)

    Returns:
        Path to the created spec file
    """
    workspace = config.workspace_root
    specs_dir = workspace / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)

    # Auto-increment spec number if not provided
    if spec_number is None:
        existing_specs = list(specs_dir.glob("[0-9][0-9][0-9][0-9]-spec-*.md"))
        if existing_specs:
            numbers = []
            for spec in existing_specs:
                try:
                    num = int(spec.name[:4])
                    numbers.append(num)
                except ValueError:
                    continue
            spec_number = max(numbers) + 1 if numbers else 1
        else:
            spec_number = 1

    # Create filename
    safe_feature_name = feature_name.lower().replace(" ", "-")
    filename = f"{spec_number:04d}-spec-{safe_feature_name}.md"
    spec_path = specs_dir / filename

    # Create stub content
    stub_content = f"""# Spec: {feature_name}

## Goals
[Describe the primary goals of this feature]

## Demoable Units of Work
1. [First demoable slice]
2. [Second demoable slice]

## Functional Requirements
- [Requirement 1]
- [Requirement 2]

## Non-Goals
- [What this spec explicitly does not cover]

## Success Metrics
- [How success will be measured]

## Open Questions
- [Any unresolved questions]
"""

    spec_path.write_text(stub_content, encoding="utf-8")
    ctx.info(f"Created spec stub: {spec_path}")

    return str(spec_path)


def summarize_diff(
    ctx: Context,
    file_path: str,
    base_content: str,
    modified_content: str,
) -> str:
    """Summarize the differences between two versions of a file.

    Args:
        ctx: MCP context
        file_path: Path to the file being compared
        base_content: Original content
        modified_content: Modified content

    Returns:
        Human-readable summary of changes
    """
    base_lines = base_content.splitlines()
    modified_lines = modified_content.splitlines()

    # Simple diff calculation
    added = len(modified_lines) - len(base_lines)
    summary_parts = [f"File: {file_path}"]

    # Line count changes
    if added > 0:
        summary_parts.append(f"  Lines added: {added}")
    elif added < 0:
        summary_parts.append(f"  Lines removed: {abs(added)}")
    else:
        summary_parts.append("  Lines changed (no net change)")

    # Character count changes
    base_chars = len(base_content)
    modified_chars = len(modified_content)
    char_diff = modified_chars - base_chars
    if char_diff != 0:
        summary_parts.append(
            f"  Characters: {base_chars} → {modified_chars} ({char_diff:+d})"
        )

    # Sample changes (first few different lines)
    changes_shown = 0
    max_changes_to_show = 3
    for i, (base_line, mod_line) in enumerate(zip(base_lines, modified_lines, strict=False)):
        if base_line != mod_line and changes_shown < max_changes_to_show:
            summary_parts.append(f"  Line {i+1}:")
            summary_parts.append(f"    - {base_line[:60]}")
            summary_parts.append(f"    + {mod_line[:60]}")
            changes_shown += 1

    return "\n".join(summary_parts)
