"""
Utility functions:
- BMI calculation
- Model loading (optional)
- Risk inference (model-backed or rule-based fallback)
- Text blocks for Results & Recommendations (Low/Medium/High)
The labels and copy mirror the design screens.  :contentReference[oaicite:1]{index=1}
"""

from typing import Optional, Tuple, Dict
import math
import pickle
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model" / "model.pkl"

def calc_bmi(weight_kg: Optional[float], height_cm: Optional[float]) -> Optional[float]:
    if not weight_kg or not height_cm or height_cm <= 0:
        return None
    h_m = height_cm / 100.0
    return round(weight_kg / (h_m * h_m), 1)

def load_model():
    try:
        if MODEL_PATH.exists():
            with open(MODEL_PATH, "rb") as f:
                return pickle.load(f)
    except Exception:
        pass
    return None

_model = load_model()

def model_predict_prob(features: Dict) -> float:
    """
    Return probability (0..1). If a trained model is available, use it;
    otherwise use a simple, interpretable fallback.
    """
    if _model is not None:
        # Expect your real feature vector construction here:
        # X = [[features["age"], features["bmi"], ...]]
        # prob = _model.predict_proba(X)[0][1]
        # For safety until user wires features:
        try:
            # Minimal example: if the model exposes 'predict_proba' and expects [age, bmi]
            X = [[features.get("age", 0), features.get("bmi", 0)]]
            prob = float(_model.predict_proba(X)[0][1])
            return max(0.0, min(1.0, prob))
        except Exception:
            pass

    # ---- Fallback risk score (very rough; replace with your model logic) ----
    age = features.get("age") or 0
    bmi = features.get("bmi") or 0

    # Simple logistic-ish mapping
    score = 0.0
    score += (age - 30) * 0.01 if age > 30 else 0
    score += (bmi - 25) * 0.02 if bmi > 25 else 0
    score = max(0.0, min(1.0, score))
    return score

def label_from_prob(p: float) -> str:
    if p < 0.34:
        return "Low"
    if p < 0.67:
        return "Medium"
    return "High"

# ---- Copy blocks ----

def welcome_copy() -> str:
    return (
        "This tool helps you understand your risk of developing type 2 diabetes. "
        "It's not a diagnosis, but it can guide you towards healthier choices."
    )

def low_risk_copy() -> str:
    return (
        "You have a low risk of developing type 2 diabetes in the next 10 years. "
        "Continue to maintain a healthy lifestyle."
    )

def medium_risk_copy() -> str:
    return (
        "Your assessment indicates a medium risk of developing type 2 diabetes. "
        "You have some risk factors; take this seriously and consider lifestyle changes to reduce your risk."
    )

def high_risk_copy() -> str:
    return (
        "Your risk of developing type 2 diabetes is high. "
        "Please consult a healthcare professional for further evaluation and personalised advice."
    )

def lifestyle_recommendations() -> str:
    return (
        "- **Regular Physical Activity**: Aim for at least 150 minutes of moderate-intensity exercise per week.\n"
        "- **Adequate Sleep**: Prioritise 7–9 hours of quality sleep each night.\n"
        "- **Stress Management**: Consider meditation, yoga, or spending time in nature."
    )

def dietary_recommendations() -> str:
    return (
        "- **Whole Grains**: Choose brown rice, quinoa, whole wheat bread over refined grains.\n"
        "- **Fruits & Vegetables**: Aim for at least five servings per day.\n"
        "- **Lean Protein**: Prefer poultry, fish, beans, and lentils.\n"
        "- **Limit** sugary drinks, processed foods, and saturated fats."
    )
