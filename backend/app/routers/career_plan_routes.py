"""
Career Plan Routes - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.career_plan_service import CareerPlanService
from app.schemas import CareerGapsRequest, CareerRoadmapRequest
from typing import Dict, Any, List

router = APIRouter()
career_service = CareerPlanService()


@router.post("/create")
async def create_career_plan(
    user_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Create a comprehensive career plan
    """
    try:
        # Mock user_id - in real app, get from auth
        user_id = 1
        
        result = career_service.create_career_plan(
            user_id=user_id,
            user_data=user_data,
            db=db
        )
        
        return {
            "success": True,
            "plan_id": result["plan_id"],
            "plan": result["plan"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-plan")
async def get_user_career_plan(db: Session = Depends(get_db)):
    """
    Get current user's career plan
    """
    # Mock user_id - in real app, get from auth
    user_id = 1
    
    plan = career_service.get_user_career_plan(user_id, db)
    if not plan:
        raise HTTPException(status_code=404, detail="Career plan not found")
    
    return plan


@router.get("/{plan_id}")
async def get_career_plan(plan_id: int, db: Session = Depends(get_db)):
    """
    Get specific career plan
    """
    plan = career_service.get_career_plan(plan_id, db)
    if not plan:
        raise HTTPException(status_code=404, detail="Career plan not found")
    
    return plan


@router.post("/analyze-gaps")
async def analyze_skill_gaps(body: CareerGapsRequest):
    """
    Analyze skill gaps
    """
    try:
        from app.agents.supervisor.supervisor import get_supervisor
        supervisor = get_supervisor()

        result = supervisor.route_request(
            agent_type="career_planner",
            task="analyze_gaps",
            data={
                "current_skills": body.current_skills,
                "target_role": body.target_role,
                "target_companies": body.target_companies
            }
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-roadmap")
async def generate_roadmap(body: CareerRoadmapRequest):
    """
    Generate learning roadmap
    """
    try:
        from app.agents.supervisor.supervisor import get_supervisor
        supervisor = get_supervisor()

        result = supervisor.route_request(
            agent_type="career_planner",
            task="generate_roadmap",
            data={
                "current_skills": body.current_skills,
                "target_role": body.target_role,
                "available_weeks": body.available_weeks
            }
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/weekly-goals")
async def get_weekly_goals(
    plan_id: int,
    week_number: int,
    db: Session = Depends(get_db)
):
    """
    Get weekly goals for a plan
    """
    try:
        result = career_service.update_weekly_goals(plan_id, week_number, db)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
