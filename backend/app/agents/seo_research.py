from app.agents.state import AgentState
from app.services.seo_service import seo_service
from app.config import settings
from datetime import datetime
from typing import List, Dict


async def seo_research_agent(state: AgentState) -> AgentState:
    """
    SEO Research Agent - Discovers keyword opportunities for digital marketing courses
    """
    print("🔍 SEO Research Agent started...")

    # Add log
    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "seo_research",
        "message": "Starting keyword research for digital marketing courses in Coimbatore",
        "level": "info"
    })

    try:
        # Seed keyword
        seed_keyword = "digital marketing course coimbatore"

        # Get search suggestions
        print("Getting search suggestions...")
        keywords = await seo_service.get_search_suggestions(seed_keyword)

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "seo_research",
            "message": f"Discovered {len(keywords)} potential keywords",
            "level": "info"
        })

        # Analyze keywords
        print(f"Analyzing {len(keywords)} keywords...")
        keyword_data = await seo_service.analyze_keyword_batch(
            keywords,
            settings.BUSINESS_CATEGORY
        )

        # Store in state
        state["discovered_keywords"] = keyword_data

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "seo_research",
            "message": f"Completed keyword analysis with verified and estimated metrics",
            "level": "info"
        })

        print(f"✓ SEO Research completed: {len(keyword_data)} keywords analyzed")

    except Exception as e:
        error_msg = f"SEO Research Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "seo_research",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg

    state["current_agent"] = "keyword_selection"
    return state
