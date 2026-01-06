from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm_pydantic.state import AgentState, AgentOutput
from llm_pydantic.tooling.tooling_mock import AgentDeps
from llm.nodes.out_of_scope_handler_node import out_of_scope_handler_node  # noqa: E402  # isort:skip


@dataclass()
class OutOfScopeHandler(BaseNode[AgentState, AgentDeps]):
    """OutOfScopeHandlerNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state
        deps = ctx.deps

        print("out_of_scope_handler_node: called")

        # taken from llm\StategraphAgent.py l99 to 119
        print(
            {
                "thought": "Query determined to be out of scope. Generating explanation...",
                "is_final": False,
                "final_content": None,
            }
        )

        new_state = out_of_scope_handler_node(
            {
                "user_query": state.user_query,
                "qc_decision_reason": state.qc_decision,
            }
        )

        state.out_of_scope_message = new_state.get("out_of_scope_message")
        state.requires_user_input = new_state.get("requires_user_input", True)
        state.error = new_state.get("error")

        # Return out-of-scope message
        out_of_scope_message = state.out_of_scope_message
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
