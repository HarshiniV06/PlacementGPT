"""
Resume Routes - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.resume_service import ResumeService
from app.schemas import ResumeAnalyzeRequest
from typing import List

router = APIRouter()
resume_service = ResumeService()


@router.post("/upload")
async def upload_resume(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and analyze a resume
    """
    try:
        # For now, read file as text
        content = await file.read()
        resume_text = content.decode('utf-8')
        
        # Mock user_id - in real app, get from auth
        user_id = 1
        
        result = resume_service.upload_and_analyze_resume(
            user_id=user_id,
            resume_title=title,
            resume_content=resume_text,
            db=db
        )
        
        return {
            "success": True,
            "resume_id": result["resume_id"],
            "analysis": result["analysis"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list")
async def list_resumes(db: Session = Depends(get_db)):
    """
    List all resumes for current user
    """
    # Mock user_id - in real app, get from auth
    user_id = 1
    
    resumes = resume_service.get_user_resumes(user_id, db)
    return {"resumes": resumes}


@router.get("/{resume_id}")
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Get specific resume analysis
    """
    resume = resume_service.get_resume(resume_id, db)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return resume


@router.post("/analyze-text")
async def analyze_resume_text(
    body: ResumeAnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze resume from text (without saving)
    """
    try:
        from app.agents.supervisor.supervisor import get_supervisor
        supervisor = get_supervisor()

        analysis = supervisor.route_request(
            agent_type="resume",
            task="analyze",
            data={
                "resume_text": body.resume_text,
                "job_description": body.job_description
            }
        )

        return analysis

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
