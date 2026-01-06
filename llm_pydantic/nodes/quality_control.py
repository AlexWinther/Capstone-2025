from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.quality_control import quality_control_node
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class QualityControl(BaseNode[AgentState, AgentDeps]):
    """QualityControlNode."""

    async def run(
        self, ctx: GraphRunContext[AgentState, AgentDeps]
    ) -> OutOfScopeHandler | ExpandSubqueries | UpdatePapersByProject:
        print("quality_control_node: called")

        state = {
            "user_query": ctx.state.user_query,
            "out_of_scope_result": ctx.state.out_of_scope_result,
            "keywords": ctx.state.keywords,
        }

        # taken from llm\StategraphAgent.py l88 to 128
        # Step 3: Quality control
        print(
            {
                "thought": "Performing quality control and filter detection...",
                "is_final": False,
                "final_content": None,
            }
        )

        state = quality_control_node(state)

        ctx.state.qc_decision = state.get("qc_decision", "accept")
        ctx.state.qc_tool_result = state.get("qc_tool_result", None)
        ctx.state.keywords = state.get("keywords", [])
        ctx.state.has_filter_instructions = state.get("has_filter_instructions", None)
        ctx.state.error = state.get("error", None)
        qc_decision = ctx.state.qc_decision

        # Check if query is out of scope
        qc_decision = ctx.state.qc_decision
        if qc_decision == "out_of_scope":
            return OutOfScopeHandler()

        # If split, expand subqueries
        if qc_decision == "split":
            return ExpandSubqueries()

        return UpdatePapersByProject()


from llm_pydantic.nodes.out_of_scope_handler import OutOfScopeHandler  # noqa: E402 # isort:skip
from llm_pydantic.nodes.expand_subqueries import ExpandSubqueries  # noqa: E402 # isort:skip
from llm_pydantic.nodes.update_papers_by_project import UpdatePapersByProject  # noqa: E402 # isort:skip
