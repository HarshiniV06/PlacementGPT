"""
Memory System
Stores and retrieves user interaction history for context
"""

from sqlalchemy.orm import Session
from app.models import MemoryLog
from typing import List, Dict, Any
from datetime import datetime, timedelta


class MemorySystem:
    """Manages user memory and interaction history"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def store_interaction(self, user_id: int, agent_type: str, interaction_type: str, 
                         input_data: Dict[str, Any], output_data: Dict[str, Any],
                         context: Dict[str, Any] = None) -> MemoryLog:
        """
        Store an agent interaction
        """
        memory_log = MemoryLog(
            user_id=user_id,
            agent_type=agent_type,
            interaction_type=interaction_type,
            input_data=input_data,
            output_data=output_data,
            context=context or {}
        )
        self.db.add(memory_log)
        self.db.commit()
        return memory_log
    
    def get_user_history(self, user_id: int, agent_type: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user interaction history
        """
        query = self.db.query(MemoryLog).filter(MemoryLog.user_id == user_id)
        
        if agent_type:
            query = query.filter(MemoryLog.agent_type == agent_type)
        
        logs = query.order_by(MemoryLog.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": log.id,
                "agent_type": log.agent_type,
                "interaction_type": log.interaction_type,
                "created_at": log.created_at,
                "summary": f"{log.interaction_type} via {log.agent_type}"
            }
            for log in logs
        ]
    
    def get_recent_context(self, user_id: int, days: int = 7) -> Dict[str, Any]:
        """
        Get recent context from the past N days
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        logs = self.db.query(MemoryLog).filter(
            MemoryLog.user_id == user_id,
            MemoryLog.created_at >= cutoff_date
        ).all()
        
        # Organize by agent type
        context = {}
        for log in logs:
            if log.agent_type not in context:
                context[log.agent_type] = []
            context[log.agent_type].append({
                "type": log.interaction_type,
                "created_at": log.created_at,
                "data": log.output_data
            })
        
        return context
    
    def get_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Get a summary of user progress
        """
        all_logs = self.db.query(MemoryLog).filter(MemoryLog.user_id == user_id).all()
        
        agent_interactions = {}
        for log in all_logs:
            if log.agent_type not in agent_interactions:
                agent_interactions[log.agent_type] = 0
            agent_interactions[log.agent_type] += 1
        
        return {
            "total_interactions": len(all_logs),
            "agent_interactions": agent_interactions,
            "first_interaction": min([log.created_at for log in all_logs]) if all_logs else None,
            "last_interaction": max([log.created_at for log in all_logs]) if all_logs else None,
        }
