"""Analytics Service - Phase 2"""

from sqlalchemy.orm import Session
from app.models import AnalyticsSnapshot, UserProgress, Resume, DSAProblem, InterviewSession, CompanyPrep, MemoryLog
from app.agents.supervisor.supervisor import get_supervisor
from app.agents.phase2.analytics_agent import AnalyticsAgent
from datetime import datetime
from typing import Dict, Any, List


class AnalyticsService:
    def _get_user_scores(self, user_id: int, db: Session) -> Dict[str, float]:
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if progress:
            return {
                "resume_score": progress.resume_score or 0,
                "dsa_score": progress.dsa_score or 0,
                "interview_score": progress.interview_score or 0,
                "company_readiness_score": progress.company_readiness_score or 0,
                "communication_score": progress.communication_score or 0,
            }

        resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.ats_score.desc()).first()
        return {
            "resume_score": resume.ats_score if resume else 0,
            "dsa_score": 0,
            "interview_score": 0,
            "company_readiness_score": 0,
            "communication_score": 0,
        }

    def _ensure_progress(self, user_id: int, db: Session) -> UserProgress:
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if not progress:
            progress = UserProgress(user_id=user_id)
            db.add(progress)
            db.commit()
            db.refresh(progress)
        return progress

    def get_readiness_score(self, user_id: int, db: Session) -> Dict[str, Any]:
        scores = self._get_user_scores(user_id, db)
        return get_supervisor().route_request("analytics", "readiness_score", {"scores": scores})

    def get_skills_analysis(self, user_id: int, db: Session) -> Dict[str, Any]:
        scores = self._get_user_scores(user_id, db)
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        dsa_count = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).count()
        interview_count = db.query(InterviewSession).filter(InterviewSession.user_id == user_id).count()

        profile = {
            "scores": scores,
            "skills": resume.skills if resume else [],
            "dsa_problems_solved": dsa_count,
            "interviews_completed": interview_count,
        }
        return get_supervisor().route_request("analytics", "skills_analysis", {"profile": profile})

    def get_progress_report(self, user_id: int, db: Session) -> Dict[str, Any]:
        snapshots = db.query(AnalyticsSnapshot).filter(
            AnalyticsSnapshot.user_id == user_id
        ).order_by(AnalyticsSnapshot.created_at).all()

        history = [
            {"overall_readiness": s.overall_readiness, "created_at": s.created_at}
            for s in snapshots
        ]
        return get_supervisor().route_request("analytics", "progress_report", {"history": history})

    def get_placement_prediction(self, user_id: int, db: Session) -> Dict[str, Any]:
        scores = self._get_user_scores(user_id, db)
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        dsa_count = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).count()

        user_data = {
            "scores": scores,
            "skills": resume.skills if resume else [],
            "dsa_problems": dsa_count,
            "resume_ats": resume.ats_score if resume else 0,
        }
        return get_supervisor().route_request("analytics", "placement_prediction", {"user_data": user_data})

    def get_dashboard_summary(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Fast dashboard — database + math only, no AI calls."""
        scores = self._get_user_scores(user_id, db)
        snapshots = db.query(AnalyticsSnapshot).filter(
            AnalyticsSnapshot.user_id == user_id
        ).order_by(AnalyticsSnapshot.created_at).all()

        history = [{"overall_readiness": s.overall_readiness} for s in snapshots]
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        dsa_count = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).count()

        user_data = {
            "scores": scores,
            "history": history,
            "skills": resume.skills if resume else [],
            "dsa_problems": dsa_count,
            "last_updated": datetime.utcnow().isoformat(),
        }
        return AnalyticsAgent().build_dashboard_fast(user_data)

    def get_dashboard(self, user_id: int, db: Session) -> Dict[str, Any]:
        scores = self._get_user_scores(user_id, db)
        snapshots = db.query(AnalyticsSnapshot).filter(
            AnalyticsSnapshot.user_id == user_id
        ).order_by(AnalyticsSnapshot.created_at).all()

        history = [{"overall_readiness": s.overall_readiness} for s in snapshots]
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        dsa_count = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).count()

        user_data = {
            "scores": scores,
            "history": history,
            "skills": resume.skills if resume else [],
            "dsa_problems": dsa_count,
            "last_updated": datetime.utcnow().isoformat(),
        }
        return get_supervisor().route_request("analytics", "dashboard", {"user_data": user_data})

    def create_snapshot(self, user_id: int, db: Session) -> Dict[str, Any]:
        scores = self._get_user_scores(user_id, db)
        readiness = get_supervisor().route_request("analytics", "readiness_score", {"scores": scores})
        prediction = get_supervisor().route_request(
            "analytics", "placement_prediction", {"user_data": {"scores": scores}}
        )

        snapshot = AnalyticsSnapshot(
            user_id=user_id,
            resume_score=scores["resume_score"],
            dsa_score=scores["dsa_score"],
            interview_score=scores["interview_score"],
            company_score=scores["company_readiness_score"],
            soft_skills_score=scores["communication_score"],
            overall_readiness=readiness.get("overall_readiness_score", 0),
            prediction=prediction,
        )
        db.add(snapshot)

        progress = self._ensure_progress(user_id, db)
        progress.overall_readiness_score = readiness.get("overall_readiness_score", 0)
        progress.updated_at = datetime.utcnow()
        db.commit()

        return {
            "snapshot_id": snapshot.id,
            "readiness": readiness,
        }
