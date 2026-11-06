from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.blog import BlogResponse
from app.models.blog import Blog
from typing import List

router = APIRouter()


@router.get("/", response_model=List[BlogResponse])
async def get_all_blogs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all published blogs
    """
    try:
        blogs = db.query(Blog).order_by(
            Blog.created_at.desc()
        ).offset(skip).limit(limit).all()

        return blogs

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch blogs: {str(e)}")


@router.get("/{slug}", response_model=BlogResponse)
async def get_blog_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific blog by slug
    """
    try:
        blog = db.query(Blog).filter(Blog.slug == slug).first()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        return blog

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch blog: {str(e)}")


@router.get("/id/{blog_id}", response_model=BlogResponse)
async def get_blog_by_id(
    blog_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific blog by ID
    """
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        return blog

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch blog: {str(e)}")
