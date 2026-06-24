"""
Resume Agent - Phase 1
Handles resume parsing, ATS scoring, keyword analysis, and improvement suggestions
"""

from typing import Dict, Any, List
import json
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class ResumeAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.7)
        
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume text and extract structured information
        """
        prompt = ChatPromptTemplate.from_template("""
        Analyze the following resume and extract structured information.
        Return the result as a JSON object.
        
        Resume:
        {resume_text}
        
        Please extract:
        1. skills (list)
        2. experience_years (float)
        3. projects (list of project names/descriptions)
        4. education (list)
        5. certifications (list)
        6. work_experience (list)
        
        Return ONLY valid JSON, no additional text.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"resume_text": resume_text})
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def score_ats(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """
        Score resume for ATS compatibility
        """
        prompt = ChatPromptTemplate.from_template("""
        Score this resume for ATS (Applicant Tracking System) compatibility.
        
        Resume:
        {resume_text}
        
        {"Job Description: " + job_description if job_description else "Consider general software engineering/placement roles"}
        
        Provide:
        1. ats_score (0-100)
        2. strengths (list)
        3. weaknesses (list)
        4. improvement_suggestions (list)
        5. missing_elements (list)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "resume_text": resume_text,
            "job_description": job_description or ""
        })
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def extract_keywords(self, resume_text: str) -> Dict[str, List[str]]:
        """
        Extract keywords and identify missing industry keywords
        """
        prompt = ChatPromptTemplate.from_template("""
        Extract keywords from this resume and identify missing important keywords.
        
        Resume:
        {resume_text}
        
        Return JSON with:
        1. present_keywords (list of found keywords)
        2. missing_keywords (list of important keywords that should be added)
        3. keyword_categories (dict mapping category to keywords)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"resume_text": resume_text})
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def generate_suggestions(self, resume_text: str) -> Dict[str, Any]:
        """
        Generate improvement suggestions for the resume
        """
        prompt = ChatPromptTemplate.from_template("""
        Generate detailed improvement suggestions for this resume.
        
        Resume:
        {resume_text}
        
        Provide:
        1. general_suggestions (list)
        2. formatting_suggestions (list)
        3. content_suggestions (list)
        4. skills_to_highlight (list)
        5. areas_to_improve (list)
        6. priority_changes (list - most important changes to make)
        
        Return ONLY valid JSON.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke({"resume_text": resume_text})
        
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"raw_response": result.content}
    
    def analyze_resume(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """
        Complete resume analysis combining all methods
        """
        return {
            "parsed_info": self.parse_resume(resume_text),
            "ats_analysis": self.score_ats(resume_text, job_description),
            "keywords": self.extract_keywords(resume_text),
            "suggestions": self.generate_suggestions(resume_text),
        }
