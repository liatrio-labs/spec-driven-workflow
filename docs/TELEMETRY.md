# SDD Workflow Telemetry (coarse phase-level)

The SDD skill can emit one OpenTelemetry event per invocation describing the
detected lifecycle phase. It is **off by default** (no endpoint configured = no
emission) and is designed to be invisible to the workflow itself.

## How it works

`scripts/assess-sdd-state.py` already runs on every skill invocation to detect
the current phase. After it prints its routing JSON to stdout, it calls
`emit_phase_event(...)` in `scripts/emit_sdd_event.py`, which POSTs a single
OTLP/HTTP log record to your collector. Because emission is anchored to this
existing deterministic step, it adds **no instructions to `SKILL.md`** and does
not change the model's working context or the artifacts it produces.

One `sdd.phase.detected` event is emitted per invocation. Since one invocation
corresponds to one phase, this gives coarse phase-entry telemetry. Re-invoking
within the same phase emits another event; dedupe or derive transitions in your
backend if you want clean phase boundaries.

## Export modes

When enabled, the emitter picks a destination by this precedence:

1. **OTLP endpoint configured** -> POST the event to your collector.
2. **No endpoint** -> append the event to a local JSON file (for testing and
   validation). The file holds newline-delimited JSON (JSONL): one complete OTLP
   payload per line, append-only, so it never corrupts across runs.

To get total silence (neither POST nor file), set `SDD_OTEL_ENABLED=false`.

> Note: because the file fallback is active whenever telemetry is enabled and no
> endpoint is set, running the skill without a collector now creates
> `sdd-otel-events.jsonl` in the workspace. Add it to `.gitignore`, or set
> `SDD_OTEL_ENABLED=false` where you want no output at all.

### Validating the local file

```bash
# run the assessor with no endpoint set, then inspect the captured events
python3 skill/scripts/assess-sdd-state.py .
cat sdd-otel-events.jsonl | python3 -m json.tool   # or: jq . sdd-otel-events.jsonl
```

## Event shape

- Signal: OTLP logs (`<endpoint>/v1/logs`)
- Body / `event.name`: `sdd.phase.detected`
- `traceId`: deterministic per `repo:feature`, so all events for one feature
  correlate without cross-process trace context propagation
- Attributes (metadata only -- never spec content): `workflow`, `phase`,
  `detailed_state`, `action`, `sequence`, `total_active_specs`, `repo`,
  and `feature` (omittable, see below)

## Configuration (environment variables)

| Variable | Default | Purpose |
| --- | --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | _(unset)_ | Base collector endpoint; logs go to `<endpoint>/v1/logs`. Unset = telemetry off. |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | _(unset)_ | Full logs endpoint, used as-is if set (overrides the base). |
| `OTEL_EXPORTER_OTLP_HEADERS` | _(unset)_ | `key1=val1,key2=val2`, e.g. auth headers. |
| `OTEL_SERVICE_NAME` | `sdd-workflow` | `service.name` resource attribute. |
| `SDD_OTEL_ENABLED` | `true` | Master on/off toggle. Set `false` for total silence (no POST, no file). |
| `SDD_OTEL_FILE` | `./sdd-otel-events.jsonl` | Local fallback path, used only when no OTLP endpoint is configured. |
| `SDD_OTEL_INCLUDE_FEATURE` | `true` | Set `false` to omit the feature slug for sensitive specs (correlation still works via the hashed trace id). |
| `SDD_OTEL_TIMEOUT` | `2` | POST timeout in seconds. |
| `SDD_OTEL_DEBUG` | `false` | `true` prints one diagnostic line to **stderr** (never stdout). |

## Verifying connectivity

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=https://your-collector:4318
SDD_OTEL_DEBUG=true python3 skill/scripts/emit_sdd_event.py --selftest
```

## Safety guarantees

- Never writes to stdout (protects the assessor's routing JSON).
- Never raises (telemetry failure cannot break a spec-driven dev run).
- Stdlib only (no pip installs; works in locked-down/offline environments,
  where it simply no-ops).
- Emits metadata only; spec, task, audit, and validation file contents are
  never sent.
