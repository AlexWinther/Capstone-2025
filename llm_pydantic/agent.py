"""Graph-powered agent entrypoint built with `pydantic_graph`.

The implementation mirrors the structure described in `llm/StategraphAgent.py`
but is intentionally lightweight: every tool call is backed by the
`MockToolbelt` so we can focus on wiring the graph described in the
`https://ai.pydantic.dev/graph/` docs.
"""

from __future__ import annotations

import asyncio

from pydantic_graph import Graph

from llm_pydantic.nodes.expand_subqueries import ExpandSubqueries
from llm_pydantic.nodes.filter_papers import FilterPapers
from llm_pydantic.nodes.get_best_papers import GetBestPapers
from llm_pydantic.nodes.input import Input
from llm_pydantic.nodes.no_results_handler import NoResultsHandler
from llm_pydantic.nodes.out_of_scope_check import OutOfScopeCheck
from llm_pydantic.nodes.out_of_scope_handler import OutOfScopeHandler
from llm_pydantic.nodes.quality_control import QualityControl
from llm_pydantic.nodes.store_papers_for_project import StorePapersForProject
from llm_pydantic.nodes.update_papers_by_project import UpdatePapersByProject
from llm_pydantic.state import AgentOutput, AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


def build_agent_graph() -> Graph[AgentState, AgentDeps, AgentOutput]:
    """Create the reusable graph instance for callers/tests."""

    return Graph(
        nodes=(
            ExpandSubqueries,
            FilterPapers,
            GetBestPapers,
            Input,
            NoResultsHandler,
            OutOfScopeCheck,
            OutOfScopeHandler,
            QualityControl,
            StorePapersForProject,
            UpdatePapersByProject,
        ),
        state_type=AgentState,
    )


async def run_agent(
    user_message: str,
    *,
    state: AgentState | None = None,
    deps: AgentDeps | None = None,
) -> AgentOutput:
    """Helper that runs the graph for a single query."""

    graph = build_agent_graph()
    run_state = state or AgentState()
    run_deps = deps or AgentDeps()
    result = await graph.run(
        Input(user_message=user_message),
        state=run_state,
        deps=run_deps,
    )
    return result.output


def run_agent_sync(
    user_message: str,
    *,
    state: AgentState | None = None,
    deps: AgentDeps | None = None,
) -> AgentOutput:
    """Synchronous convenience wrapper for quick experiments."""

    return asyncio.run(run_agent(user_message, state=state, deps=deps))
