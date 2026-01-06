from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm_pydantic.node_logger import NodeLogger
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps

# --- Node: Input Handler ---


node_logger = NodeLogger(
    "input_node",
    input_keys=["user_query"],
    output_keys=["user_query", "keywords", "project_id"],
)


@dataclass()
class Input(BaseNode[AgentState, AgentDeps]):
    """
    Initialize the state with the user query and extract project_id if present.
    Args:
        state (dict): The current agent state.
    Returns:
        dict: Updated state with user_query, keywords, and project_id.
    """

    user_message: str

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> OutOfScopeCheck:
        print("input_node: called")

        # Initialize state
        ctx.state.user_query = self.user_message

        state = {
            "user_query": self.user_message,
        }
        # Step 1: Input node
        print(
            {
                "thought": "Processing user input...",
                "is_final": False,
                "final_content": None,
            }
        )

        node_logger.log_begin(state)

        # begin llm\nodes\input.py
        # Initialize the state with the user query
        user_query = state["user_query"]
        # Extract project_id if appended to the user_query (e.g., '... project ID: <id>')
        project_id = None
        if "project ID:" in user_query:
            parts = user_query.rsplit("project ID:", 1)
            user_query = parts[0].strip()
            project_id = parts[1].strip()
        # If the query is a single word or phrase, use it as the initial keyword
        keywords = []
        if user_query and len(user_query.split()) == 1:
            keywords = [user_query]
        # Add project_id to state
        state = {
            "user_query": user_query,
            "keywords": keywords,
            "reformulated_query": None,
            "papers_raw": [],
            "papers_filtered": [],
            "final_output": None,
            "project_id": project_id,
        }

        # end llm\nodes\input.py

        node_logger.log_end(state)

        ctx.state.user_query = state["user_query"]
        ctx.state.project_id = state["project_id"]
        ctx.state.keywords = state["keywords"]

        return OutOfScopeCheck()


from llm_pydantic.nodes.out_of_scope_check import OutOfScopeCheck  # noqa: E402 # isort:skip
