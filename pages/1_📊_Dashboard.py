"""
Dashboard page with analytics and metrics.
"""
import streamlit as st
from auth.session_manager import session
from models.candidate import candidate_model
from models.call_history import call_history_model
from components.charts import (
    create_status_pie_chart,
    create_source_bar_chart,
    create_recruiter_performance_chart,
    create_pipeline_funnel
)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

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
st.title("📊 Dashboard")
st.markdown("---")

# Get statistics
stats = candidate_model.get_statistics()

# Key Metrics
st.subheader("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Candidates", stats.get('total', 0))

with col2:
    applied_count = stats.get('by_status', {}).get('Applied', 0)
    st.metric("Applied", applied_count)

with col3:
    interview_count = stats.get('by_status', {}).get('Interview', 0)
    st.metric("In Interview", interview_count)

with col4:
    hired_count = stats.get('by_status', {}).get('Hired', 0)
    st.metric("Hired", hired_count)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Status Distribution")
    if stats.get('by_status'):
        fig_status = create_status_pie_chart(stats['by_status'])
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("No data available")

with col2:
    st.subheader("Recruitment Pipeline")
    if stats.get('by_status'):
        fig_funnel = create_pipeline_funnel(stats['by_status'])
        st.plotly_chart(fig_funnel, use_container_width=True)
    else:
        st.info("No data available")

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Candidates by Source")
    if stats.get('by_source'):
        fig_source = create_source_bar_chart(stats['by_source'])
        st.plotly_chart(fig_source, use_container_width=True)
    else:
        st.info("No data available")

with col4:
    st.subheader("Candidates by Recruiter")
    if stats.get('by_recruiter'):
        fig_recruiter = create_recruiter_performance_chart(stats['by_recruiter'])
        st.plotly_chart(fig_recruiter, use_container_width=True)
    else:
        st.info("No data available")

# Recent Activity
st.markdown("---")
st.subheader("📞 Recent Interactions")

recent_calls = call_history_model.get_all(limit=10)

if recent_calls:
    import pandas as pd
    df = pd.DataFrame(recent_calls)
    display_cols = ['call_date', 'candidate_name', 'call_type', 'outcome', 'recruiter_name']
    display_cols = [col for col in display_cols if col in df.columns]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
else:
    st.info("No recent interactions found.")

# Upcoming Follow-ups
st.markdown("---")
st.subheader("📅 Upcoming Follow-ups")

followups = call_history_model.get_upcoming_followups()

if followups:
    import pandas as pd
    df = pd.DataFrame(followups)
    display_cols = ['next_action_date', 'candidate_name', 'next_action', 'recruiter_name']
    display_cols = [col for col in display_cols if col in df.columns]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
else:
    st.info("No upcoming follow-ups scheduled.")
