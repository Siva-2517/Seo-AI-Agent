from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.research import ResearchResponse
from app.models.keyword import Keyword
from app.models.execution import Execution

router = APIRouter()


@router.get("/{execution_id}", response_model=ResearchResponse)
async def get_research_data(
    execution_id: str,
    db: Session = Depends(get_db)
):
    """
    Get keyword research data for a specific execution
    """
    try:
        # Check if execution exists
        execution = db.query(Execution).filter(
            Execution.execution_id == execution_id
        ).first()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        # Get keywords for this execution
        keywords = db.query(Keyword).filter(
            Keyword.execution_id == execution_id
        ).all()

        # Get selected keywords from associated blog
        from app.models.blog import Blog
        blog = db.query(Blog).filter(
            Blog.execution_id == execution_id
        ).first()

        selected_primary = blog.primary_keyword if blog else None
        selected_secondary = blog.secondary_keywords if blog else None

        return ResearchResponse(
            execution_id=execution_id,
            keywords=[
                {
                    "keyword": kw.keyword,
                    "search_intent": kw.search_intent,
                    "relevance": kw.relevance,
                    "competition": kw.competition,
                    "search_volume": kw.search_volume,
                    "data_confidence": kw.data_confidence,
                    "source": kw.source,
                    "opportunity_score": kw.opportunity_score
                }
                for kw in keywords
            ],
            selected_primary_keyword=selected_primary,
            selected_secondary_keywords=selected_secondary,
            selection_reasoning=None  # Could be added to execution model
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch research data: {str(e)}")
