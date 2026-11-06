from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import add_messages
import operator


class KeywordData(TypedDict):
    keyword: str
    search_intent: str
    relevance: str
    competition: str
    search_volume: str
    data_confidence: str
    source: Optional[str]
    opportunity_score: Optional[float]


class ContentPlan(TypedDict):
    title: str
    slug: str
    meta_title: str
    meta_description: str
    h1: str
    outline: dict
    target_audience: str
    search_intent: str
    content_objective: str
    internal_links: List[str]


class ValidationResult(TypedDict):
    passed: bool
    score: float
    passed_checks: List[str]
    failed_checks: List[str]
    suggestions: List[str]


class BlogContent(TypedDict):
    introduction: str
    main_content: str
    faq: List[dict]
    conclusion: str
    cta: str


class AgentState(TypedDict):
    # Execution tracking
    execution_id: str
    current_agent: str
    logs: Annotated[List[dict], operator.add]

    # SEO Research
    discovered_keywords: List[KeywordData]

    # Keyword Selection
    primary_keyword: Optional[str]
    secondary_keywords: List[str]
    semantic_keywords: List[str]
    selection_reasoning: str

    # Content Planning
    content_plan: Optional[ContentPlan]

    # Duplicate Detection
    is_duplicate: bool
    duplicate_reason: Optional[str]

    # Blog Writing
    blog_content: Optional[BlogContent]
    full_blog_html: Optional[str]

    # SEO Validation
    validation_result: Optional[ValidationResult]
    retry_count: int

    # Publishing
    blog_id: Optional[int]
    blog_url: Optional[str]
    published: bool

    # Error handling
    error: Optional[str]
