from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class GetBestPapers(BaseNode[AgentState, AgentDeps]):
    """GetBestPapersNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> FilterPapers:
        state = ctx.state

        deps = ctx.deps

        print("get_best_papers_node: called")

        # Step 5: Get best papers
        print(
            {
                "thought": "Retrieving most relevant papers...",
                "is_final": False,
                "final_content": None,
            }
        )

        return FilterPapers()


from llm_pydantic.nodes.filter_papers import FilterPapers  # noqa: E402 # isort:skip
