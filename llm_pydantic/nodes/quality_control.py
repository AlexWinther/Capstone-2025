from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

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

        # Step 3: Quality control
        print(
            {
                "thought": "Performing quality control and filter detection...",
                "is_final": False,
                "final_content": None,
            }
        )

        qc_decision = state.qc_decision

        # Check if query is out of scope
        if qc_decision == "out_of_scope":
            print("quality_control_node: query is out of scope")
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
            print("quality_control_node: splitting query into subqueries")
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
