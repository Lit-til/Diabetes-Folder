"""
Risk Assessment Page
--------------------
This page collects user input (basic health data) required by the model,
computes the diabetes risk using the trained model, maps the probability
into Low / Medium / High categories, and then navigates to the Results page.
"""

import streamlit as st
from state import ensure_state, CURRENT_FORM_KEY, CURRENT_RESULT_KEY
from utils import calc_bmi, model_predict_prob, label_from_prob
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Risk Assessment", page_icon="🔎", layout="centered")
ensure_state()

# Page header (mirrors the design: "Step 1 of 10")
st.caption("Step 1 of 10 • Basic Information")
st.title("Risk Assessment")

# --- Collect basic user inputs for model prediction ---
form = st.session_state[CURRENT_FORM_KEY]

with st.form("assessment_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        form["age"] = st.number_input("Age (years)", min_value=1, max_value=120, value=form.get("age") or 30)
        form["weight"] = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=form.get("weight") or 70.0, step=0.1)
    with col2:
        form["height"] = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=form.get("height") or 170.0, step=0.1)

    # Auto-calculate BMI once weight & height are entered
    if form.get("weight") and form.get("height"):
        form["bmi"] = calc_bmi(form["weight"], form["height"])
        st.write(f"**Calculated BMI:** {form['bmi']}")

    # Add other questionnaire inputs if required by your model
    # Example:
    # form["family_history"] = st.radio("Do you have a family history of diabetes?", ["Yes", "No"])

    # Submit button: triggers model computation
    submitted = st.form_submit_button("Compute Risk", type="primary")

# --- When the user submits ---
if submitted:
    # Validate inputs
    if not all([form.get("age"), form.get("weight"), form.get("height"), form.get("bmi")]):
        st.error("Please complete all fields before continuing.")
        st.stop()

    # Run model prediction (returns probability between 0–1)
    prob = model_predict_prob(form)

    # Map probability to risk category
    label = label_from_prob(prob)

    # Save result into session state
    st.session_state[CURRENT_RESULT_KEY] = {
        "prob": prob,
        "label": label,
        "created_at": datetime.utcnow().isoformat(),
        "inputs": form.copy(),
    }

    # Navigate to results page
    st.success("Risk computed successfully! Redirecting to results...")
    st.switch_page("pages/2_📊_Results.py")
