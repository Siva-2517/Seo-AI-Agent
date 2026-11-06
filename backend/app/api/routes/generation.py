from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.execution import GenerationRequest, GenerationResponse, ExecutionStatus
from app.agents.graph import seo_workflow
from app.agents.state import AgentState
from app.models.execution import Execution
from app.models.keyword import Keyword
from datetime import datetime
import uuid
import asyncio
from typing import Dict

router = APIRouter()

# Store for tracking ongoing executions
executions_store: Dict[str, dict] = {}


@router.post("/create", response_model=GenerationResponse)
async def create_blog(
    request: GenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Start the complete AI workflow to generate a blog
    """
    try:
        # Generate execution ID
        execution_id = f"exec_{uuid.uuid4().hex[:12]}"

        # Create execution record
        execution = Execution(
            execution_id=execution_id,
            current_agent="seo_research",
            status="running",
            execution_logs=[]
        )
        db.add(execution)
        db.commit()

        # Initialize state
        initial_state: AgentState = {
            "execution_id": execution_id,
            "current_agent": "seo_research",
            "logs": [],
            "discovered_keywords": [],
            "primary_keyword": None,
            "secondary_keywords": [],
            "semantic_keywords": [],
            "selection_reasoning": "",
            "content_plan": None,
            "is_duplicate": False,
            "duplicate_reason": None,
            "blog_content": None,
            "full_blog_html": None,
            "validation_result": None,
            "retry_count": 0,
            "blog_id": None,
            "blog_url": None,
            "published": False,
            "error": None
        }

        # Store initial state
        executions_store[execution_id] = {
            "state": initial_state,
            "status": "running",
            "task": None
        }

        # Run workflow asynchronously with streaming updates
        async def run_workflow():
            try:
                # Execute the workflow with streaming for real-time updates
                async for output in seo_workflow.astream(initial_state, stream_mode="updates"):
                    # output is a dict with node name as key and state update as value
                    for node_name, node_output in output.items():
                        if node_output and isinstance(node_output, dict):
                            # Update the stored state with the latest values
                            current_state = executions_store[execution_id]["state"]
                            current_state.update(node_output)

                            # Update execution in database with current progress
                            db_exec = db.query(Execution).filter(
                                Execution.execution_id == execution_id
                            ).first()

                            if db_exec:
                                db_exec.current_agent = current_state.get("current_agent", node_name)
                                db_exec.execution_logs = current_state.get("logs", [])
                                db.commit()

                            # Update in-memory store
                            executions_store[execution_id]["state"] = current_state
                            executions_store[execution_id]["status"] = "running"

                # Get final state after streaming completes
                final_state = executions_store[execution_id]["state"]

                # Final database update
                db_exec = db.query(Execution).filter(
                    Execution.execution_id == execution_id
                ).first()

                if db_exec:
                    db_exec.status = "completed" if final_state.get("published") else "failed"
                    db_exec.current_agent = final_state.get("current_agent")
                    db_exec.execution_logs = final_state.get("logs", [])
                    db_exec.completed_at = datetime.utcnow()
                    if final_state.get("error"):
                        db_exec.error_message = final_state.get("error")
                    db.commit()

                # Save keywords to database
                if final_state.get("discovered_keywords"):
                    for kw_data in final_state.get("discovered_keywords", []):
                        keyword = Keyword(
                            execution_id=execution_id,
                            keyword=kw_data.get("keyword"),
                            search_intent=kw_data.get("search_intent"),
                            relevance=kw_data.get("relevance"),
                            competition=kw_data.get("competition"),
                            search_volume=kw_data.get("search_volume"),
                            data_confidence=kw_data.get("data_confidence"),
                            source=kw_data.get("source"),
                            opportunity_score=kw_data.get("opportunity_score")
                        )
                        db.add(keyword)
                    db.commit()

                # Update store to completed
                executions_store[execution_id]["state"] = final_state
                executions_store[execution_id]["status"] = "completed"

            except Exception as e:
                print(f"Workflow error: {str(e)}")
                import traceback
                traceback.print_exc()

                # Update execution status
                db_exec = db.query(Execution).filter(
                    Execution.execution_id == execution_id
                ).first()
                if db_exec:
                    db_exec.status = "failed"
                    db_exec.error_message = str(e)
                    db_exec.completed_at = datetime.utcnow()
                    db.commit()

                executions_store[execution_id]["status"] = "failed"

        # Start workflow in background
        task = asyncio.create_task(run_workflow())
        executions_store[execution_id]["task"] = task

        return GenerationResponse(
            execution_id=execution_id,
            status="running",
            message="Blog generation started successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start generation: {str(e)}")


@router.get("/{execution_id}", response_model=ExecutionStatus)
async def get_execution_status(
    execution_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the current status of an execution
    """
    try:
        # First check memory store
        if execution_id in executions_store:
            state = executions_store[execution_id]["state"]
            status = executions_store[execution_id]["status"]

            return ExecutionStatus(
                execution_id=execution_id,
                current_agent=state.get("current_agent"),
                status=status,
                execution_logs=state.get("logs", []),
                started_at=datetime.utcnow(),  # Simplified
                completed_at=datetime.utcnow() if status == "completed" else None,
                error_message=state.get("error")
            )

        # Check database
        execution = db.query(Execution).filter(
            Execution.execution_id == execution_id
        ).first()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        return ExecutionStatus(
            execution_id=execution.execution_id,
            current_agent=execution.current_agent,
            status=execution.status,
            execution_logs=execution.execution_logs,
            started_at=execution.started_at,
            completed_at=execution.completed_at,
            error_message=execution.error_message
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")
