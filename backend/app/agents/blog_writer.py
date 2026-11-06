from app.agents.state import AgentState
from app.services.gemini_service import gemini_service
from app.services.website_analyzer import website_analyzer
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class FAQ(BaseModel):
    question: str
    answer: str


class BlogContent(BaseModel):
    introduction: str = Field(description="Engaging introduction (2-3 paragraphs)")
    main_content: str = Field(description="Main content with H2 and H3 sections in HTML format")
    faq: List[FAQ] = Field(description="5-7 frequently asked questions with detailed answers")
    conclusion: str = Field(description="Conclusion paragraph summarizing key points")
    cta: str = Field(description="Call-to-action promoting Appin Technology's course")


async def blog_writer_agent(state: AgentState) -> AgentState:
    """
    Blog Writer Agent - Generates complete SEO-optimized blog content
    """
    print("✍️ Blog Writer Agent started...")

    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "blog_writer",
        "message": "Generating complete blog content",
        "level": "info"
    })

    try:
        content_plan = state.get("content_plan")
        primary_keyword = state.get("primary_keyword")
        secondary_keywords = state.get("secondary_keywords", [])
        semantic_keywords = state.get("semantic_keywords", [])
        is_duplicate = state.get("is_duplicate", False)

        if not content_plan or not primary_keyword:
            raise ValueError("Content plan or primary keyword not found")

        # Get business context
        business_context = await website_analyzer.get_business_context()

        # Note about duplicate
        duplicate_note = ""
        if is_duplicate:
            duplicate_note = f"\n⚠️ NOTE: {state.get('duplicate_reason')}. Ensure this content takes a unique angle and does not cannibalize existing content.\n"

        prompt = f"""You are an expert content writer creating an SEO-optimized blog post for a digital marketing institute.

{duplicate_note}

Content Plan:
- Title: {content_plan['title']}
- H1: {content_plan['h1']}
- Primary Keyword: {primary_keyword}
- Secondary Keywords: {', '.join(secondary_keywords)}
- Semantic Keywords: {', '.join(semantic_keywords)}
- Target Audience: {content_plan['target_audience']}
- Search Intent: {content_plan['search_intent']}
- Content Objective: {content_plan['content_objective']}

Content Outline:
{_format_outline(content_plan['outline'])}

Business Context:
- Name: {business_context['business_name']}
- Location: {business_context['location']}
- Courses: {', '.join(business_context['courses'])}
- Key Offerings: {', '.join(business_context['key_offerings'])}

Task: Write a complete, original, and valuable blog post with:

1. **Introduction** (2-3 paragraphs):
   - Hook the reader with a relevant question or statement
   - Address the search intent directly
   - Preview what the reader will learn
   - Naturally include the primary keyword

2. **Main Content** (HTML format with proper H2 and H3 tags):
   - Follow the outline structure
   - Use <h2> and <h3> tags for sections
   - Write 3-4 paragraphs per section
   - Include practical information about digital marketing training
   - Naturally incorporate primary and secondary keywords (avoid stuffing)
   - Use semantic keywords naturally
   - Provide actionable insights and real value
   - Include specific information about Coimbatore's digital marketing landscape where relevant
   - Use <p> tags for paragraphs
   - Use <ul> and <li> for lists where appropriate
   - Use <strong> for emphasis sparingly

3. **FAQs** (5-7 questions):
   - Address common student questions about digital marketing courses
   - Include questions about fees, duration, placement, curriculum, prerequisites
   - Provide detailed, helpful answers (3-4 sentences each)
   - Naturally include keywords in questions and answers

4. **Conclusion** (1 paragraph):
   - Summarize key takeaways
   - Reinforce the value proposition
   - Lead naturally to the CTA

5. **CTA** (2-3 sentences):
   - Promote Appin Technology's Digital Marketing Course in Coimbatore
   - Include a clear action (enroll, contact, visit, learn more)
   - Make it compelling and benefit-focused

Content Guidelines:
- Write for humans first, search engines second
- Be conversational but professional
- Provide genuine value and insights
- NO fabricated statistics or unsupported claims
- NO guarantee of specific salaries or placement
- Use "placement assistance" not "placement guarantee"
- Be specific about Coimbatore context where relevant
- Avoid generic filler content
- Keep paragraphs readable (3-5 sentences)
- Natural keyword integration throughout

Write content that actually helps someone researching digital marketing courses in Coimbatore make an informed decision.
"""

        # Generate blog content
        blog_content = await gemini_service.generate_structured(prompt, BlogContent)

        # Assemble full HTML content
        full_html = _assemble_html(blog_content, content_plan)

        # Store in state
        state["blog_content"] = {
            "introduction": blog_content.introduction,
            "main_content": blog_content.main_content,
            "faq": [{"question": faq.question, "answer": faq.answer} for faq in blog_content.faq],
            "conclusion": blog_content.conclusion,
            "cta": blog_content.cta
        }
        state["full_blog_html"] = full_html

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "blog_writer",
            "message": f"Blog content generated ({len(full_html)} characters)",
            "level": "info"
        })

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "blog_writer",
            "message": f"Generated {len(blog_content.faq)} FAQ items",
            "level": "info"
        })

        print(f"✓ Blog Writing completed: {len(full_html)} characters")

    except Exception as e:
        error_msg = f"Blog Writer Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "blog_writer",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg

    state["current_agent"] = "seo_validation"
    return state


def _format_outline(outline: dict) -> str:
    """Format outline for prompt"""
    sections = outline.get('h2_sections', [])
    formatted = []
    for i, section in enumerate(sections, 1):
        title = section.get('title', section.get('h2', ''))
        desc = section.get('description', section.get('content', ''))
        formatted.append(f"  {i}. {title}: {desc}")
    return "\n".join(formatted)


def _assemble_html(blog_content: BlogContent, content_plan: dict) -> str:
    """Assemble complete HTML blog content"""
    html_parts = []

    # H1
    html_parts.append(f"<h1>{content_plan['h1']}</h1>\n")

    # Introduction
    html_parts.append(f"<div class='introduction'>\n{blog_content.introduction}\n</div>\n")

    # Main content (already has HTML tags)
    html_parts.append(f"<div class='main-content'>\n{blog_content.main_content}\n</div>\n")

    # FAQ section
    if blog_content.faq:
        html_parts.append("<div class='faq-section'>\n<h2>Frequently Asked Questions</h2>\n")
        for faq in blog_content.faq:
            html_parts.append(f"<div class='faq-item'>\n")
            html_parts.append(f"<h3 class='faq-question'>{faq.question}</h3>\n")
            html_parts.append(f"<p class='faq-answer'>{faq.answer}</p>\n")
            html_parts.append(f"</div>\n")
        html_parts.append("</div>\n")

    # Conclusion
    html_parts.append(f"<div class='conclusion'>\n<h2>Conclusion</h2>\n<p>{blog_content.conclusion}</p>\n</div>\n")

    # CTA
    html_parts.append(f"<div class='cta'>\n<p><strong>{blog_content.cta}</strong></p>\n</div>\n")

    return "".join(html_parts)
