from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from llm_pydantic.state import AgentState
from llm_pydantic.tooling.tooling_mock import AgentDeps


@dataclass()
class ExpandSubqueries(BaseNode[AgentState, AgentDeps]):
    """ExpandSubqueriesNode."""

    async def run(self, ctx: GraphRunContext[AgentState, AgentDeps]) -> End:
        state = ctx.state

        deps = ctx.deps

        print("expand_subqueries_node: called")

        return End()
