"""
Main FastAPI Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.db import engine, Base
from app.models import *  # noqa: F401, F403
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.warning("Could not connect to database on startup: %s", e)
    yield


app = FastAPI(
    title="PlacementGPT",
    description="Multi-Agent AI Placement Coach - Phases 1-5",
    version="0.5.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import (  # noqa: E402
    resume_routes,
    career_plan_routes,
    dsa_routes,
    analytics_routes,
    interview_routes,
    company_routes,
    voice_routes,
)

app.include_router(resume_routes.router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(career_plan_routes.router, prefix="/api/v1/career", tags=["Career Planning"])
app.include_router(dsa_routes.router, prefix="/api/v1/dsa", tags=["DSA"])
app.include_router(analytics_routes.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(interview_routes.router, prefix="/api/v1/interview", tags=["Interview"])
app.include_router(company_routes.router, prefix="/api/v1/company", tags=["Company Intelligence"])
app.include_router(voice_routes.router, prefix="/api/v1/voice", tags=["Voice Interview"])


@app.get("/")
async def root():
    return {
        "name": "PlacementGPT",
        "version": "0.5.0",
        "status": "running",
        "description": "Multi-Agent AI Placement Coach - Phases 1-5 Complete",
        "phases": {
            "phase1": "Resume + Career Planner",
            "phase2": "DSA + Analytics",
            "phase3": "Interview Agent",
            "phase4": "Company Intelligence + RAG",
            "phase5": "Voice Interview",
        },
    }


@app.get("/api/v1/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }


@app.get("/api/v1/agents/status")
async def agent_status():
    from app.agents.supervisor.supervisor import AGENT_STATUS
    return AGENT_STATUS
