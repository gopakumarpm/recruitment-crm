"""
Search page with advanced filtering.
"""
import streamlit as st
import pandas as pd
from auth.session_manager import session
from models.candidate import candidate_model
from utils.constants import CANDIDATE_STATUSES, CANDIDATE_SOURCES

st.set_page_config(page_title="Search", page_icon="🔍", layout="wide")

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
st.title("🔍 Advanced Search")
st.markdown("---")

# Filters
st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    search_text = st.text_input("🔎 Search Name/Email/Skills", placeholder="Type to search...")
    status_filter = st.multiselect("Status", options=CANDIDATE_STATUSES)

with col2:
    source_filter = st.selectbox("Source", options=["All"] + CANDIDATE_SOURCES)
    min_exp = st.number_input("Min Experience (years)", min_value=0, value=0)

with col3:
    location_filter = st.text_input("Location", placeholder="City, State")
    max_exp = st.number_input("Max Experience (years)", min_value=0, value=50)

# Search button
if st.button("🔍 Search", use_container_width=True, type="primary"):
    # Build filters
    filters = {}

    if search_text:
        filters['search_text'] = search_text

    if status_filter:
        filters['status'] = status_filter

    if source_filter and source_filter != "All":
        filters['source'] = source_filter

    if min_exp > 0:
        filters['min_experience'] = min_exp

    if max_exp < 50:
        filters['max_experience'] = max_exp

    if location_filter:
        filters['location'] = location_filter

    # Search
    results = candidate_model.search(filters) if filters else candidate_model.get_all()

    st.markdown("---")
    st.subheader(f"Search Results ({len(results)} found)")

    if results:
        df = pd.DataFrame(results)

        display_columns = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'current_role', 'years_of_experience', 'status', 'location'
        ]

        display_columns = [col for col in display_columns if col in df.columns]
        df_display = df[display_columns]

        df_display = df_display.rename(columns={
            'id': 'ID',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'current_role': 'Role',
            'years_of_experience': 'Experience',
            'status': 'Status',
            'location': 'Location'
        })

        st.dataframe(df_display, use_container_width=True, hide_index=True)

    else:
        st.info("No candidates found matching your criteria.")
else:
    st.info("Use the filters above to search for candidates.")
