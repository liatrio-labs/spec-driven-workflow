"""Sampling orchestrator for requesting client-generated summaries.

This module provides functionality to request summaries and analysis
from connected MCP clients using the sampling protocol.
"""


from fastmcp import Context


class SamplingOrchestrator:
    """Orchestrates sampling requests to connected MCP clients."""

    async def request_summary(
        self,
        ctx: Context,
        content: str,
        max_tokens: int = 500,
    ) -> str:
        """Request a summary of content from the client.

        Args:
            ctx: MCP context for making sampling requests
            content: Content to summarize
            max_tokens: Maximum tokens for the summary

        Returns:
            Generated summary from the client
        """
        prompt = f"""Please provide a concise summary of the following content:

{content}

Keep the summary under {max_tokens} tokens."""

        try:
            result = await ctx.sample(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )

            if hasattr(result, "content") and hasattr(result.content, "text"):
                return result.content.text
            elif isinstance(result, dict):
                return result.get("content", {}).get("text", "No summary generated")
            else:
                return str(result)
        except Exception as e:
            ctx.error(f"Sampling request failed: {e}")
            return f"Error requesting summary: {e}"

    async def request_analysis(
        self,
        ctx: Context,
        content: str,
        analysis_type: str = "general",
        max_tokens: int = 1000,
    ) -> str:
        """Request an analysis of content from the client.

        Args:
            ctx: MCP context for making sampling requests
            content: Content to analyze
            analysis_type: Type of analysis requested (general, technical, etc.)
            max_tokens: Maximum tokens for the analysis

        Returns:
            Generated analysis from the client
        """
        prompt_templates = {
            "general": "Provide a general analysis of the following content:",
            "technical": "Provide a technical analysis focusing on implementation details:",
            "requirements": "Analyze the requirements and identify gaps or ambiguities:",
            "risks": "Identify potential risks and concerns in the following:",
        }

        prompt_intro = prompt_templates.get(
            analysis_type, prompt_templates["general"]
        )
        prompt = f"""{prompt_intro}

{content}

Provide detailed insights and recommendations."""

        try:
            result = await ctx.sample(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )

            if hasattr(result, "content") and hasattr(result.content, "text"):
                return result.content.text
            elif isinstance(result, dict):
                return result.get("content", {}).get("text", "No analysis generated")
            else:
                return str(result)
        except Exception as e:
            ctx.error(f"Sampling request failed: {e}")
            return f"Error requesting analysis: {e}"

    async def request_comparison(
        self,
        ctx: Context,
        content1: str,
        content2: str,
        comparison_focus: str = "differences",
        max_tokens: int = 750,
    ) -> str:
        """Request a comparison of two pieces of content from the client.

        Args:
            ctx: MCP context for making sampling requests
            content1: First content to compare
            content2: Second content to compare
            comparison_focus: Focus of comparison (differences, similarities, evolution)
            max_tokens: Maximum tokens for the comparison

        Returns:
            Generated comparison from the client
        """
        prompt = f"""Compare the following two pieces of content, focusing on {comparison_focus}:

Content 1:
{content1}

Content 2:
{content2}

Provide a clear comparison highlighting key points."""

        try:
            result = await ctx.sample(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )

            if hasattr(result, "content") and hasattr(result.content, "text"):
                return result.content.text
            elif isinstance(result, dict):
                return result.get("content", {}).get("text", "No comparison generated")
            else:
                return str(result)
        except Exception as e:
            ctx.error(f"Sampling request failed: {e}")
            return f"Error requesting comparison: {e}"


# Global orchestrator instance
orchestrator = SamplingOrchestrator()
