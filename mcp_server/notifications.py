"""Notification broadcaster for workspace file events.

This module provides functionality to emit notifications when workspace
artifacts (specs, tasks) are created, modified, or deleted.
"""

from pathlib import Path
from typing import Literal

from fastmcp import Context

from .config import config

EventType = Literal["created", "modified", "deleted"]


class NotificationBroadcaster:
    """Broadcasts workspace file events to connected MCP clients."""

    def __init__(self) -> None:
        """Initialize the notification broadcaster."""
        self.workspace_root = config.workspace_root

    def notify_artifact_change(
        self,
        ctx: Context,
        artifact_type: Literal["spec", "task"],
        event_type: EventType,
        file_path: Path,
    ) -> None:
        """Notify clients about artifact changes.

        Args:
            ctx: MCP context for sending notifications
            artifact_type: Type of artifact (spec or task)
            event_type: Type of event (created, modified, deleted)
            file_path: Path to the affected file
        """
        ctx.info(f"Artifact {event_type}: {artifact_type} - {file_path.name}")

        # Send resource list changed notification to MCP clients
        # This signals that the resource list may need to be refreshed
        ctx.send_resource_list_changed()

    def notify_spec_created(self, ctx: Context, spec_path: Path) -> None:
        """Notify clients that a spec was created.

        Args:
            ctx: MCP context
            spec_path: Path to the created spec
        """
        self.notify_artifact_change(ctx, "spec", "created", spec_path)

    def notify_spec_modified(self, ctx: Context, spec_path: Path) -> None:
        """Notify clients that a spec was modified.

        Args:
            ctx: MCP context
            spec_path: Path to the modified spec
        """
        self.notify_artifact_change(ctx, "spec", "modified", spec_path)

    def notify_spec_deleted(self, ctx: Context, spec_path: Path) -> None:
        """Notify clients that a spec was deleted.

        Args:
            ctx: MCP context
            spec_path: Path to the deleted spec
        """
        self.notify_artifact_change(ctx, "spec", "deleted", spec_path)

    def notify_task_created(self, ctx: Context, task_path: Path) -> None:
        """Notify clients that a task was created.

        Args:
            ctx: MCP context
            task_path: Path to the created task
        """
        self.notify_artifact_change(ctx, "task", "created", task_path)

    def notify_task_modified(self, ctx: Context, task_path: Path) -> None:
        """Notify clients that a task was modified.

        Args:
            ctx: MCP context
            task_path: Path to the modified task
        """
        self.notify_artifact_change(ctx, "task", "modified", task_path)

    def notify_task_deleted(self, ctx: Context, task_path: Path) -> None:
        """Notify clients that a task was deleted.

        Args:
            ctx: MCP context
            task_path: Path to the deleted task
        """
        self.notify_artifact_change(ctx, "task", "deleted", task_path)


# Global broadcaster instance
broadcaster = NotificationBroadcaster()
