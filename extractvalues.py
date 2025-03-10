import re
import fitz  # PyMuPDF for PDF text extraction

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# Function to extract test values using regex
def extract_test_values(text):
    patterns = {
        "Hemoglobin": r"Hemoglobin:\s*([\d\.]+)",
        "WBC Count": r"WBC Count:\s*([\d\.]+)",
        "Platelet Count": r"Platelet Count:\s*([\d]+)",
        "Fasting Blood Sugar": r"Fasting Blood Sugar:\s*([\d]+)",
        "HbA1c": r"HbA1c:\s*([\d\.]+)",
        "Total Cholesterol": r"Total Cholesterol:\s*([\d]+)",
        "LDL Cholesterol": r"LDL Cholesterol:\s*([\d]+)",
        "HDL Cholesterol": r"HDL Cholesterol:\s*([\d]+)",
        "Triglycerides": r"Triglycerides:\s*([\d]+)",
        "TSH": r"TSH:\s*([\d\.]+)",
        "ALT": r"ALT:\s*([\d]+)",
        "AST": r"AST:\s*([\d]+)",
        "Bilirubin": r"Bilirubin:\s*([\d\.]+)",
        "CRP": r"CRP:\s*([\d\.]+)"
    }
    
    extracted_values = {}
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            extracted_values[test] = float(match.group(1))  # Convert to float
            
    return extracted_values

# Run the process
pdf_path = "Sample_Pathology_Report_Fixed.pdf"  # Change this to your actual PDF file path
extracted_text = extract_text_from_pdf(pdf_path)  # Extract text from PDF
test_values = extract_test_values(extracted_text)  # Extract values using regex

print("Extracted Test Values:", test_values)
