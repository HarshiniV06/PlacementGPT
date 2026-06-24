"""
Career Planner Agent - Phase 1
Handles skill gap analysis, roadmap generation, and goal setting
"""

from typing import Dict, Any, List
import json
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class CareerPlannerAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.7)
    
    def analyze_skill_gaps(self, current_skills: List[str], target_role: str, target_companies: List[str] = None) -> Dict[str, Any]:
        """
        Analyze skill gaps based on current skills and target role
        """
        prompt = ChatPromptTemplate.from_template("""
        Analyze skill gaps for a student targeting the {target_role} role.
        
        Current Skills:
        {current_skills}
        
        Target Companies (optional):
        {target_companies}
        
        Provide:
        1. skill_gaps (list of missing skills)
        2. gap_severity (list mapping skill to priority: critical, high, medium, low)
        3. learning_resources (dict mapping skill to learning resources)
        4. estimated_learning_time (dict mapping skill to weeks needed)
        5. quick_wins (list of easy skills to learn quickly)
        6. important_skills (list of most critical skills)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "target_role": target_role,
            "current_skills": ", ".join(current_skills),
            "target_companies": ", ".join(target_companies) if target_companies else "Not specified"
        })
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def generate_roadmap(self, current_skills: List[str], target_role: str, available_weeks: int = 16) -> Dict[str, Any]:
        """
        Generate a personalized learning roadmap
        """
        prompt = ChatPromptTemplate.from_template("""
        Create a {available_weeks}-week personalized roadmap for placement preparation.
        
        Target Role: {target_role}
        Current Skills: {current_skills}
        
        Structure the roadmap with:
        1. phases (list of learning phases)
        2. weekly_breakdown (dict with week by week breakdown)
        3. milestones (list of key achievements)
        4. resources (dict of recommended resources)
        5. assessment_points (list of checkpoints)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "available_weeks": available_weeks,
            "target_role": target_role,
            "current_skills": ", ".join(current_skills),
        })
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def set_weekly_goals(self, roadmap: Dict[str, Any], week_number: int) -> Dict[str, Any]:
        """
        Set specific goals for the current week
        """
        prompt = ChatPromptTemplate.from_template("""
        Based on this roadmap, set specific SMART goals for week {week_number}.
        
        Roadmap:
        {roadmap}
        
        Provide:
        1. weekly_goals (list of specific goals)
        2. daily_breakdown (dict with day-wise breakdown)
        3. resources (list of links/resources to use)
        4. success_criteria (list of ways to measure success)
        5. difficulty_level (easy/medium/hard)
        6. estimated_hours (total hours needed)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "week_number": week_number,
            "roadmap": json.dumps(roadmap, indent=2)
        })
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def set_monthly_goals(self, roadmap: Dict[str, Any], month_number: int = 1) -> Dict[str, Any]:
        """
        Set monthly milestones and goals
        """
        prompt = ChatPromptTemplate.from_template("""
        Based on this roadmap, set monthly goals for month {month_number}.
        
        Roadmap:
        {roadmap}
        
        Provide:
        1. monthly_goals (list of major goals)
        2. focus_areas (list of what to focus on)
        3. checkpoints (list of progress check dates)
        4. expected_outcomes (what should be achieved by month end)
        5. success_metrics (how to measure progress)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "month_number": month_number,
            "roadmap": json.dumps(roadmap, indent=2)
        })
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def generate_career_recommendations(self, skills: List[str], interests: List[str], experience_years: float) -> Dict[str, Any]:
        """
        Generate career path recommendations
        """
        prompt = ChatPromptTemplate.from_template("""
        Recommend career paths and roles based on the profile.
        
        Skills: {skills}
        Interests: {interests}
        Experience: {experience_years} years
        
        Provide:
        1. recommended_roles (list of suitable roles)
        2. recommended_companies (list of companies matching profile)
        3. salary_expectation (estimated salary range)
        4. career_growth_path (progression path)
        5. next_steps (immediate action items)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "skills": ", ".join(skills),
            "interests": ", ".join(interests),
            "experience_years": experience_years,
        })
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def create_full_career_plan(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive career plan
        """
        current_skills = user_data.get("skills", [])
        target_role = user_data.get("target_role", "Software Engineer")
        target_companies = user_data.get("target_companies", [])
        interests = user_data.get("interests", [])
        experience_years = user_data.get("experience_years", 0.0)
        
        return {
            "skill_gaps": self.analyze_skill_gaps(current_skills, target_role, target_companies),
            "roadmap": self.generate_roadmap(current_skills, target_role),
            "recommendations": self.generate_career_recommendations(current_skills, interests, experience_years),
        }
