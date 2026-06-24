"""
Resume Service
Handles resume processing logic
"""

from sqlalchemy.orm import Session
from app.models import Resume, User, MemoryLog
from app.agents.supervisor.supervisor import get_supervisor
from datetime import datetime
from typing import Dict, Any, List


class ResumeService:
    def upload_and_analyze_resume(self, user_id: int, resume_title: str, resume_content: str, db: Session) -> Dict[str, Any]:
        """
        Upload resume and perform analysis
        """
        # Create resume record
        resume = Resume(
            user_id=user_id,
            title=resume_title,
            file_content=resume_content,
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        # Analyze using supervisor agent
        analysis_result = get_supervisor().route_request(
            agent_type="resume",
            task="analyze",
            data={"resume_text": resume_content}
        )
        
        # Update resume with analysis
        resume.ats_score = analysis_result.get("ats_analysis", {}).get("ats_score", 0)
        resume.skills = analysis_result.get("parsed_info", {}).get("skills", [])
        resume.keywords = analysis_result.get("keywords", {}).get("present_keywords", [])
        resume.missing_keywords = analysis_result.get("keywords", {}).get("missing_keywords", [])
        resume.suggestions = analysis_result.get("suggestions", {}).get("general_suggestions", [])
        resume.ats_feedback = analysis_result.get("ats_analysis", {})
        resume.analyzed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(resume)
        
        # Log to memory
        memory_log = MemoryLog(
            user_id=user_id,
            agent_type="resume",
            interaction_type="analysis",
            input_data={"title": resume_title, "content_length": len(resume_content)},
            output_data=analysis_result
        )
        db.add(memory_log)
        db.commit()
        
        return {
            "resume_id": resume.id,
            "analysis": analysis_result
        }
    
    def get_resume(self, resume_id: int, db: Session) -> Dict[str, Any]:
        """Get resume with analysis"""
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return None
        
        return {
            "id": resume.id,
            "title": resume.title,
            "ats_score": resume.ats_score,
            "skills": resume.skills,
            "keywords": resume.keywords,
            "suggestions": resume.suggestions,
            "created_at": resume.created_at,
            "analyzed_at": resume.analyzed_at,
        }
    
    def get_user_resumes(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        """Get all resumes for a user"""
        resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "ats_score": r.ats_score,
                "created_at": r.created_at,
            }
            for r in resumes
        ]
