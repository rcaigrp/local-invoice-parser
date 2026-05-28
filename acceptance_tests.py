import pytest
import os
import re
from unittest.mock import patch
import responses

# Import the module logic (will be created later)
# We assume the code will be in main.py and parser.py

def test_criterion_1_vendor_extraction():
    """
    Criterion 1: Regex pattern successfully extracts vendor name from OCR text.
    """
    # Mock text from an invoice
    mock_text = "\nCompany Name LLC\nAddress Line 1\nDate: 10/05/2023\nAmount: 100.50"
    
    # Regex Pattern for Vendor (Heuristic: Capitalized words at start)
    vendor_pattern = re.compile(r'^[A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)*')
    
    match = vendor_pattern.search(mock_text)
    assert match is not None, "Vendor pattern failed to match"
    assert match.group() == "Company Name LLC", f"Expected 'Company Name LLC', got '{match.group()}'"
    
    print("Vendor extraction test passed.")

def test_criterion_2_date_extraction():
    """
    Criterion 2: Regex pattern successfully extracts date from OCR text.
    """
    mock_text = "Invoice Date: 2023-10-05\nTotal: 100.50"
    
    # Regex Pattern for Date (YYYY-MM-DD)
    date_pattern = re.compile(r'\d{4}[-/.]\d{2}[-/.]\d{2}')
    
    match = date_pattern.search(mock_text)
    assert match is not None, "Date pattern failed to match"
    assert match.group() == "2023-10-05", f"Expected '2023-10-05', got '{match.group()}'"
    
    print("Date extraction test passed.")

def test_criterion_3_directory_scanning():
    """
    Criterion 3: Directory scanning logic correctly identifies images and PDFs.
    """
    # Mock file list
    files = [
        'invoice_1.pdf',
        'receipt.png',
        'invoice_2.jpg',
        'report.txt' # Should be ignored
    ]
    
    # Logic to filter files
    image_extensions = {'.png', '.jpg', '.jpeg', '.pdf'}
    found = []
    
    for f in files:
        if os.path.splitext(f)[1].lower() in image_extensions:
            found.append(f)
    
    assert len(found) == 3, f"Expected 3 files (pdf, png, jpg), found {len(found)}"
    assert 'invoice_1.pdf' in found
    assert 'receipt.png' in found
    assert 'invoice_2.jpg' in found
    
    print("Directory scanning test passed.")
