from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.quality_control_node import quality_control_node
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class QualityControl(BaseNode[AgentState, AgentDeps]):
    """QualityControlNode."""

    async def run(
        self, ctx: GraphRunContext[AgentState, AgentDeps]
    ) -> OutOfScopeHandler | ExpandSubqueries | UpdatePapersByProject:
        state = ctx.state
        deps = ctx.deps

        print("quality_control_node: called")

        # taken from llm\StategraphAgent.py l88 to 128
        # Step 3: Quality control
        print(
            {
                "thought": "Performing quality control and filter detection...",
                "is_final": False,
                "final_content": None,
            }
        )

        new_state = quality_control_node(
            {
                "user_query": state.user_query,
                "out_of_scope_result": state.out_of_scope_result,
                "keywords": state.keywords,
            }
        )

        state.qc_decision = new_state.get("qc_decision", "accept")
        state.qc_tool_result = new_state.get("qc_tool_result", None)
        state.keywords = new_state.get("keywords", [])
        state.has_filter_instructions = new_state.get("has_filter_instructions", None)
        state.error = new_state.get("error", None)
        qc_decision = state.qc_decision

        # Check if query is out of scope
        qc_decision = state.qc_decision
        if qc_decision == "out_of_scope":
            print(
                {
                    "thought": "Query determined to be out of scope. Generating explanation...",
                    "is_final": False,
                    "final_content": None,
                }
            )
            return OutOfScopeHandler()

        # If split, expand subqueries
        if qc_decision == "split":
            print(
                {
                    "thought": "Splitting query into subqueries...",
                    "is_final": False,
                    "final_content": None,
                }
            )
            return ExpandSubqueries()

        return UpdatePapersByProject()


from llm_pydantic.nodes.out_of_scope_handler import OutOfScopeHandler  # noqa: E402 # isort:skip
from llm_pydantic.nodes.expand_subqueries import ExpandSubqueries  # noqa: E402 # isort:skip
from llm_pydantic.nodes.update_papers_by_project import UpdatePapersByProject  # noqa: E402 # isort:skip
