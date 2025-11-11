"""Structured logging and observability for the SDD MCP server.

This module provides structured logging capabilities and health endpoints
for monitoring and debugging the MCP server.
"""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from .config import config


class StructuredLogger:
    """Provides structured logging with JSON or text output."""

    def __init__(self, name: str = "sdd-mcp") -> None:
        """Initialize the structured logger.

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))

        # Remove existing handlers
        self.logger.handlers.clear()

        # Add appropriate handler based on format
        handler = logging.StreamHandler(sys.stdout)
        if config.log_format == "json":
            handler.setFormatter(JSONFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )

        self.logger.addHandler(handler)

    def log(
        self,
        level: str,
        message: str,
        **kwargs: Any,
    ) -> None:
        """Log a structured message.

        Args:
            level: Log level (debug, info, warning, error, critical)
            message: Log message
            **kwargs: Additional structured fields
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message, extra={"structured_data": kwargs})

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message."""
        self.log("debug", message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message."""
        self.log("info", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message."""
        self.log("warning", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message."""
        self.log("error", message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message."""
        self.log("critical", message, **kwargs)


class JSONFormatter(logging.Formatter):
    """Custom formatter for JSON-structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        log_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add structured data if available
        if hasattr(record, "structured_data"):
            log_data.update(record.structured_data)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class HealthChecker:
    """Provides health check functionality for the MCP server."""

    def __init__(self) -> None:
        """Initialize the health checker."""
        self.start_time = datetime.now(UTC)
        self.logger = StructuredLogger("health-checker")

    def check_health(self) -> dict[str, Any]:
        """Perform health check of the server.

        Returns:
            Health check results
        """
        uptime = (datetime.now(UTC) - self.start_time).total_seconds()

        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(UTC).isoformat(),
            "uptime_seconds": uptime,
            "checks": {},
        }

        # Check workspace accessibility
        try:
            workspace_exists = config.workspace_root.exists()
            workspace_writable = (
                workspace_exists and config.workspace_root.is_dir()
            )
            workspace_status = "healthy" if workspace_writable else "unhealthy"
            health_status["checks"]["workspace"] = {
                "status": workspace_status,
                "path": str(config.workspace_root),
                "exists": workspace_exists,
                "writable": workspace_writable,
            }
            if workspace_status == "unhealthy":
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["workspace"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["status"] = "degraded"

        # Check prompts directory
        try:
            prompts_exists = config.prompts_dir.exists()
            prompts_readable = prompts_exists and config.prompts_dir.is_dir()
            prompts_status = "healthy" if prompts_readable else "unhealthy"
            health_status["checks"]["prompts"] = {
                "status": prompts_status,
                "path": str(config.prompts_dir),
                "exists": prompts_exists,
                "readable": prompts_readable,
            }
            if prompts_status == "unhealthy":
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["prompts"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["status"] = "degraded"

        # Log health check
        self.logger.info(
            "Health check performed",
            status=health_status["status"],
            uptime=uptime,
        )

        return health_status


# Global instances
logger = StructuredLogger()
health_checker = HealthChecker()
