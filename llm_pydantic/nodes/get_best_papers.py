from __future__ import annotations

import logging
from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.tools.Tools_aggregator import get_tools
from llm_pydantic.node_logger import NodeLogger
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps

logger = logging.getLogger("get_best_papers_node")
logger.setLevel(logging.WARNING)

# --- Get Best Papers Node ---


node_logger = NodeLogger(
    "get_best_papers",
    input_keys=["project_id", "has_filter_instructions"],
    output_keys=["papers_raw", "error"],
)


@dataclass()
class GetBestPapers(BaseNode[AgentState, AgentDeps]):
    """
    Retrieve the most relevant papers for a project based on filter instructions.
    Args:
        state (dict): The current agent state.
    Returns:
        dict: Updated state with papers_raw.
    """

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> FilterPapers:
        print("get_best_papers_node: called")

        state = {
            "project_id": ctx.state.project_id,
            "has_filter_instructions": ctx.state.has_filter_instructions,
        }
        # Step 5: Get best papers
        print(
            {
                "thought": "Retrieving most relevant papers...",
                "is_final": False,
                "final_content": None,
            }
        )

        node_logger.log_begin(state)

        # begin llm\nodes\get_best_papers.py
        tools = get_tools()
        tool_map = {getattr(tool, "name", None): tool for tool in tools}
        get_best_papers_tool = tool_map.get("get_best_papers")
        papers_raw = []
        try:
            # Prefer keywords if available, else use user_query

            project_id = state.get("project_id", "")

            # Determine retrieval count based on filter instructions
            has_filter_instructions = state.get("has_filter_instructions", False)
            retrieval_count = (
                50 if has_filter_instructions else 10
            )  # More papers if filtering will be applied

            if get_best_papers_tool:
                # Use num_candidates parameter based on filter instructions
                papers_raw = get_best_papers_tool.invoke(
                    {"project_id": project_id, "num_candidates": retrieval_count}
                )

                logger.info(
                    f"Retrieved {len(papers_raw)} papers (filter instructions: {has_filter_instructions}, requested: {retrieval_count})"
                )

            state["papers_raw"] = papers_raw
        except Exception as e:
            state["error"] = f"Get best papers node error: {e}"

        # end llm\nodes\get_best_papers.py

        node_logger.log_end(state)

        ctx.state.papers_raw = state.get("papers_raw", [])
        ctx.state.error = state.get("error", None)

        return FilterPapers()


from llm_pydantic.nodes.filter_papers import FilterPapers  # noqa: E402 # isort:skip
