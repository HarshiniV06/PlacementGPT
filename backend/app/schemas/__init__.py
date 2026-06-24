from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    college: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[str] = None
    target_companies: List[str] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    college: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[str] = None
    target_companies: Optional[List[str]] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Resume Schemas
class ResumeBase(BaseModel):
    title: str


class ResumeCreate(ResumeBase):
    file_content: str


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    is_primary: Optional[bool] = None


class ResumeAnalysis(BaseModel):
    ats_score: float
    ats_feedback: Dict[str, Any]
    skills: List[str]
    keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
    improvement_areas: List[str]


class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    ats_score: float
    skills: List[str]
    keywords: List[str]
    suggestions: List[str]
    created_at: datetime
    updated_at: datetime
    analyzed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Career Plan Schemas
class CareerPlanBase(BaseModel):
    pass


class CareerPlanCreate(CareerPlanBase):
    pass


class CareerPlanUpdate(BaseModel):
    weekly_goals: Optional[List[str]] = None
    monthly_goals: Optional[List[str]] = None


class CareerPlanResponse(CareerPlanBase):
    id: int
    user_id: int
    skill_gaps: List[str]
    roadmap: List[Dict[str, Any]]
    weekly_goals: List[str]
    monthly_goals: List[str]
    recommended_roles: List[str]
    recommended_companies: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Progress Schemas
class UserProgressResponse(BaseModel):
    id: int
    user_id: int
    resume_score: float
    career_plan_score: float
    dsa_score: float
    interview_score: float
    company_readiness_score: float
    overall_readiness_score: float
    updated_at: datetime

    class Config:
        from_attributes = True


# Request body schemas
class ResumeAnalyzeRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None


class CareerGapsRequest(BaseModel):
    current_skills: List[str]
    target_role: str = "Software Engineer"
    target_companies: Optional[List[str]] = None


class CareerRoadmapRequest(BaseModel):
    current_skills: List[str]
    target_role: str = "Software Engineer"
    available_weeks: int = 16


class WeeklyScheduleRequest(BaseModel):
    weak_topics: List[str]
    problems_per_day: int = 3

