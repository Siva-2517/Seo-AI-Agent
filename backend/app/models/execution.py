from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(String(100), unique=True, nullable=False, index=True)
    current_agent = Column(String(100), nullable=True)
    status = Column(String(50), default="running")  # running, completed, failed
    execution_logs = Column(JSON, default=list)  # List of log entries
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Execution {self.execution_id}>"
