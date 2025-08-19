"""
Profile page: shows 'Past Assessments' and a 'Risk Level Over Time' chart,
mirroring the table + trend visual in your mockups.  :contentReference[oaicite:7]{index=7}
"""

import streamlit as st
from state import ensure_state, ASSESSMENTS_KEY
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="Profile", page_icon="👤", layout="centered")
ensure_state()

st.title("My Health")

assessments = st.session_state[ASSESSMENTS_KEY]
if not assessments:
    st.info("No past assessments yet. Complete an assessment to see history.")
    st.page_link("pages/1_🔎_Risk_Assessment.py", label="Start Assessment")
    st.stop()

df = pd.DataFrame(assessments)
df["created_at"] = pd.to_datetime(df["created_at"])

st.subheader("Past Assessments")
st.dataframe(
    df[["created_at", "risk_label", "risk_prob", "age", "weight", "height", "bmi"]]
      .sort_values("created_at", ascending=False),
    use_container_width=True
)

st.subheader("Risk Level Over Time")
fig, ax = plt.subplots()  # NOTE: one chart per plot, no seaborn, no style set (per restrictions)
df_sort = df.sort_values("created_at")
ax.plot(df_sort["created_at"], df_sort["risk_prob"])
ax.set_xlabel("Date")
ax.set_ylabel("Risk Probability")
ax.set_title("Risk Trend (0–1)")
st.pyplot(fig)

# Simple export
csv = df.to_csv(index=False)
st.download_button("Download Assessment History (CSV)", data=csv, file_name="assessments.csv", mime="text/csv")

st.divider()
row = st.columns(3)
with row[0]:
    st.page_link("Home.py", label="🏠 Home")
with row[1]:
    st.page_link("pages/1_🔎_Risk_Assessment.py", label="🔎 New Assessment")
with row[2]:
    st.page_link("pages/3_📝_Recommendations.py", label="📝 Recommendations")
