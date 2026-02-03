"""
Chart components for data visualization.
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List


def create_status_pie_chart(status_data: Dict[str, int]) -> go.Figure:
    """Create a pie chart showing candidate distribution by status."""
    if not status_data:
        return go.Figure()

    fig = px.pie(
        names=list(status_data.keys()),
        values=list(status_data.values()),
        title="Candidates by Status"
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_source_bar_chart(source_data: Dict[str, int]) -> go.Figure:
    """Create a bar chart showing candidate distribution by source."""
    if not source_data:
        return go.Figure()

    fig = px.bar(
        x=list(source_data.keys()),
        y=list(source_data.values()),
        title="Candidates by Source",
        labels={'x': 'Source', 'y': 'Count'}
    )

    return fig


def create_recruiter_performance_chart(recruiter_data: Dict[str, int]) -> go.Figure:
    """Create a bar chart showing recruiter performance."""
    if not recruiter_data:
        return go.Figure()

    fig = px.bar(
        x=list(recruiter_data.keys()),
        y=list(recruiter_data.values()),
        title="Candidates by Recruiter",
        labels={'x': 'Recruiter', 'y': 'Candidates'}
    )

    return fig


def create_pipeline_funnel(status_data: Dict[str, int]) -> go.Figure:
    """Create a funnel chart showing recruitment pipeline."""
    if not status_data:
        return go.Figure()

    # Order statuses for funnel
    funnel_order = ['Applied', 'Screening', 'Interview', 'Offer', 'Hired']
    values = [status_data.get(status, 0) for status in funnel_order]

    fig = go.Figure(go.Funnel(
        y=funnel_order,
        x=values,
        textinfo="value+percent initial"
    ))

    fig.update_layout(title="Recruitment Pipeline")
    return fig
