from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.seo_research import seo_research_agent
from app.agents.keyword_selector import keyword_selection_agent
from app.agents.content_planner import content_planning_agent
from app.agents.duplicate_detector import duplicate_detection_agent
from app.agents.blog_writer import blog_writer_agent
from app.agents.seo_validator import seo_validation_agent
from app.agents.publisher import publisher_agent
from app.config import settings


def should_retry_writing(state: AgentState) -> str:
    """Conditional edge: decide whether to retry writing or publish"""
    validation_result = state.get("validation_result")
    retry_count = state.get("retry_count", 0)

    if validation_result and not validation_result.get("passed"):
        if retry_count < settings.MAX_RETRY_ATTEMPTS:
            return "retry"

    return "publish"


def create_seo_workflow() -> StateGraph:
    """
    Create the LangGraph workflow for SEO blog generation

    Workflow:
    START → SEO Research → Keyword Selection → Content Planning →
    Duplicate Detection → Blog Writer → SEO Validation →
    (Conditional: Pass → Publisher | Fail → Blog Writer retry) → END
    """

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes (agents)
    workflow.add_node("seo_research", seo_research_agent)
    workflow.add_node("keyword_selection", keyword_selection_agent)
    workflow.add_node("content_planning", content_planning_agent)
    workflow.add_node("duplicate_detection", duplicate_detection_agent)
    workflow.add_node("blog_writer", blog_writer_agent)
    workflow.add_node("seo_validation", seo_validation_agent)
    workflow.add_node("publisher", publisher_agent)

    # Set entry point
    workflow.set_entry_point("seo_research")

    # Add edges (workflow flow)
    workflow.add_edge("seo_research", "keyword_selection")
    workflow.add_edge("keyword_selection", "content_planning")
    workflow.add_edge("content_planning", "duplicate_detection")
    workflow.add_edge("duplicate_detection", "blog_writer")
    workflow.add_edge("blog_writer", "seo_validation")

    # Add conditional edge for validation
    workflow.add_conditional_edges(
        "seo_validation",
        should_retry_writing,
        {
            "retry": "blog_writer",
            "publish": "publisher"
        }
    )

    # End after publishing
    workflow.add_edge("publisher", END)

    return workflow.compile()


# Create the compiled workflow
seo_workflow = create_seo_workflow()
