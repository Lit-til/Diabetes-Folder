import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# Samples
n_samples = 500

# Generate features
age = np.random.normal(43, 12, n_samples).astype(int)
age = np.clip(age, 18, 80)

sex = np.random.choice(["Male", "Female"], size=n_samples, p=[0.45, 0.55])

bmi = np.random.normal(27.5, 5, n_samples)
bmi = np.clip(bmi, 15, 45)

waist = np.random.normal(90, 12, n_samples)
waist = np.clip(waist, 60, 130)

family_history = np.random.choice(["Yes", "No"], size=n_samples, p=[0.3, 0.7])

fbs = np.random.normal(110, 25, n_samples)
fbs = np.clip(fbs, 70, 200)

hypertension = np.random.choice(["Yes", "No"], size=n_samples, p=[0.25, 0.75])

activity = np.random.choice(["Low", "Moderate", "High"], size=n_samples, p=[0.5, 0.35, 0.15])

smoker = np.random.choice(["Yes", "No"], size=n_samples, p=[0.1, 0.9])

# Target outcome (300 positives, 200 negatives)
outcome = np.zeros(n_samples)
outcome[:300] = 1
np.random.shuffle(outcome)

# Build DataFrame
df = pd.DataFrame({
    "Age": age,
    "Sex": sex,
    "BMI": bmi.round(1),
    "Waist_Circumference_cm": waist.round(1),
    "Family_History": family_history,
    "Fasting_Blood_Sugar_mg_dL": fbs.round(1),
    "Hypertension": hypertension,
    "Physical_Activity": activity,
    "Smoker": smoker,
    "Outcome": outcome.astype(int)
})

# Save as CSV in Colab
df.to_csv("diabetes_nigeria.csv", index=False)

# Preview
print(df['Outcome'].value_counts())
df.head()
