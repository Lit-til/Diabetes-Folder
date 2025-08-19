"""
Results page: displays 'Your Diabetes Risk' with Low/Medium/High states and
mirrors the explanatory copy, including the 'Learn More' affordance.  :contentReference[oaicite:4]{index=4}
"""

import streamlit as st
from state import ensure_state, CURRENT_RESULT_KEY, save_assessment
from utils import low_risk_copy, medium_risk_copy, high_risk_copy

st.set_page_config(page_title="Results", page_icon="📊", layout="centered")
ensure_state()

res = st.session_state[CURRENT_RESULT_KEY]
if not res:
    st.warning("No recent assessment found. Please complete the assessment first.")
    st.page_link("pages/1_🔎_Risk_Assessment.py", label="Start Assessment")
    st.stop()

p = res["prob"]
label = res["label"]
percent = round(p * 100)

st.title("Your Diabetes Risk")
st.metric(label="Risk Level", value=f"{label} ({percent}%)")

# Explanatory paragraph mirrors the design text blocks
if label == "Low":
    st.info(low_risk_copy())
elif label == "Medium":
    st.warning(medium_risk_copy())
else:
    st.error(high_risk_copy())

st.caption("Disclaimer: This is not a diagnosis. For personalised advice, consult a healthcare professional.")  # :contentReference[oaicite:5]{index=5}

save_assessment(res)

cols = st.columns(3)
with cols[0]:
    st.page_link("pages/3_📝_Recommendations.py", label="See Recommendations →")
with cols[1]:
    st.page_link("pages/4_📚_Learn.py", label="Learn More")
with cols[2]:
    st.page_link("pages/5_👤_Profile.py", label="View Profile")

st.divider()
st.page_link("Home.py", label="← Back to Home")
