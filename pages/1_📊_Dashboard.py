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

# Recruiter Leaderboard
st.markdown("---")
st.markdown("<h2 style='margin-bottom: 30px;'>🏆 Recruiter Leaderboard</h2>", unsafe_allow_html=True)

from models.user import user_model
recruiters = user_model.get_recruiters()

if recruiters:
    leaderboard_data = []

    for recruiter in recruiters:
        # Get all candidates for this recruiter
        recruiter_candidates = candidate_model.search({'recruiter_id': recruiter['id']})

        total_candidates = len(recruiter_candidates)

        # Count by status
        hired_count = len([c for c in recruiter_candidates if c.get('status') == 'Hired'])
        interview_count = len([c for c in recruiter_candidates if c.get('status') == 'Interview'])
        offer_count = len([c for c in recruiter_candidates if c.get('status') == 'Offer'])
        rejected_count = len([c for c in recruiter_candidates if c.get('status') == 'Rejected'])

        # Calculate success rate
        success_rate = (hired_count / total_candidates * 100) if total_candidates > 0 else 0

        # Calculate conversion rate (Interview or beyond / Total)
        conversion_count = interview_count + offer_count + hired_count
        conversion_rate = (conversion_count / total_candidates * 100) if total_candidates > 0 else 0

        leaderboard_data.append({
            'recruiter': recruiter['full_name'],
            'total': total_candidates,
            'hired': hired_count,
            'interview': interview_count,
            'offer': offer_count,
            'rejected': rejected_count,
            'success_rate': success_rate,
            'conversion_rate': conversion_rate
        })

    # Sort by success rate, then by total candidates
    leaderboard_data.sort(key=lambda x: (x['success_rate'], x['total']), reverse=True)

    # Display leaderboard cards
    for idx, data in enumerate(leaderboard_data, 1):
        # Medal emoji for top 3
        if idx == 1:
            medal = "🥇"
            border_color = "#FFD700"  # Gold
        elif idx == 2:
            medal = "🥈"
            border_color = "#C0C0C0"  # Silver
        elif idx == 3:
            medal = "🥉"
            border_color = "#CD7F32"  # Bronze
        else:
            medal = f"#{idx}"
            border_color = "#e5e7eb"

        st.markdown(f"""
        <div style='background: rgba(240, 249, 255, 0.75); padding: 20px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 6px solid {border_color}; backdrop-filter: blur(10px);'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <span style='font-size: 36px;'>{medal}</span>
                    <div>
                        <h3 style='margin: 0; color: #1f2937;'>{data['recruiter']}</h3>
                        <p style='margin: 5px 0 0 0; color: #6b7280; font-size: 14px;'>Total Candidates: {data['total']}</p>
                    </div>
                </div>
                <div style='text-align: right;'>
                    <div style='display: flex; gap: 20px;'>
                        <div>
                            <p style='margin: 0; color: #6b7280; font-size: 12px;'>Success Rate</p>
                            <p style='margin: 5px 0 0 0; color: #10b981; font-size: 24px; font-weight: 700;'>{data['success_rate']:.1f}%</p>
                        </div>
                        <div>
                            <p style='margin: 0; color: #6b7280; font-size: 12px;'>Conversion Rate</p>
                            <p style='margin: 5px 0 0 0; color: #6366f1; font-size: 24px; font-weight: 700;'>{data['conversion_rate']:.1f}%</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid #e5e7eb;'>
                <div style='display: flex; gap: 20px; justify-content: space-around;'>
                    <div style='text-align: center;'>
                        <p style='margin: 0; color: #6b7280; font-size: 12px;'>✅ Hired</p>
                        <p style='margin: 5px 0 0 0; color: #10b981; font-size: 20px; font-weight: 600;'>{data['hired']}</p>
                    </div>
                    <div style='text-align: center;'>
                        <p style='margin: 0; color: #6b7280; font-size: 12px;'>📋 Offer</p>
                        <p style='margin: 5px 0 0 0; color: #8b5cf6; font-size: 20px; font-weight: 600;'>{data['offer']}</p>
                    </div>
                    <div style='text-align: center;'>
                        <p style='margin: 0; color: #6b7280; font-size: 12px;'>💼 Interview</p>
                        <p style='margin: 5px 0 0 0; color: #f59e0b; font-size: 20px; font-weight: 600;'>{data['interview']}</p>
                    </div>
                    <div style='text-align: center;'>
                        <p style='margin: 0; color: #6b7280; font-size: 12px;'>❌ Rejected</p>
                        <p style='margin: 5px 0 0 0; color: #ef4444; font-size: 20px; font-weight: 600;'>{data['rejected']}</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Summary statistics
    st.markdown("---")
    st.markdown("### 📊 Leaderboard Summary")

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    total_all_candidates = sum(d['total'] for d in leaderboard_data)
    total_hired = sum(d['hired'] for d in leaderboard_data)
    avg_success_rate = sum(d['success_rate'] for d in leaderboard_data) / len(leaderboard_data) if leaderboard_data else 0
    top_recruiter = leaderboard_data[0]['recruiter'] if leaderboard_data else "N/A"

    with summary_col1:
        st.metric("Total Active Recruiters", len(leaderboard_data))

    with summary_col2:
        st.metric("Total Candidates Managed", total_all_candidates)

    with summary_col3:
        st.metric("Total Hires", total_hired)

    with summary_col4:
        st.metric("Average Success Rate", f"{avg_success_rate:.1f}%")

else:
    st.info("No recruiters found. Add recruiters in the Settings page.")

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
