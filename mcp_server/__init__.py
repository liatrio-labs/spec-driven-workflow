"""Spec-Driven Development MCP Server.

A FastMCP-based server providing prompts, resources, and tools for
spec-driven development workflows.
"""

from fastmcp import Context, FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

try:
    from __version__ import __version__
except ImportError:
    # Fallback for when installed as a package
    from importlib.metadata import version

    __version__ = version("spec-driven-development-mcp")

from .config import config
from .logging import health_checker, logger
from .prompts_loader import register_prompts
from .tools import create_spec_stub, list_artifacts, summarize_diff


def create_app() -> FastMCP:
    """Create and configure the FastMCP application.

    Returns:
        Configured FastMCP server instance
    """
    # Initialize FastMCP server
    mcp = FastMCP(name="spec-driven-development-mcp")

    logger.info("Initializing Spec-Driven Development MCP server", version=__version__)

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> PlainTextResponse:
        return PlainTextResponse("OK")

    @mcp.custom_route("/mcp/health", methods=["GET"])
    async def mcp_health_check(request: Request) -> JSONResponse:
        """Detailed health check endpoint with readiness information."""
        health_status = health_checker.check_health()
        status_code = 200 if health_status["status"] == "healthy" else 503
        return JSONResponse(health_status, status_code=status_code)

    # Load prompts from the prompts directory and register them
    register_prompts(mcp, config.prompts_dir)

    @mcp.tool(name="basic-example", description="Return a static message for testing.")
    def basic_example_tool() -> str:
        """Basic example tool used to verify MCP tool registration."""
        return "Basic example tool invoked successfully."

    # Register helper tools
    @mcp.tool(
        name="list-artifacts",
        description="List workspace artifacts (specs, tasks, or all)",
    )
    def list_artifacts_tool(
        ctx: Context,
        artifact_type: str = "all",
    ) -> str:
        """List artifacts in the workspace."""
        logger.info("Listing artifacts", artifact_type=artifact_type)
        return list_artifacts(ctx, artifact_type)  # type: ignore

    @mcp.tool(
        name="create-spec-stub",
        description="Create a new spec stub file in the workspace",
    )
    def create_spec_stub_tool(
        ctx: Context,
        feature_name: str,
        spec_number: int | None = None,
    ) -> str:
        """Create a spec stub file."""
        logger.info("Creating spec stub", feature_name=feature_name, spec_number=spec_number)
        return create_spec_stub(ctx, feature_name, spec_number)

    @mcp.tool(
        name="summarize-diff",
        description="Summarize differences between two versions of a file",
    )
    def summarize_diff_tool(
        ctx: Context,
        file_path: str,
        base_content: str,
        modified_content: str,
    ) -> str:
        """Summarize file differences."""
        logger.info("Summarizing diff", file_path=file_path)
        return summarize_diff(ctx, file_path, base_content, modified_content)

    logger.info("MCP server initialized successfully")

    return mcp
