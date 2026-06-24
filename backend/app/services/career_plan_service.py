"""
Career Plan Service
Handles career planning logic
"""

from sqlalchemy.orm import Session
from app.models import CareerPlan, User, MemoryLog
from app.agents.supervisor.supervisor import get_supervisor
from datetime import datetime
from typing import Dict, Any


class CareerPlanService:
    def create_career_plan(self, user_id: int, user_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Create a comprehensive career plan
        """
        # Generate plan using supervisor agent
        plan_result = get_supervisor().route_request(
            agent_type="career_planner",
            task="create_plan",
            data={"user_data": user_data}
        )
        
        # Create career plan record
        career_plan = CareerPlan(
            user_id=user_id,
            skill_gaps=plan_result.get("skill_gaps", {}).get("skill_gaps", []),
            gap_analysis=plan_result.get("skill_gaps", {}),
            roadmap=plan_result.get("roadmap", {}).get("weekly_breakdown", {}),
            phases=plan_result.get("roadmap", {}).get("phases", []),
            recommended_roles=plan_result.get("recommendations", {}).get("recommended_roles", []),
            recommended_companies=plan_result.get("recommendations", {}).get("recommended_companies", []),
        )
        
        db.add(career_plan)
        db.commit()
        db.refresh(career_plan)
        
        # Log to memory
        memory_log = MemoryLog(
            user_id=user_id,
            agent_type="career_planner",
            interaction_type="plan_creation",
            input_data=user_data,
            output_data=plan_result
        )
        db.add(memory_log)
        db.commit()
        
        return {
            "plan_id": career_plan.id,
            "plan": plan_result
        }
    
    def get_career_plan(self, plan_id: int, db: Session) -> Dict[str, Any]:
        """Get career plan"""
        plan = db.query(CareerPlan).filter(CareerPlan.id == plan_id).first()
        if not plan:
            return None
        
        return {
            "id": plan.id,
            "skill_gaps": plan.skill_gaps,
            "roadmap": plan.roadmap,
            "phases": plan.phases,
            "weekly_goals": plan.weekly_goals,
            "monthly_goals": plan.monthly_goals,
            "recommended_roles": plan.recommended_roles,
            "recommended_companies": plan.recommended_companies,
            "created_at": plan.created_at,
        }
    
    def update_weekly_goals(self, plan_id: int, week_number: int, db: Session) -> Dict[str, Any]:
        """Update weekly goals"""
        plan = db.query(CareerPlan).filter(CareerPlan.id == plan_id).first()
        if not plan:
            return {"error": "Plan not found"}
        
        # Generate weekly goals
        goals_result = get_supervisor().route_request(
            agent_type="career_planner",
            task="set_weekly_goals",
            data={
                "roadmap": plan.roadmap,
                "week_number": week_number
            }
        )
        
        plan.weekly_goals = goals_result.get("weekly_goals", [])
        db.commit()
        
        return goals_result
    
    def get_user_career_plan(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get career plan for a user"""
        plan = db.query(CareerPlan).filter(CareerPlan.user_id == user_id).first()
        if not plan:
            return None
        
        return self.get_career_plan(plan.id, db)
