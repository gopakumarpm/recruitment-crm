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
    tab1, tab2 = st.tabs(["👤 Profile", "👥 User Management"])
else:
    tab1 = st.tabs(["👤 Profile"])[0]
    tab2 = None

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
