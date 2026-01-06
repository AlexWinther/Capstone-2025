from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps
from llm.nodes.expand_subqueries_node import expand_subqueries_node


@dataclass()
class ExpandSubqueries(BaseNode[AgentState, AgentDeps]):
    """ExpandSubqueriesNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state

        deps = ctx.deps

        print("expand_subqueries_node: called")

        # taken from llm\StategraphAgent.py l121 to 128
        print(
            {
                "thought": "Splitting query into subqueries...",
                "is_final": False,
                "final_content": None,
            }
        )
        new_state = expand_subqueries_node(
            {
                "qc_tool_result": state.qc_tool_result,
            }
        )

        state.subqueries = new_state.get("subqueries", None)

        return UpdatePapersByProject()


from llm_pydantic.nodes.update_papers_by_project import UpdatePapersByProject  # noqa: E402
