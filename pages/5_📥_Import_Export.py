"""
Import/Export page for data management.
"""
import streamlit as st
from auth.session_manager import session
from auth.authenticator import auth
from models.candidate import candidate_model
from utils.exporters import export_to_csv, export_to_excel, generate_filename

st.set_page_config(page_title="Import/Export", page_icon="📥", layout="wide")

# Check authentication
if not session.is_authenticated():
    st.warning("Please login to access this page.")
    st.stop()

current_user = session.get_current_user()
user_role = current_user['role']

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {current_user['full_name']}")
    st.markdown(f"**Role:** {user_role.capitalize()}")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        session.clear_session()
        st.rerun()

# Main content
st.title("📥 Import/Export Data")
st.markdown("---")

# Check export permission
can_export = auth.check_permission(user_role, 'export')

if not can_export:
    st.warning("You don't have permission to export data.")
    st.stop()

# Export Section
st.subheader("📤 Export Candidates")

col1, col2 = st.columns(2)

with col1:
    export_format = st.radio(
        "Select Export Format",
        options=["CSV", "Excel"],
        horizontal=True
    )

with col2:
    export_all = st.checkbox("Export All Candidates", value=True)

st.markdown("---")

if st.button("📥 Download Data", use_container_width=True, type="primary"):
    # Get candidates
    candidates = candidate_model.get_all()

    if not candidates:
        st.warning("No candidates to export.")
    else:
        # Export based on format
        if export_format == "CSV":
            data = export_to_csv(candidates)
            filename = generate_filename("candidates", "csv")
            mime_type = "text/csv"

        else:  # Excel
            data = export_to_excel(candidates)
            filename = generate_filename("candidates", "xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        if data:
            st.download_button(
                label=f"⬇️ Download {export_format} File",
                data=data,
                file_name=filename,
                mime=mime_type,
                use_container_width=True
            )

            st.success(f"✅ Ready to download {len(candidates)} candidates as {export_format}!")

        else:
            st.error("Failed to generate export file.")

st.markdown("---")

# Export Statistics
st.subheader("📊 Export Statistics")

col1, col2, col3 = st.columns(3)

candidates = candidate_model.get_all()

with col1:
    st.metric("Total Candidates", len(candidates))

with col2:
    active_count = len([c for c in candidates if c.get('status') not in ['Rejected', 'Hired']])
    st.metric("Active Candidates", active_count)

with col3:
    hired_count = len([c for c in candidates if c.get('status') == 'Hired'])
    st.metric("Hired", hired_count)
