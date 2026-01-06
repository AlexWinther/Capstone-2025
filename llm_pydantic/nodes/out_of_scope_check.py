from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.out_of_scope_check_node import out_of_scope_check_node
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps

logger = logging.getLogger("OutOfScopeCheck")
logger.setLevel(logging.WARNING)


@dataclass()
class OutOfScopeCheck(BaseNode[AgentState, AgentDeps]):
    """OutOfScopeCheckNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> QualityControl:
        print("out_of_scope_check_node: called")

        state = {
            "user_query": ctx.state.user_query,
        }

        # Step 2: Out-of-scope check
        print(
            {
                "thought": "Checking if query is within scope...",
                "is_final": False,
                "final_content": None,
            }
        )

        state = out_of_scope_check_node(state)

        ctx.state.out_of_scope_result = state["out_of_scope_result"]
        ctx.state.error = state.get("error", None)

        # taken from llm\StategraphAgent.py l73 to 86
        # Extract keywords from out_of_scope_result if available
        out_of_scope_result = ctx.state.out_of_scope_result
        if out_of_scope_result:
            try:
                parsed = json.loads(out_of_scope_result)
                if parsed.get("status") == "valid" and "keywords" in parsed:
                    ctx.state.keywords = parsed["keywords"]
                    print(
                        {
                            "thought": f"Extracted keywords: {ctx.state.keywords}",
                            "is_final": False,
                            "final_content": None,
                        }
                    )
            except Exception as e:
                logger.error(f"Error parsing out_of_scope_result: {e}")

        return QualityControl()


from llm_pydantic.nodes.quality_control import QualityControl  # noqa: E402 # isort:skip
