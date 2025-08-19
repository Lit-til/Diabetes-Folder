"""
Home page: mirrors the welcome hero and primary action ('Start Assessment').
Navigation reflects: Home · Learn · Profile, as shown in the design.  :contentReference[oaicite:2]{index=2}
"""

import streamlit as st
from state import ensure_state
from utils import welcome_copy

st.set_page_config(page_title="Diabetes Risk Predictor", page_icon="🩺", layout="centered")
ensure_state()

# --- Header / Hero ---
st.title("Diabetes Risk Predictor")
st.subheader("Welcome to Your Health Journey")
st.write(welcome_copy(''))

# --- Primary CTA ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Start Assessment", type="primary"):
        st.switch_page("pages/risk.py")

st.divider()

# --- Footer-like quick nav (mirroring footer tabs in mockup) ---
cols = st.columns(3)
with cols[0]:
    st.page_link("Home.py", label="Home", icon="🏠")
with cols[1]:
    st.page_link("pages/Learn.py", label=" Learn", icon ="📚")
with cols[2]:
    st.page_link("pages/Profile.py", label="Profile",  icon="👤")
