from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(String(100), nullable=False, index=True)
    keyword = Column(String(255), nullable=False)
    search_intent = Column(String(100), nullable=True)
    relevance = Column(String(50), nullable=True)
    competition = Column(String(50), nullable=True)
    search_volume = Column(String(50), nullable=True)
    data_confidence = Column(String(50), nullable=False)  # verified, estimated, unavailable
    source = Column(String(255), nullable=True)
    opportunity_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Keyword {self.keyword}>"
