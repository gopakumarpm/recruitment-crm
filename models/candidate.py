"""
Candidate model for handling candidate-related database operations.
"""
from typing import List, Dict, Any, Optional
from database.db_manager import db


class CandidateModel:
    """Handles candidate CRUD operations."""

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[int]:
        """
        Create a new candidate.

        Args:
            data: Candidate data dictionary

        Returns:
            Candidate ID if successful, None otherwise
        """
        try:
            query = """
                INSERT INTO candidates (
                    first_name, last_name, email, phone, location, linkedin_url,
                    current_role, current_company, years_of_experience, skills, education,
                    status, position_applied, recruiter_id, source,
                    salary_expectation, notice_period, resume_url, notes, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                data.get('first_name'),
                data.get('last_name'),
                data.get('email'),
                data.get('phone'),
                data.get('location'),
                data.get('linkedin_url'),
                data.get('current_role'),
                data.get('current_company'),
                data.get('years_of_experience'),
                data.get('skills'),
                data.get('education'),
                data.get('status', 'Applied'),
                data.get('position_applied'),
                data.get('recruiter_id'),
                data.get('source'),
                data.get('salary_expectation'),
                data.get('notice_period'),
                data.get('resume_url'),
                data.get('notes'),
                data.get('created_by')
            )

            candidate_id = db.execute_write(query, params)
            return candidate_id

        except Exception as e:
            print(f"Error creating candidate: {e}")
            return None

    @staticmethod
    def get_by_id(candidate_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a candidate by ID.

        Args:
            candidate_id: Candidate ID

        Returns:
            Candidate dictionary or None
        """
        query = """
            SELECT c.*, u.full_name as recruiter_name
            FROM candidates c
            LEFT JOIN users u ON c.recruiter_id = u.id
            WHERE c.id = ?
        """
        return db.get_one(query, (candidate_id,))

    @staticmethod
    def get_all(limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all candidates.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of candidate dictionaries
        """
        query = """
            SELECT c.*, u.full_name as recruiter_name
            FROM candidates c
            LEFT JOIN users u ON c.recruiter_id = u.id
            ORDER BY c.created_at DESC
        """

        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"

        return db.execute_query(query)

    @staticmethod
    def update(candidate_id: int, data: Dict[str, Any]) -> bool:
        """
        Update a candidate.

        Args:
            candidate_id: Candidate ID
            data: Updated candidate data

        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                UPDATE candidates
                SET first_name = ?, last_name = ?, email = ?, phone = ?, location = ?,
                    linkedin_url = ?, current_role = ?, current_company = ?,
                    years_of_experience = ?, skills = ?, education = ?, status = ?,
                    position_applied = ?, recruiter_id = ?, source = ?,
                    salary_expectation = ?, notice_period = ?, resume_url = ?, notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """

            params = (
                data.get('first_name'),
                data.get('last_name'),
                data.get('email'),
                data.get('phone'),
                data.get('location'),
                data.get('linkedin_url'),
                data.get('current_role'),
                data.get('current_company'),
                data.get('years_of_experience'),
                data.get('skills'),
                data.get('education'),
                data.get('status'),
                data.get('position_applied'),
                data.get('recruiter_id'),
                data.get('source'),
                data.get('salary_expectation'),
                data.get('notice_period'),
                data.get('resume_url'),
                data.get('notes'),
                candidate_id
            )

            db.execute_write(query, params)
            return True

        except Exception as e:
            print(f"Error updating candidate: {e}")
            return False

    @staticmethod
    def delete(candidate_id: int) -> bool:
        """
        Delete a candidate.

        Args:
            candidate_id: Candidate ID

        Returns:
            True if successful, False otherwise
        """
        try:
            query = "DELETE FROM candidates WHERE id = ?"
            db.execute_write(query, (candidate_id,))
            return True

        except Exception as e:
            print(f"Error deleting candidate: {e}")
            return False

    @staticmethod
    def search(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search candidates with filters.

        Args:
            filters: Dictionary of filter criteria

        Returns:
            List of matching candidate dictionaries
        """
        query = """
            SELECT c.*, u.full_name as recruiter_name
            FROM candidates c
            LEFT JOIN users u ON c.recruiter_id = u.id
            WHERE 1=1
        """
        params = []

        # Text search (name, email, skills)
        if filters.get('search_text'):
            search_text = f"%{filters['search_text']}%"
            query += """ AND (c.first_name LIKE ? OR c.last_name LIKE ? OR
                           c.email LIKE ? OR c.skills LIKE ?)"""
            params.extend([search_text, search_text, search_text, search_text])

        # Status filter
        if filters.get('status'):
            if isinstance(filters['status'], list):
                placeholders = ','.join('?' * len(filters['status']))
                query += f" AND c.status IN ({placeholders})"
                params.extend(filters['status'])
            else:
                query += " AND c.status = ?"
                params.append(filters['status'])

        # Experience range
        if filters.get('min_experience') is not None:
            query += " AND c.years_of_experience >= ?"
            params.append(filters['min_experience'])

        if filters.get('max_experience') is not None:
            query += " AND c.years_of_experience <= ?"
            params.append(filters['max_experience'])

        # Location filter
        if filters.get('location'):
            query += " AND c.location LIKE ?"
            params.append(f"%{filters['location']}%")

        # Recruiter filter
        if filters.get('recruiter_id'):
            query += " AND c.recruiter_id = ?"
            params.append(filters['recruiter_id'])

        # Source filter
        if filters.get('source'):
            query += " AND c.source = ?"
            params.append(filters['source'])

        # Position filter
        if filters.get('position'):
            query += " AND c.position_applied LIKE ?"
            params.append(f"%{filters['position']}%")

        # Date range
        if filters.get('start_date'):
            query += " AND DATE(c.created_at) >= ?"
            params.append(filters['start_date'])

        if filters.get('end_date'):
            query += " AND DATE(c.created_at) <= ?"
            params.append(filters['end_date'])

        query += " ORDER BY c.created_at DESC"

        return db.execute_query(query, tuple(params))

    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """
        Get candidate statistics for dashboard.

        Returns:
            Dictionary of statistics
        """
        stats = {}

        # Total candidates
        stats['total'] = db.get_table_count('candidates')

        # By status
        status_query = """
            SELECT status, COUNT(*) as count
            FROM candidates
            GROUP BY status
        """
        status_data = db.execute_query(status_query)
        stats['by_status'] = {row['status']: row['count'] for row in status_data}

        # By source
        source_query = """
            SELECT source, COUNT(*) as count
            FROM candidates
            WHERE source IS NOT NULL
            GROUP BY source
            ORDER BY count DESC
        """
        source_data = db.execute_query(source_query)
        stats['by_source'] = {row['source']: row['count'] for row in source_data}

        # By recruiter
        recruiter_query = """
            SELECT u.full_name, COUNT(c.id) as count
            FROM candidates c
            LEFT JOIN users u ON c.recruiter_id = u.id
            WHERE c.recruiter_id IS NOT NULL
            GROUP BY u.full_name
            ORDER BY count DESC
        """
        recruiter_data = db.execute_query(recruiter_query)
        stats['by_recruiter'] = {row['full_name']: row['count'] for row in recruiter_data}

        # Recent candidates (last 7 days)
        recent_query = """
            SELECT COUNT(*) as count
            FROM candidates
            WHERE DATE(created_at) >= DATE('now', '-7 days')
        """
        recent_data = db.get_one(recent_query)
        stats['recent'] = recent_data['count'] if recent_data else 0

        return stats

    @staticmethod
    def get_by_status(status: str) -> List[Dict[str, Any]]:
        """
        Get candidates by status.

        Args:
            status: Candidate status

        Returns:
            List of candidate dictionaries
        """
        query = """
            SELECT c.*, u.full_name as recruiter_name
            FROM candidates c
            LEFT JOIN users u ON c.recruiter_id = u.id
            WHERE c.status = ?
            ORDER BY c.created_at DESC
        """
        return db.execute_query(query, (status,))

    @staticmethod
    def update_status(candidate_id: int, new_status: str) -> bool:
        """
        Update only the status of a candidate.

        Args:
            candidate_id: Candidate ID
            new_status: New status

        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                UPDATE candidates
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            db.execute_write(query, (new_status, candidate_id))
            return True

        except Exception as e:
            print(f"Error updating candidate status: {e}")
            return False


# Create global instance
candidate_model = CandidateModel()
