"""
FastAPI main application file.
"""
from fastapi import FastAPI
from app.api.routes import agents, expense, task, userprofile
from app.core.config import settings
from app.core.startup import register_all_agents

app = FastAPI(
    title="Personal Assistant API",
    description="API for exposing LangGraph agents",
    version="1.0.0"
)

# Register all agents on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    register_all_agents()

# Include routers
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(expense.router, prefix="/api", tags=["expense"])
app.include_router(task.router, prefix="/api", tags=["task"])
app.include_router(userprofile.router, prefix="/api", tags=["userprofile"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Personal Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

