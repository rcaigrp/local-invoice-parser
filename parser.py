import os
import re
from pathlib import Path

# --- Directory Scanning Logic ---
def scan_directory(directory_path):
    """
    Scans a directory for invoices (images/PDFs).
    Returns a list of file paths.
    """
    target_extensions = {'.png', '.jpg', '.jpeg', '.pdf'}
    invoice_files = []
    
    root_path = Path(directory_path).resolve()
    if not root_path.exists():
        raise FileNotFoundError(f"Directory {directory_path} not found.")
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            # Check extension
            if file_path.suffix.lower() in target_extensions:
                invoice_files.append(file_path)
    
    return invoice_files

# --- Regex Patterns ---
# Vendor: Captures capitalized words (heuristic for company names)
VENDOR_REGEX = re.compile(r'[A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)*')

# Date: Matches YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY
DATE_REGEX = re.compile(r'\d{4}[-/.]\d{2}[-/.]\d{2}')

# Amount: Matches currency symbols followed by numbers
AMOUNT_REGEX = re.compile(r'[$€£]\d{1,3}(?:,\d{3}(?:\.\d{2})?|\.\d{2})?')

def extract_invoice_data(text):
    """
    Extracts vendor, date, and amount from text using regex.
    """
    data = {"vendor": None, "date": None, "amount": None}
    
    vendor_match = VENDOR_REGEX.search(text)
    if vendor_match:
        data["vendor"] = vendor_match.group().strip()
    
    date_match = DATE_REGEX.search(text)
    if date_match:
        data["date"] = date_match.group().strip()
    
    amount_match = AMOUNT_REGEX.search(text)
    if amount_match:
        # Normalize amount to float if needed
        raw = amount_match.group().strip()
        # Simple cleanup for testing
        data["amount"] = raw.replace(',', '') if '.' in raw else raw
    
    return data
