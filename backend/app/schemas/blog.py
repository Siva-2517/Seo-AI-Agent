from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class KeywordData(BaseModel):
    keyword: str
    search_intent: str
    relevance: str
    competition: str
    search_volume: str
    data_confidence: str  # verified, estimated, unavailable
    source: Optional[str] = None
    opportunity_score: Optional[float] = None


class BlogOutline(BaseModel):
    h1: str
    h2_sections: List[dict]


class FAQItem(BaseModel):
    question: str
    answer: str


class BlogCreate(BaseModel):
    title: str
    slug: str
    meta_title: str
    meta_description: str
    h1: str
    primary_keyword: str
    secondary_keywords: List[str]
    content: str
    faq: Optional[List[FAQItem]] = None
    outline: Optional[BlogOutline] = None
    internal_links: Optional[List[str]] = None
    image_suggestions: Optional[List[str]] = None
    validation_score: float
    execution_id: str


class BlogResponse(BaseModel):
    id: int
    title: str
    slug: str
    meta_title: str
    meta_description: str
    h1: str
    primary_keyword: str
    secondary_keywords: List[str]
    content: str
    faq: Optional[List[FAQItem]] = None
    validation_score: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
