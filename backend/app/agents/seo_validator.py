from app.agents.state import AgentState
from app.utils.seo_scoring import seo_validator
from app.config import settings
from datetime import datetime


async def seo_validation_agent(state: AgentState) -> AgentState:
    """
    SEO Validation Agent - Validates blog content against SEO best practices
    """
    print("✅ SEO Validation Agent started...")

    state["logs"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "agent": "seo_validation",
        "message": "Validating blog content against SEO best practices",
        "level": "info"
    })

    try:
        content_plan = state.get("content_plan")
        blog_content = state.get("blog_content")
        full_html = state.get("full_blog_html")
        primary_keyword = state.get("primary_keyword")
        secondary_keywords = state.get("secondary_keywords", [])

        if not content_plan or not blog_content or not full_html:
            raise ValueError("Content not found for validation")

        # Prepare blog data for validation
        blog_data = {
            "title": content_plan.get("title"),
            "slug": content_plan.get("slug"),
            "meta_title": content_plan.get("meta_title"),
            "meta_description": content_plan.get("meta_description"),
            "h1": content_plan.get("h1"),
            "primary_keyword": primary_keyword,
            "secondary_keywords": secondary_keywords,
            "content": full_html,
            "faq": blog_content.get("faq", [])
        }

        # Validate
        validation_result = seo_validator.validate_blog(blog_data)

        # Store validation result
        state["validation_result"] = validation_result

        # Log results
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "seo_validation",
            "message": f"SEO validation score: {validation_result['score']}/100",
            "level": "info"
        })

        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "seo_validation",
            "message": f"Passed checks: {len(validation_result['passed_checks'])}, Failed: {len(validation_result['failed_checks'])}",
            "level": "info"
        })

        # Check if validation passed
        if validation_result['passed']:
            state["logs"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "seo_validation",
                "message": "✓ Content passed SEO validation, proceeding to publish",
                "level": "info"
            })
            print(f"✓ SEO Validation passed: {validation_result['score']}/100")
            state["current_agent"] = "publisher"
        else:
            # Check retry count
            retry_count = state.get("retry_count", 0)

            if retry_count < settings.MAX_RETRY_ATTEMPTS:
                state["retry_count"] = retry_count + 1
                state["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "seo_validation",
                    "message": f"⚠️ Validation failed (score: {validation_result['score']}). Retry {retry_count + 1}/{settings.MAX_RETRY_ATTEMPTS}",
                    "level": "warning"
                })
                print(f"⚠️ Validation failed, retry {retry_count + 1}/{settings.MAX_RETRY_ATTEMPTS}")

                # Log suggestions for improvement
                if validation_result['suggestions']:
                    suggestions_text = "; ".join(validation_result['suggestions'][:3])
                    state["logs"].append({
                        "timestamp": datetime.utcnow().isoformat(),
                        "agent": "seo_validation",
                        "message": f"Improvements needed: {suggestions_text}",
                        "level": "warning"
                    })

                # Route back to blog writer for improvement
                state["current_agent"] = "blog_writer"
            else:
                # Max retries reached, proceed anyway
                state["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "seo_validation",
                    "message": f"⚠️ Max retries reached. Publishing with score: {validation_result['score']}/100",
                    "level": "warning"
                })
                print(f"⚠️ Max retries reached, publishing anyway")
                state["current_agent"] = "publisher"

    except Exception as e:
        error_msg = f"SEO Validation Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "seo_validation",
            "message": error_msg,
            "level": "error"
        })
        state["error"] = error_msg
        # Proceed to publisher despite validation error
        state["current_agent"] = "publisher"

    return state
