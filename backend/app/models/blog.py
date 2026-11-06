from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    meta_title = Column(String(255), nullable=False)
    meta_description = Column(String(500), nullable=False)
    h1 = Column(String(255), nullable=False)
    primary_keyword = Column(String(255), nullable=False)
    secondary_keywords = Column(JSON, nullable=False)  # List of keywords
    content = Column(Text, nullable=False)
    faq = Column(JSON, nullable=True)  # List of FAQ objects
    outline = Column(JSON, nullable=True)  # Content structure
    internal_links = Column(JSON, nullable=True)  # List of internal links
    image_suggestions = Column(JSON, nullable=True)  # List of image suggestions
    validation_score = Column(Float, nullable=False)
    status = Column(String(50), default="published")  # published, draft, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    execution_id = Column(String(100), nullable=False, index=True)

    def __repr__(self):
        return f"<Blog {self.title}>"
