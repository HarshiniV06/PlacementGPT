"""
Supervisor Agent
Manages and orchestrates all specialized agents across Phases 1-5
"""

from typing import Dict, Any
from app.agents.phase1.resume_agent import ResumeAgent
from app.agents.phase1.career_planner_agent import CareerPlannerAgent
from app.agents.phase2.dsa_agent import DSAAgent
from app.agents.phase2.analytics_agent import AnalyticsAgent
from app.agents.phase3.interview_agent import InterviewAgent
from app.agents.phase4.company_intelligence_agent import CompanyIntelligenceAgent
from app.agents.phase5.voice_interview_agent import VoiceInterviewAgent
from app.services.rag_service import RAGService


class SupervisorAgent:
    """Main supervisor that manages all agents"""

    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.career_planner_agent = CareerPlannerAgent()
        self.dsa_agent = DSAAgent()
        self.analytics_agent = AnalyticsAgent()
        self.interview_agent = InterviewAgent()
        self.rag_service = RAGService()
        self.company_agent = CompanyIntelligenceAgent(rag_service=self.rag_service)
        self.voice_agent = VoiceInterviewAgent()

    def route_request(self, agent_type: str, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        handlers = {
            "resume": self._handle_resume_request,
            "career_planner": self._handle_career_planner_request,
            "dsa": self._handle_dsa_request,
            "analytics": self._handle_analytics_request,
            "interview": self._handle_interview_request,
            "company": self._handle_company_request,
            "voice": self._handle_voice_request,
        }
        handler = handlers.get(agent_type)
        if not handler:
            return {"error": f"Unknown agent type: {agent_type}"}
        return handler(task, data)

    def _handle_resume_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if task == "analyze":
            return self.resume_agent.analyze_resume(
                data.get("resume_text", ""), data.get("job_description")
            )
        if task == "parse":
            return self.resume_agent.parse_resume(data.get("resume_text", ""))
        if task == "score_ats":
            return self.resume_agent.score_ats(
                data.get("resume_text", ""), data.get("job_description")
            )
        if task == "extract_keywords":
            return self.resume_agent.extract_keywords(data.get("resume_text", ""))
        if task == "suggest_improvements":
            return self.resume_agent.generate_suggestions(data.get("resume_text", ""))
        return {"error": f"Unknown resume task: {task}"}

    def _handle_career_planner_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if task == "analyze_gaps":
            return self.career_planner_agent.analyze_skill_gaps(
                data.get("current_skills", []),
                data.get("target_role", "Software Engineer"),
                data.get("target_companies"),
            )
        if task == "generate_roadmap":
            return self.career_planner_agent.generate_roadmap(
                data.get("current_skills", []),
                data.get("target_role", "Software Engineer"),
                data.get("available_weeks", 16),
            )
        if task == "set_weekly_goals":
            return self.career_planner_agent.set_weekly_goals(
                data.get("roadmap", {}), data.get("week_number", 1)
            )
        if task == "set_monthly_goals":
            return self.career_planner_agent.set_monthly_goals(
                data.get("roadmap", {}), data.get("month_number", 1)
            )
        if task == "get_recommendations":
            return self.career_planner_agent.generate_career_recommendations(
                data.get("skills", []),
                data.get("interests", []),
                data.get("experience_years", 0.0),
            )
        if task == "create_plan":
            return self.career_planner_agent.create_full_career_plan(
                data.get("user_data", {})
            )
        return {"error": f"Unknown career planner task: {task}"}

    def _handle_dsa_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        problems = data.get("problems", [])
        if task == "analyze_progress":
            return self.dsa_agent.analyze_progress(problems)
        if task == "weak_topics":
            return self.dsa_agent.identify_weak_topics(problems)
        if task == "daily_plan":
            return self.dsa_agent.generate_daily_plan(
                data.get("weak_topics", []),
                data.get("available_hours", 2.0),
                data.get("difficulty_preference", "mixed"),
            )
        if task == "weekly_schedule":
            return self.dsa_agent.generate_weekly_schedule(
                data.get("weak_topics", []),
                data.get("problems_per_day", 3),
            )
        if task == "consistency":
            return self.dsa_agent.calculate_consistency(
                problems, data.get("days", 30)
            )
        if task == "calculate_score":
            score = self.dsa_agent.calculate_dsa_score(problems)
            return {"dsa_score": score}
        return {"error": f"Unknown DSA task: {task}"}

    def _handle_analytics_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if task == "readiness_score":
            return self.analytics_agent.calculate_readiness_score(data.get("scores", {}))
        if task == "skills_analysis":
            return self.analytics_agent.analyze_skills(data.get("profile", {}))
        if task == "progress_report":
            return self.analytics_agent.generate_progress_report(data.get("history", []))
        if task == "placement_prediction":
            return self.analytics_agent.predict_placement_success(data.get("user_data", {}))
        if task == "dashboard":
            return self.analytics_agent.build_dashboard(data.get("user_data", {}))
        if task == "dashboard_fast":
            return self.analytics_agent.build_dashboard_fast(data.get("user_data", {}))
        return {"error": f"Unknown analytics task: {task}"}

    def _handle_interview_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if task == "start_technical":
            return self.interview_agent.start_technical_interview(
                role=data.get("role", "Software Engineer"),
                difficulty=data.get("difficulty", "medium"),
                topics=data.get("topics"),
                question_count=data.get("question_count", 5),
            )
        if task == "start_hr":
            return self.interview_agent.start_hr_interview(
                role=data.get("role", "Software Engineer"),
                company=data.get("company", "Tech Company"),
                question_count=data.get("question_count", 5),
            )
        if task == "evaluate_answer":
            return self.interview_agent.evaluate_answer(
                question=data.get("question", ""),
                answer=data.get("answer", ""),
                interview_type=data.get("interview_type", "technical"),
                role=data.get("role", "Software Engineer"),
            )
        if task == "evaluate_code":
            return self.interview_agent.evaluate_coding_solution(
                problem=data.get("problem", ""),
                solution_code=data.get("solution_code", ""),
                language=data.get("language", "python"),
            )
        if task == "complete_session":
            return self.interview_agent.complete_session(
                questions_and_answers=data.get("questions_and_answers", []),
                interview_type=data.get("interview_type", "technical"),
                role=data.get("role", "Software Engineer"),
            )
        return {"error": f"Unknown interview task: {task}"}

    def _handle_company_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if task == "analyze":
            return self.company_agent.analyze_company(
                data.get("company", ""), data.get("role", "Software Engineer")
            )
        if task == "faqs":
            return self.company_agent.get_frequently_asked_questions(
                data.get("company", ""),
                data.get("role", "Software Engineer"),
                data.get("round_type", "technical"),
            )
        if task == "important_topics":
            return self.company_agent.identify_important_topics(
                data.get("company", ""),
                data.get("role", "Software Engineer"),
                data.get("user_skills"),
            )
        if task == "readiness_report":
            return self.company_agent.generate_readiness_report(
                data.get("company", ""),
                data.get("role", "Software Engineer"),
                data.get("user_profile", {}),
            )
        if task == "compare":
            return self.company_agent.compare_companies(
                data.get("companies", []),
                data.get("role", "Software Engineer"),
            )
        return {"error": f"Unknown company task: {task}"}

    def _handle_voice_request(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if task == "analyze_transcript":
            return self.voice_agent.analyze_transcript(
                transcript=data.get("transcript", ""),
                question=data.get("question", ""),
                duration_seconds=data.get("duration_seconds"),
            )
        if task == "complete_session":
            return self.voice_agent.analyze_full_session(data.get("responses", []))
        if task == "practice_prompts":
            return self.voice_agent.generate_practice_prompts(
                data.get("weak_areas", []),
                data.get("count", 5),
            )
        return {"error": f"Unknown voice task: {task}"}

    def get_agent_status(self) -> Dict[str, Any]:
        return AGENT_STATUS


AGENT_STATUS = {
    "phase1": {
        "resume_agent": "active",
        "career_planner_agent": "active",
    },
    "phase2": {
        "dsa_agent": "active",
        "analytics_agent": "active",
    },
    "phase3": {
        "interview_agent": "active",
    },
    "phase4": {
        "company_intelligence_agent": "active",
        "rag_system": "active",
    },
    "phase5": {
        "voice_interview_agent": "active",
    },
}


_supervisor: "SupervisorAgent | None" = None


def get_supervisor() -> "SupervisorAgent":
    """Return a cached supervisor instance (avoids re-initializing agents/RAG per request)."""
    global _supervisor
    if _supervisor is None:
        _supervisor = SupervisorAgent()
    return _supervisor
