from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from llm.nodes.input import input_node
from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class Input(BaseNode[AgentState, AgentDeps]):
    """InputNode."""

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

        state = input_node(state)

        ctx.state.user_query = state["user_query"]
        ctx.state.project_id = state["project_id"]
        ctx.state.keywords = state["keywords"]

        return OutOfScopeCheck()


from llm_pydantic.nodes.out_of_scope_check import OutOfScopeCheck  # noqa: E402 # isort:skip
