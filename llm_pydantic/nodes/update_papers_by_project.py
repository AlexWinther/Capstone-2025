from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class UpdatePapersByProject(BaseNode[AgentState, AgentDeps]):
    """UpdatePapersByProjectNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> GetBestPapers:
        state = ctx.state
        deps = ctx.deps

        print("update_papers_by_project_node: called")

        # Step 5: Get best papers
        print(
            {
                "thought": "Updating paper database with latest research...",
                "is_final": False,
                "final_content": None,
            }
        )

        return GetBestPapers()


from llm_pydantic.nodes.get_best_papers import GetBestPapers  # noqa: E402 # isort:skip
