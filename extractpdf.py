import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Open PDF
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"  # Extract plain text
    return text

# Test with Sample PDF
pdf_path = "Sample_Pathology_Report_Fixed.pdf"  # Use your actual file path
extracted_text = extract_text_from_pdf(pdf_path)

print("Extracted Text:\n", extracted_text)