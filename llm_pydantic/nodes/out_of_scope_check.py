from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class OutOfScopeCheck(BaseNode[AgentState, AgentDeps]):
    """OutOfScopeCheckNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> QualityControl:
        state = ctx.state
        deps = ctx.deps

        print("out_of_scope_check_node: called")

        # Step 2: Out-of-scope check
        print(
            {
                "thought": "Checking if query is within scope...",
                "is_final": False,
                "final_content": None,
            }
        )

        return QualityControl()


from llm_pydantic.nodes.quality_control import QualityControl  # noqa: E402 # isort:skip
