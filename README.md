# PlacementGPT

An AI-powered placement preparation platform that helps students improve their resume, plan their career path, practice DSA, prepare for interviews, and track overall placement readiness from one dashboard.

PlacementGPT brings multiple preparation tools into a single guided system, powered by specialized AI agents for resume analysis, career planning, coding practice, mock interviews, company preparation, analytics, and voice practice.

## Overview

Placement preparation is often scattered across different tools: resume checkers, coding platforms, notes, mock interview sheets, company research, and personal progress trackers.

PlacementGPT solves this by creating one centralized AI career coach that can:

- Analyze resumes and suggest improvements
- Build personalized preparation roadmaps
- Track DSA progress and weak topics
- Generate daily and weekly study plans
- Conduct technical and HR interview practice
- Provide company-specific preparation guidance
- Review voice interview transcripts
- Show placement readiness through analytics

## Problem

Students preparing for placements often struggle with three things:

- They do not know where they currently stand.
- They do not know what to improve next.
- Their preparation data is spread across too many places.

Because of this, preparation becomes unstructured and hard to track. A student may solve coding problems, edit resumes, and practice interviews, but still lack a clear picture of overall readiness.

## Solution

PlacementGPT acts as a multi-agent AI placement coach.

Each agent focuses on one part of preparation, while a Supervisor Agent coordinates the system and routes requests to the right module. This makes the platform organized, scalable, and easier to extend with new placement-preparation features.

## Architecture

```text
User Interface (Next.js + React)
          |
          v
API Gateway (FastAPI)
          |
          v
Supervisor Agent (LangGraph)
     /        |        |        \
    v         v        v         v
Phase 1   Phase 2   Phase 3   Phase 4
Resume    DSA       Interview Company
Career    Analytics Agent     Intelligence
Planner
          |
          v
Memory Layer (PostgreSQL)
          |
          v
RAG System (ChromaDB)
```

## AI Agents

The system uses a supervisor-based multi-agent design.

- Supervisor Agent: routes user requests to the correct specialized agent.
- Resume Agent: analyzes resumes, scores ATS readiness, extracts keywords, and suggests improvements.
- Career Planner Agent: identifies skill gaps and creates personalized roadmaps.
- DSA Agent: tracks coding practice, weak topics, consistency, and daily plans.
- Analytics Agent: calculates placement readiness and progress insights.
- Interview Agent: supports technical and HR mock interview practice.
- Company Intelligence Agent: gives company-specific preparation guidance.
- Voice Interview Agent: reviews spoken answers for clarity, filler words, and delivery.

## Key Design Decisions

**Multi-agent structure**  
Each placement-preparation area is handled by a dedicated agent, which keeps the system modular and easier to improve.

**Supervisor-based routing**  
The Supervisor Agent works as the central coordinator, deciding which agent should handle each request.

**Full-stack dashboard**  
The frontend gives students one place to access resume analysis, DSA tracking, interviews, company prep, and analytics.

**Persistent memory layer**  
PostgreSQL stores user progress, resume history, career plans, DSA logs, interview sessions, and readiness data.

**RAG-based company preparation**  
ChromaDB supports searchable knowledge for company-specific preparation and interview guidance.

## Tech Stack

| Layer | Tools |
| --- | --- |
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python |
| Database | PostgreSQL, SQLAlchemy |
| AI Orchestration | LangGraph, LangChain |
| LLM | Gemini API |
| Knowledge Search | ChromaDB |

## Main Modules

- Dashboard
- Resume Analyzer
- Career Planner
- DSA Tracker
- Mock Interview
- Company Prep
- Voice Practice

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL
- Gemini API key

### Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

The backend runs on:

```text
http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on:

```text
http://localhost:3000
```

## Environment Variables

Create a `.env` file inside the `backend` folder:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_database_url
```

Optional frontend variable:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```text
AI CAREER_COACH/
|-- backend/
|   |-- app/
|   |   |-- agents/
|   |   |-- routers/
|   |   |-- services/
|   |   |-- models/
|   |   |-- schemas/
|   |   |-- database/
|   |   |-- memory/
|   |   `-- main.py
|   |-- requirements.txt
|   `-- run.py
|
|-- frontend/
|   |-- src/
|   |   |-- pages/
|   |   |-- components/
|   |   `-- services/
|   |-- package.json
|   `-- next.config.js
|
`-- README.md
```

## Current Status

The core placement-preparation modules are implemented across resume analysis, career planning, DSA tracking, interviews, company preparation, analytics, and voice practice.

Authentication and production deployment are planned as future improvements.

## Future Work

- Add user authentication and personal profiles.
- Deploy the frontend and backend.
- Add richer progress charts and historical analytics.
- Expand company-specific preparation knowledge.
- Add automated tests.
