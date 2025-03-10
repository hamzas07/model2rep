from flask import Flask, request, jsonify
import joblib
import numpy as np
import requests  # For calling LLaMA API

app = Flask(__name__)


# Load trained ML model
model = joblib.load("blood_disease_model.pkl")

# Feature order (same as training)
feature_order = [
    "Hemoglobin (g/dL)", "RBC Count (million cells/μL)", "WBC Count (thousand cells/μL)",
    "Platelet Count (thousand/μL)", "Fasting Blood Sugar (mg/dL)", "HbA1c (%)",
    "Total Cholesterol (mg/dL)", "LDL (mg/dL)", "HDL (mg/dL)", "Triglycerides (mg/dL)",
    "TSH (mU/L)", "T3 (ng/dL)", "T4 (ng/dL)", "ALT (U/L)", "AST (U/L)", "ALP (U/L)",
    "Bilirubin (mg/dL)", "CRP (mg/L)",  
    "HbA1c (%) Reference Range", "Hemoglobin (g/dL) Reference Range",
    "Platelet Count (thousand/μL) Reference Range", "TSH (mU/L) Reference Range",
    "ALT (U/L) Reference Range", "AST (U/L) Reference Range",
    "Triglycerides (mg/dL) Reference Range"
]


disease_labels = ["Diabetes", "Typhoid", "Malaria", "Thyroid Disorder", "High Cholesterol", "Liver Disease", "Stomach Infection"]

# LLaMA API URL (Modify if using different provider)
LLAMA_API_URL = "https://api.together.xyz/v1/chat/completions"
LLAMA_API_KEY = "tgp_v1_4TDi_9-bRFrxoBl1eV5waB1QtbfRyntD6w-6OuVDEZQ"


# Chatbot API Route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").lower()

    # Dummy test values for now
    test_values = {feature: np.random.uniform(4, 15) for feature in feature_order}

    # Prepare input for ML model
    input_values = np.array([[test_values.get(feature, 0) for feature in feature_order]])

    # Predict diseases
    prediction = model.predict(input_values)
    predicted_diseases = [disease_labels[i] for i in range(len(disease_labels)) if prediction[0][i] == 1]

    if not predicted_diseases:
        predicted_diseases = ["No Disease Detected"]

    # Generate response using LLaMA API
    llama_response = ""
    if LLAMA_API_KEY:
        headers = {"Authorization": f"Bearer {LLAMA_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "messages": [{"role": "system", "content": "You are a medical assistant."},
                         {"role": "user", "content": f"What do you know about {', '.join(predicted_diseases)}?"}],
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "temperature": 0.7
        }
        response = requests.post(LLAMA_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            llama_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            llama_response = "Error fetching response from LLaMA API."

    return jsonify({
        "predicted_diseases": predicted_diseases,
        "explanation": llama_response
    })

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)


