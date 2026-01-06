from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm.nodes.no_results_handler_node import no_results_handler_node
from llm_pydantic.state import AgentOutput, AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class NoResultsHandler(BaseNode[AgentState, AgentDeps]):
    """NoResultsHandlerNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state
        deps = ctx.deps

        print("no_results_handler_node: called")

        # taken from llm\StategraphAgent.py l162 to 175
        new_state = no_results_handler_node(
            {
                "user_query": state.user_query,
                "papers_raw": state.all_papers,
                "papers_filtered": state.papers_filtered,
                "applied_filter_criteria": state.subqueries,
            }
        )

        state.no_results_message = new_state.get("no_results_message", "")

        no_results_message = state.no_results_message
        print(
            {
                "thought": "No papers found. Please try broadening your search or adjusting your filter.",
                "is_final": True,
                "final_content": json.dumps(
                    {
                        "type": "no_results",
                        "message": no_results_message,
                        "requires_user_input": True,
                    }
                ),
            }
        )

        return End(AgentOutput(status="no_results_handled"))
