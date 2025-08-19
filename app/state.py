"""
Centralised session-state keys and helpers.
Keeps all page files consistent and avoids key typos.
"""

import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

ASSESSMENTS_KEY = "assessments"     # list of dicts, each a completed assessment
CURRENT_FORM_KEY = "current_form"   # dict of in-progress inputs
CURRENT_RESULT_KEY = "current_result"  # dict with 'prob' (0-1), 'label', 'created_at'

def ensure_state() -> None:
    """Initialise session state containers once per session."""
    if ASSESSMENTS_KEY not in st.session_state:
        st.session_state[ASSESSMENTS_KEY]: List[Dict[str, Any]] = []
    if CURRENT_FORM_KEY not in st.session_state:
        st.session_state[CURRENT_FORM_KEY] = {
            "age": None, "weight": None, "height": None, "bmi": None,
            # Add additional questionnaire fields here if needed.
        }
    if CURRENT_RESULT_KEY not in st.session_state:
        st.session_state[CURRENT_RESULT_KEY] = None

def save_assessment(result: Dict[str, Any]) -> None:
    """Append a completed assessment (inputs + result) into history."""
    ensure_state()
    data = {
        "created_at": result.get("created_at", datetime.utcnow().isoformat()),
        "age": st.session_state[CURRENT_FORM_KEY].get("age"),
        "weight": st.session_state[CURRENT_FORM_KEY].get("weight"),
        "height": st.session_state[CURRENT_FORM_KEY].get("height"),
        "bmi": st.session_state[CURRENT_FORM_KEY].get("bmi"),
        "risk_prob": result.get("prob"),
        "risk_label": result.get("label"),
    }
    st.session_state[ASSESSMENTS_KEY].append(data)

def clear_current() -> None:
    """Clear only the in-progress form and result."""
    st.session_state[CURRENT_FORM_KEY] = {
        "age": None, "weight": None, "height": None, "bmi": None,
    }
    st.session_state[CURRENT_RESULT_KEY] = None
