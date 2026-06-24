"""Analytics Routes - Phase 2"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/readiness-score")
async def get_readiness_score(db: Session = Depends(get_db)):
    user_id = 1
    return analytics_service.get_readiness_score(user_id, db)


@router.get("/skills")
async def get_skills(db: Session = Depends(get_db)):
    user_id = 1
    return analytics_service.get_skills_analysis(user_id, db)


@router.get("/progress")
async def get_progress(db: Session = Depends(get_db)):
    user_id = 1
    return analytics_service.get_progress_report(user_id, db)


@router.get("/placement-prediction")
async def get_prediction(db: Session = Depends(get_db)):
    user_id = 1
    return analytics_service.get_placement_prediction(user_id, db)


@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Fast dashboard summary — no AI calls."""
    user_id = 1
    return analytics_service.get_dashboard_summary(user_id, db)


@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    user_id = 1
    return analytics_service.get_dashboard(user_id, db)


@router.post("/snapshot")
async def create_snapshot(db: Session = Depends(get_db)):
    try:
        user_id = 1
        return analytics_service.create_snapshot(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
