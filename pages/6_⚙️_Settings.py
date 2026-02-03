"""
Settings page for user profile and administration.
"""
import streamlit as st
import pandas as pd
from auth.session_manager import session
from auth.authenticator import auth
from models.user import user_model
from utils.constants import ROLES

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

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
st.title("⚙️ Settings")
st.markdown("---")

# Tabs based on role
if user_role == 'admin':
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "👥 User Management", "🔄 Reassign Candidates"])
else:
    tab1 = st.tabs(["👤 Profile"])[0]
    tab2 = None
    tab3 = None

# TAB 1: User Profile
with tab1:
    st.subheader("Your Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Username:** {current_user['username']}")
        st.markdown(f"**Email:** {current_user['email']}")
        st.markdown(f"**Role:** {current_user['role'].capitalize()}")

    st.markdown("---")

    # Update Profile
    st.subheader("Update Profile")

    with st.form("update_profile_form"):
        new_full_name = st.text_input("Full Name", value=current_user['full_name'])
        new_email = st.text_input("Email", value=current_user['email'])

        update_submitted = st.form_submit_button("💾 Update Profile", use_container_width=True)

        if update_submitted:
            if user_model.update_profile(current_user['id'], new_full_name, new_email):
                st.success("✅ Profile updated successfully!")
                # Update session
                current_user['full_name'] = new_full_name
                current_user['email'] = new_email
                session.set_current_user(current_user)
                st.rerun()
            else:
                st.error("Failed to update profile.")

    st.markdown("---")

    # Change Password
    st.subheader("Change Password")

    with st.form("change_password_form"):
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        password_submitted = st.form_submit_button("🔒 Change Password", use_container_width=True)

        if password_submitted:
            if not old_password or not new_password or not confirm_password:
                st.error("All fields are required.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                if auth.change_password(current_user['id'], old_password, new_password):
                    st.success("✅ Password changed successfully!")
                else:
                    st.error("Failed to change password. Check your current password.")

# TAB 2: User Management (Admin only)
if tab2 is not None:
    with tab2:
        st.subheader("User Management")

        # Get all users
        users = user_model.get_all(include_inactive=True)

        if users:
            df = pd.DataFrame(users)

            display_columns = ['id', 'username', 'full_name', 'email', 'role', 'is_active', 'created_at']
            display_columns = [col for col in display_columns if col in df.columns]
            df_display = df[display_columns]

            df_display = df_display.rename(columns={
                'id': 'ID',
                'username': 'Username',
                'full_name': 'Full Name',
                'email': 'Email',
                'role': 'Role',
                'is_active': 'Active',
                'created_at': 'Created'
            })

            st.dataframe(df_display, use_container_width=True, hide_index=True)

        else:
            st.info("No users found.")

        st.markdown("---")

        # Add New User
        st.subheader("Add New User")

        with st.form("add_user_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_username = st.text_input("Username*", placeholder="johndoe")
                new_user_email = st.text_input("Email*", placeholder="john@example.com")
                new_user_password = st.text_input("Password*", type="password", placeholder="Min 8 characters")

            with col2:
                new_user_full_name = st.text_input("Full Name*", placeholder="John Doe")
                new_user_role = st.selectbox("Role*", options=ROLES)

            add_user_submitted = st.form_submit_button("➕ Add User", use_container_width=True)

            if add_user_submitted:
                if not all([new_username, new_user_email, new_user_password, new_user_full_name]):
                    st.error("All fields are required.")
                elif len(new_user_password) < 8:
                    st.error("Password must be at least 8 characters long.")
                else:
                    if auth.create_user(
                        new_username,
                        new_user_email,
                        new_user_password,
                        new_user_full_name,
                        new_user_role
                    ):
                        st.success(f"✅ User '{new_username}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create user. Username or email may already exist.")

        st.markdown("---")

        # Manage Existing Users
        st.subheader("Manage Existing Users")

        if users:
            user_options = {u['id']: f"{u['full_name']} ({u['username']})" for u in users}

            selected_user_id = st.selectbox(
                "Select User",
                options=list(user_options.keys()),
                format_func=lambda x: user_options[x]
            )

            if selected_user_id:
                selected_user = user_model.get_by_id(selected_user_id)

                if selected_user:
                    col1, col2 = st.columns(2)

                    with col1:
                        new_role = st.selectbox(
                            "Change Role",
                            options=ROLES,
                            index=ROLES.index(selected_user['role'])
                        )

                        if st.button("💾 Update Role"):
                            if user_model.update_role(selected_user_id, new_role):
                                st.success(f"✅ Role updated to {new_role}!")
                                st.rerun()
                            else:
                                st.error("Failed to update role.")

                    with col2:
                        status_text = "Active" if selected_user['is_active'] else "Inactive"
                        if st.button(f"🔄 Toggle Status (Currently: {status_text})"):
                            if user_model.toggle_active_status(selected_user_id):
                                st.success("✅ User status updated!")
                                st.rerun()
                            else:
                                st.error("Failed to update status.")

                    # Delete User Section
                    st.markdown("---")
                    st.markdown("### 🗑️ Delete User")
                    st.warning(f"⚠️ Are you sure you want to delete **{selected_user['full_name']}**? This action cannot be undone!")

                    # Check if user has assigned candidates
                    from models.candidate import candidate_model
                    assigned_candidates = candidate_model.search({'recruiter_id': selected_user_id})

                    if assigned_candidates:
                        st.info(f"📋 This user has {len(assigned_candidates)} candidate(s) assigned. Deleting will unassign these candidates.")

                    if st.button("🗑️ Delete User", type="secondary", key="delete_user_btn"):
                        if selected_user_id == current_user['id']:
                            st.error("❌ You cannot delete your own account!")
                        else:
                            if user_model.delete(selected_user_id):
                                st.success(f"✅ User '{selected_user['full_name']}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete user.")

# TAB 3: Reassign Candidates (Admin only)
if tab3 is not None:
    with tab3:
        st.subheader("🔄 Reassign Candidates Between Recruiters")

        from models.candidate import candidate_model

        # Get all recruiters
        recruiters = user_model.get_recruiters()

        if len(recruiters) < 2:
            st.warning("⚠️ You need at least 2 recruiters to reassign candidates.")
        else:
            # Create two columns for from/to selection
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📤 From Recruiter")
                recruiter_options = {r['id']: r['full_name'] for r in recruiters}
                recruiter_options[None] = "Unassigned Candidates"

                from_recruiter_id = st.selectbox(
                    "Select Source Recruiter",
                    options=list(recruiter_options.keys()),
                    format_func=lambda x: recruiter_options[x],
                    key="from_recruiter"
                )

            with col2:
                st.markdown("### 📥 To Recruiter")
                to_recruiter_options = {r['id']: r['full_name'] for r in recruiters if r['id'] != from_recruiter_id}

                if to_recruiter_options:
                    to_recruiter_id = st.selectbox(
                        "Select Target Recruiter",
                        options=list(to_recruiter_options.keys()),
                        format_func=lambda x: to_recruiter_options[x],
                        key="to_recruiter"
                    )
                else:
                    st.info("Select a different source recruiter")
                    to_recruiter_id = None

            st.markdown("---")

            # Show candidates assigned to selected recruiter
            if from_recruiter_id is not None or from_recruiter_id is None:
                st.subheader("📋 Candidates to Reassign")

                # Get candidates for selected recruiter
                if from_recruiter_id is None:
                    candidates = candidate_model.search({'recruiter_id': None})
                    candidates = [c for c in candidate_model.get_all() if c.get('recruiter_id') is None]
                else:
                    candidates = candidate_model.search({'recruiter_id': from_recruiter_id})

                if not candidates:
                    st.info(f"No candidates assigned to {recruiter_options[from_recruiter_id]}")
                else:
                    st.info(f"Found {len(candidates)} candidate(s)")

                    # Display candidates
                    df = pd.DataFrame(candidates)
                    display_cols = ['id', 'first_name', 'last_name', 'email', 'status', 'position_applied']
                    display_cols = [col for col in display_cols if col in df.columns]

                    if display_cols:
                        st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

                    # Reassignment options
                    st.markdown("---")
                    st.subheader("🔄 Reassignment Options")

                    col_a, col_b = st.columns(2)

                    with col_a:
                        # Bulk reassign all
                        if st.button(f"🔄 Reassign All {len(candidates)} Candidates", use_container_width=True, type="primary"):
                            if to_recruiter_id is None:
                                st.error("Please select a target recruiter")
                            else:
                                success_count = 0
                                for candidate in candidates:
                                    candidate_data = dict(candidate)
                                    candidate_data['recruiter_id'] = to_recruiter_id
                                    if candidate_model.update(candidate['id'], candidate_data):
                                        success_count += 1

                                if success_count == len(candidates):
                                    st.success(f"✅ Successfully reassigned {success_count} candidate(s) to {to_recruiter_options.get(to_recruiter_id)}!")
                                    st.rerun()
                                else:
                                    st.warning(f"⚠️ Reassigned {success_count} out of {len(candidates)} candidates")

                    with col_b:
                        # Individual reassignment
                        if candidates:
                            candidate_options = {c['id']: f"{c['first_name']} {c['last_name']}" for c in candidates}

                            selected_candidate_id = st.selectbox(
                                "Or select individual candidate",
                                options=list(candidate_options.keys()),
                                format_func=lambda x: candidate_options[x]
                            )

                            if st.button("🔄 Reassign Selected Candidate", use_container_width=True):
                                if to_recruiter_id is None:
                                    st.error("Please select a target recruiter")
                                else:
                                    selected_candidate = next((c for c in candidates if c['id'] == selected_candidate_id), None)
                                    if selected_candidate:
                                        candidate_data = dict(selected_candidate)
                                        candidate_data['recruiter_id'] = to_recruiter_id
                                        if candidate_model.update(selected_candidate_id, candidate_data):
                                            st.success(f"✅ Reassigned {candidate_options[selected_candidate_id]} to {to_recruiter_options.get(to_recruiter_id)}!")
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to reassign candidate")

            # Quick Stats
            st.markdown("---")
            st.subheader("📊 Candidate Distribution by Recruiter")

            recruiter_stats = []
            for recruiter in recruiters:
                count = len(candidate_model.search({'recruiter_id': recruiter['id']}))
                recruiter_stats.append({
                    'Recruiter': recruiter['full_name'],
                    'Candidates': count
                })

            # Add unassigned count
            all_candidates = candidate_model.get_all()
            unassigned_count = len([c for c in all_candidates if c.get('recruiter_id') is None])
            recruiter_stats.append({
                'Recruiter': 'Unassigned',
                'Candidates': unassigned_count
            })

            if recruiter_stats:
                df_stats = pd.DataFrame(recruiter_stats)
                st.dataframe(df_stats, use_container_width=True, hide_index=True)
