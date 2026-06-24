# PlacementGPT - Multi-Agent AI Placement Coach

> An AI-powered career mentor that continuously analyzes, guides, evaluates, and prepares students for placements.

## 🎯 Project Overview

PlacementGPT combines resume optimization, DSA tracking, interview preparation, company analysis, and career planning into one comprehensive platform. Using a Supervisor Agent that manages 6 specialized agents, it provides personalized guidance 24/7.

### Key Features
- **Resume Agent**: ATS scoring, keyword analysis, improvement suggestions
- **Career Planner Agent**: Skill gap analysis, roadmap generation, goal setting
- **DSA Agent**: Track progress, generate learning plans (Phase 2)
- **Interview Agent**: Mock interviews, communication scoring (Phase 3)
- **Company Intelligence Agent**: Company-specific prep (Phase 4)
- **Analytics Agent**: Placement readiness metrics (Phase 2)
- **Memory System**: Personalized context and history
- **RAG Knowledge Base**: Interview experiences and resources

## 🏗️ Architecture

```
User Interface (Next.js + React)
          ↓
API Gateway (FastAPI)
          ↓
Supervisor Agent (LangGraph)
     ↙    ↙    ↙    ↙
Phase 1: Resume + Career Planner
Phase 2: DSA + Analytics
Phase 3: Interview Agent
Phase 4: Company Intelligence
          ↓
Memory Layer (PostgreSQL)
          ↓
RAG System (ChromaDB)
```

## 📋 Development Phases

### Phase 1: Resume Agent + Career Planner
- ✅ Resume parsing and ATS scoring
- ✅ Keyword analysis
- ✅ Improvement suggestions
- ✅ Skill gap analysis
- ✅ Career roadmap generation
- ✅ Weekly/monthly goal setting
- ✅ Career recommendations

### Phase 2: DSA Agent + Analytics
- DSA progress tracking (LeetCode/GFG)
- Weak topic identification
- Daily/weekly plan generation
- Consistency tracking
- Skill analysis
- Success prediction

### Phase 3: Interview Agent
- Technical mock interviews
- HR mock interviews
- Coding assessments
- Communication evaluation
- Feedback generation

### Phase 4: RAG + Company Intelligence
- Company-specific preparation
- Interview pattern analysis
- Frequently asked questions
- Important topics identification
- Readiness reports

### Phase 5: Voice Interviews + Deployment
- Speech-to-text
- Confidence analysis
- Filler word detection
- Production deployment

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 + React 18
- Tailwind CSS
- Recharts (data visualization)
- Axios (HTTP client)
- Zustand (state management)

**Backend:**
- FastAPI
- LangGraph (agent orchestration)
- LangChain (LLM integration)
- SQLAlchemy (ORM)
- PostgreSQL (database)
- ChromaDB (vector DB)
- Gemini API (LLM)

**Deployment:**
- Vercel (frontend)
- Render/AWS (backend)

## 📦 Project Structure

```
AI CAREER_COACH/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── phase1/           # Phase 1: Resume & Career Planner
│   │   │   │   ├── resume_agent.py
│   │   │   │   ├── career_planner_agent.py
│   │   │   │   └── __init__.py
│   │   │   ├── supervisor/       # Supervisor managing all agents
│   │   │   │   ├── supervisor.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── services/             # Business logic layer
│   │   │   ├── resume_service.py
│   │   │   ├── career_plan_service.py
│   │   │   └── __init__.py
│   │   ├── database/
│   │   │   ├── db.py
│   │   │   └── __init__.py
│   │   ├── models/               # SQLAlchemy models
│   │   │   └── __init__.py
│   │   ├── schemas/              # Pydantic schemas
│   │   │   └── __init__.py
│   │   ├── routers/              # API endpoints
│   │   │   ├── resume_routes.py
│   │   │   ├── career_plan_routes.py
│   │   │   └── __init__.py
│   │   ├── memory/               # Memory system
│   │   │   ├── memory_system.py
│   │   │   └── __init__.py
│   │   ├── config.py
│   │   ├── main.py              # FastAPI app entry
│   │   └── __init__.py
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/               # Next.js pages (when created)
│   │   ├── components/          # React components (when created)
│   │   ├── services/            # API services
│   │   ├── stores/              # Zustand stores
│   │   └── globals.css
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── postcss.config.mjs
│
├── docs/
│   ├── API.md                   # API documentation
│   ├── SETUP.md                 # Setup guide
│   ├── AGENTS.md                # Agent documentation
│   └── PHASE_2_ROADMAP.md       # Phase 2 guide
│
├── .env.example
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- Git
