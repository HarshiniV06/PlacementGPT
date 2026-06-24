"""DSA Service - Phase 2"""

from sqlalchemy.orm import Session
from app.models import DSAProblem, DailyPlan, MemoryLog, UserProgress
from app.agents.supervisor.supervisor import get_supervisor
from datetime import datetime, date
from typing import Dict, Any, List


class DSAService:
    def _problems_to_dicts(self, problems: List[DSAProblem]) -> List[Dict[str, Any]]:
        return [
            {
                "platform": p.platform,
                "problem_id": p.problem_id,
                "problem_title": p.problem_title,
                "topic": p.topic,
                "difficulty": p.difficulty,
                "solved_date": p.solved_date,
                "attempts": p.attempts,
                "time_taken": p.time_taken,
                "is_correct": p.is_correct,
            }
            for p in problems
        ]

    def log_problem(self, user_id: int, problem_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        problem = DSAProblem(
            user_id=user_id,
            platform=problem_data.get("platform", "leetcode"),
            problem_id=problem_data.get("problem_id", ""),
            problem_title=problem_data.get("problem_title", ""),
            topic=problem_data.get("topic", "general"),
            difficulty=problem_data.get("difficulty", "medium"),
            attempts=problem_data.get("attempts", 1),
            time_taken=problem_data.get("time_taken", 0),
            is_correct=problem_data.get("is_correct", True),
        )
        db.add(problem)
        db.commit()
        db.refresh(problem)

        self._update_progress(user_id, db)

        db.add(MemoryLog(
            user_id=user_id,
            agent_type="dsa",
            interaction_type="log_problem",
            input_data=problem_data,
            output_data={"problem_id": problem.id},
        ))
        db.commit()

        return {"success": True, "problem_id": problem.id}

    def _update_progress(self, user_id: int, db: Session):
        problems = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).all()
        problem_dicts = self._problems_to_dicts(problems)
        dsa_score = get_supervisor().route_request("dsa", "calculate_score", {"problems": problem_dicts})
        consistency = get_supervisor().route_request("dsa", "consistency", {"problems": problem_dicts})

        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if not progress:
            progress = UserProgress(user_id=user_id)
            db.add(progress)
        progress.dsa_score = dsa_score.get("dsa_score", 0) if isinstance(dsa_score, dict) else dsa_score
        progress.dsa_consistency = consistency.get("consistency_score", 0)
        db.commit()

    def get_weak_topics(self, user_id: int, db: Session) -> Dict[str, Any]:
        problems = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).all()
        return get_supervisor().route_request(
            "dsa", "weak_topics", {"problems": self._problems_to_dicts(problems)}
        )

    def generate_daily_plan(self, user_id: int, plan_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        weak = self.get_weak_topics(user_id, db)
        weak_topics = [t["topic"] for t in weak.get("weak_topics", [])]
        if plan_data.get("focus_areas"):
            weak_topics = plan_data["focus_areas"]

        plan = get_supervisor().route_request("dsa", "daily_plan", {
            "weak_topics": weak_topics,
            "available_hours": plan_data.get("available_hours", 2.0),
            "difficulty_preference": plan_data.get("difficulty_preference", "mixed"),
        })

        daily = DailyPlan(
            user_id=user_id,
            plan_date=date.today(),
            problems=plan.get("problems", []),
            time_allocation=plan.get("time_allocation", {}),
            topics_focus=plan.get("topics_focus", []),
        )
        db.add(daily)
        db.commit()

        return plan

    def get_consistency(self, user_id: int, db: Session, days: int = 30) -> Dict[str, Any]:
        problems = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).all()
        return get_supervisor().route_request(
            "dsa", "consistency", {"problems": self._problems_to_dicts(problems), "days": days}
        )

    def get_progress(self, user_id: int, db: Session) -> Dict[str, Any]:
        problems = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).all()
        problem_dicts = self._problems_to_dicts(problems)
        return {
            "progress": get_supervisor().route_request("dsa", "analyze_progress", {"problems": problem_dicts}),
            "dsa_score": get_supervisor().route_request("dsa", "calculate_score", {"problems": problem_dicts}),
            "consistency": get_supervisor().route_request("dsa", "consistency", {"problems": problem_dicts}),
            "total_problems": len(problems),
        }

    def get_user_problems(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        problems = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).order_by(
            DSAProblem.solved_date.desc()
        ).all()
        return [
            {
                "id": p.id,
                "platform": p.platform,
                "problem_title": p.problem_title,
                "topic": p.topic,
                "difficulty": p.difficulty,
                "solved_date": p.solved_date,
                "is_correct": p.is_correct,
            }
            for p in problems
        ]
