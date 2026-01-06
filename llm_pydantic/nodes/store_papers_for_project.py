from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm.nodes.store_papers_for_project_node import store_papers_for_project_node
from llm_pydantic.state import AgentOutput, AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class StorePapersForProject(BaseNode[AgentState, AgentDeps]):
    """StorePapersForProjectNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state
        deps = ctx.deps

        print("store_papers_for_project_node: called")

        # taken from llm\StategraphAgent.py l177 to 189
        # Final step: store papers for project
        print(
            {
                "thought": "Storing recommended papers for this project...",
                "is_final": False,
                "final_content": None,
            }
        )
        new_state = store_papers_for_project_node(
            {
                "project_id": state.project_id,
                "papers_filtered": state.papers_filtered,
                "papers_raw": state.papers_raw,
                "user_query": state.user_query,
            }
        )

        state.store_papers_for_project_result = new_state.get(
            "store_papers_for_project_result"
        )

        # corrected key name, this was wrong in the stategraph before
        store_result = state.store_papers_for_project_result
        print(
            {
                "thought": "Agent workflow complete.",
                "is_final": True,
                "final_content": json.dumps({"status": store_result}),
            }
        )

        return End(AgentOutput(status="finished"))
