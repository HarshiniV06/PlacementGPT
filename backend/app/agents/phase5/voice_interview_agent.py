"""
Voice Interview Agent - Phase 5
Analyzes spoken interview responses (transcript-based with speech metrics)
"""

from typing import Dict, Any, List, Optional
import json
import re
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class VoiceInterviewAgent:
    FILLER_WORDS = [
        "um", "uh", "like", "you know", "basically", "actually",
        "literally", "sort of", "kind of", "i mean", "right",
    ]

    def __init__(self):
        self.llm = get_llm(temperature=0.5)

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def analyze_transcript(
        self,
        transcript: str,
        question: str = "",
        duration_seconds: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Analyze a voice interview transcript for delivery quality."""
        words = transcript.lower().split()
        word_count = len(words)

        filler_count = 0
        filler_details = {}
        text_lower = transcript.lower()
        for filler in self.FILLER_WORDS:
            count = len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
            if count > 0:
                filler_details[filler] = count
                filler_count += count

        filler_rate = (filler_count / word_count * 100) if word_count else 0
        wpm = (word_count / (duration_seconds / 60)) if duration_seconds and duration_seconds > 0 else None

        prompt = ChatPromptTemplate.from_template("""
        Analyze this spoken interview response transcript.

        Question: {question}
        Transcript: {transcript}
        Word Count: {word_count}
        Filler Words Detected: {filler_count}
        Speaking Rate (WPM): {wpm}

        Return JSON with:
        1. confidence_score (0-100)
        2. clarity_score (0-100)
        3. content_relevance_score (0-100)
        4. overall_delivery_score (0-100)
        5. tone_assessment (string)
        6. pacing_feedback (string - too fast/slow/good)
        7. content_feedback (string)
        8. improvement_tips (list of 5)
        9. rewritten_response (improved version of the answer)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "question": question or "General interview question",
            "transcript": transcript,
            "word_count": word_count,
            "filler_count": filler_count,
            "wpm": wpm or "unknown",
        })
        ai_analysis = self._parse_json(result.content)

        return {
            "speech_metrics": {
                "word_count": word_count,
                "filler_word_count": filler_count,
                "filler_word_rate_percent": round(filler_rate, 1),
                "filler_words_detected": filler_details,
                "words_per_minute": round(wpm, 1) if wpm else None,
                "duration_seconds": duration_seconds,
            },
            "delivery_analysis": ai_analysis,
        }

    def analyze_full_session(
        self,
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Analyze a full voice interview session with multiple responses."""
        individual_analyses = []
        scores = []

        for resp in responses:
            analysis = self.analyze_transcript(
                transcript=resp.get("transcript", ""),
                question=resp.get("question", ""),
                duration_seconds=resp.get("duration_seconds"),
            )
            individual_analyses.append({
                "question": resp.get("question"),
                "analysis": analysis,
            })
            delivery = analysis.get("delivery_analysis", {})
            scores.append(delivery.get("overall_delivery_score", 0))

        avg_score = sum(scores) / len(scores) if scores else 0
        total_fillers = sum(
            a["analysis"]["speech_metrics"]["filler_word_count"]
            for a in individual_analyses
        )

        prompt = ChatPromptTemplate.from_template("""
        Provide overall voice interview session feedback.

        Number of Responses: {count}
        Average Delivery Score: {avg_score}
        Total Filler Words: {total_fillers}
        Individual Analyses Summary: {summary}

        Return JSON with:
        1. session_score (0-100)
        2. confidence_trend (improving/stable/declining across responses)
        3. strongest_response (which question number performed best)
        4. weakest_response (which question number needs work)
        5. overall_feedback (string)
        6. practice_recommendations (list)
        7. ready_for_real_interview (boolean)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "count": len(responses),
            "avg_score": avg_score,
            "total_fillers": total_fillers,
            "summary": json.dumps(scores),
        })
        session_summary = self._parse_json(result.content)

        return {
            "session_score": round(avg_score, 1),
            "total_filler_words": total_fillers,
            "response_analyses": individual_analyses,
            "session_summary": session_summary,
        }

    def generate_practice_prompts(
        self,
        weak_areas: List[str],
        count: int = 5,
    ) -> Dict[str, Any]:
        """Generate voice practice prompts for weak areas."""
        prompt = ChatPromptTemplate.from_template("""
        Generate voice interview practice prompts.

        Weak Areas: {weak_areas}
        Number of Prompts: {count}

        Return JSON with:
        1. prompts (list with: question, category, target_duration_seconds, tips_for_delivery)
        2. warm_up_exercise (string - 30 second speaking exercise)
        3. recording_tips (list)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "weak_areas": ", ".join(weak_areas) if weak_areas else "communication, confidence",
            "count": count,
        })
        return self._parse_json(result.content)
