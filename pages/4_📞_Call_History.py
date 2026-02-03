"""
Call History page for tracking candidate interactions.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from auth.session_manager import session
from models.call_history import call_history_model
from models.candidate import candidate_model
from utils.constants import CALL_TYPES, CALL_OUTCOMES

st.set_page_config(page_title="Call History", page_icon="📞", layout="wide")

# Check authentication
if not session.is_authenticated():
    st.warning("Please login to access this page.")
    st.stop()

current_user = session.get_current_user()

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {current_user['full_name']}")
    st.markdown(f"**Role:** {current_user['role'].capitalize()}")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        session.clear_session()
        st.rerun()

# Main content
st.title("📞 Call History")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 All Calls", "➕ Log New Call", "📅 Follow-ups"])

# TAB 1: All Calls
with tab1:
    st.subheader("All Interactions")

    calls = call_history_model.get_all()

    if calls:
        df = pd.DataFrame(calls)

        display_columns = [
            'call_date', 'candidate_name', 'call_type', 'duration',
            'outcome', 'recruiter_name', 'next_action', 'next_action_date'
        ]

        display_columns = [col for col in display_columns if col in df.columns]
        df_display = df[display_columns]

        df_display = df_display.rename(columns={
            'call_date': 'Date',
            'candidate_name': 'Candidate',
            'call_type': 'Type',
            'duration': 'Duration (min)',
            'outcome': 'Outcome',
            'recruiter_name': 'Recruiter',
            'next_action': 'Next Action',
            'next_action_date': 'Follow-up Date'
        })

        st.dataframe(df_display, use_container_width=True, hide_index=True)

    else:
        st.info("No call history found. Log your first interaction!")

# TAB 2: Log New Call
with tab2:
    st.subheader("Log New Interaction")

    # Get all candidates for selection
    candidates = candidate_model.get_all()

    if not candidates:
        st.warning("No candidates available. Please add candidates first.")
    else:
        with st.form("log_call_form"):
            # Candidate selection
            candidate_options = {
                c['id']: f"{c['first_name']} {c['last_name']} ({c['email']})"
                for c in candidates
            }

            selected_candidate_id = st.selectbox(
                "Select Candidate*",
                options=list(candidate_options.keys()),
                format_func=lambda x: candidate_options[x]
            )

            col1, col2 = st.columns(2)

            with col1:
                call_type = st.selectbox("Call Type*", options=CALL_TYPES)
                call_date = st.date_input("Call Date*", value=date.today())
                call_time = st.time_input("Call Time", value=datetime.now().time())
                duration = st.number_input("Duration (minutes)", min_value=0, value=30)

            with col2:
                outcome = st.selectbox("Outcome", options=[""] + CALL_OUTCOMES)
                next_action = st.text_input("Next Action", placeholder="e.g., Schedule technical interview")
                next_action_date = st.date_input("Follow-up Date", value=None)

            notes = st.text_area("Notes", placeholder="Call details, discussion points, etc.")

            submitted = st.form_submit_button("📞 Log Call", use_container_width=True)

            if submitted:
                # Combine date and time
                call_datetime = datetime.combine(call_date, call_time)

                call_data = {
                    'candidate_id': selected_candidate_id,
                    'recruiter_id': current_user['id'],
                    'call_date': call_datetime.isoformat(),
                    'call_type': call_type,
                    'duration': duration,
                    'outcome': outcome if outcome else None,
                    'notes': notes,
                    'next_action': next_action if next_action else None,
                    'next_action_date': next_action_date.isoformat() if next_action_date else None
                }

                call_id = call_history_model.create(call_data)

                if call_id:
                    st.success("✅ Call logged successfully!")
                    st.balloons()
                else:
                    st.error("Failed to log call. Please try again.")

# TAB 3: Follow-ups
with tab3:
    st.subheader("Upcoming Follow-ups")

    followups = call_history_model.get_upcoming_followups()

    if followups:
        df = pd.DataFrame(followups)

        display_columns = [
            'next_action_date', 'candidate_name', 'candidate_email',
            'next_action', 'recruiter_name', 'call_date'
        ]

        display_columns = [col for col in display_columns if col in df.columns]
        df_display = df[display_columns]

        df_display = df_display.rename(columns={
            'next_action_date': 'Follow-up Date',
            'candidate_name': 'Candidate',
            'candidate_email': 'Email',
            'next_action': 'Action Required',
            'recruiter_name': 'Assigned To',
            'call_date': 'Last Contact'
        })

        st.dataframe(df_display, use_container_width=True, hide_index=True)

    else:
        st.info("No upcoming follow-ups scheduled.")
