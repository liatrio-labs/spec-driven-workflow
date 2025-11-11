# Operations Guide

This guide covers deployment, configuration, and operation of the Spec-Driven Development MCP server.

## Local Development

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository and navigate to the project directory
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Run tests to verify setup:

   ```bash
   uv run pytest
   ```

### Running the Server

#### STDIO Transport (Default)

The STDIO transport is ideal for local development and integration with MCP clients like Claude Desktop:

```bash
uvx fastmcp run server.py
```

Or using the development server with the MCP Inspector:

```bash
uvx fastmcp dev server.py
```

This will start the server and open the MCP Inspector in your browser, allowing you to:

- Browse available prompts, resources, and tools
- Test prompt invocations
- View server logs and metrics

#### HTTP Transport

For remote access or integration with web-based clients:

```bash
uvx fastmcp run server.py --transport http --port 8000
```

The server will be available at `http://localhost:8000`.

## Configuration

The server can be configured via environment variables:

### Workspace Configuration

- `SDD_WORKSPACE_ROOT`: Root directory for generated specs and tasks (default: `/workspace`)
- `SDD_PROMPTS_DIR`: Directory containing prompt templates (default: `./prompts`)

### Transport Configuration

- `SDD_TRANSPORT`: Transport type - `stdio` or `http` (default: `stdio`)
- `SDD_HTTP_HOST`: HTTP server host (default: `0.0.0.0`)
- `SDD_HTTP_PORT`: HTTP server port (default: `8000`)

### Logging Configuration

- `SDD_LOG_LEVEL`: Logging level - `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`)
- `SDD_LOG_FORMAT`: Log format - `json` or `text` (default: `json`)

### CORS Configuration (HTTP only)

- `SDD_CORS_ENABLED`: Enable CORS (default: `true`)
- `SDD_CORS_ORIGINS`: Comma-separated list of allowed origins (default: `*`)

### Example

```bash
export SDD_WORKSPACE_ROOT=/home/user/workspace
export SDD_LOG_LEVEL=DEBUG
uvx fastmcp run server.py
```

## MCP Client Integration

### Claude Desktop

Add the following to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "spec-driven-development": {
      "command": "uvx",
      "args": ["fastmcp", "run", "/path/to/spec-driven-development-mcp/server.py"]
    }
  }
}
```

### VS Code MCP Plugin

1. Install the MCP plugin for VS Code
2. Add the server configuration to your workspace settings:

   ```json
   {
     "mcp.servers": {
       "spec-driven-development": {
         "command": "uvx",
         "args": ["fastmcp", "run", "/path/to/spec-driven-development-mcp/server.py"]
       }
     }
   }
   ```

### FastMCP Inspector

The FastMCP Inspector provides a web-based interface for testing and debugging:

```bash
uvx fastmcp dev server.py
```

This will:

1. Start the MCP server
2. Start the Inspector proxy
3. Open the Inspector UI in your browser

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run with Coverage

```bash
uv run pytest --cov=mcp_server --cov=slash_commands --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the detailed coverage report.

```bash
uv run pytest tests/test_prompts.py -v
```

## Observability and Monitoring

### Health Endpoints

The SDD MCP server provides health check endpoints for monitoring:

#### `/health` - Basic Health Check

Simple health check endpoint that returns `OK` when the server is running.

```bash
curl http://localhost:8000/health
```

Response: `OK`

#### `/mcp/health` - Detailed Readiness Check

Comprehensive health check with detailed status information about server components.

```bash
curl http://localhost:8000/mcp/health
```

Example healthy response:

```json
{
  "status": "healthy",
  "timestamp": "2025-11-11T18:10:21.614Z",
  "uptime_seconds": 123.45,
  "checks": {
    "workspace": {
      "status": "healthy",
      "path": "/workspace",
      "exists": true,
      "writable": true
    },
    "prompts": {
      "status": "healthy",
      "path": "/path/to/prompts",
      "exists": true,
      "readable": true
    }
  }
}
```

Example degraded response (HTTP 503):

```json
{
  "status": "degraded",
  "timestamp": "2025-11-11T18:10:21.614Z",
  "uptime_seconds": 123.45,
  "checks": {
    "workspace": {
      "status": "unhealthy",
      "path": "/workspace",
      "exists": false,
      "writable": false
    },
    "prompts": {
      "status": "healthy",
      "path": "/path/to/prompts",
      "exists": true,
      "readable": true
    }
  }
}
```

### Structured Logging

The server uses structured logging to provide detailed operational insights. Logs can be configured via environment variables:

- `SDD_LOG_LEVEL`: Set log level (DEBUG, INFO, WARNING, ERROR)
- `SDD_LOG_FORMAT`: Choose output format (json or text)

#### JSON Format (Default)

```json
{
  "timestamp": "2025-11-11T18:10:21.614Z",
  "level": "INFO",
  "logger": "sdd-mcp",
  "message": "MCP server initialized successfully",
  "module": "__init__",
  "function": "create_app",
  "line": 95,
  "version": "1.8.0"
}
```

#### Text Format

```
2025-11-11 18:10:21,614 - sdd-mcp - INFO - MCP server initialized successfully
```

### Helper Tools

The server exposes the following helper tools for workspace management:

#### `list-artifacts`

List workspace artifacts (specs, tasks, or all).

Parameters:
- `artifact_type`: Type of artifacts to list ("specs", "tasks", or "all")

Example output:
```
Specs (2):
  - 0001-spec-user-auth.md
  - 0002-spec-api-gateway.md
Tasks (1):
  - tasks-0001-spec-user-auth.md
```

#### `create-spec-stub`

Create a new spec stub file in the workspace.

Parameters:
- `feature_name`: Name of the feature (used in filename)
- `spec_number`: Optional spec number (auto-incremented if not provided)

Example output:
```
/workspace/specs/0003-spec-new-feature.md
```

#### `summarize-diff`

Summarize differences between two versions of a file.

Parameters:
- `file_path`: Path to the file being compared
- `base_content`: Original content
- `modified_content`: Modified content

Example output:
```
File: test.txt
  Lines added: 2
  Characters: 100 → 150 (+50)
  Line 1:
    - original line
    + modified line
```

### Notifications

The server broadcasts notifications when workspace artifacts change:

- `notify_spec_created`: Emitted when a new spec is created
- `notify_spec_modified`: Emitted when a spec is modified
- `notify_spec_deleted`: Emitted when a spec is deleted
- `notify_task_created`: Emitted when a new task is created
- `notify_task_modified`: Emitted when a task is modified
- `notify_task_deleted`: Emitted when a task is deleted

All notifications trigger a `resource_list_changed` event to notify MCP clients that the resource list should be refreshed.

### Sampling

The server supports MCP sampling protocol for requesting client-generated summaries and analysis:

- `request_summary`: Request a summary of content from the client
- `request_analysis`: Request an analysis (general, technical, requirements, risks)
- `request_comparison`: Request a comparison of two pieces of content

These sampling capabilities enable the server to leverage client AI capabilities for advanced content processing.

## Troubleshooting

### Server Won't Start

1. Verify Python version: `python --version` (should be 3.12+)
2. Reinstall dependencies: `uv sync`
3. Check for port conflicts (if using HTTP transport)

### Prompts Not Loading

1. Verify prompts directory exists and contains `.md` files
2. Check that prompt files have valid YAML frontmatter
3. Review server logs for parsing errors

### Tests Failing

1. Ensure all dependencies are installed: `uv sync`
2. Run tests with verbose output: `uv run pytest -v`
3. Check for environment variable conflicts

### Health Check Issues

1. Check `/mcp/health` endpoint for detailed status
2. Verify workspace directory exists and is writable
3. Verify prompts directory exists and is readable
4. Review structured logs for error details
