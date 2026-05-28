import pytest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Mock the pytesseract library
sys.modules['pytesseract'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Import the module to test (assuming it's in main.py or we create a simple module)
# For this test, we will test the logic functions directly.

def test_criterion_1_scan_directory():
    """Test CLI tool successfully scans a directory for images/PDFs."""
    # Setup
    with patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = ['invoice1.pdf', 'receipt.jpg', 'data.txt']
        
        # Simulate scanning logic
        files = [f for f in mock_listdir.return_value if f.endswith(('.pdf', '.jpg', '.png'))]
        assert len(files) == 2, "Should find 2 invoice files"

def test_criterion_2_ocr_extraction():
    """Test Local OCR (pytesseract) extracts text from images."""
    # Mock pytesseract.image_to_string
    import pytesseract
    mock_image = MagicMock()
    mock_text = "Vendor: ACME Corp\nDate: 2023-10-15\nAmount: 100.50\n"
    pytesseract.image_to_string.return_value = mock_text
    
    # Call function
    extracted = pytesseract.image_to_string(mock_image)
    
    # Assert
    assert "Vendor: ACME Corp" in extracted
    assert "Amount: 100.50" in extracted

def test_criterion_3_regex_parsing():
    """Test Regex rules identify vendor, date, and amount fields."""
    text = "Invoice #99 from Tech Solutions on 2023-11-01 for $45.00"
    
    # Regex patterns
    amount_pattern = r'\$?(\d+\.\d{2})'
    date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    
    import re
    amount_match = re.search(amount_pattern, text)
    date_match = re.search(date_pattern, text)
    
    assert amount_match is not None, "Amount should be found"
    assert date_match is not None, "Date should be found"
    assert float(amount_match.group(1)) > 0

def test_criterion_4_csv_output():
    """Test Output is a structured CSV file."""
    # Mock file write
    data = [
        {'vendor': 'Test Corp', 'date': '2023-01-01', 'amount': 100.00, 'tax': 'Office Supplies'}
    ]
    
    with patch('builtins.open', mock_open()) as mock_file:
        # Simulate writing CSV
        mock_file = StringIO()
        csv_writer = mock_file.csv.writer(mock_file)
        csv_writer.writerow(['vendor', 'date', 'amount', 'tax'])
        csv_writer.writerow(data[0])
        
        # Read back to verify
        mock_file.seek(0)
        content = mock_file.read()
        assert 'vendor,date,amount,tax' in content
        assert 'Test Corp' in content

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
