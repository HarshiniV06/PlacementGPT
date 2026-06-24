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

### Backend Setup

1. **Clone repository and navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Gemini API key and database URL
```

5. **Run database migrations (create tables):**
```bash
python -c "from app.database.db import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine)"
```

6. **Start the server:**
```bash
python run.py
# or
uvicorn app.main:app --reload --port 8000
```

Server will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create .env.local:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Start development server:**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Resume Agent Endpoints

#### Upload and Analyze Resume
```
POST /api/v1/resume/upload
Content-Type: multipart/form-data

Parameters:
- title (string): Resume title
- file (file): Resume file

Response:
{
  "success": true,
  "resume_id": 1,
  "analysis": {
    "parsed_info": {...},
    "ats_analysis": {...},
    "keywords": {...},
    "suggestions": {...}
  }
}
```

#### Analyze Resume Text
```
POST /api/v1/resume/analyze-text
Content-Type: application/json

{
  "resume_text": "...",
  "job_description": "..." (optional)
}
```

#### Get Resume List
```
GET /api/v1/resume/list
```

### Career Planning Endpoints

#### Create Career Plan
```
POST /api/v1/career/create
Content-Type: application/json

{
  "user_data": {
    "skills": ["Python", "JavaScript"],
    "target_role": "Software Engineer",
    "target_companies": ["Google", "Microsoft"],
    "interests": ["Backend", "DevOps"],
    "experience_years": 0
  }
}
```

#### Analyze Skill Gaps
```
POST /api/v1/career/analyze-gaps

{
  "current_skills": ["Python"],
  "target_role": "Software Engineer",
  "target_companies": ["Google"]
}
```

#### Generate Learning Roadmap
```
POST /api/v1/career/generate-roadmap

{
  "current_skills": ["Python"],
  "target_role": "Software Engineer",
  "available_weeks": 16
}
```

## 🔑 Environment Variables

Create a `.env` file with:

```
# API
GEMINI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/placementgpt_db

# Backend
BACKEND_URL=http://localhost:8000
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Frontend
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
DEBUG=true
```

## 📊 Phase 1 Completion Checklist

### Resume Agent ✅
- [x] Resume parsing
- [x] ATS scoring
- [x] Keyword analysis
- [x] Improvement suggestions
- [x] API endpoints

### Career Planner Agent ✅
- [x] Skill gap analysis
- [x] Roadmap generation
- [x] Weekly goal setting
- [x] Monthly goal setting
- [x] Career recommendations
- [x] API endpoints

### Infrastructure ✅
- [x] Database models
- [x] API routes
- [x] Services layer
- [x] Memory system
- [x] Supervisor agent
- [x] Frontend scaffolding

## 🚧 Next Steps (Phase 2)

1. **DSA Agent Implementation**
   - LeetCode API integration
   - GeeksforGeeks tracking
   - Problem categorization
   - Daily challenge generation

2. **Analytics Agent**
   - Progress dashboard
   - Score calculation
   - Trend analysis
   - Prediction models

3. **Frontend Development**
   - Resume upload UI
   - Career plan dashboard
   - Progress tracking
   - Goal management

## 🧠 Agent Architecture

Each agent follows this pattern:

```python
class SpecializedAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(...)
    
    def task_method(self, inputs):
        # Create prompt template
        # Chain with LLM
        # Parse and return results
```

All agents report to the `SupervisorAgent` which routes requests appropriately.

## 💾 Database Schema

### Key Tables
- **users**: User accounts and profiles
- **resumes**: Uploaded resumes with analysis
- **career_plans**: User career plans
- **user_progress**: Tracks scores across all phases
- **memory_logs**: Interaction history
- **skills**: User skills and proficiency

## 🔐 Security Notes

- Currently uses mock user_id=1
- Implement Firebase authentication before deployment
- Add JWT token validation
- Secure API keys in environment variables
- Validate all file uploads

## 🤝 Contributing

1. Create a new branch for each phase
2. Follow existing code structure
3. Add tests for new features
4. Update documentation

## 📝 License

MIT License - See LICENSE file

## 🆘 Support

For issues and questions:
1. Check existing documentation
2. Review Phase 1 API docs
3. Check agent implementations
4. File an issue with details

## 🎓 Learning Outcomes

By building PlacementGPT, you'll learn:
- Multi-agent systems with LangGraph
- LLM engineering and prompt optimization
- FastAPI backend development
- Next.js full-stack development
- Database design and optimization
- System architecture and design patterns
- RAG systems and vector databases
- Production deployment strategies

---

**Current Version**: 0.1.0 (Phase 1 - Scaffolding Complete)  
**Status**: Ready for Phase 1 Implementation  
**Last Updated**: June 2, 2026
