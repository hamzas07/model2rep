import pandas as pd

# Load the dataset used for training
df = pd.read_csv("Final_Blood_Report_Analysis.csv")

# Get the feature names (excluding target disease columns)
disease_columns = ["Diabetes", "Typhoid", "Malaria", "Thyroid Disorder", "High Cholesterol", "Liver Disease", "Stomach Infection"]
features_used = df.drop(["Patient_ID", "Age", "Gender"] + disease_columns, axis=1).columns

print("Features used for training:", list(features_used))
