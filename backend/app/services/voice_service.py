"""Voice Interview Service - Phase 5"""

from sqlalchemy.orm import Session
from app.models import VoiceSession, MemoryLog, UserProgress
from app.agents.supervisor.supervisor import get_supervisor
from typing import Dict, Any, List
import uuid


class VoiceService:
    def analyze_response(
        self,
        user_id: int,
        transcript: str,
        question: str = "",
        duration_seconds: float = None,
        db: Session = None,
    ) -> Dict[str, Any]:
        result = get_supervisor().route_request("voice", "analyze_transcript", {
            "transcript": transcript,
            "question": question,
            "duration_seconds": duration_seconds,
        })

        if db:
            db.add(MemoryLog(
                user_id=user_id,
                agent_type="voice",
                interaction_type="analyze",
                input_data={"question": question, "word_count": len(transcript.split())},
                output_data=result,
            ))
            db.commit()

        return result

    def complete_session(self, user_id: int, responses: List[Dict[str, Any]], db: Session) -> Dict[str, Any]:
        result = get_supervisor().route_request("voice", "complete_session", {
            "responses": responses,
        })

        session_id = str(uuid.uuid4())[:8]
        total_fillers = result.get("total_filler_words", 0)

        session = VoiceSession(
            user_id=user_id,
            session_id=session_id,
            responses=responses,
            speech_metrics=result.get("response_analyses", []),
            session_score=result.get("session_score", 0),
            filler_word_count=total_fillers,
            status="completed",
        )
        db.add(session)
        db.commit()

        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if progress:
            progress.communication_score = result.get("session_score", 0)
            db.commit()

        return {**result, "session_id": session_id}

    def get_practice_prompts(self, weak_areas: List[str], count: int = 5) -> Dict[str, Any]:
        return get_supervisor().route_request("voice", "practice_prompts", {
            "weak_areas": weak_areas, "count": count,
        })

    def get_user_sessions(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        sessions = db.query(VoiceSession).filter(
            VoiceSession.user_id == user_id
        ).order_by(VoiceSession.created_at.desc()).all()
        return [
            {
                "session_id": s.session_id,
                "session_score": s.session_score,
                "filler_word_count": s.filler_word_count,
                "created_at": s.created_at,
            }
            for s in sessions
        ]
