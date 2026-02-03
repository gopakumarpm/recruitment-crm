"""
Authentication module for user login, logout, and password management.
"""
import bcrypt
from typing import Optional, Dict, Any
from database.db_manager import db
from utils.constants import ROLE_ADMIN, ROLE_RECRUITER, ROLE_VIEWER


class Authenticator:
    """Handles user authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password
            password_hash: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

    @staticmethod
    def login(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with username and password.

        Args:
            username: User's username
            password: User's password

        Returns:
            User dictionary if successful, None otherwise
        """
        try:
            # Get user from database
            query = "SELECT * FROM users WHERE username = ? AND is_active = TRUE"
            user = db.get_one(query, (username,))

            if not user:
                return None

            # Verify password
            if Authenticator.verify_password(password, user['password_hash']):
                # Remove password hash from returned user data
                user_data = dict(user)
                del user_data['password_hash']
                return user_data
            else:
                return None

        except Exception as e:
            print(f"Error during login: {e}")
            return None

    @staticmethod
    def create_user(username: str, email: str, password: str, full_name: str, role: str) -> bool:
        """
        Create a new user.

        Args:
            username: Unique username
            email: User's email
            password: Plain text password (will be hashed)
            full_name: User's full name
            role: User role (admin, recruiter, viewer)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate role
            if role not in [ROLE_ADMIN, ROLE_RECRUITER, ROLE_VIEWER]:
                raise ValueError(f"Invalid role: {role}")

            # Hash password
            password_hash = Authenticator.hash_password(password)

            # Insert user
            query = """
                INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                VALUES (?, ?, ?, ?, ?, TRUE)
            """
            db.execute_write(query, (username, email, password_hash, full_name, role))
            return True

        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change a user's password.

        Args:
            user_id: User's ID
            old_password: Current password
            new_password: New password

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get user's current password hash
            query = "SELECT password_hash FROM users WHERE id = ?"
            result = db.get_one(query, (user_id,))

            if not result:
                return False

            # Verify old password
            if not Authenticator.verify_password(old_password, result['password_hash']):
                return False

            # Hash new password
            new_password_hash = Authenticator.hash_password(new_password)

            # Update password
            update_query = """
                UPDATE users
                SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            db.execute_write(update_query, (new_password_hash, user_id))
            return True

        except Exception as e:
            print(f"Error changing password: {e}")
            return False

    @staticmethod
    def check_permission(role: str, action: str) -> bool:
        """
        Check if a role has permission for an action.

        Args:
            role: User role
            action: Action to check (e.g., 'create', 'edit', 'delete', 'manage_users')

        Returns:
            True if permitted, False otherwise
        """
        permissions = {
            ROLE_ADMIN: ['create', 'edit', 'delete', 'view', 'manage_users', 'export'],
            ROLE_RECRUITER: ['create', 'edit', 'delete', 'view', 'export'],
            ROLE_VIEWER: ['view', 'export']
        }

        return action in permissions.get(role, [])


# Create global instance
auth = Authenticator()
