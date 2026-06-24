"""
Analytics Agent - Phase 2
Calculates placement readiness, skill analysis, and success predictions
"""

from typing import Dict, Any, List, Optional
import json
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class AnalyticsAgent:
    WEIGHTS = {
        "resume": 0.30,
        "dsa": 0.30,
        "interview": 0.20,
        "company": 0.10,
        "soft_skills": 0.10,
    }

    def __init__(self):
        self.llm = get_llm(temperature=0.5)

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def calculate_readiness_score(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Calculate weighted overall placement readiness score."""
        resume = scores.get("resume_score", 0)
        dsa = scores.get("dsa_score", 0)
        interview = scores.get("interview_score", 0)
        company = scores.get("company_readiness_score", 0)
        soft_skills = scores.get("communication_score", scores.get("soft_skills_score", 0))

        overall = (
            resume * self.WEIGHTS["resume"]
            + dsa * self.WEIGHTS["dsa"]
            + interview * self.WEIGHTS["interview"]
            + company * self.WEIGHTS["company"]
            + soft_skills * self.WEIGHTS["soft_skills"]
        )

        breakdown = {
            "resume": {"score": resume, "weight": self.WEIGHTS["resume"], "contribution": round(resume * self.WEIGHTS["resume"], 1)},
            "dsa": {"score": dsa, "weight": self.WEIGHTS["dsa"], "contribution": round(dsa * self.WEIGHTS["dsa"], 1)},
            "interview": {"score": interview, "weight": self.WEIGHTS["interview"], "contribution": round(interview * self.WEIGHTS["interview"], 1)},
            "company": {"score": company, "weight": self.WEIGHTS["company"], "contribution": round(company * self.WEIGHTS["company"], 1)},
            "soft_skills": {"score": soft_skills, "weight": self.WEIGHTS["soft_skills"], "contribution": round(soft_skills * self.WEIGHTS["soft_skills"], 1)},
        }

        weakest = min(breakdown.items(), key=lambda x: x[1]["score"])
        strongest = max(breakdown.items(), key=lambda x: x[1]["score"])

        return {
            "overall_readiness_score": round(overall, 1),
            "breakdown": breakdown,
            "weakest_area": weakest[0],
            "strongest_area": strongest[0],
            "readiness_level": self._score_to_level(overall),
        }

    def _score_to_level(self, score: float) -> str:
        if score >= 80:
            return "placement_ready"
        if score >= 60:
            return "almost_ready"
        if score >= 40:
            return "making_progress"
        return "needs_focus"

    def analyze_skills(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Provide detailed skill analysis."""
        prompt = ChatPromptTemplate.from_template("""
        Analyze this student's placement readiness skills profile.

        Profile: {profile}

        Return JSON with:
        1. technical_skills (dict: skill -> level beginner/intermediate/advanced)
        2. soft_skills (dict: skill -> score 0-100)
        3. industry_gap (list of gaps vs industry standards)
        4. growth_trajectory (string: improving/stable/declining)
        5. top_strengths (list)
        6. critical_improvements (list)
        7. recommended_focus (list of 3 priorities)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({"profile": json.dumps(user_profile)})
        return self._parse_json(result.content)

    def generate_progress_report(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate progress report from historical snapshots."""
        if not history:
            return {
                "trend": "no_data",
                "message": "No historical data available yet. Keep practicing!",
                "snapshots_count": 0,
            }

        scores = [h.get("overall_readiness", 0) for h in history]
        trend = "stable"
        if len(scores) >= 2:
            if scores[-1] > scores[0] + 5:
                trend = "improving"
            elif scores[-1] < scores[0] - 5:
                trend = "declining"

        return {
            "trend": trend,
            "current_score": scores[-1] if scores else 0,
            "starting_score": scores[0] if scores else 0,
            "improvement": round(scores[-1] - scores[0], 1) if len(scores) >= 2 else 0,
            "snapshots_count": len(history),
            "score_history": scores,
            "milestones_achieved": self._check_milestones(scores),
        }

    def _check_milestones(self, scores: List[float]) -> List[str]:
        milestones = []
        if any(s >= 40 for s in scores):
            milestones.append("Reached 40% readiness")
        if any(s >= 60 for s in scores):
            milestones.append("Reached 60% readiness - Almost ready!")
        if any(s >= 80 for s in scores):
            milestones.append("Reached 80% readiness - Placement ready!")
        return milestones

    def predict_placement_success(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict placement success probability using profile data."""
        prompt = ChatPromptTemplate.from_template("""
        Predict placement success for this student profile.

        Data: {data}

        Return JSON with:
        1. success_probability (0-100)
        2. confidence_level (low/medium/high)
        3. estimated_timeline_weeks (int)
        4. success_factors (list of positive factors)
        5. risk_areas (list of concerns)
        6. recommended_actions (list of 5 specific actions)
        7. target_companies_feasibility (dict: company -> feasibility low/medium/high)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({"data": json.dumps(user_data)})
        return self._parse_json(result.content)

    def build_dashboard(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build complete analytics dashboard data."""
        scores = user_data.get("scores", {})
        readiness = self.calculate_readiness_score(scores)
        skills = self.analyze_skills(user_data)
        progress = self.generate_progress_report(user_data.get("history", []))
        prediction = self.predict_placement_success(user_data)

        return {
            "readiness": readiness,
            "skills": skills,
            "progress": progress,
            "prediction": prediction,
            "last_updated": user_data.get("last_updated"),
        }

    def build_dashboard_fast(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build dashboard from DB scores only — no LLM calls (instant)."""
        scores = user_data.get("scores", {})
        readiness = self.calculate_readiness_score(scores)
        progress = self.generate_progress_report(user_data.get("history", []))
        overall = readiness.get("overall_readiness_score", 0)

        return {
            "readiness": readiness,
            "progress": progress,
            "prediction": {
                "success_probability": round(overall, 1),
                "confidence_level": "estimated",
                "note": "Based on your current scores. Use full dashboard for AI prediction.",
            },
            "stats": {
                "dsa_problems": user_data.get("dsa_problems", 0),
                "skills_count": len(user_data.get("skills", [])),
            },
            "scores": scores,
            "last_updated": user_data.get("last_updated"),
            "ai_enriched": False,
        }
