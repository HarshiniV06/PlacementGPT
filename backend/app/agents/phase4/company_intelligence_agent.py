"""
Company Intelligence Agent - Phase 4
Company-specific preparation, interview patterns, and RAG-enhanced insights
"""

from typing import Dict, Any, List, Optional
import json
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class CompanyIntelligenceAgent:
    def __init__(self, rag_service=None):
        self.llm = get_llm(temperature=0.6)
        self.rag_service = rag_service

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def _get_rag_context(self, company: str, query: str) -> str:
        if self.rag_service:
            results = self.rag_service.query(f"{company} {query}", n_results=3)
            if results:
                return "\n".join([r["content"] for r in results])
        return ""

    def analyze_company(
        self,
        company: str,
        role: str = "Software Engineer",
    ) -> Dict[str, Any]:
        """Analyze company interview patterns and requirements."""
        rag_context = self._get_rag_context(company, f"interview process {role}")

        prompt = ChatPromptTemplate.from_template("""
        Provide company-specific placement preparation intelligence.

        Company: {company}
        Role: {role}
        Known Interview Experiences: {rag_context}

        Return JSON with:
        1. company_overview (string)
        2. interview_rounds (list of round descriptions)
        3. common_topics (list)
        4. difficulty_level (easy/medium/hard)
        5. typical_timeline (string)
        6. salary_range (string for freshers)
        7. preparation_tips (list)
        8. key_skills_required (list)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "company": company,
            "role": role,
            "rag_context": rag_context or "No specific data available - use general knowledge",
        })
        analysis = self._parse_json(result.content)
        analysis["company"] = company
        analysis["role"] = role
        return analysis

    def get_frequently_asked_questions(
        self,
        company: str,
        role: str = "Software Engineer",
        round_type: str = "technical",
    ) -> Dict[str, Any]:
        """Get frequently asked questions for a company."""
        rag_context = self._get_rag_context(company, f"FAQs {round_type} {role}")

        prompt = ChatPromptTemplate.from_template("""
        List frequently asked interview questions for {company} - {role} ({round_type} round).

        Context from interview experiences: {rag_context}

        Return JSON with:
        1. technical_questions (list of 10 questions with difficulty)
        2. coding_questions (list of 5 with topics)
        3. hr_questions (list of 5)
        4. system_design_questions (list of 3, if applicable)
        5. tips_for_this_round (list)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "company": company,
            "role": role,
            "round_type": round_type,
            "rag_context": rag_context or "Use general industry knowledge",
        })
        return self._parse_json(result.content)

    def identify_important_topics(
        self,
        company: str,
        role: str = "Software Engineer",
        user_skills: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Identify important topics to study for a specific company."""
        user_skills = user_skills or []
        rag_context = self._get_rag_context(company, f"important topics {role}")

        prompt = ChatPromptTemplate.from_template("""
        Identify important study topics for {company} - {role} interviews.

        User's Current Skills: {user_skills}
        Interview Data: {rag_context}

        Return JSON with:
        1. must_know_topics (list with priority critical/high/medium)
        2. nice_to_have_topics (list)
        3. user_gaps (topics user should learn based on their skills)
        4. study_plan_2_weeks (dict: week_1, week_2 with daily topics)
        5. resource_recommendations (list of free resources)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "company": company,
            "role": role,
            "user_skills": ", ".join(user_skills) if user_skills else "Not specified",
            "rag_context": rag_context or "General tech company preparation",
        })
        return self._parse_json(result.content)

    def generate_readiness_report(
        self,
        company: str,
        role: str,
        user_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate company-specific readiness report."""
        rag_context = self._get_rag_context(company, f"selection criteria {role}")

        prompt = ChatPromptTemplate.from_template("""
        Generate a company-specific placement readiness report.

        Company: {company}
        Role: {role}
        User Profile: {profile}
        Company Context: {rag_context}

        Return JSON with:
        1. readiness_score (0-100 for this specific company)
        2. match_percentage (how well profile matches requirements)
        3. strengths_for_this_company (list)
        4. gaps_for_this_company (list)
        5. preparation_checklist (list of 10 items with done/pending status based on profile)
        6. estimated_preparation_weeks (int)
        7. verdict (string: one sentence assessment)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "company": company,
            "role": role,
            "profile": json.dumps(user_profile),
            "rag_context": rag_context or "Standard software engineering role",
        })
        report = self._parse_json(result.content)
        report["company"] = company
        report["role"] = role
        return report

    def compare_companies(
        self,
        companies: List[str],
        role: str = "Software Engineer",
    ) -> Dict[str, Any]:
        """Compare interview difficulty and preparation across companies."""
        prompt = ChatPromptTemplate.from_template("""
        Compare placement preparation for these companies: {companies}
        Role: {role}

        Return JSON with:
        1. comparison (dict per company: difficulty, focus_areas, avg_prep_weeks)
        2. easiest_to_crack (company name)
        3. hardest_to_crack (company name)
        4. recommended_order (list - which to apply to first)
        5. common_preparation (topics shared across all)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "companies": ", ".join(companies),
            "role": role,
        })
        return self._parse_json(result.content)
