from app.agents.state import AgentState
from app.services.gemini_service import gemini_service
from app.services.website_analyzer import website_analyzer
from app.utils.slug import generate_slug
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict


class ContentOutline(BaseModel):
    h1: str = Field(description="Main H1 heading for the blog")
    h2_sections: List[Dict[str, str]] = Field(description="List of H2 sections with titles and brief descriptions")


class ContentPlan(BaseModel):
    title: str = Field(description="SEO-optimized blog title")
    slug: str = Field(description="URL-friendly slug")
    meta_title: str = Field(description="Meta title (50-60 chars)")
    meta_description: str = Field(description="Meta description (120-160 chars)")
    h1: str = Field(description="H1 heading")
    outline: ContentOutline = Field(description="Content structure with H2 sections")
    target_audience: str = Field(description="Who this content is for")
    search_intent: str = Field(description="What the reader wants to accomplish")
    content_objective: str = Field(description="What the content should achieve")


async def content_planning_agent(state: AgentState) -> AgentState:
    """
    Content Planning Agent - Creates comprehensive content plan
    """
    print("📋 Content Planning Agent started...")

    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "content_planning",
        "message": "Creating SEO-optimized content plan",
        "level": "info"
    })

    try:
        primary_keyword = state.get("primary_keyword")
        secondary_keywords = state.get("secondary_keywords", [])

        if not primary_keyword:
            raise ValueError("Primary keyword not found in state")

        # Get business context
        business_context = await website_analyzer.get_business_context()
        internal_links = await website_analyzer.get_internal_link_suggestions(primary_keyword)

        prompt = f"""You are an SEO content strategist planning a blog post.

Primary Keyword: {primary_keyword}
Secondary Keywords: {', '.join(secondary_keywords)}

Business Context:
- Name: {business_context['business_name']}
- Category: {business_context['business_category']}
- Location: {business_context['location']}
- Courses: {', '.join(business_context['courses'])}

Task: Create a comprehensive content plan that includes:

1. **Title**: SEO-friendly, compelling blog title that includes the primary keyword
2. **Slug**: URL-friendly slug (lowercase, hyphens, no special chars)
3. **Meta Title**: 50-60 characters, includes primary keyword, compelling
4. **Meta Description**: 120-160 characters, includes primary keyword, includes CTA
5. **H1**: Different from meta title, engaging, includes primary keyword
6. **Outline**: Structure with H2 sections (5-7 sections) covering:
   - Introduction to the topic
   - Main content sections addressing user intent
   - Practical information (courses, training, benefits)
   - Why choose our institute
   - Conclusion with CTA
7. **Target Audience**: Specific description
8. **Search Intent**: What the reader wants
9. **Content Objective**: What we want to achieve

Guidelines:
- Natural keyword integration (avoid stuffing)
- Focus on providing value to students seeking digital marketing training
- Address local intent (Coimbatore focus)
- Structure for readability and SEO
- Plan for internal linking opportunities
"""

        # Generate content plan
        plan = await gemini_service.generate_structured(prompt, ContentPlan)

        # Ensure slug is generated properly
        if not plan.slug:
            plan.slug = generate_slug(plan.title)

        # Store in state
        state["content_plan"] = {
            "title": plan.title,
            "slug": plan.slug,
            "meta_title": plan.meta_title,
            "meta_description": plan.meta_description,
            "h1": plan.h1,
            "outline": plan.outline.dict(),
            "target_audience": plan.target_audience,
            "search_intent": plan.search_intent,
            "content_objective": plan.content_objective,
            "internal_links": internal_links
        }

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "content_planning",
            "message": f"Content plan created: {plan.title}",
            "level": "info"
        })

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "content_planning",
            "message": f"URL slug: {plan.slug}",
            "level": "info"
        })

        print(f"✓ Content Planning completed: {plan.title}")

    except Exception as e:
        error_msg = f"Content Planning Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "content_planning",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg

    state["current_agent"] = "duplicate_detection"
    return state
