"""Tests for protocol extensions: tools, notifications, sampling, and logging."""

import json
import logging
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastmcp import Context

from mcp_server.logging import HealthChecker, JSONFormatter, StructuredLogger
from mcp_server.notifications import NotificationBroadcaster
from mcp_server.sampling import SamplingOrchestrator
from mcp_server.tools import create_spec_stub, list_artifacts, summarize_diff


class TestHelperTools:
    """Test suite for helper tools."""

    def test_list_artifacts_all(self, temp_workspace):
        """Test listing all artifacts."""
        # Create test artifacts
        (temp_workspace / "specs" / "0001-spec-feature.md").write_text("# Spec")
        (temp_workspace / "tasks" / "tasks-0001-spec-feature.md").write_text("# Tasks")

        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = list_artifacts(ctx, "all")

        assert "Specs (1)" in result
        assert "0001-spec-feature.md" in result
        assert "Tasks (1)" in result
        assert "tasks-0001-spec-feature.md" in result

    def test_list_artifacts_specs_only(self, temp_workspace):
        """Test listing specs only."""
        (temp_workspace / "specs" / "0001-spec-feature.md").write_text("# Spec")
        (temp_workspace / "tasks" / "tasks-0001-spec-feature.md").write_text("# Tasks")

        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = list_artifacts(ctx, "specs")

        assert "Specs (1)" in result
        assert "0001-spec-feature.md" in result
        assert "Tasks" not in result

    def test_list_artifacts_tasks_only(self, temp_workspace):
        """Test listing tasks only."""
        (temp_workspace / "specs" / "0001-spec-feature.md").write_text("# Spec")
        (temp_workspace / "tasks" / "tasks-0001-spec-feature.md").write_text("# Tasks")

        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = list_artifacts(ctx, "tasks")

        assert "Tasks (1)" in result
        assert "tasks-0001-spec-feature.md" in result
        assert "Specs" not in result

    def test_list_artifacts_empty_workspace(self, temp_workspace):
        """Test listing artifacts in empty workspace."""
        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = list_artifacts(ctx, "all")

        assert "Specs: (none)" in result
        assert "Tasks: (none)" in result

    def test_create_spec_stub_with_number(self, temp_workspace):
        """Test creating spec stub with specific number."""
        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = create_spec_stub(ctx, "User Authentication", spec_number=1)

        spec_path = Path(result)
        assert spec_path.exists()
        assert spec_path.name == "0001-spec-user-authentication.md"

        content = spec_path.read_text()
        assert "# Spec: User Authentication" in content
        assert "## Goals" in content
        assert "## Demoable Units of Work" in content
        assert "## Functional Requirements" in content

    def test_create_spec_stub_auto_increment(self, temp_workspace):
        """Test creating spec stub with auto-incremented number."""
        # Create existing specs
        (temp_workspace / "specs" / "0001-spec-existing.md").write_text("# Spec")
        (temp_workspace / "specs" / "0002-spec-another.md").write_text("# Spec")

        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = create_spec_stub(ctx, "New Feature")

        spec_path = Path(result)
        assert spec_path.exists()
        assert spec_path.name == "0003-spec-new-feature.md"

    def test_create_spec_stub_first_spec(self, temp_workspace):
        """Test creating first spec in workspace."""
        ctx = Mock(spec=Context)

        with patch("mcp_server.tools.config.workspace_root", temp_workspace):
            result = create_spec_stub(ctx, "First Feature")

        spec_path = Path(result)
        assert spec_path.exists()
        assert spec_path.name == "0001-spec-first-feature.md"

    def test_summarize_diff_added_lines(self):
        """Test summarizing diff with added lines."""
        ctx = Mock(spec=Context)
        base = "line 1\nline 2"
        modified = "line 1\nline 2\nline 3\nline 4"

        result = summarize_diff(ctx, "test.txt", base, modified)

        assert "test.txt" in result
        assert "Lines added: 2" in result

    def test_summarize_diff_removed_lines(self):
        """Test summarizing diff with removed lines."""
        ctx = Mock(spec=Context)
        base = "line 1\nline 2\nline 3"
        modified = "line 1"

        result = summarize_diff(ctx, "test.txt", base, modified)

        assert "test.txt" in result
        assert "Lines removed: 2" in result

    def test_summarize_diff_modified_lines(self):
        """Test summarizing diff with modified lines."""
        ctx = Mock(spec=Context)
        base = "original line\nstay the same"
        modified = "modified line\nstay the same"

        result = summarize_diff(ctx, "test.txt", base, modified)

        assert "test.txt" in result
        assert "Line 1:" in result
        assert "original line" in result
        assert "modified line" in result


class TestNotificationBroadcaster:
    """Test suite for notification broadcaster."""

    def test_notify_spec_created(self):
        """Test spec created notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        spec_path = Path("/workspace/specs/0001-spec-test.md")

        broadcaster.notify_spec_created(ctx, spec_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()

    def test_notify_spec_modified(self):
        """Test spec modified notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        spec_path = Path("/workspace/specs/0001-spec-test.md")

        broadcaster.notify_spec_modified(ctx, spec_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()

    def test_notify_spec_deleted(self):
        """Test spec deleted notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        spec_path = Path("/workspace/specs/0001-spec-test.md")

        broadcaster.notify_spec_deleted(ctx, spec_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()

    def test_notify_task_created(self):
        """Test task created notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        task_path = Path("/workspace/tasks/tasks-0001-spec-test.md")

        broadcaster.notify_task_created(ctx, task_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()

    def test_notify_task_modified(self):
        """Test task modified notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        task_path = Path("/workspace/tasks/tasks-0001-spec-test.md")

        broadcaster.notify_task_modified(ctx, task_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()

    def test_notify_task_deleted(self):
        """Test task deleted notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        task_path = Path("/workspace/tasks/tasks-0001-spec-test.md")

        broadcaster.notify_task_deleted(ctx, task_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()

    def test_notify_artifact_change(self):
        """Test generic artifact change notification."""
        broadcaster = NotificationBroadcaster()
        ctx = Mock(spec=Context)
        file_path = Path("/workspace/specs/test.md")

        broadcaster.notify_artifact_change(ctx, "spec", "created", file_path)

        ctx.info.assert_called_once()
        ctx.send_resource_list_changed.assert_called_once()


class TestSamplingOrchestrator:
    """Test suite for sampling orchestrator."""

    @pytest.mark.anyio
    async def test_request_summary_success(self):
        """Test successful summary request."""
        orchestrator = SamplingOrchestrator()
        ctx = Mock(spec=Context)

        # Mock the sample method
        mock_result = Mock()
        mock_result.content.text = "This is a summary"
        ctx.sample = AsyncMock(return_value=mock_result)

        result = await orchestrator.request_summary(ctx, "Some long content", max_tokens=100)

        assert result == "This is a summary"
        ctx.sample.assert_called_once()

    @pytest.mark.anyio
    async def test_request_summary_dict_response(self):
        """Test summary request with dict response."""
        orchestrator = SamplingOrchestrator()
        ctx = Mock(spec=Context)

        # Mock the sample method with dict response
        mock_result = {"content": {"text": "Summary from dict"}}
        ctx.sample = AsyncMock(return_value=mock_result)

        result = await orchestrator.request_summary(ctx, "Content to summarize")

        assert result == "Summary from dict"

    @pytest.mark.anyio
    async def test_request_summary_error(self):
        """Test summary request error handling."""
        orchestrator = SamplingOrchestrator()
        ctx = Mock(spec=Context)

        # Mock the sample method to raise an error
        ctx.sample = AsyncMock(side_effect=Exception("API error"))

        result = await orchestrator.request_summary(ctx, "Content to summarize")

        assert "Error requesting summary" in result
        ctx.error.assert_called_once()

    @pytest.mark.anyio
    async def test_request_analysis_general(self):
        """Test general analysis request."""
        orchestrator = SamplingOrchestrator()
        ctx = Mock(spec=Context)

        mock_result = Mock()
        mock_result.content.text = "General analysis result"
        ctx.sample = AsyncMock(return_value=mock_result)

        result = await orchestrator.request_analysis(ctx, "Content to analyze", "general")

        assert result == "General analysis result"

    @pytest.mark.anyio
    async def test_request_analysis_technical(self):
        """Test technical analysis request."""
        orchestrator = SamplingOrchestrator()
        ctx = Mock(spec=Context)

        mock_result = Mock()
        mock_result.content.text = "Technical analysis result"
        ctx.sample = AsyncMock(return_value=mock_result)

        result = await orchestrator.request_analysis(ctx, "Code to analyze", "technical")

        assert result == "Technical analysis result"

    @pytest.mark.anyio
    async def test_request_comparison(self):
        """Test comparison request."""
        orchestrator = SamplingOrchestrator()
        ctx = Mock(spec=Context)

        mock_result = Mock()
        mock_result.content.text = "Comparison result"
        ctx.sample = AsyncMock(return_value=mock_result)

        result = await orchestrator.request_comparison(
            ctx, "Content 1", "Content 2", "differences"
        )

        assert result == "Comparison result"


class TestStructuredLogging:
    """Test suite for structured logging."""

    def test_logger_initialization(self):
        """Test logger initialization."""
        logger = StructuredLogger("test-logger")
        assert logger.logger.name == "test-logger"

    def test_json_formatter(self):
        """Test JSON formatter."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        parsed = json.loads(result)

        assert parsed["level"] == "INFO"
        assert parsed["message"] == "Test message"
        assert "timestamp" in parsed

    def test_json_formatter_with_structured_data(self):
        """Test JSON formatter with structured data."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.structured_data = {"user_id": 123, "action": "login"}

        result = formatter.format(record)
        parsed = json.loads(result)

        assert parsed["user_id"] == 123
        assert parsed["action"] == "login"

    def test_logger_info_method(self):
        """Test logger info method."""
        logger = StructuredLogger("test-logger")

        with patch.object(logger.logger, "info") as mock_info:
            logger.info("Test message", user_id=123)
            mock_info.assert_called_once()

    def test_logger_error_method(self):
        """Test logger error method."""
        logger = StructuredLogger("test-logger")

        with patch.object(logger.logger, "error") as mock_error:
            logger.error("Error message", error_code="E001")
            mock_error.assert_called_once()


class TestHealthChecker:
    """Test suite for health checker."""

    def test_health_check_healthy(self, temp_workspace):
        """Test health check with healthy status."""
        checker = HealthChecker()

        with patch("mcp_server.logging.config.workspace_root", temp_workspace), patch(
            "mcp_server.logging.config.prompts_dir",
            temp_workspace / "prompts",
        ):
            (temp_workspace / "prompts").mkdir()
            result = checker.check_health()

        assert result["status"] == "healthy"
        assert "uptime_seconds" in result
        assert result["checks"]["workspace"]["status"] == "healthy"
        assert result["checks"]["prompts"]["status"] == "healthy"

    def test_health_check_degraded_workspace(self, temp_workspace):
        """Test health check with missing workspace."""
        checker = HealthChecker()

        with (
            patch("mcp_server.logging.config.workspace_root", temp_workspace / "nonexistent"),
            patch("mcp_server.logging.config.prompts_dir", temp_workspace / "prompts"),
        ):
            (temp_workspace / "prompts").mkdir()
            result = checker.check_health()

        assert result["status"] == "degraded"
        assert result["checks"]["workspace"]["status"] == "unhealthy"

    def test_health_check_degraded_prompts(self, temp_workspace):
        """Test health check with missing prompts directory."""
        checker = HealthChecker()

        with patch("mcp_server.logging.config.workspace_root", temp_workspace), patch(
            "mcp_server.logging.config.prompts_dir",
            temp_workspace / "nonexistent",
        ):
            result = checker.check_health()

        assert result["status"] == "degraded"
        assert result["checks"]["prompts"]["status"] == "unhealthy"

    def test_health_check_includes_paths(self, temp_workspace):
        """Test that health check includes path information."""
        checker = HealthChecker()

        with (
            patch("mcp_server.logging.config.workspace_root", temp_workspace),
            patch("mcp_server.logging.config.prompts_dir", temp_workspace / "prompts"),
        ):
            (temp_workspace / "prompts").mkdir()
            result = checker.check_health()

        assert "path" in result["checks"]["workspace"]
        assert "path" in result["checks"]["prompts"]
