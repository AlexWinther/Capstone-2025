from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class OutOfScopeHandler(BaseNode[AgentState, AgentDeps]):
    """OutOfScopeHandlerNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state
        deps = ctx.deps

        print("out_of_scope_handler_node: called")

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

        return End()
