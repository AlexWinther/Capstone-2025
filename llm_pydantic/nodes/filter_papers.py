from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class FilterPapers(BaseNode[AgentState, AgentDeps]):
    """FilterPapersNode."""

    async def run(
        self, ctx: GraphRunContext[AgentState, AgentDeps]
    ) -> NoResultsHandler | StorePapersForProject:
        state = ctx.state
        deps = ctx.deps

        print("filter_papers_node: called")

        # Step 6: Filter papers
        print(
            {
                "thought": "Applying filters to refine results...",
                "is_final": False,
                "final_content": None,
            }
        )

        # Todo

        # Check for no results
        papers_filtered = state.papers_filtered
        if not papers_filtered:
            print(
                {
                    "thought": "No papers found after filtering. Generating smart no-results explanation...",
                    "is_final": False,
                    "final_content": None,
                }
            )

            return NoResultsHandler()
        else:
            return StorePapersForProject()


from llm_pydantic.nodes.no_results_handler import NoResultsHandler  # noqa: E402 # isort:skip
from llm_pydantic.nodes.store_papers_for_project import StorePapersForProject  # noqa: E402 # isort:skip
