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
from config import APP_NAME, APP_TAGLINE, APP_VERSION, DATABASE_PATH

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
    }

    /* Card styling */
    .stForm, .element-container {
        background: #F9FAFB;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 10px;
        transition: border-color 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #10B981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #10B981;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10B981 0%, #059669 100%);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] p {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h3 {
        color: white !important;
    }

    /* Sidebar navigation links */
    [data-testid="stSidebar"] .css-17lntkn,
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] span {
        color: white !important;
    }

    /* Page navigation */
    section[data-testid="stSidebar"] nav a {
        color: white !important;
    }

    section[data-testid="stSidebar"] nav a:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }

    /* All sidebar text elements */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar links and buttons */
    [data-testid="stSidebar"] button {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* Headers */
    h1 {
        color: #1f2937;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2, h3 {
        color: #374151;
        font-weight: 700;
    }

    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 15px;
    }

    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        background-color: #f3f4f6;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
    }

    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background-color: #f9fafb;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def init_app():
    """Initialize the application and database."""
    # Check if database exists, if not create it
    if not DATABASE_PATH.exists():
        with st.spinner("Initializing database..."):
            initialize_database()

def show_login_page():
    """Display the login page."""
    # Hero section
    st.markdown(f"""
    <div style='text-align: center; padding: 40px 0 20px 0; background: transparent;'>
        <h1 style='font-size: 48px; margin-bottom: 10px;'>🎯 {APP_NAME}</h1>
        <p style='font-size: 20px; color: #1f2937; font-weight: 500;'>{APP_TAGLINE}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Login card
        st.markdown("""
        <div style='background: rgba(240, 249, 255, 0.85); padding: 40px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); backdrop-filter: blur(10px);'>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🔐 Welcome Back!</h2>", unsafe_allow_html=True)

            username = st.text_input("👤 Username", placeholder="Enter your username", label_visibility="visible")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", label_visibility="visible")

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")

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

        st.markdown("""
        <div style='margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #10B98115, #05966915); border-radius: 15px; border-left: 4px solid #10B981;'>
            <p style='margin: 0; font-weight: 600; color: #374151;'>🔑 Default Admin Credentials:</p>
            <p style='margin: 10px 0 0 0; color: #6b7280;'>
                • Username: <code style='background: #f3f4f6; padding: 2px 8px; border-radius: 4px;'>admin</code><br>
                • Password: <code style='background: #f3f4f6; padding: 2px 8px; border-radius: 4px;'>admin123</code>
            </p>
            <p style='margin: 15px 0 0 0; color: #ef4444; font-size: 14px;'>⚠️ Please change the default password after first login!</p>
        </div>
        """, unsafe_allow_html=True)

def show_welcome_page():
    """Display the welcome page after login."""
    user = session.get_current_user()

    # Sidebar user info and logout
    with st.sidebar:
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px; margin-bottom: 20px; backdrop-filter: blur(10px);'>
            <h3 style='color: white; margin: 0 0 10px 0;'>👤 {user['full_name']}</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 5px 0;'><strong>Role:</strong> {user['role'].capitalize()}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 5px 0; font-size: 14px;'><strong>Email:</strong> {user['email']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            session.clear_session()
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: rgba(255,255,255,0.7); text-align: center; font-size: 14px;'><strong>{APP_NAME}</strong> v{APP_VERSION}</p>", unsafe_allow_html=True)

    # Main welcome content with hero section
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 42px; margin-bottom: 10px;'>👥 Welcome to {APP_NAME}</h1>
        <p style='font-size: 24px; color: #6b7280;'>Hello, {user['full_name']}! 👋</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick stats with modern cards
    st.markdown("<h2 style='margin-bottom: 30px;'>📊 Quick Stats</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # Get candidate statistics
    try:
        total_candidates = db.get_table_count('candidates')
        applied = db.execute_query("SELECT COUNT(*) as count FROM candidates WHERE status = 'Applied'")[0]['count']
        screening = db.execute_query("SELECT COUNT(*) as count FROM candidates WHERE status = 'Screening'")[0]['count']
        interview = db.execute_query("SELECT COUNT(*) as count FROM candidates WHERE status = 'Interview'")[0]['count']

        metrics = [
            ("👥 Total Candidates", total_candidates, "#10B981"),
            ("📝 Applied", applied, "#059669"),
            ("🔍 Screening", screening, "#f59e0b"),
            ("💼 Interview", interview, "#6366f1")
        ]

        for col, (label, value, color) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.markdown(f"""
                <div style='background: rgba(240, 249, 255, 0.75); padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid {color}; transition: transform 0.3s ease; backdrop-filter: blur(10px);'>
                    <p style='color: #6b7280; font-size: 14px; margin: 0 0 10px 0; font-weight: 600;'>{label}</p>
                    <h2 style='color: {color}; font-size: 36px; margin: 0; font-weight: 800;'>{value}</h2>
                </div>
                """, unsafe_allow_html=True)

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
