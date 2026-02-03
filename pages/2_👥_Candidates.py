"""
Candidates page for managing candidate information.
"""
import streamlit as st
import pandas as pd
from auth.session_manager import session
from auth.authenticator import auth
from models.candidate import candidate_model
from models.user import user_model
from utils.validators import validate_candidate_data
from utils.constants import (
    CANDIDATE_STATUSES, CANDIDATE_SOURCES, COMMON_POSITIONS,
    NOTICE_PERIODS, EDUCATION_LEVELS
)

# Page configuration
st.set_page_config(page_title="Candidates", page_icon="👥", layout="wide")

# Check authentication
if not session.is_authenticated():
    st.warning("Please login to access this page.")
    st.stop()

# Get current user
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
st.title("👥 Candidate Management")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit/Delete"])

# TAB 1: View All Candidates
with tab1:
    st.subheader("All Candidates")

    # Get all candidates
    candidates = candidate_model.get_all()

    if candidates:
        # Convert to DataFrame for display
        df = pd.DataFrame(candidates)

        # Select columns to display
        display_columns = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'location',
            'current_role', 'status', 'position_applied', 'recruiter_name'
        ]

        # Filter columns that exist
        display_columns = [col for col in display_columns if col in df.columns]
        df_display = df[display_columns]

        # Rename columns for better display
        df_display = df_display.rename(columns={
            'id': 'ID',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'location': 'Location',
            'current_role': 'Current Role',
            'status': 'Status',
            'position_applied': 'Position Applied',
            'recruiter_name': 'Recruiter'
        })

        st.dataframe(df_display, use_container_width=True, hide_index=True)
        st.info(f"**Total Candidates:** {len(candidates)}")

    else:
        st.info("No candidates found. Add your first candidate using the 'Add New' tab.")

# TAB 2: Add New Candidate
with tab2:
    st.subheader("Add New Candidate")

    can_create = auth.check_permission(user_role, 'create')

    if not can_create:
        st.warning("You don't have permission to add candidates.")
    else:
        with st.form("add_candidate_form"):
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name*", placeholder="John")
                last_name = st.text_input("Last Name*", placeholder="Doe")
                email = st.text_input("Email*", placeholder="john.doe@example.com")
                phone = st.text_input("Phone", placeholder="+1234567890")
                location = st.text_input("Location", placeholder="New York, NY")
                linkedin_url = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/johndoe")

            with col2:
                current_role = st.text_input("Current Role", placeholder="Software Engineer")
                current_company = st.text_input("Current Company", placeholder="ABC Corp")
                years_of_experience = st.number_input("Years of Experience", min_value=0, max_value=70, value=0)
                skills = st.text_area("Skills (comma-separated)", placeholder="Python, JavaScript, SQL")
                education = st.selectbox("Education Level", options=[""] + EDUCATION_LEVELS)
                position_applied = st.selectbox("Position Applied For", options=[""] + COMMON_POSITIONS)

            col3, col4 = st.columns(2)

            with col3:
                status = st.selectbox("Status*", options=CANDIDATE_STATUSES, index=0)
                source = st.selectbox("Source", options=[""] + CANDIDATE_SOURCES)

            with col4:
                # Get recruiters for assignment
                recruiters = user_model.get_recruiters()
                recruiter_options = {r['id']: r['full_name'] for r in recruiters}
                recruiter_id = st.selectbox(
                    "Assign to Recruiter",
                    options=[None] + list(recruiter_options.keys()),
                    format_func=lambda x: "Unassigned" if x is None else recruiter_options[x]
                )

                salary_expectation = st.text_input("Salary Expectation", placeholder="$80,000 - $100,000")
                notice_period = st.selectbox("Notice Period", options=[""] + NOTICE_PERIODS)

            resume_url = st.text_input("Resume URL", placeholder="https://drive.google.com/...")
            notes = st.text_area("Notes", placeholder="Additional information about the candidate...")

            submitted = st.form_submit_button("➕ Add Candidate", use_container_width=True)

            if submitted:
                # Prepare candidate data
                candidate_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'linkedin_url': linkedin_url,
                    'current_role': current_role,
                    'current_company': current_company,
                    'years_of_experience': years_of_experience,
                    'skills': skills,
                    'education': education if education else None,
                    'status': status,
                    'position_applied': position_applied if position_applied else None,
                    'recruiter_id': recruiter_id,
                    'source': source if source else None,
                    'salary_expectation': salary_expectation,
                    'notice_period': notice_period if notice_period else None,
                    'resume_url': resume_url,
                    'notes': notes,
                    'created_by': current_user['id']
                }

                # Validate data
                is_valid, errors = validate_candidate_data(candidate_data)

                if not is_valid:
                    for error in errors:
                        st.error(error)
                else:
                    # Create candidate
                    candidate_id = candidate_model.create(candidate_data)

                    if candidate_id:
                        st.success(f"✅ Candidate added successfully! ID: {candidate_id}")
                        st.balloons()
                    else:
                        st.error("Failed to add candidate. Please try again.")

# TAB 3: Edit/Delete Candidate
with tab3:
    st.subheader("Edit or Delete Candidate")

    can_edit = auth.check_permission(user_role, 'edit')
    can_delete = auth.check_permission(user_role, 'delete')

    if not can_edit and not can_delete:
        st.warning("You don't have permission to edit or delete candidates.")
    else:
        # Get all candidates for selection
        candidates = candidate_model.get_all()

        if not candidates:
            st.info("No candidates available.")
        else:
            # Create a selection dropdown
            candidate_options = {
                c['id']: f"{c['first_name']} {c['last_name']} ({c['email']})"
                for c in candidates
            }

            selected_id = st.selectbox(
                "Select Candidate",
                options=list(candidate_options.keys()),
                format_func=lambda x: candidate_options[x]
            )

            if selected_id:
                candidate = candidate_model.get_by_id(selected_id)

                if candidate:
                    # Show current details
                    with st.expander("📄 Current Details", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Name:** {candidate['first_name']} {candidate['last_name']}")
                            st.write(f"**Email:** {candidate['email']}")
                            st.write(f"**Phone:** {candidate.get('phone', 'N/A')}")
                            st.write(f"**Status:** {candidate['status']}")
                        with col2:
                            st.write(f"**Current Role:** {candidate.get('current_role', 'N/A')}")
                            st.write(f"**Experience:** {candidate.get('years_of_experience', 'N/A')} years")
                            st.write(f"**Position Applied:** {candidate.get('position_applied', 'N/A')}")
                            st.write(f"**Recruiter:** {candidate.get('recruiter_name', 'Unassigned')}")

                    # Edit form
                    if can_edit:
                        st.markdown("### Edit Details")

                        with st.form("edit_candidate_form"):
                            col1, col2 = st.columns(2)

                            with col1:
                                first_name = st.text_input("First Name*", value=candidate['first_name'])
                                last_name = st.text_input("Last Name*", value=candidate['last_name'])
                                email = st.text_input("Email*", value=candidate['email'])
                                phone = st.text_input("Phone", value=candidate.get('phone', ''))
                                location = st.text_input("Location", value=candidate.get('location', ''))
                                linkedin_url = st.text_input("LinkedIn URL", value=candidate.get('linkedin_url', ''))

                            with col2:
                                current_role = st.text_input("Current Role", value=candidate.get('current_role', ''))
                                current_company = st.text_input("Current Company", value=candidate.get('current_company', ''))
                                years_of_experience = st.number_input(
                                    "Years of Experience",
                                    min_value=0,
                                    max_value=70,
                                    value=candidate.get('years_of_experience', 0)
                                )
                                skills = st.text_area("Skills", value=candidate.get('skills', ''))
                                status = st.selectbox(
                                    "Status*",
                                    options=CANDIDATE_STATUSES,
                                    index=CANDIDATE_STATUSES.index(candidate['status'])
                                )

                            notes = st.text_area("Notes", value=candidate.get('notes', ''))

                            update_submitted = st.form_submit_button("💾 Update Candidate", use_container_width=True)

                            if update_submitted:
                                updated_data = {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'email': email,
                                    'phone': phone,
                                    'location': location,
                                    'linkedin_url': linkedin_url,
                                    'current_role': current_role,
                                    'current_company': current_company,
                                    'years_of_experience': years_of_experience,
                                    'skills': skills,
                                    'education': candidate.get('education'),
                                    'status': status,
                                    'position_applied': candidate.get('position_applied'),
                                    'recruiter_id': candidate.get('recruiter_id'),
                                    'source': candidate.get('source'),
                                    'salary_expectation': candidate.get('salary_expectation'),
                                    'notice_period': candidate.get('notice_period'),
                                    'resume_url': candidate.get('resume_url'),
                                    'notes': notes
                                }

                                is_valid, errors = validate_candidate_data(updated_data)

                                if not is_valid:
                                    for error in errors:
                                        st.error(error)
                                else:
                                    if candidate_model.update(selected_id, updated_data):
                                        st.success("✅ Candidate updated successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update candidate.")

                    # Delete button
                    if can_delete:
                        st.markdown("---")
                        st.markdown("### Delete Candidate")
                        st.warning("⚠️ This action cannot be undone!")

                        if st.button("🗑️ Delete Candidate", type="secondary"):
                            if candidate_model.delete(selected_id):
                                st.success("Candidate deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete candidate.")
