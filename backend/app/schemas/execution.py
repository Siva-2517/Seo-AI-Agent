from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ExecutionLog(BaseModel):
    timestamp: str
    agent: str
    message: str
    level: str = "info"  # info, warning, error


class ExecutionCreate(BaseModel):
    execution_id: str


class ExecutionStatus(BaseModel):
    execution_id: str
    current_agent: Optional[str] = None
    status: str
    execution_logs: List[ExecutionLog] = []
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class GenerationRequest(BaseModel):
    pass  # No input required for now


class GenerationResponse(BaseModel):
    execution_id: str
    status: str
    message: str
