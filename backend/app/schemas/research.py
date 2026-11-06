from pydantic import BaseModel, Field
from typing import List, Optional


class KeywordResearchResult(BaseModel):
    keyword: str
    search_intent: str
    relevance: str
    competition: str
    search_volume: str
    data_confidence: str
    source: Optional[str] = None
    opportunity_score: Optional[float] = None


class ResearchResponse(BaseModel):
    execution_id: str
    keywords: List[KeywordResearchResult]
    selected_primary_keyword: Optional[str] = None
    selected_secondary_keywords: Optional[List[str]] = None
    selection_reasoning: Optional[str] = None

    class Config:
        from_attributes = True
