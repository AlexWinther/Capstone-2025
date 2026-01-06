from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.get_best_papers_node import get_best_papers_node
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class GetBestPapers(BaseNode[AgentState, AgentDeps]):
    """GetBestPapersNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> FilterPapers:
        print("get_best_papers_node: called")

        state = {
            "project_id": ctx.state.project_id,
            "has_filter_instructions": ctx.state.has_filter_instructions,
        }
        # Step 5: Get best papers
        print(
            {
                "thought": "Retrieving most relevant papers...",
                "is_final": False,
                "final_content": None,
            }
        )

        state = get_best_papers_node(state)

        ctx.state.papers_raw = state.get("papers_raw", [])
        ctx.state.error = state.get("error", None)

        return FilterPapers()


from llm_pydantic.nodes.filter_papers import FilterPapers  # noqa: E402 # isort:skip
