"""
Call history model for tracking candidate interactions.
"""
from typing import List, Dict, Any, Optional
from database.db_manager import db


class CallHistoryModel:
    """Handles call history CRUD operations."""

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[int]:
        """Create a new call record."""
        try:
            query = """
                INSERT INTO call_history (
                    candidate_id, recruiter_id, call_date, call_type,
                    duration, outcome, notes, next_action, next_action_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                data.get('candidate_id'),
                data.get('recruiter_id'),
                data.get('call_date'),
                data.get('call_type'),
                data.get('duration'),
                data.get('outcome'),
                data.get('notes'),
                data.get('next_action'),
                data.get('next_action_date')
            )

            return db.execute_write(query, params)

        except Exception as e:
            print(f"Error creating call history: {e}")
            return None

    @staticmethod
    def get_by_candidate(candidate_id: int) -> List[Dict[str, Any]]:
        """Get all calls for a specific candidate."""
        query = """
            SELECT ch.*, u.full_name as recruiter_name,
                   c.first_name || ' ' || c.last_name as candidate_name
            FROM call_history ch
            LEFT JOIN users u ON ch.recruiter_id = u.id
            LEFT JOIN candidates c ON ch.candidate_id = c.id
            WHERE ch.candidate_id = ?
            ORDER BY ch.call_date DESC
        """
        return db.execute_query(query, (candidate_id,))

    @staticmethod
    def get_all(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all call history records."""
        query = """
            SELECT ch.*, u.full_name as recruiter_name,
                   c.first_name || ' ' || c.last_name as candidate_name
            FROM call_history ch
            LEFT JOIN users u ON ch.recruiter_id = u.id
            LEFT JOIN candidates c ON ch.candidate_id = c.id
            ORDER BY ch.call_date DESC
        """

        if limit:
            query += f" LIMIT {limit}"

        return db.execute_query(query)

    @staticmethod
    def get_upcoming_followups() -> List[Dict[str, Any]]:
        """Get upcoming follow-up actions."""
        query = """
            SELECT ch.*, u.full_name as recruiter_name,
                   c.first_name || ' ' || c.last_name as candidate_name,
                   c.email as candidate_email
            FROM call_history ch
            LEFT JOIN users u ON ch.recruiter_id = u.id
            LEFT JOIN candidates c ON ch.candidate_id = c.id
            WHERE ch.next_action_date >= DATE('now')
            ORDER BY ch.next_action_date ASC
        """
        return db.execute_query(query)

    @staticmethod
    def delete(call_id: int) -> bool:
        """Delete a call record."""
        try:
            query = "DELETE FROM call_history WHERE id = ?"
            db.execute_write(query, (call_id,))
            return True
        except Exception as e:
            print(f"Error deleting call history: {e}")
            return False


call_history_model = CallHistoryModel()
