"""
Recommendations page: presents Lifestyle and Dietary guidance cards
using the exact themes shown in your design (exercise, sleep, stress;
whole grains, fruit/veg, lean protein, limits).  :contentReference[oaicite:6]{index=6}
"""

import streamlit as st
from state import ensure_state
from utils import lifestyle_recommendations, dietary_recommendations

st.set_page_config(page_title="Recommendations", page_icon="📝", layout="centered")
ensure_state()

st.title("Your Health Recommendations")

st.header("Lifestyle")
st.markdown(lifestyle_recommendations())

st.header("Dietary")
st.markdown(dietary_recommendations())

st.divider()
row = st.columns(3)
with row[0]:
    st.page_link("Home.py", label="🏠 Home")
with row[1]:
    st.page_link("pages/4_📚_Learn.py", label="📚 Learn")
with row[2]:
    st.page_link("pages/5_👤_Profile.py", label="👤 Profile")
