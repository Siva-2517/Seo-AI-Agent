from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.routes import generation, blogs, research, health

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SEO Agent - AI-powered SEO blog generation system"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "SEO Agent - AI-powered SEO blog generation system"
    }


# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(generation.router, prefix="/api/generation")
app.include_router(blogs.router, prefix="/api/blogs")
app.include_router(research.router, prefix="/api/research")


@app.get("/api/generation/{execution_id}/stream")
async def stream_execution(
    execution_id: str
):
    """
    Server-Sent Events stream for real-time execution progress
    """
    from fastapi.responses import StreamingResponse
    import json
    import time

    async def event_generator():
        """Generate SSE events for execution progress"""
        while True:
            # Check if execution exists
            if execution_id in generation.executions_store:
                state = generation.executions_store[execution_id]["state"]
                status = generation.executions_store[execution_id]["status"]

                yield f"data: {json.dumps({'status': status, 'current_agent': state.get('current_agent'), 'logs': state.get('logs', [])})}\n\n"

                if status == "completed":
                    break
            else:
                yield f"data: {json.dumps({'status': 'not_found'})}\n\n"
                break

            # Small delay to prevent tight loop
            await asyncio.sleep(1)

    import asyncio
    return StreamingResponse(event_generator(), media_type="text/event-stream")
