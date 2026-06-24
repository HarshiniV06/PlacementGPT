"""
RAG Service - Phase 4
Vector database for interview experiences and company knowledge
"""

import os
from typing import List, Dict, Any, Optional
from app.config import settings


SAMPLE_DOCUMENTS = [
    {
        "id": "google_swe_1",
        "content": "Google SWE interview typically has 4-5 rounds: phone screen, 2 coding rounds (LeetCode medium-hard), system design, and Googleyness/behavioral. Focus on graphs, dynamic programming, and system design basics.",
        "metadata": {"company": "Google", "role": "Software Engineer", "type": "interview_experience"},
    },
    {
        "id": "google_swe_2",
        "content": "Google coding interviews emphasize clean code, optimal time complexity, and explaining your thought process. Common topics: arrays, trees, graphs, dynamic programming, greedy algorithms.",
        "metadata": {"company": "Google", "role": "Software Engineer", "type": "topics"},
    },
    {
        "id": "microsoft_swe_1",
        "content": "Microsoft interview has 4-5 rounds including coding (2 rounds), system design, and behavioral. Azure and cloud knowledge is a plus. Coding difficulty is medium, focus on arrays, strings, linked lists.",
        "metadata": {"company": "Microsoft", "role": "Software Engineer", "type": "interview_experience"},
    },
    {
        "id": "amazon_swe_1",
        "content": "Amazon uses Leadership Principles heavily in behavioral rounds. Technical rounds focus on OOP, data structures, and system design. Bar raiser round is critical. Prepare STAR format stories.",
        "metadata": {"company": "Amazon", "role": "Software Engineer", "type": "interview_experience"},
    },
    {
        "id": "tcs_nqt_1",
        "content": "TCS NQT has aptitude, programming logic, coding, and advanced coding sections. Focus on basic DSA, C/Java programming, and aptitude. Cutoff varies by college tier.",
        "metadata": {"company": "TCS", "role": "Graduate Trainee", "type": "interview_experience"},
    },
    {
        "id": "infosys_1",
        "content": "Infosys placement has online test (aptitude + technical + coding) followed by technical and HR interview. Coding is usually easy-medium level. DBMS and OOP concepts are frequently asked.",
        "metadata": {"company": "Infosys", "role": "Software Engineer", "type": "interview_experience"},
    },
    {
        "id": "wipro_1",
        "content": "Wipro NLTH has aptitude, essay writing, coding, and technical interview. Focus on basic programming, SQL queries, and communication skills.",
        "metadata": {"company": "Wipro", "role": "Project Engineer", "type": "interview_experience"},
    },
    {
        "id": "meta_swe_1",
        "content": "Meta (Facebook) interviews include 2 coding rounds (hard LeetCode), system design, and behavioral. Strong focus on product sense and scalability. Graph and tree problems are very common.",
        "metadata": {"company": "Meta", "role": "Software Engineer", "type": "interview_experience"},
    },
    {
        "id": "general_dsa_1",
        "content": "For most product-based companies, master these DSA topics: arrays, strings, linked lists, stacks, queues, trees, graphs, dynamic programming, greedy, binary search, two pointers, sliding window.",
        "metadata": {"company": "General", "role": "Software Engineer", "type": "topics"},
    },
    {
        "id": "general_system_design_1",
        "content": "System design basics for freshers: URL shortener, chat application, news feed, rate limiter. Understand load balancing, caching, databases (SQL vs NoSQL), REST APIs, and microservices basics.",
        "metadata": {"company": "General", "role": "Software Engineer", "type": "topics"},
    },
]


class RAGService:
    """ChromaDB-based retrieval augmented generation service."""

    def __init__(self):
        self._client = None
        self._collection = None
        self._initialized = False

    def _ensure_initialized(self):
        if self._initialized:
            return
        try:
            import chromadb
            os.makedirs(settings.chroma_db_path, exist_ok=True)
            self._client = chromadb.PersistentClient(path=settings.chroma_db_path)
            self._collection = self._client.get_or_create_collection(
                name="placement_knowledge",
                metadata={"description": "Interview experiences and company prep"},
            )
            if self._collection.count() == 0:
                self._seed_documents()
            self._initialized = True
        except Exception as e:
            self._initialized = False
            raise RuntimeError(f"Failed to initialize ChromaDB: {e}")

    def _seed_documents(self):
        ids = [doc["id"] for doc in SAMPLE_DOCUMENTS]
        documents = [doc["content"] for doc in SAMPLE_DOCUMENTS]
        metadatas = [doc["metadata"] for doc in SAMPLE_DOCUMENTS]
        self._collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Add a document to the knowledge base."""
        self._ensure_initialized()
        self._collection.add(ids=[doc_id], documents=[content], metadatas=[metadata])
        return True

    def query(self, query_text: str, n_results: int = 5, company: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query the knowledge base."""
        try:
            self._ensure_initialized()
        except RuntimeError:
            return self._fallback_search(query_text, company)

        where_filter = {"company": company} if company else None
        try:
            results = self._collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_filter,
            )
        except Exception:
            results = self._collection.query(query_texts=[query_text], n_results=n_results)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        return [
            {
                "content": doc,
                "metadata": meta,
                "relevance_score": round(1 - dist, 3) if dist else 1.0,
            }
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]

    def _fallback_search(self, query_text: str, company: Optional[str] = None) -> List[Dict[str, Any]]:
        """Keyword fallback when ChromaDB is unavailable."""
        query_lower = query_text.lower()
        results = []
        for doc in SAMPLE_DOCUMENTS:
            if company and doc["metadata"].get("company", "").lower() != company.lower():
                if doc["metadata"].get("company") != "General":
                    continue
            if any(word in doc["content"].lower() for word in query_lower.split()):
                results.append({
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "relevance_score": 0.5,
                })
        return results[:5]

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        try:
            self._ensure_initialized()
            return {
                "document_count": self._collection.count(),
                "status": "active",
                "path": settings.chroma_db_path,
            }
        except Exception as e:
            return {
                "document_count": len(SAMPLE_DOCUMENTS),
                "status": "fallback",
                "error": str(e),
            }
