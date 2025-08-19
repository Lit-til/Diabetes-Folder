"""
Learn page: a lightweight info hub the design references via footer/tab.
Add links, FAQs, or educational content as desired.
"""

import streamlit as st
from state import ensure_state

st.set_page_config(page_title="Learn", page_icon="📚", layout="centered")
ensure_state()

st.title("Learn")
st.write(
    "Explore resources on diabetes risk, prevention, and healthy living. "
    "You can add curated articles, FAQs, and local screening information here."
)

st.markdown(
    """
- What is type 2 diabetes?
- Common risk factors and what they mean
- Screening and when to see a clinician
- Building sustainable habits (diet, movement, sleep, stress)
"""
)

st.divider()
st.page_link("Home.py", label="← Back to Home")
