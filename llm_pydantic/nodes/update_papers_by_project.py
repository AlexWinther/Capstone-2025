from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.update_papers_by_project_node import update_papers_by_project_node
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class UpdatePapersByProject(BaseNode[AgentState, AgentDeps]):
    """UpdatePapersByProjectNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> GetBestPapers:
        print("update_papers_by_project_node: called")

        state = {
            "user_query": ctx.state.user_query,
            "qc_decision": ctx.state.qc_decision,
            "qc_tool_result": ctx.state.qc_tool_result,
            "project_id": ctx.state.project_id,
            "subqueries": ctx.state.subqueries,
            "keywords": ctx.state.keywords,
        }

        # Step 5: Get best papers
        print(
            {
                "thought": "Updating paper database with latest research...",
                "is_final": False,
                "final_content": None,
            }
        )
        state = update_papers_by_project_node(state)

        ctx.state.update_papers_by_project_result = state.get(
            "update_papers_by_project_result", None
        )
        ctx.state.all_papers = state.get("all_papers", [])
        ctx.state.error = state.get("error", None)
        return GetBestPapers()


from llm_pydantic.nodes.get_best_papers import GetBestPapers  # noqa: E402 # isort:skip
