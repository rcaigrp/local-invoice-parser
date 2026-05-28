import os
import tempfile
import shutil
import pytest
import re
from unittest.mock import patch, MagicMock

# Assuming the main module is imported
# import invoice_parser # Uncomment when main.py exists

class TestInvoiceParser:
    """Test suite for Local Invoice Parser acceptance criteria."""

    def setup_method(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        # Create dummy files
        with open(os.path.join(self.test_dir, 'invoice1.pdf'), 'w') as f:
            f.write('dummy pdf content')
        with open(os.path.join(self.test_dir, 'receipt.png'), 'w') as f:
            f.write('dummy png content')

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_criterion_1_directory_scan(self):
        """
        Criterion: The module scans a directory recursively for image and PDF files.
        Definition of Done: Verify that the scanner identifies .pdf and .png files and returns a list.
        """
        # Mock the file reading part to avoid actually reading files in tests
        with patch('os.listdir', return_value=['invoice1.pdf', 'receipt.png']):
            # If the module uses glob, we mock the glob result
            from invoice_parser import scan_directory
            files = scan_directory(self.test_dir)
            assert len(files) == 2
            assert 'invoice1.pdf' in files
            assert 'receipt.png' in files

    def test_criterion_2_ocr_and_regex(self):
        """
        Criterion: The module mocks pytesseract to extract text and applies regex to find vendor, date, and amount.
        Definition of Done: Verify that regex matches the mock output and extracts the correct data points.
        """
        # Mock the pytesseract output to simulate extracted text
        mock_text = "Invoice #9988 from ACME Corp, Date: 2023-10-27, Total: $150.00"
        
        with patch('pytesseract.image_to_string', return_value=mock_text):
            from invoice_parser import extract_invoice_data
            data = extract_invoice_data(os.path.join(self.test_dir, 'receipt.png'))
            
            # Assert regex extraction
            assert 'ACME Corp' in data.get('vendor', '')
            assert '2023-10-27' in data.get('date', '')
            assert '150.00' in data.get('amount', '')

    def test_criterion_3_output_generation(self):
        """
        Criterion: The module outputs a structured CSV/JSON file based on extracted data.
        Definition of Done: Verify that the CSV file is created with the correct headers and data.
        """
        output_path = os.path.join(self.test_dir, 'output.csv')
        
        # Mock the entire extraction process
        mock_data = [
            {"vendor": "TestVendor", "date": "2023-01-01", "amount": "100.00"},
            {"vendor": "AnotherVendor", "date": "2023-01-02", "amount": "50.00"}
        ]
        
        with patch('invoice_parser.extract_invoice_data', return_value=mock_data):
            # Call the function that writes the file
            # We assume the main module has a function generate_report(data, output_path)
            # for this test to pass. 
            pass # Logic to be implemented in main.py
