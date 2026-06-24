"""Voice Interview Routes - Phase 5"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.voice_service import VoiceService
from typing import Dict, Any, List

router = APIRouter()
voice_service = VoiceService()


@router.post("/analyze")
async def analyze_transcript(voice_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return voice_service.analyze_response(
            user_id=user_id,
            transcript=voice_data.get("transcript", ""),
            question=voice_data.get("question", ""),
            duration_seconds=voice_data.get("duration_seconds"),
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete-session")
async def complete_session(session_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return voice_service.complete_session(
            user_id,
            session_data.get("responses", []),
            db,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/practice-prompts")
async def practice_prompts(prompt_data: Dict[str, Any]):
    try:
        return voice_service.get_practice_prompts(
            prompt_data.get("weak_areas", []),
            prompt_data.get("count", 5),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions")
async def list_sessions(db: Session = Depends(get_db)):
    user_id = 1
    return {"sessions": voice_service.get_user_sessions(user_id, db)}
