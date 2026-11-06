from app.agents.state import AgentState
from app.database import SessionLocal
from app.models.blog import Blog
from app.utils.slug import ensure_unique_slug
from datetime import datetime
from sqlalchemy.sql import func


async def publisher_agent(state: AgentState) -> AgentState:
    """
    Publisher Agent - Saves blog to database and generates accessible URL
    """
    print("🚀 Publisher Agent started...")

    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "publisher",
        "message": "Publishing blog to database",
        "level": "info"
    })

    try:
        content_plan = state.get("content_plan")
        blog_content = state.get("blog_content")
        full_html = state.get("full_blog_html")
        primary_keyword = state.get("primary_keyword")
        secondary_keywords = state.get("secondary_keywords", [])
        validation_result = state.get("validation_result", {})
        execution_id = state.get("execution_id")

        if not all([content_plan, blog_content, full_html, primary_keyword]):
            raise ValueError("Incomplete blog data for publishing")

        db = SessionLocal()
        try:
            # Get existing slugs to ensure uniqueness
            existing_slugs = [blog.slug for blog in db.query(Blog.slug).all()]

            # Ensure unique slug
            base_slug = content_plan.get("slug")
            unique_slug = ensure_unique_slug(base_slug, existing_slugs)

            if unique_slug != base_slug:
                state["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "publisher",
                    "message": f"Slug modified for uniqueness: {base_slug} → {unique_slug}",
                    "level": "info"
                })

            # Create blog entry
            blog = Blog(
                title=content_plan.get("title"),
                slug=unique_slug,
                meta_title=content_plan.get("meta_title"),
                meta_description=content_plan.get("meta_description"),
                h1=content_plan.get("h1"),
                primary_keyword=primary_keyword,
                secondary_keywords=secondary_keywords,
                content=full_html,
                faq=blog_content.get("faq"),
                outline=content_plan.get("outline"),
                internal_links=content_plan.get("internal_links", []),
                image_suggestions=[],
                validation_score=validation_result.get("score", 0),
                status="published",
                execution_id=execution_id
            )

            db.add(blog)
            db.commit()
            db.refresh(blog)

            # Generate blog URL
            blog_url = f"/blogs/{unique_slug}"

            # Update state
            state["blog_id"] = blog.id
            state["blog_url"] = blog_url
            state["published"] = True

            state["logs"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "publisher",
                "message": f"✓ Blog published successfully: {blog_url}",
                "level": "info"
            })

            state["logs"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "publisher",
                "message": f"Blog ID: {blog.id}",
                "level": "info"
            })

            print(f"✓ Blog published: {blog_url}")

        finally:
            db.close()

    except Exception as e:
        error_msg = f"Publisher Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "publisher",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg
        state["published"] = False

    state["current_agent"] = "completed"
    return state
