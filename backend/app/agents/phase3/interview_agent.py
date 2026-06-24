"""
Interview Agent - Phase 3
Technical and HR mock interviews with feedback and scoring
"""

from typing import Dict, Any, List, Optional
import json
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class InterviewAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.7)

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def start_technical_interview(
        self,
        role: str = "Software Engineer",
        difficulty: str = "medium",
        topics: Optional[List[str]] = None,
        question_count: int = 5,
    ) -> Dict[str, Any]:
        """Generate technical interview questions."""
        topics = topics or ["DSA", "System Design", "OOP", "DBMS"]
        prompt = ChatPromptTemplate.from_template("""
        Generate a technical mock interview for a {role} position.

        Difficulty: {difficulty}
        Topics: {topics}
        Number of Questions: {question_count}

        Return JSON with:
        1. session_id (generate a short unique id string)
        2. interview_type ("technical")
        3. questions (list of objects with: id, question, topic, difficulty, expected_time_minutes, hints)
        4. evaluation_criteria (list of what interviewer looks for)
        5. total_duration_minutes (int)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "role": role,
            "difficulty": difficulty,
            "topics": ", ".join(topics),
            "question_count": question_count,
        })
        return self._parse_json(result.content)

    def start_hr_interview(
        self,
        role: str = "Software Engineer",
        company: str = "Tech Company",
        question_count: int = 5,
    ) -> Dict[str, Any]:
        """Generate HR/behavioral interview questions."""
        prompt = ChatPromptTemplate.from_template("""
        Generate an HR/behavioral mock interview.

        Role: {role}
        Company: {company}
        Number of Questions: {question_count}

        Return JSON with:
        1. session_id (generate a short unique id string)
        2. interview_type ("hr")
        3. questions (list with: id, question, category, star_framework_tip)
        4. evaluation_criteria (list)
        5. total_duration_minutes (int)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "role": role,
            "company": company,
            "question_count": question_count,
        })
        return self._parse_json(result.content)

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        interview_type: str = "technical",
        role: str = "Software Engineer",
    ) -> Dict[str, Any]:
        """Evaluate a single interview answer."""
        prompt = ChatPromptTemplate.from_template("""
        Evaluate this {interview_type} interview answer for a {role} role.

        Question: {question}
        Answer: {answer}

        Return JSON with:
        1. score (0-100)
        2. strengths (list)
        3. weaknesses (list)
        4. feedback (detailed string)
        5. improved_answer (string - how to answer better)
        6. communication_score (0-100)
        7. technical_accuracy (0-100, for technical; null for HR)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "interview_type": interview_type,
            "role": role,
            "question": question,
            "answer": answer,
        })
        return self._parse_json(result.content)

    def evaluate_coding_solution(
        self,
        problem: str,
        solution_code: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        """Evaluate a coding interview solution."""
        prompt = ChatPromptTemplate.from_template("""
        Evaluate this coding interview solution.

        Problem: {problem}
        Language: {language}
        Solution:
        {solution_code}

        Return JSON with:
        1. correctness_score (0-100)
        2. time_complexity (string)
        3. space_complexity (string)
        4. code_quality_score (0-100)
        5. edge_cases_handled (boolean)
        6. feedback (list of improvements)
        7. optimal_approach (string)
        8. overall_score (0-100)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "problem": problem,
            "language": language,
            "solution_code": solution_code,
        })
        return self._parse_json(result.content)

    def complete_session(
        self,
        questions_and_answers: List[Dict[str, str]],
        interview_type: str = "technical",
        role: str = "Software Engineer",
    ) -> Dict[str, Any]:
        """Evaluate a complete interview session."""
        evaluations = []
        total_score = 0
        comm_scores = []

        for qa in questions_and_answers:
            eval_result = self.evaluate_answer(
                question=qa.get("question", ""),
                answer=qa.get("answer", ""),
                interview_type=interview_type,
                role=role,
            )
            evaluations.append({
                "question": qa.get("question"),
                "evaluation": eval_result,
            })
            total_score += eval_result.get("score", 0)
            comm_scores.append(eval_result.get("communication_score", 0))

        avg_score = total_score / len(questions_and_answers) if questions_and_answers else 0
        avg_comm = sum(comm_scores) / len(comm_scores) if comm_scores else 0

        prompt = ChatPromptTemplate.from_template("""
        Provide overall interview session feedback.

        Interview Type: {interview_type}
        Role: {role}
        Average Score: {avg_score}
        Individual Evaluations: {evaluations}

        Return JSON with:
        1. overall_score (0-100)
        2. summary (string)
        3. key_strengths (list)
        4. areas_to_improve (list)
        5. next_steps (list of 3 actions)
        6. readiness_level (not_ready/needs_practice/almost_ready/ready)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "interview_type": interview_type,
            "role": role,
            "avg_score": avg_score,
            "evaluations": json.dumps(evaluations)[:3000],
        })
        session_summary = self._parse_json(result.content)

        return {
            "overall_score": round(avg_score, 1),
            "communication_score": round(avg_comm, 1),
            "technical_score": round(avg_score, 1) if interview_type == "technical" else None,
            "question_evaluations": evaluations,
            "session_summary": session_summary,
        }
