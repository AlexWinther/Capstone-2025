from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class StorePapersForProject(BaseNode[AgentState, AgentDeps]):
    """StorePapersForProjectNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state
        deps = ctx.deps

        print("store_papers_for_project_node: called")

        store_result = state.get("store_papers_result", "No result")
        print(
            {
                "thought": "Agent workflow complete.",
                "is_final": True,
                "final_content": json.dumps({"status": store_result}),
            }
        )

        return End()
