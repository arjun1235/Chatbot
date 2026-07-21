import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("ROOT:", ROOT)
print("sys.path:", sys.path)

from database.database import Database

db = Database()

st.set_page_config(
    page_title="ArcTech Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ArcTech Helpdesk Dashboard")

stats = db.get_statistics()

col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", stats["total"])
col2.metric("Open Tickets", stats["open"])
col3.metric(
    "Average Confidence",
    f"{stats['avg_confidence']:.2f}"
)

st.divider()

tickets = db.get_all_tickets()

if tickets:

    df = pd.DataFrame(
        tickets,
        columns=[
            "ID",
            "Issue",
            "Priority",
            "Status",
            "Confidence",
            "Created"
        ]
    )

    st.subheader("All Tickets")

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("No tickets yet.")

st.divider()

issues = db.get_issue_counts()

if issues:

    issue_df = pd.DataFrame(
        issues,
        columns=[
            "Issue",
            "Count"
        ]
    )

    fig = px.bar(
        issue_df,
        x="Issue",
        y="Count",
        title="Most Common Issues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )