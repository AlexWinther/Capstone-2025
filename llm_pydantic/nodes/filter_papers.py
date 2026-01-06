from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.filter_papers_node import filter_papers_node
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

        # taken from llm\StategraphAgent.py l146 to 175
        # Step 6: Filter papers
        print(
            {
                "thought": "Applying filters to refine results...",
                "is_final": False,
                "final_content": None,
            }
        )

        new_state = filter_papers_node(
            {
                "user_query": state.user_query,
                "papers_raw": state.papers_raw,
                "has_filter_instructions": state.has_filter_instructions,
            }
        )

        state.papers_filtered = new_state.get("papers_filtered", [])
        state.applied_filter_criteria = new_state.get("applied_filter_criteria", {})
        state.error = new_state.get("error", None)

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
