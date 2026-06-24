"""DSA Routes - Phase 2"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.dsa_service import DSAService
from typing import Dict, Any
from app.schemas import WeeklyScheduleRequest

router = APIRouter()
dsa_service = DSAService()


@router.post("/log-problem")
async def log_problem(problem_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return dsa_service.log_problem(user_id, problem_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/weak-topics")
async def get_weak_topics(db: Session = Depends(get_db)):
    user_id = 1
    return dsa_service.get_weak_topics(user_id, db)


@router.post("/daily-plan")
async def generate_daily_plan(plan_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return dsa_service.generate_daily_plan(user_id, plan_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/consistency")
async def get_consistency(days: int = 30, db: Session = Depends(get_db)):
    user_id = 1
    return dsa_service.get_consistency(user_id, db, days)


@router.get("/progress")
async def get_progress(db: Session = Depends(get_db)):
    user_id = 1
    return dsa_service.get_progress(user_id, db)


@router.get("/problems")
async def list_problems(db: Session = Depends(get_db)):
    user_id = 1
    return {"problems": dsa_service.get_user_problems(user_id, db)}


@router.post("/weekly-schedule")
async def weekly_schedule(body: WeeklyScheduleRequest):
    from app.agents.supervisor.supervisor import get_supervisor
    supervisor = get_supervisor()
    return supervisor.route_request("dsa", "weekly_schedule", {
        "weak_topics": body.weak_topics,
        "problems_per_day": body.problems_per_day,
    })
