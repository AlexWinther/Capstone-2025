from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AgentState:
    """
    State that flows through the agent graph.
    Each node can read and modify this state.
    """

    all_papers: list[dict[str, Any]] = field(default_factory=list)
    # used by: NoResultsHandler, UpdatePapersByProject

    applied_filter_criteria: dict[str, Any] = field(default_factory=dict)
    # used by: FilterPapers

    error: Optional[str] = None
    # used by: FilterPapers, GetBestPapers, OutOfScopeCheck, QualityControl, UpdatePapersByProject

    has_filter_instructions: Optional[bool] = None
    # used by: GetBestPapers, QualityControl

    keywords: list[str] = field(default_factory=list)
    # used by: Input, OutOfScopeCheck, QualityControl, UpdatePapersByProject

    no_results_message: Any = None
    # used by: NoResultsHandler

    out_of_scope_message: Any = None
    # used by: OutOfScopeHandler

    out_of_scope_result: str = ""
    # used by: OutOfScopeCheck, QualityControl

    papers_filtered: Any = None
    # used by: FilterPapers, NoResultsHandler, StorePapersForProject

    papers_raw: Any = None
    # used by: GetBestPapers, StorePapersForProject

    project_id: str = ""
    # used by: GetBestPapers, Input, StorePapersForProject, UpdatePapersByProject

    qc_decision: str = ""
    # used by: QualityControl, UpdatePapersByProject

    qc_tool_result: Optional[str] = None
    # used by: QualityControl, UpdatePapersByProject

    requires_user_input: bool = False
    # used by: OutOfScopeHandler

    store_papers_for_project_result: Any = None
    # used by: StorePapersForProject

    subqueries: Any = None
    # used by: NoResultsHandler, UpdatePapersByProject

    update_papers_by_project_result: Any = None
    # used by: UpdatePapersByProject

    user_query: str = ""
    # used by: Input, NoResultsHandler, OutOfScopeCheck, QualityControl, StorePapersForProject, UpdatePapersByProject


@dataclass
class AgentOutput:
    """Lightweight container returned when the graph ends."""

    status: str = "no status"
