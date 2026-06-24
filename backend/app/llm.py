"""Shared LLM client for all agents."""

from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings


def get_llm(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.gemini_api_key,
        temperature=temperature,
    )
