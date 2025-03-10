import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load Dataset
df = pd.read_csv("Final_Blood_Report_Analysis.csv")

# Convert categorical disease labels (Yes/No) into binary (1/0)
disease_columns = ["Diabetes", "Typhoid", "Malaria", "Thyroid Disorder", "High Cholesterol", "Liver Disease", "Stomach Infection"]
df[disease_columns] = df[disease_columns].replace({"Yes": 1, "No": 0})

# Select Features (Blood Test Values) & Labels (Diseases)
X = df.drop(["Patient_ID", "Age", "Gender"] + disease_columns, axis=1)  # Features
y = df[disease_columns]  # Labels

# Train-Test Split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize Features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Dataset Preprocessing Complete! ✅")

# Train the Model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the Model
joblib.dump(model, "blood_disease_model.pkl")
print("Model Trained & Saved! ✅")
