# Testing

Run the deterministic skill validation tests and repository quality gates before submitting changes:

```bash
python -m pytest -q
pre-commit run --all-files
```

The pytest suite covers the skill workspace-assessment script and static skill contract checks. These tests keep the new `skill/` install path verifiable without requiring live AI-agent execution.

Promptfoo evaluations are tracked separately from this first skill-install integration milestone. The initial gate is deterministic script behavior plus static skill contract checks.
