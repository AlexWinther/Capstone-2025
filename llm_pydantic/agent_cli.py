"""Minimal CLI entrypoint for driving the Pydantic graph agent."""

import os
import sys
from datetime import datetime

# Ensure project root is on sys.path when running this module directly
if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from llm_pydantic.agent import build_agent_graph
from llm_pydantic.nodes.input import Input
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


def main():
    user_query = "Machine learning for healthcare after 2018"
    project_name = f"CLI Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
    project_id = project_name.replace(" ", "-")
    final_query = f"{user_query} project ID: {project_id}"
    print("Using project:", project_id)
    print("User query:", final_query)

    graph = build_agent_graph()
    state = AgentState()
    deps = AgentDeps()
    result = graph.run_sync(Input(user_message=final_query), state=state, deps=deps)

    if not result:
        print("\nAgent did not return a payload.")


if __name__ == "__main__":
    main()
