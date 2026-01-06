"""Graph-powered agent entrypoint built with `pydantic_graph`.

The implementation mirrors the structure described in `llm/StategraphAgent.py`
but is intentionally lightweight: every tool call is backed by the
`MockToolbelt` so we can focus on wiring the graph described in the
`https://ai.pydantic.dev/graph/` docs.
"""

from __future__ import annotations

import asyncio
import json
import logging

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

logger = logging.getLogger("PydanticStategraphAgent")
logger.setLevel(logging.WARNING)


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


async def trigger_stategraph_agent_show_thoughts_async(user_message: str):
    """
    Async generator that yields each step of the Pydantic agent's thought process for frontend streaming.

    Args:
        user_message (str): The user's research query or message.

    Yields:
        dict: Thought and state at each step, including final output.
    """
    try:
        # Initialize state and dependencies
        state = AgentState()
        deps = AgentDeps()
        graph = build_agent_graph()

        # Map node class names to user-friendly descriptions
        node_descriptions = {
            "Input": "Processing user input PYDANTIC...",
            "OutOfScopeCheck": "Checking if query is within scope PYDANTIC...",
            "QualityControl": "Performing quality control and filter detection PYDANTIC...",
            "OutOfScopeHandler": "Query determined to be out of scope. Generating explanation PYDANTIC...",
            "ExpandSubqueries": "Splitting query into subqueries PYDANTIC...",
            "UpdatePapersByProject": "Updating paper database with latest research PYDANTIC...",
            "GetBestPapers": "Retrieving most relevant papers PYDANTIC...",
            "FilterPapers": "Applying filters to refine results PYDANTIC...",
            "NoResultsHandler": "No papers found after filtering. Generating smart no-results explanation PYDANTIC...",
            "StorePapersForProject": "Storing recommended papers for this project PYDANTIC...",
        }

        # Run the graph with streaming events using iter context manager
        async with graph.iter(
            Input(user_message=user_message),
            state=state,
            deps=deps,
        ) as graph_run:
            async for node in graph_run:
                # Each event is a node instance (BaseNode or End)
                node_name = node.__class__.__name__

                # Get description or use node name
                thought = node_descriptions.get(node_name, f"Running {node_name}...")

                yield {
                    "thought": thought,
                    "is_final": False,
                    "final_content": None,
                }

                # Check for special conditions based on state
                if node_name == "OutOfScopeCheck" and state.keywords:
                    yield {
                        "thought": f"Extracted keywords: {state.keywords}",
                        "is_final": False,
                        "final_content": None,
                    }

        # Check final state for special cases
        if state.qc_decision == "out_of_scope":
            yield {
                "thought": "Query rejected as out of scope. Please provide a new query.",
                "is_final": True,
                "final_content": json.dumps(
                    {
                        "type": "out_of_scope",
                        "message": state.out_of_scope_message or {},
                        "requires_user_input": True,
                    }
                ),
            }
            return

        if not state.papers_filtered:
            yield {
                "thought": "No papers found. Please try broadening your search or adjusting your filter.",
                "is_final": True,
                "final_content": json.dumps(
                    {
                        "type": "no_results",
                        "message": state.no_results_message or {},
                        "requires_user_input": True,
                    }
                ),
            }
            return

        # Success case
        yield {
            "thought": "Agent workflow complete.",
            "is_final": True,
            "final_content": json.dumps(
                {"status": str(state.store_papers_for_project_result or "No result")}
            ),
        }

    except Exception as e:
        logger.error(f"Error in Pydantic Stategraph agent: {e}")
        yield {
            "thought": f"An error occurred: {str(e)}",
            "is_final": True,
            "final_content": None,
        }


def trigger_stategraph_agent_show_thoughts(user_message: str):
    """
    Synchronous generator wrapper for trigger_stategraph_agent_show_thoughts_async.

    Args:
        user_message (str): The user's research query or message.

    Yields:
        dict: Thought and state at each step, including final output.
    """
    # Create a new event loop for this generator
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Get the async generator
        async_gen = trigger_stategraph_agent_show_thoughts_async(user_message)

        # Manually iterate through the async generator
        while True:
            try:
                # Get the next item from the async generator
                result = loop.run_until_complete(async_gen.__anext__())
                yield result
            except StopAsyncIteration:
                break
    finally:
        loop.close()
