from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm_pydantic.state import AgentOutput, AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps

from llm.nodes.out_of_scope_handler import out_of_scope_handler_node  # noqa: E402  # isort:skip


@dataclass()
class OutOfScopeHandler(BaseNode[AgentState, AgentDeps]):
    """OutOfScopeHandlerNode."""

    async def run(
        self, ctx: GraphRunContext[AgentState, AgentDeps]
    ) -> End[AgentOutput]:  # ty:ignore[invalid-method-override]
        print("out_of_scope_handler_node: called")

        state = {
            "user_query": ctx.state.user_query,
            "qc_decision_reason": ctx.state.qc_decision,
        }

        # taken from llm\StategraphAgent.py l99 to 119
        print(
            {
                "thought": "Query determined to be out of scope. Generating explanation...",
                "is_final": False,
                "final_content": None,
            }
        )

        state = out_of_scope_handler_node()

        ctx.state.out_of_scope_message = state.get("out_of_scope_message")
        ctx.state.requires_user_input = state.get("requires_user_input", True)
        ctx.state.error = state.get("error")

        # Return out-of-scope message
        out_of_scope_message = ctx.state.out_of_scope_message
        print(
            {
                "thought": "Query rejected as out of scope. Please provide a new query.",
                "is_final": True,
                "final_content": json.dumps(
                    {
                        "type": "out_of_scope",
                        "message": out_of_scope_message,
                        "requires_user_input": True,
                    }
                ),
            }
        )

        return End(AgentOutput("out of scope"))
