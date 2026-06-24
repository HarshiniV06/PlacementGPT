"""Company Intelligence Service - Phase 4"""

from sqlalchemy.orm import Session
from app.models import CompanyPrep, MemoryLog, UserProgress
from app.agents.supervisor.supervisor import get_supervisor
from app.services.rag_service import RAGService
from typing import Dict, Any, List, Optional


class CompanyService:
    def __init__(self):
        self._rag = None

    def _get_rag(self) -> RAGService:
        if self._rag is None:
            self._rag = RAGService()
        return self._rag

    def analyze_company(self, user_id: int, company: str, role: str, db: Session) -> Dict[str, Any]:
        result = get_supervisor().route_request("company", "analyze", {
            "company": company, "role": role,
        })

        prep = CompanyPrep(
            user_id=user_id,
            company=company,
            role=role,
            analysis=result,
        )
        db.add(prep)
        db.commit()

        db.add(MemoryLog(
            user_id=user_id,
            agent_type="company",
            interaction_type="analyze",
            input_data={"company": company, "role": role},
            output_data=result,
        ))
        db.commit()

        return result

    def get_faqs(self, company: str, role: str, round_type: str = "technical") -> Dict[str, Any]:
        return get_supervisor().route_request("company", "faqs", {
            "company": company, "role": role, "round_type": round_type,
        })

    def get_important_topics(self, company: str, role: str, user_skills: Optional[List[str]] = None) -> Dict[str, Any]:
        return get_supervisor().route_request("company", "important_topics", {
            "company": company, "role": role, "user_skills": user_skills or [],
        })

    def get_readiness_report(self, user_id: int, company: str, role: str, db: Session) -> Dict[str, Any]:
        from app.models import Resume, DSAProblem
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        dsa_count = db.query(DSAProblem).filter(DSAProblem.user_id == user_id).count()
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

        profile = {
            "resume_score": resume.ats_score if resume else 0,
            "skills": resume.skills if resume else [],
            "dsa_problems": dsa_count,
            "overall_score": progress.overall_readiness_score if progress else 0,
        }

        result = get_supervisor().route_request("company", "readiness_report", {
            "company": company, "role": role, "user_profile": profile,
        })

        prep = db.query(CompanyPrep).filter(
            CompanyPrep.user_id == user_id, CompanyPrep.company == company
        ).first()
        if prep:
            prep.readiness_score = result.get("readiness_score", 0)
            db.commit()
        elif result.get("readiness_score"):
            prep = CompanyPrep(
                user_id=user_id, company=company, role=role,
                readiness_score=result.get("readiness_score", 0),
                analysis=result,
            )
            db.add(prep)
            db.commit()

        if progress:
            progress.company_readiness_score = result.get("readiness_score", 0)
            db.commit()

        return result

    def compare_companies(self, companies: List[str], role: str) -> Dict[str, Any]:
        return get_supervisor().route_request("company", "compare", {
            "companies": companies, "role": role,
        })

    def search_knowledge(self, query: str, company: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._get_rag().query(query, n_results=5, company=company)

    def add_knowledge(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        return self._get_rag().add_document(doc_id, content, metadata)

    def get_knowledge_stats(self) -> Dict[str, Any]:
        return self._get_rag().get_stats()

    def get_user_preps(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        preps = db.query(CompanyPrep).filter(CompanyPrep.user_id == user_id).all()
        return [
            {
                "id": p.id,
                "company": p.company,
                "role": p.role,
                "readiness_score": p.readiness_score,
                "created_at": p.created_at,
            }
            for p in preps
        ]
