from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.node_logger import NodeLogger
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps

logger = logging.getLogger("expand_subqueries_node")
logger.setLevel(logging.WARNING)


node_logger = NodeLogger(
    "filter_papers",
    input_keys=["user_query", "papers_raw", "has_filter_instructions"],
    output_keys=["papers_filtered", "applied_filter_criteria", "error"],
)


@dataclass()
class ExpandSubqueries(BaseNode[AgentState, AgentDeps]):
    """
    If the QC decision was 'split', extract subqueries and keywords from the multi_step_reasoning tool result.
    Args:
        state (dict): The current agent state.
    Returns:
        dict: Updated state with extracted subqueries.
    """

    async def run(
        self, ctx: GraphRunContext[AgentState, AgentDeps]
    ) -> UpdatePapersByProject:
        print("expand_subqueries_node: called")
        state = {
            "qc_tool_result": ctx.state.qc_tool_result,
        }

        # taken from llm\StategraphAgent.py l121 to 128
        print(
            {
                "thought": "Splitting query into subqueries...",
                "is_final": False,
                "final_content": None,
            }
        )

        node_logger.log_begin(state)

        # begin llm\nodes\expand_subqueries_node.py
        qc_tool_result = state.get("qc_tool_result")
        subqueries = []
        if qc_tool_result:
            try:
                parsed = (
                    json.loads(qc_tool_result)
                    if isinstance(qc_tool_result, str)
                    else qc_tool_result
                )
                if parsed.get("status") == "success" and "subqueries" in parsed:
                    for sub in parsed["subqueries"]:
                        subqueries.append(
                            {
                                "description": sub.get("sub_description", ""),
                                "keywords": sub.get("keywords", []),
                            }
                        )
            except Exception as e:
                logger.error(f"Error parsing subqueries: {e}")
        state["subqueries"] = subqueries
        logger.info(f"Extracted {len(subqueries)} subqueries from split.")
        # end llm\nodes\expand_subqueries_node.py

        node_logger.log_end(state)

        ctx.state.subqueries = state.get("subqueries", None)

        return UpdatePapersByProject()


from llm_pydantic.nodes.update_papers_by_project import (  # noqa: E402
    UpdatePapersByProject,
)
