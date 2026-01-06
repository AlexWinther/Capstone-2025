from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps
from llm.nodes.expand_subqueries_node import expand_subqueries_node


@dataclass()
class ExpandSubqueries(BaseNode[AgentState, AgentDeps]):
    """ExpandSubqueriesNode."""

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
        state = expand_subqueries_node(state)

        ctx.state.subqueries = state.get("subqueries", None)

        return UpdatePapersByProject()


from llm_pydantic.nodes.update_papers_by_project import UpdatePapersByProject  # noqa: E402
