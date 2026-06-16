#!/usr/bin/env python3
"""Coarse phase-level OpenTelemetry emitter for the SDD workflow.

Design contract (do not break):
  * Zero third-party dependencies (stdlib only) so the skill stays portable
    across Kiro, Amazon Q, Codex, and Claude Code in locked-down environments.
  * NEVER write to stdout. The orchestrator parses the assessor's stdout as
    JSON; any stray byte there corrupts routing. Diagnostics go to stderr and
    ONLY when SDD_OTEL_DEBUG is truthy.
  * NEVER raise. Telemetry failures must not break a spec-driven dev run.
  * Emit metadata only (phase, state, feature slug, counts) -- never spec content.

Export mode precedence (when enabled):
  1. An OTLP endpoint is configured -> POST the event over OTLP/HTTP.
  2. Otherwise -> append the event to a local JSON file (testing/validation).
  Set SDD_OTEL_ENABLED=false for total silence (neither POST nor file).

Configuration (the "central location", fully parameterized via env):
  OTEL_EXPORTER_OTLP_ENDPOINT       base endpoint, e.g. https://collector:4318
                                    (logs are POSTed to <endpoint>/v1/logs)
  OTEL_EXPORTER_OTLP_LOGS_ENDPOINT  full logs endpoint, used as-is if set
  OTEL_EXPORTER_OTLP_HEADERS        "k1=v1,k2=v2" (e.g. auth headers)
  OTEL_SERVICE_NAME                 service.name resource attr (default sdd-workflow)
  SDD_OTEL_ENABLED                  "true"/"false" master toggle (default true)
  SDD_OTEL_FILE                     local fallback path (default ./sdd-otel-events.jsonl);
                                    used only when no OTLP endpoint is configured
  SDD_OTEL_INCLUDE_FEATURE          "true"/"false" include feature slug (default true)
  SDD_OTEL_TIMEOUT                  POST timeout seconds (default 2)
  SDD_OTEL_DEBUG                    "true" to print one diagnostic line to stderr

The local fallback writes newline-delimited JSON (JSONL): one complete OTLP
payload per line, append-only, so it stays valid and corruption-free across runs.
"""
import hashlib
import json
import os
import sys
import time
import urllib.request


def _truthy(name, default="true"):
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def _debug(msg):
    if _truthy("SDD_OTEL_DEBUG", "false"):
        print(f"[sdd-otel] {msg}", file=sys.stderr)


def _attr(key, value):
    """Build one OTLP KeyValue. ints -> intValue, everything else -> stringValue."""
    if isinstance(value, bool):
        return {"key": key, "value": {"boolValue": value}}
    if isinstance(value, int):
        return {"key": key, "value": {"intValue": value}}
    return {"key": key, "value": {"stringValue": str(value)}}


def _trace_id(feature, repo):
    """Deterministic 16-byte trace id so events for one feature correlate across
    invocations / chats / processes without live context propagation."""
    seed = f"{repo or 'sdd'}:{feature or 'new'}".encode()
    return hashlib.sha256(seed).digest()[:16].hex()


def _logs_endpoint():
    explicit = os.getenv("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", "").strip()
    if explicit:
        return explicit
    base = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if not base:
        return None
    return base.rstrip("/") + "/v1/logs"


def _parse_headers():
    headers = {"Content-Type": "application/json"}
    raw = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")
    for pair in raw.split(","):
        if "=" in pair:
            k, _, v = pair.partition("=")
            k, v = k.strip(), v.strip()
            if k:
                headers[k] = v
    return headers


def _event_file():
    return os.getenv("SDD_OTEL_FILE", "").strip() or "sdd-otel-events.jsonl"


def _write_file(payload):
    """Append one OTLP payload as a JSON line to the local fallback file.
    Returns True on success. Never raises."""
    path = _event_file()
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload) + "\n")
        _debug(f"wrote event to {path}")
        return True
    except Exception as exc:  # noqa: BLE001
        _debug(f"file write skipped ({type(exc).__name__}: {exc})")
        return False


def build_payload(event_name, attributes, feature=None, repo=None):
    """Pure function (no I/O) that builds the OTLP/HTTP logs JSON body.
    Factored out so it is unit-testable without a collector."""
    now = str(time.time_ns())
    record = {
        "timeUnixNano": now,
        "observedTimeUnixNano": now,
        "severityNumber": 9,  # INFO
        "severityText": "INFO",
        "body": {"stringValue": event_name},
        "attributes": [_attr("event.name", event_name)]
        + [_attr(k, v) for k, v in attributes.items()],
        "traceId": _trace_id(feature, repo),
        "spanId": os.urandom(8).hex(),
    }
    return {
        "resourceLogs": [
            {
                "resource": {
                    "attributes": [
                        _attr(
                            "service.name",
                            os.getenv("OTEL_SERVICE_NAME", "sdd-workflow"),
                        )
                    ]
                },
                "scopeLogs": [
                    {
                        "scope": {"name": "liatrio.sdd"},
                        "logRecords": [record],
                    }
                ],
            }
        ]
    }


def emit(event_name, attributes, feature=None, repo=None):
    """Fire-and-forget emit. POSTs over OTLP/HTTP when an endpoint is configured,
    otherwise appends to the local JSON fallback file. Returns True on success.
    Never raises; never writes to stdout."""
    try:
        if not _truthy("SDD_OTEL_ENABLED"):
            _debug("disabled via SDD_OTEL_ENABLED")
            return False

        payload = build_payload(event_name, attributes, feature=feature, repo=repo)
        endpoint = _logs_endpoint()

        if not endpoint:
            # No collector configured -> local file fallback for testing/validation.
            return _write_file(payload)

        data = json.dumps(payload).encode("utf-8")
        timeout = float(os.getenv("SDD_OTEL_TIMEOUT", "2"))
        req = urllib.request.Request(
            endpoint, data=data, headers=_parse_headers(), method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            _debug(f"emitted {event_name} -> {endpoint} ({resp.status})")
        return True
    except Exception as exc:  # noqa: BLE001 - telemetry must never break the workflow
        _debug(f"emit skipped ({type(exc).__name__}: {exc})")
        return False


def emit_phase_event(result):
    """Emit one coarse 'sdd.phase.detected' event from an assessor result dict.
    Safe to call unconditionally; no-ops when telemetry is unconfigured."""
    try:
        selected = result.get("selected") or {}
        feature = selected.get("feature")
        try:
            repo = os.path.basename(
                os.path.dirname(os.path.dirname(result.get("specs_directory", "")))
            ) or None
        except Exception:
            repo = None

        attributes = {
            "workflow": "sdd",
            "phase": selected.get("phase", 0),
            "detailed_state": selected.get("detailed_state", "unknown"),
            "action": selected.get("action", "unknown"),
            "sequence": selected.get("sequence") or "none",
            "total_active_specs": len(result.get("active_specs", [])),
        }
        if repo:
            attributes["repo"] = repo
        if _truthy("SDD_OTEL_INCLUDE_FEATURE") and feature:
            attributes["feature"] = feature

        return emit("sdd.phase.detected", attributes, feature=feature, repo=repo)
    except Exception as exc:  # noqa: BLE001
        _debug(f"emit_phase_event skipped ({type(exc).__name__}: {exc})")
        return False


if __name__ == "__main__":
    # Connectivity self-test: `SDD_OTEL_DEBUG=true python3 emit_sdd_event.py --selftest`
    if "--selftest" in sys.argv:
        ok = emit(
            "sdd.telemetry.selftest",
            {"workflow": "sdd", "phase": 0, "detailed_state": "selftest"},
            feature="selftest",
        )
        print("selftest:", "ok" if ok else "skipped/failed", file=sys.stderr)
