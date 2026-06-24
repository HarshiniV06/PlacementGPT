"""Company Intelligence Routes - Phase 4"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.company_service import CompanyService
from typing import Dict, Any, List, Optional

router = APIRouter()
company_service = CompanyService()


@router.post("/analyze")
async def analyze_company(company_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return company_service.analyze_company(
            user_id,
            company_data.get("company", ""),
            company_data.get("role", "Software Engineer"),
            db,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/faqs")
async def get_faqs(company_data: Dict[str, Any]):
    try:
        return company_service.get_faqs(
            company_data.get("company", ""),
            company_data.get("role", "Software Engineer"),
            company_data.get("round_type", "technical"),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/important-topics")
async def get_topics(company_data: Dict[str, Any]):
    try:
        return company_service.get_important_topics(
            company_data.get("company", ""),
            company_data.get("role", "Software Engineer"),
            company_data.get("user_skills"),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/readiness-report")
async def readiness_report(company_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        user_id = 1
        return company_service.get_readiness_report(
            user_id,
            company_data.get("company", ""),
            company_data.get("role", "Software Engineer"),
            db,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare")
async def compare_companies(data: Dict[str, Any]):
    try:
        return company_service.compare_companies(
            data.get("companies", []),
            data.get("role", "Software Engineer"),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search")
async def search_knowledge(query: str, company: Optional[str] = None):
    return {"results": company_service.search_knowledge(query, company)}


@router.post("/knowledge")
async def add_knowledge(doc_data: Dict[str, Any]):
    try:
        success = company_service.add_knowledge(
            doc_data.get("id", ""),
            doc_data.get("content", ""),
            doc_data.get("metadata", {}),
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/knowledge/stats")
async def knowledge_stats():
    return company_service.get_knowledge_stats()


@router.get("/my-preps")
async def my_preps(db: Session = Depends(get_db)):
    user_id = 1
    return {"preps": company_service.get_user_preps(user_id, db)}
