# Testing

Run the repository quality gate before submitting changes:

```bash
pre-commit run --all-files
```

The pre-commit gate runs the deterministic pytest suite first, then checks YAML syntax, Markdown formatting, spelling, committed secrets, and commit-message format where applicable. The pytest suite covers the skill workspace-assessment script, the phase-level telemetry emitter, and static skill contract checks. These tests keep the new `skill/` install path verifiable without requiring live AI-agent execution.

For the optional OpenTelemetry instrumentation emitted alongside workspace assessment, see [TELEMETRY.md](TELEMETRY.md). It is off by default and never affects routing.

CI runs the same deterministic skill tests explicitly before `pre-commit run --all-files`, so failures are visible as a dedicated CI step and also enforced locally through pre-commit.

Promptfoo evaluations are tracked separately from this first skill-install integration milestone. The initial gate is deterministic script behavior plus static skill contract checks.
