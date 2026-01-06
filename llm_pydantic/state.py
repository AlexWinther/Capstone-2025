"""Shared state definitions for the Pydantic AI demo agent.

This module keeps the graph state/data models small and serialisable so we can
use `pydantic_graph` persistence later without refactoring. Fields are chosen to
mirror the legacy `llm.StategraphAgent` dict keys while remaining optional
because nodes only fill the pieces they care about.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    """
    State that flows through the agent graph.
    Each node can read and modify this state.
    """

    user_query: str = ""
    """The original user research query"""

    project_id: str = ""
    """Project ID for storing/retrieving papers - REQUIRED for real mode"""

    qc_decision: str = ""
    """Quality control decision from QC node"""

    papers_filtered: list[dict[str, Any]] = field(default_factory=list)
    """List of filtered paper metadata dicts"""

    no_results_message: str = ""
    """Message to show when no results are found"""


@dataclass
class AgentOutput:
    """Lightweight container returned when the graph ends."""

    status: str = "no status"
