import joblib
import numpy as np

# Load trained model
model = joblib.load("blood_disease_model.pkl")

# Extracted test values from PDF
test_values = {'Hemoglobin': 13.5, 'WBC Count': 7.2, 'Platelet Count': 250.0, 'Fasting Blood Sugar': 110.0, 
               'HbA1c': 6.2, 'Total Cholesterol': 220.0, 'LDL Cholesterol': 140.0, 'HDL Cholesterol': 45.0, 
               'Triglycerides': 180.0, 'TSH': 2.8, 'ALT': 35.0, 'AST': 30.0, 'Bilirubin': 1.0, 'CRP': 4.2}

# Feature order expected by the model
feature_order = [
    "Hemoglobin (g/dL)", "RBC Count (million cells/μL)", "WBC Count (thousand cells/μL)", 
    "Platelet Count (thousand/μL)", "Fasting Blood Sugar (mg/dL)", "HbA1c (%)", "Total Cholesterol (mg/dL)", 
    "LDL (mg/dL)", "HDL (mg/dL)", "Triglycerides (mg/dL)", "TSH (mU/L)", "T3 (ng/dL)", "T4 (ng/dL)", 
    "ALT (U/L)", "AST (U/L)", "ALP (U/L)", "Bilirubin (mg/dL)", "CRP (mg/L)", 
    "HbA1c (%) Reference Range", "Hemoglobin (g/dL) Reference Range", 
    "Platelet Count (thousand/μL) Reference Range", "TSH (mU/L) Reference Range", 
    "ALT (U/L) Reference Range", "AST (U/L) Reference Range", "Triglycerides (mg/dL) Reference Range"
]

# Default values for missing features
default_values = {
    "RBC Count (million cells/μL)": 5.0,  # Normal range ~ 4.7-6.1
    "T3 (ng/dL)": 100.0,  # Normal range ~ 80-200
    "T4 (ng/dL)": 7.5,  # Normal range ~ 4.5-12
    "ALP (U/L)": 70.0,  # Normal range ~ 40-150
    "HbA1c (%) Reference Range": 5.7,
    "Hemoglobin (g/dL) Reference Range": 15.0,
    "Platelet Count (thousand/μL) Reference Range": 300.0,
    "TSH (mU/L) Reference Range": 2.0,
    "ALT (U/L) Reference Range": 30.0,
    "AST (U/L) Reference Range": 25.0,
    "Triglycerides (mg/dL) Reference Range": 120.0
}

# Fill missing values
for feature in feature_order:
    if feature not in test_values:
        test_values[feature] = default_values.get(feature, 0)  # Use default or 0 if missing

# Convert to NumPy array
input_values = np.array([[test_values[feature] for feature in feature_order]])

# Make prediction
prediction = model.predict(input_values)

# Disease labels
disease_labels = ["Diabetes", "Typhoid", "Malaria", "Thyroid Disorder", "High Cholesterol", "Liver Disease", "Stomach Infection"]

# Show predictions
predicted_diseases = [disease_labels[i] for i in range(len(disease_labels)) if prediction[0][i] == 1]

print("Predicted Diseases:", predicted_diseases if predicted_diseases else "No Disease Detected")
