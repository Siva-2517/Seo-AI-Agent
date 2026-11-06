from app.agents.state import AgentState
from app.database import SessionLocal
from app.models.blog import Blog
from datetime import datetime
from sqlalchemy import or_


async def duplicate_detection_agent(state: AgentState) -> AgentState:
    """
    Duplicate Detection Agent - Checks for duplicate topics and keyword cannibalization
    """
    print("🔍 Duplicate Detection Agent started...")

    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "duplicate_detection",
        "message": "Checking for duplicate topics and keyword cannibalization",
        "level": "info"
    })

    try:
        content_plan = state.get("content_plan")
        primary_keyword = state.get("primary_keyword")

        if not content_plan or not primary_keyword:
            raise ValueError("Content plan or primary keyword not found")

        slug = content_plan.get("slug")
        title = content_plan.get("title")

        # Check database for duplicates
        db = SessionLocal()
        try:
            # Check for duplicate slug
            existing_slug = db.query(Blog).filter(Blog.slug == slug).first()
            if existing_slug:
                state["is_duplicate"] = True
                state["duplicate_reason"] = f"Slug '{slug}' already exists"
                state["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "duplicate_detection",
                    "message": f"⚠️ Duplicate slug detected: {slug}",
                    "level": "warning"
                })
                print(f"⚠️ Duplicate slug detected: {slug}")
                state["current_agent"] = "blog_writer"
                return state

            # Check for similar primary keyword
            existing_keyword = db.query(Blog).filter(
                Blog.primary_keyword == primary_keyword
            ).first()

            if existing_keyword:
                state["is_duplicate"] = True
                state["duplicate_reason"] = f"Primary keyword '{primary_keyword}' already targeted"
                state["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "duplicate_detection",
                    "message": f"⚠️ Keyword cannibalization risk: {primary_keyword}",
                    "level": "warning"
                })
                print(f"⚠️ Keyword cannibalization detected: {primary_keyword}")
                state["current_agent"] = "blog_writer"
                return state

            # Check for very similar titles
            similar_title = db.query(Blog).filter(
                or_(
                    Blog.title.like(f"%{title}%"),
                    Blog.title == title
                )
            ).first()

            if similar_title:
                state["is_duplicate"] = True
                state["duplicate_reason"] = f"Similar title already exists"
                state["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "duplicate_detection",
                    "message": f"⚠️ Similar title detected",
                    "level": "warning"
                })
                print(f"⚠️ Similar title detected")
                state["current_agent"] = "blog_writer"
                return state

            # No duplicates found
            state["is_duplicate"] = False
            state["duplicate_reason"] = None

            state["logs"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "duplicate_detection",
                "message": "✓ No duplicates found, proceeding with content generation",
                "level": "info"
            })
            print("✓ No duplicates detected")

        finally:
            db.close()

    except Exception as e:
        error_msg = f"Duplicate Detection Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "duplicate_detection",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg
        state["is_duplicate"] = False  # Proceed despite error

    state["current_agent"] = "blog_writer"
    return state
