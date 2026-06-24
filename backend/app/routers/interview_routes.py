"""Interview Routes - Phase 3"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.interview_service import InterviewService
from typing import Dict, Any

router = APIRouter()
interview_service = InterviewService()


@router.post("/start")
async def start_interview(session_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return interview_service.start_session(user_id, session_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submit-answer")
async def submit_answer(answer_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        return interview_service.submit_answer(
            session_id=answer_data.get("session_id", ""),
            question=answer_data.get("question", ""),
            answer=answer_data.get("answer", ""),
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete/{session_id}")
async def complete_interview(session_id: str, db: Session = Depends(get_db)):
    try:
        return interview_service.complete_session(session_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluate-code")
async def evaluate_code(code_data: Dict[str, Any]):
    try:
        return interview_service.evaluate_code(
            problem=code_data.get("problem", ""),
            solution_code=code_data.get("solution_code", ""),
            language=code_data.get("language", "python"),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions")
async def list_sessions(db: Session = Depends(get_db)):
    user_id = 1
    return {"sessions": interview_service.get_user_sessions(user_id, db)}


@router.get("/session/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    session = interview_service.get_session(session_id, db)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
