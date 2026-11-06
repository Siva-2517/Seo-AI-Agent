from app.agents.state import AgentState
from app.services.gemini_service import gemini_service
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class KeywordSelection(BaseModel):
    primary_keyword: str = Field(description="The best primary keyword to target")
    secondary_keywords: List[str] = Field(description="3-6 supporting secondary keywords")
    semantic_keywords: List[str] = Field(description="Related semantic keywords")
    reasoning: str = Field(description="Explanation of why this cluster was selected")


async def keyword_selection_agent(state: AgentState) -> AgentState:
    """
    Keyword Selection Agent - Selects the best keyword cluster based on opportunity
    """
    print("🎯 Keyword Selection Agent started...")

    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "keyword_selection",
        "message": "Evaluating discovered keywords to select optimal cluster",
        "level": "info"
    })

    try:
        discovered_keywords = state.get("discovered_keywords", [])

        if not discovered_keywords:
            raise ValueError("No keywords discovered in previous step")

        # Prepare keyword data for LLM
        keyword_summary = "\n".join([
            f"- {kw['keyword']}: Relevance={kw['relevance']}, Intent={kw['search_intent']}, "
            f"Competition={kw['competition']}, Score={kw.get('opportunity_score', 'N/A')}, "
            f"Volume={kw['search_volume']} (Confidence: {kw['data_confidence']})"
            for kw in discovered_keywords
        ])

        prompt = f"""You are an SEO expert selecting keywords for a digital marketing course in Coimbatore.

Business: Appin Technology
Category: Digital Marketing Course in Coimbatore
Goal: Attract students looking for digital marketing training

Available Keywords:
{keyword_summary}

Task: Select the best keyword cluster:
1. Choose ONE primary keyword with the best balance of:
   - High relevance to our business
   - Clear conversion intent (transactional/local)
   - Manageable competition
   - Good opportunity score

2. Choose 3-6 secondary keywords that:
   - Support the primary keyword topic
   - Cover different search intents
   - Include location-specific variations
   - Target related course topics

3. Identify semantic keywords (related terms to use naturally in content)

4. Explain your selection reasoning focusing on:
   - Why this primary keyword is the best opportunity
   - How the secondary keywords complement it
   - Expected conversion potential

Prioritize keywords that will attract students ready to enroll or learn more about courses.
"""

        # Generate structured selection
        selection = await gemini_service.generate_structured(prompt, KeywordSelection)

        # Update state
        state["primary_keyword"] = selection.primary_keyword
        state["secondary_keywords"] = selection.secondary_keywords
        state["semantic_keywords"] = selection.semantic_keywords
        state["selection_reasoning"] = selection.reasoning

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "keyword_selection",
            "message": f"Selected primary keyword: {selection.primary_keyword}",
            "level": "info"
        })

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "keyword_selection",
            "message": f"Selected {len(selection.secondary_keywords)} secondary keywords",
            "level": "info"
        })

        print(f"✓ Keyword Selection completed: {selection.primary_keyword}")

    except Exception as e:
        error_msg = f"Keyword Selection Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "keyword_selection",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg

    state["current_agent"] = "content_planning"
    return state
