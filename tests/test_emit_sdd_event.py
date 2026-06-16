import json
import sys
from pathlib import Path

import pytest

script_dir = Path(__file__).parent.parent / "skill" / "scripts"
sys.path.append(str(script_dir))
import emit_sdd_event as emitter  # noqa: E402


@pytest.fixture(autouse=True)
def clean_env(monkeypatch, tmp_path):
    """Start each test with a known-empty telemetry config, and point the local
    fallback at a temp file so stray emits never litter the repo."""
    for var in [
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT",
        "OTEL_EXPORTER_OTLP_HEADERS",
        "OTEL_SERVICE_NAME",
        "SDD_OTEL_ENABLED",
        "SDD_OTEL_INCLUDE_FEATURE",
        "SDD_OTEL_DEBUG",
    ]:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("SDD_OTEL_FILE", str(tmp_path / "events.jsonl"))
    yield


def _sample_result(phase=2, feature="auth", sequence="01"):
    return {
        "specs_directory": "/work/repo/docs/specs",
        "active_specs": [{"feature": feature}],
        "selected": {
            "phase": phase,
            "detailed_state": "S2_START",
            "action": "Generate Task List (Phase 2)",
            "feature": feature,
            "sequence": sequence,
        },
    }


def test_no_endpoint_writes_local_file(tmp_path, monkeypatch):
    # No endpoint configured -> append the event to the local fallback file.
    path = tmp_path / "out.jsonl"
    monkeypatch.setenv("SDD_OTEL_FILE", str(path))
    assert emitter.emit_phase_event(_sample_result()) is True
    assert path.exists()
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])  # each line is a complete OTLP payload
    record = payload["resourceLogs"][0]["scopeLogs"][0]["logRecords"][0]
    assert record["body"]["stringValue"] == "sdd.phase.detected"


def test_file_fallback_appends(tmp_path, monkeypatch):
    path = tmp_path / "out.jsonl"
    monkeypatch.setenv("SDD_OTEL_FILE", str(path))
    emitter.emit_phase_event(_sample_result(phase=1))
    emitter.emit_phase_event(_sample_result(phase=2))
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 2


def test_file_fallback_creates_parent_dirs(tmp_path, monkeypatch):
    path = tmp_path / "nested" / "dir" / "events.jsonl"
    monkeypatch.setenv("SDD_OTEL_FILE", str(path))
    assert emitter.emit("sdd.phase.detected", {"phase": 1}) is True
    assert path.exists()


def test_emit_never_raises():
    # Even with a totally broken file target, emit must return False, not raise.
    import os as _os

    bad = "/this/path/should/not/be/writable/" + "x" * 5 + "/e.jsonl"
    _os.environ["SDD_OTEL_FILE"] = bad
    try:
        # makedirs may succeed in some sandboxes; the contract is "never raises".
        assert emitter.emit("sdd.phase.detected", {"phase": 1}) in (True, False)
    finally:
        _os.environ.pop("SDD_OTEL_FILE", None)


def test_disabled_toggle_writes_nothing(tmp_path, monkeypatch):
    path = tmp_path / "out.jsonl"
    monkeypatch.setenv("SDD_OTEL_FILE", str(path))
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "https://collector:4318")
    monkeypatch.setenv("SDD_OTEL_ENABLED", "false")
    assert emitter.emit_phase_event(_sample_result()) is False
    assert not path.exists()


def test_logs_endpoint_derivation(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "https://collector:4318/")
    assert emitter._logs_endpoint() == "https://collector:4318/v1/logs"
    monkeypatch.setenv(
        "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", "https://gw/custom/logs"
    )
    assert emitter._logs_endpoint() == "https://gw/custom/logs"


def test_payload_is_valid_otlp_logs_json():
    payload = emitter.build_payload(
        "sdd.phase.detected",
        {"phase": 2, "feature": "auth", "total_active_specs": 1},
        feature="auth",
        repo="repo",
    )
    # round-trips as JSON
    json.dumps(payload)
    record = payload["resourceLogs"][0]["scopeLogs"][0]["logRecords"][0]
    assert record["body"]["stringValue"] == "sdd.phase.detected"
    # trace id is 16 bytes (32 hex chars) and deterministic for the same inputs
    assert len(record["traceId"]) == 32
    assert (
        record["traceId"]
        == emitter.build_payload("x", {}, feature="auth", repo="repo")[
            "resourceLogs"
        ][0]["scopeLogs"][0]["logRecords"][0]["traceId"]
    )
    # span id is 8 bytes (16 hex chars)
    assert len(record["spanId"]) == 16
    # int attributes use intValue, strings use stringValue
    attrs = {a["key"]: a["value"] for a in record["attributes"]}
    assert attrs["phase"] == {"intValue": 2}
    assert attrs["feature"] == {"stringValue": "auth"}


def test_feature_can_be_excluded(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "https://collector:4318")
    monkeypatch.setenv("SDD_OTEL_INCLUDE_FEATURE", "false")
    captured = {}

    def fake_emit(event_name, attributes, feature=None, repo=None):
        captured["attributes"] = attributes
        return True

    monkeypatch.setattr(emitter, "emit", fake_emit)
    emitter.emit_phase_event(_sample_result(feature="classified-thing"))
    assert "feature" not in captured["attributes"]


def test_header_parsing(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_HEADERS", "Authorization=Bearer x,team=core")
    headers = emitter._parse_headers()
    assert headers["Authorization"] == "Bearer x"
    assert headers["team"] == "core"
    assert headers["Content-Type"] == "application/json"
