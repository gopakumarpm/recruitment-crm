"""
User model for handling user-related database operations.
"""
from typing import List, Dict, Any, Optional
from database.db_manager import db


class UserModel:
    """Handles user CRUD operations."""

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a user by ID.

        Args:
            user_id: User ID

        Returns:
            User dictionary or None
        """
        query = "SELECT * FROM users WHERE id = ?"
        user = db.get_one(query, (user_id,))

        if user:
            user_dict = dict(user)
            # Remove password hash from returned data
            if 'password_hash' in user_dict:
                del user_dict['password_hash']
            return user_dict

        return None

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        """
        Get a user by username.

        Args:
            username: Username

        Returns:
            User dictionary or None
        """
        query = "SELECT * FROM users WHERE username = ?"
        user = db.get_one(query, (username,))

        if user:
            user_dict = dict(user)
            if 'password_hash' in user_dict:
                del user_dict['password_hash']
            return user_dict

        return None

    @staticmethod
    def get_all(include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Get all users.

        Args:
            include_inactive: Include inactive users

        Returns:
            List of user dictionaries
        """
        if include_inactive:
            query = "SELECT * FROM users ORDER BY created_at DESC"
        else:
            query = "SELECT * FROM users WHERE is_active = TRUE ORDER BY created_at DESC"

        users = db.execute_query(query)

        # Remove password hashes
        for user in users:
            if 'password_hash' in user:
                del user['password_hash']

        return users

    @staticmethod
    def get_by_role(role: str) -> List[Dict[str, Any]]:
        """
        Get all users with a specific role.

        Args:
            role: User role

        Returns:
            List of user dictionaries
        """
        query = "SELECT * FROM users WHERE role = ? AND is_active = TRUE ORDER BY full_name"
        users = db.execute_query(query, (role,))

        # Remove password hashes
        for user in users:
            if 'password_hash' in user:
                del user['password_hash']

        return users

    @staticmethod
    def update_profile(user_id: int, full_name: str, email: str) -> bool:
        """
        Update user profile information.

        Args:
            user_id: User ID
            full_name: New full name
            email: New email

        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                UPDATE users
                SET full_name = ?, email = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            db.execute_write(query, (full_name, email, user_id))
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False

    @staticmethod
    def update_role(user_id: int, new_role: str) -> bool:
        """
        Update a user's role.

        Args:
            user_id: User ID
            new_role: New role

        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                UPDATE users
                SET role = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            db.execute_write(query, (new_role, user_id))
            return True
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False

    @staticmethod
    def toggle_active_status(user_id: int) -> bool:
        """
        Toggle user's active status.

        Args:
            user_id: User ID

        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
                UPDATE users
                SET is_active = NOT is_active, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            db.execute_write(query, (user_id,))
            return True
        except Exception as e:
            print(f"Error toggling user status: {e}")
            return False

    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            True if successful, False otherwise
        """
        try:
            query = "DELETE FROM users WHERE id = ?"
            db.execute_write(query, (user_id,))
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    @staticmethod
    def get_recruiters() -> List[Dict[str, Any]]:
        """
        Get all active recruiters (users with recruiter or admin role).

        Returns:
            List of recruiter dictionaries
        """
        query = """
            SELECT * FROM users
            WHERE (role = 'recruiter' OR role = 'admin') AND is_active = TRUE
            ORDER BY full_name
        """
        users = db.execute_query(query)

        # Remove password hashes
        for user in users:
            if 'password_hash' in user:
                del user['password_hash']

        return users


# Create global instance
user_model = UserModel()
