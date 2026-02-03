"""
Main entry point for the Recruitment CRM application.
"""
import streamlit as st
import os
from pathlib import Path
from database.schema import initialize_database
from auth.authenticator import auth
from auth.session_manager import session
from database.db_manager import db
from config import APP_NAME, APP_VERSION, DATABASE_PATH

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_app():
    """Initialize the application and database."""
    # Check if database exists, if not create it
    if not DATABASE_PATH.exists():
        with st.spinner("Initializing database..."):
            initialize_database()

def show_login_page():
    """Display the login page."""
    st.title("🔐 Recruitment CRM Login")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.subheader("Welcome Back!")

            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    user = auth.login(username, password)

                    if user:
                        session.set_current_user(user)
                        st.success(f"Welcome, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        st.info("""
        **Default Admin Credentials:**
        - Username: `admin`
        - Password: `admin123`

        ⚠️ Please change the default password after first login!
        """)

def show_welcome_page():
    """Display the welcome page after login."""
    user = session.get_current_user()

    # Sidebar user info and logout
    with st.sidebar:
        st.markdown(f"### 👤 {user['full_name']}")
        st.markdown(f"**Role:** {user['role'].capitalize()}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            session.clear_session()
            st.rerun()

        st.markdown("---")
        st.markdown(f"**{APP_NAME}** v{APP_VERSION}")

    # Main welcome content
    st.title(f"👥 Welcome to {APP_NAME}")
    st.markdown(f"### Hello, {user['full_name']}!")
    st.markdown("---")

    # Quick stats
    st.subheader("📊 Quick Stats")

    col1, col2, col3, col4 = st.columns(4)

    # Get candidate statistics
    try:
        total_candidates = db.get_table_count('candidates')
        applied = db.execute_query("SELECT COUNT(*) as count FROM candidates WHERE status = 'Applied'")[0]['count']
        screening = db.execute_query("SELECT COUNT(*) as count FROM candidates WHERE status = 'Screening'")[0]['count']
        interview = db.execute_query("SELECT COUNT(*) as count FROM candidates WHERE status = 'Interview'")[0]['count']

        with col1:
            st.metric("Total Candidates", total_candidates)

        with col2:
            st.metric("Applied", applied)

        with col3:
            st.metric("Screening", screening)

        with col4:
            st.metric("Interview", interview)

    except Exception as e:
        st.warning("Unable to load statistics. The database may be initializing.")

    st.markdown("---")

    # Navigation guide
    st.subheader("🗺️ Navigation Guide")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **📊 Dashboard** - View analytics and recruitment metrics

        **👥 Candidates** - Manage candidate information
        - Add new candidates
        - View and edit existing candidates
        - Delete candidates

        **🔍 Search** - Advanced search and filtering
        - Filter by status, skills, experience
        - Export search results
        - Bulk operations
        """)

    with col2:
        st.markdown("""
        **📞 Call History** - Track interactions
        - Log calls and meetings
        - View interaction timeline
        - Set follow-up reminders

        **📥 Import/Export** - Data management
        - Export candidates to Excel/CSV
        - Download reports

        **⚙️ Settings** - User and system settings
        - Update your profile
        - Change password
        - Admin: Manage users
        """)

    st.markdown("---")

    # Help section
    with st.expander("❓ Need Help?"):
        st.markdown("""
        ### Getting Started
        1. Use the sidebar to navigate between different sections
        2. Start by adding candidates in the **Candidates** page
        3. Log interactions in the **Call History** page
        4. View analytics on the **Dashboard**

        ### Features by Role
        - **Admin**: Full access to all features including user management
        - **Recruiter**: Can create, edit, and delete candidates and call history
        - **Viewer**: Read-only access to view candidates and reports

        ### Tips
        - Use the **Search** page for advanced filtering
        - Export data regularly from the **Import/Export** page
        - Set follow-up reminders in **Call History** to track next actions
        """)

def main():
    """Main application logic."""
    # Initialize app and database
    init_app()

    # Initialize session state
    session.init_session_state()

    # Check for session timeout
    if session.check_session_timeout():
        st.warning("Your session has expired. Please login again.")

    # Show appropriate page based on authentication
    if session.is_authenticated():
        show_welcome_page()
    else:
        show_login_page()


if __name__ == "__main__":
    main()
