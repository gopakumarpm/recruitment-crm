"""
Session manager for handling Streamlit session state.
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import SESSION_TIMEOUT_HOURS


class SessionManager:
    """Manages user session state in Streamlit."""

    @staticmethod
    def init_session_state():
        """Initialize session state variables."""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False

        if 'user' not in st.session_state:
            st.session_state.user = None

        if 'login_time' not in st.session_state:
            st.session_state.login_time = None

    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if user is authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        SessionManager.init_session_state()
        return st.session_state.get('authenticated', False)

    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """
        Get the current logged-in user.

        Returns:
            User dictionary if authenticated, None otherwise
        """
        SessionManager.init_session_state()
        return st.session_state.get('user')

    @staticmethod
    def set_current_user(user: Dict[str, Any]):
        """
        Set the current user in session state.

        Args:
            user: User dictionary
        """
        st.session_state.authenticated = True
        st.session_state.user = user
        st.session_state.login_time = datetime.now()

    @staticmethod
    def clear_session():
        """Clear the session state (logout)."""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.login_time = None

    @staticmethod
    def check_session_timeout() -> bool:
        """
        Check if the session has timed out.

        Returns:
            True if timed out, False otherwise
        """
        if not st.session_state.get('login_time'):
            return False

        login_time = st.session_state.login_time
        current_time = datetime.now()
        time_difference = current_time - login_time

        if time_difference > timedelta(hours=SESSION_TIMEOUT_HOURS):
            SessionManager.clear_session()
            return True

        return False

    @staticmethod
    def get_user_role() -> Optional[str]:
        """
        Get the current user's role.

        Returns:
            User role string, or None if not authenticated
        """
        user = SessionManager.get_current_user()
        return user.get('role') if user else None

    @staticmethod
    def get_user_id() -> Optional[int]:
        """
        Get the current user's ID.

        Returns:
            User ID, or None if not authenticated
        """
        user = SessionManager.get_current_user()
        return user.get('id') if user else None

    @staticmethod
    def get_user_name() -> Optional[str]:
        """
        Get the current user's full name.

        Returns:
            User's full name, or None if not authenticated
        """
        user = SessionManager.get_current_user()
        return user.get('full_name') if user else None


# Create global instance
session = SessionManager()
