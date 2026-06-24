"""
DSA Agent - Phase 2
Tracks competitive programming progress, identifies weak topics, generates plans
"""

from typing import Dict, Any, List, Optional
import json
from collections import defaultdict
from datetime import datetime, timedelta
from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


class DSAAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.7)

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def analyze_progress(self, problems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze solved problems and compute topic-wise stats."""
        if not problems:
            return {
                "total_solved": 0,
                "by_topic": {},
                "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
                "by_platform": {},
                "success_rate": 0.0,
            }

        by_topic: Dict[str, Dict[str, int]] = defaultdict(lambda: {"solved": 0, "attempted": 0})
        by_difficulty = {"easy": 0, "medium": 0, "hard": 0}
        by_platform: Dict[str, int] = defaultdict(int)
        correct = 0

        for p in problems:
            topic = p.get("topic", "general")
            by_topic[topic]["attempted"] += 1
            if p.get("is_correct", True):
                by_topic[topic]["solved"] += 1
                correct += 1
            diff = p.get("difficulty", "medium").lower()
            if diff in by_difficulty:
                by_difficulty[diff] += 1
            by_platform[p.get("platform", "leetcode")] += 1

        topic_stats = {}
        for topic, stats in by_topic.items():
            rate = (stats["solved"] / stats["attempted"] * 100) if stats["attempted"] else 0
            topic_stats[topic] = {
                "solved": stats["solved"],
                "attempted": stats["attempted"],
                "success_rate": round(rate, 1),
            }

        return {
            "total_solved": correct,
            "total_attempted": len(problems),
            "by_topic": topic_stats,
            "by_difficulty": by_difficulty,
            "by_platform": dict(by_platform),
            "success_rate": round(correct / len(problems) * 100, 1) if problems else 0,
        }

    def identify_weak_topics(self, problems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify weak topics from problem history."""
        progress = self.analyze_progress(problems)
        topic_stats = progress.get("by_topic", {})

        weak_topics = []
        strong_topics = []
        for topic, stats in topic_stats.items():
            if stats["success_rate"] < 60 or stats["solved"] < 3:
                weak_topics.append({
                    "topic": topic,
                    "solved": stats["solved"],
                    "success_rate": stats["success_rate"],
                    "priority": "critical" if stats["success_rate"] < 40 else "high",
                })
            elif stats["success_rate"] >= 80 and stats["solved"] >= 5:
                strong_topics.append({"topic": topic, "success_rate": stats["success_rate"]})

        weak_topics.sort(key=lambda x: x["success_rate"])

        prompt = ChatPromptTemplate.from_template("""
        Based on this DSA practice data, provide focused recommendations.

        Topic Stats: {topic_stats}
        Weak Topics: {weak_topics}

        Return JSON with:
        1. focus_areas (list of top 3 topics to focus on)
        2. practice_strategy (string)
        3. recommended_problem_count (int per week)
        4. difficulty_progression (list: easy/medium/hard order)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "topic_stats": json.dumps(topic_stats),
            "weak_topics": json.dumps(weak_topics),
        })
        ai_recs = self._parse_json(result.content)

        return {
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "recommendations": ai_recs,
            "progress_summary": progress,
        }

    def generate_daily_plan(
        self,
        weak_topics: List[str],
        available_hours: float = 2.0,
        difficulty_preference: str = "mixed",
    ) -> Dict[str, Any]:
        """Generate a personalized daily DSA practice plan."""
        prompt = ChatPromptTemplate.from_template("""
        Create a daily DSA practice plan.

        Weak Topics: {weak_topics}
        Available Hours: {available_hours}
        Difficulty Preference: {difficulty_preference}

        Return JSON with:
        1. problems (list of 3-5 problems with: title, topic, difficulty, platform, estimated_minutes, learning_goal)
        2. time_allocation (dict mapping activity to minutes)
        3. topics_focus (list)
        4. warm_up (string - quick revision tip)
        5. cool_down (string - reflection task)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "weak_topics": ", ".join(weak_topics) if weak_topics else "arrays, strings, trees",
            "available_hours": available_hours,
            "difficulty_preference": difficulty_preference,
        })
        plan = self._parse_json(result.content)
        plan["date"] = datetime.utcnow().strftime("%Y-%m-%d")
        plan["available_hours"] = available_hours
        return plan

    def generate_weekly_schedule(
        self,
        weak_topics: List[str],
        problems_per_day: int = 3,
    ) -> Dict[str, Any]:
        """Generate a weekly DSA practice schedule."""
        prompt = ChatPromptTemplate.from_template("""
        Create a 7-day DSA practice schedule.

        Weak Topics: {weak_topics}
        Problems Per Day: {problems_per_day}

        Return JSON with:
        1. weekly_theme (string)
        2. daily_schedule (dict with day_1 through day_7, each having: topics, problem_count, focus, rest_day boolean)
        3. weekly_goal (string)
        4. milestone (what to achieve by week end)

        Return ONLY valid JSON.
        """)
        chain = prompt | self.llm
        result = chain.invoke({
            "weak_topics": ", ".join(weak_topics) if weak_topics else "general DSA",
            "problems_per_day": problems_per_day,
        })
        return self._parse_json(result.content)

    def calculate_consistency(self, problems: List[Dict[str, Any]], days: int = 30) -> Dict[str, Any]:
        """Calculate practice consistency and streaks."""
        if not problems:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "days_active": 0,
                "avg_problems_per_day": 0,
                "consistency_score": 0,
                "daily_activity": {},
            }

        cutoff = datetime.utcnow() - timedelta(days=days)
        daily_counts: Dict[str, int] = defaultdict(int)

        for p in problems:
            solved_date = p.get("solved_date")
            if solved_date:
                if isinstance(solved_date, str):
                    date_str = solved_date[:10]
                else:
                    date_str = solved_date.strftime("%Y-%m-%d")
                daily_counts[date_str] += 1

        sorted_dates = sorted(daily_counts.keys())
        days_active = len(sorted_dates)

        current_streak = 0
        longest_streak = 0
        streak = 0
        today = datetime.utcnow().date()
        for i in range(days):
            d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            if d in daily_counts:
                streak += 1
                if i == 0 or current_streak > 0:
                    current_streak = streak if i == 0 else current_streak + 1
            else:
                if i == 0:
                    current_streak = 0
                streak = 0
            longest_streak = max(longest_streak, streak)

        total_problems = sum(daily_counts.values())
        avg_per_day = round(total_problems / days_active, 1) if days_active else 0
        consistency_score = min(100, round((days_active / days) * 100))

        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "days_active": days_active,
            "period_days": days,
            "avg_problems_per_day": avg_per_day,
            "consistency_score": consistency_score,
            "daily_activity": dict(daily_counts),
            "total_in_period": total_problems,
        }

    def calculate_dsa_score(self, problems: List[Dict[str, Any]]) -> float:
        """Calculate overall DSA readiness score (0-100)."""
        if not problems:
            return 0.0

        progress = self.analyze_progress(problems)
        consistency = self.calculate_consistency(problems)

        solved_score = min(40, progress["total_solved"] * 2)
        difficulty_score = (
            progress["by_difficulty"].get("easy", 0) * 0.5
            + progress["by_difficulty"].get("medium", 0) * 1.5
            + progress["by_difficulty"].get("hard", 0) * 3
        )
        difficulty_score = min(30, difficulty_score)
        consistency_score = consistency["consistency_score"] * 0.3

        topic_count = len(progress.get("by_topic", {}))
        breadth_score = min(30, topic_count * 3)

        return round(min(100, solved_score + difficulty_score * 0.3 + consistency_score + breadth_score * 0.3), 1)
