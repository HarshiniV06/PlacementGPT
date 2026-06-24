from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    password_hash = Column(String)
    profile_picture = Column(String, nullable=True)
    college = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    year = Column(String, nullable=True)
    target_companies = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")
    career_plans = relationship("CareerPlan", back_populates="user")
    user_progress = relationship("UserProgress", back_populates="user")
    memory_logs = relationship("MemoryLog", back_populates="user")


class Resume(Base):
    """Resume model - Phase 1"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    file_path = Column(String)
    file_content = Column(Text)  # Raw text from resume
    
    # ATS Scoring
    ats_score = Column(Float, default=0.0)
    ats_feedback = Column(JSON, default={})
    
    # Skills extracted
    skills = Column(JSON, default=[])
    experience_years = Column(Float, default=0.0)
    projects = Column(JSON, default=[])
    
    # Keywords
    keywords = Column(JSON, default=[])
    missing_keywords = Column(JSON, default=[])
    
    # Suggestions
    suggestions = Column(JSON, default=[])
    improvement_areas = Column(JSON, default=[])
    
    # Metadata
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    analyzed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="resumes")


class Skill(Base):
    """User skills model"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_name = Column(String, index=True)
    proficiency_level = Column(String)  # beginner, intermediate, advanced, expert
    years_of_experience = Column(Float, default=0.0)
    last_used = Column(DateTime, nullable=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CareerPlan(Base):
    """Career plan model - Phase 1"""
    __tablename__ = "career_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Skill gaps
    skill_gaps = Column(JSON, default=[])
    gap_analysis = Column(JSON, default={})
    
    # Roadmap
    roadmap = Column(JSON, default=[])
    phases = Column(JSON, default=[])
    
    # Goals
    weekly_goals = Column(JSON, default=[])
    monthly_goals = Column(JSON, default=[])
    yearly_goals = Column(JSON, default=[])
    
    # Career recommendations
    recommended_roles = Column(JSON, default=[])
    recommended_companies = Column(JSON, default=[])
    
    # Timeline
    target_graduation_date = Column(DateTime, nullable=True)
    estimated_ready_date = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_reviewed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="career_plans")


class UserProgress(Base):
    """Track user progress across all phases"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Phase 1: Resume + Career Planner
    resume_score = Column(Float, default=0.0)
    career_plan_score = Column(Float, default=0.0)
    
    # Phase 2: DSA + Analytics
    dsa_score = Column(Float, default=0.0)
    dsa_consistency = Column(Float, default=0.0)
    
    # Phase 3: Interview
    interview_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    
    # Phase 4: Company Intelligence
    company_readiness_score = Column(Float, default=0.0)
    
    # Overall
    overall_readiness_score = Column(Float, default=0.0)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="user_progress")


class MemoryLog(Base):
    """Store user interaction history for memory layer"""
    __tablename__ = "memory_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    agent_type = Column(String)  # resume, dsa, interview, company, career, analytics
    interaction_type = Column(String)  # query, feedback, update, analysis
    
    input_data = Column(JSON)
    output_data = Column(JSON)
    
    # Context
    context = Column(JSON, default={})
    extra_data = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = relationship("User", back_populates="memory_logs")


class DSAProblem(Base):
    """DSA problem tracking - Phase 2"""
    __tablename__ = "dsa_problems"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String)
    problem_id = Column(String)
    problem_title = Column(String)
    topic = Column(String)
    difficulty = Column(String)
    solved_date = Column(DateTime, default=datetime.utcnow)
    attempts = Column(Integer, default=1)
    time_taken = Column(Integer, default=0)
    is_correct = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DailyPlan(Base):
    """Daily DSA practice plan - Phase 2"""
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_date = Column(Date, default=datetime.utcnow)
    problems = Column(JSON, default=[])
    time_allocation = Column(JSON, default={})
    topics_focus = Column(JSON, default=[])
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalyticsSnapshot(Base):
    """Analytics snapshot - Phase 2"""
    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_score = Column(Float, default=0.0)
    dsa_score = Column(Float, default=0.0)
    interview_score = Column(Float, default=0.0)
    company_score = Column(Float, default=0.0)
    soft_skills_score = Column(Float, default=0.0)
    overall_readiness = Column(Float, default=0.0)
    prediction = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class InterviewSession(Base):
    """Interview session - Phase 3"""
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String, index=True)
    interview_type = Column(String)
    role = Column(String)
    company = Column(String, nullable=True)
    questions = Column(JSON, default=[])
    answers = Column(JSON, default=[])
    evaluations = Column(JSON, default=[])
    overall_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    status = Column(String, default="in_progress")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class CompanyPrep(Base):
    """Company preparation record - Phase 4"""
    __tablename__ = "company_preps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company = Column(String, index=True)
    role = Column(String)
    analysis = Column(JSON, default={})
    readiness_score = Column(Float, default=0.0)
    important_topics = Column(JSON, default=[])
    faqs = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VoiceSession(Base):
    """Voice interview session - Phase 5"""
    __tablename__ = "voice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String, index=True)
    responses = Column(JSON, default=[])
    speech_metrics = Column(JSON, default={})
    session_score = Column(Float, default=0.0)
    filler_word_count = Column(Integer, default=0)
    status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)
