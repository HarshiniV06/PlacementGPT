"""Interview Service - Phase 3"""

from sqlalchemy.orm import Session
from app.models import InterviewSession, MemoryLog, UserProgress
from app.agents.supervisor.supervisor import get_supervisor
from datetime import datetime
from typing import Dict, Any, List
import uuid


class InterviewService:
    def start_session(self, user_id: int, session_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        interview_type = session_data.get("interview_type", "technical")

        if interview_type == "hr":
            result = get_supervisor().route_request("interview", "start_hr", session_data)
        else:
            result = get_supervisor().route_request("interview", "start_technical", session_data)

        session_id = result.get("session_id", str(uuid.uuid4())[:8])

        session = InterviewSession(
            user_id=user_id,
            session_id=session_id,
            interview_type=interview_type,
            role=session_data.get("role", "Software Engineer"),
            company=session_data.get("company"),
            questions=result.get("questions", []),
            status="in_progress",
        )
        db.add(session)
        db.commit()
        db.refresh(session)

        result["db_session_id"] = session.id
        return result

    def submit_answer(self, session_id: str, question: str, answer: str, db: Session) -> Dict[str, Any]:
        session = db.query(InterviewSession).filter(InterviewSession.session_id == session_id).first()
        if not session:
            return {"error": "Session not found"}

        evaluation = get_supervisor().route_request("interview", "evaluate_answer", {
            "question": question,
            "answer": answer,
            "interview_type": session.interview_type,
            "role": session.role,
        })

        answers = session.answers or []
        answers.append({"question": question, "answer": answer})
        session.answers = answers

        evaluations = session.evaluations or []
        evaluations.append(evaluation)
        session.evaluations = evaluations
        db.commit()

        return evaluation

    def complete_session(self, session_id: str, db: Session) -> Dict[str, Any]:
        session = db.query(InterviewSession).filter(InterviewSession.session_id == session_id).first()
        if not session:
            return {"error": "Session not found"}

        qa_pairs = [
            {"question": a["question"], "answer": a["answer"]}
            for a in (session.answers or [])
        ]

        result = get_supervisor().route_request("interview", "complete_session", {
            "questions_and_answers": qa_pairs,
            "interview_type": session.interview_type,
            "role": session.role,
        })

        session.overall_score = result.get("overall_score", 0)
        session.communication_score = result.get("communication_score", 0)
        session.technical_score = result.get("technical_score", 0) or 0
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        db.commit()

        progress = db.query(UserProgress).filter(UserProgress.user_id == session.user_id).first()
        if not progress:
            progress = UserProgress(user_id=session.user_id)
            db.add(progress)
        progress.interview_score = result.get("overall_score", 0)
        progress.communication_score = result.get("communication_score", 0)
        progress.technical_score = result.get("technical_score", 0) or 0
        db.commit()

        db.add(MemoryLog(
            user_id=session.user_id,
            agent_type="interview",
            interaction_type="session_complete",
            input_data={"session_id": session_id},
            output_data=result,
        ))
        db.commit()

        return result

    def evaluate_code(self, problem: str, solution_code: str, language: str = "python") -> Dict[str, Any]:
        return get_supervisor().route_request("interview", "evaluate_code", {
            "problem": problem,
            "solution_code": solution_code,
            "language": language,
        })

    def get_user_sessions(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        sessions = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id
        ).order_by(InterviewSession.created_at.desc()).all()
        return [
            {
                "id": s.id,
                "session_id": s.session_id,
                "interview_type": s.interview_type,
                "role": s.role,
                "overall_score": s.overall_score,
                "status": s.status,
                "created_at": s.created_at,
            }
            for s in sessions
        ]

    def get_session(self, session_id: str, db: Session) -> Dict[str, Any]:
        session = db.query(InterviewSession).filter(InterviewSession.session_id == session_id).first()
        if not session:
            return None
        return {
            "session_id": session.session_id,
            "interview_type": session.interview_type,
            "role": session.role,
            "questions": session.questions,
            "answers": session.answers,
            "evaluations": session.evaluations,
            "overall_score": session.overall_score,
            "status": session.status,
        }
