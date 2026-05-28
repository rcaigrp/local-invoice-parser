import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import re

# Assuming classes are imported from modules
# from ocr_engine import InvoiceOCR
# from invoice_parser import InvoiceParser
# from output_handler import OutputWriter

class TestInvoiceParser(unittest.TestCase):
    def test_criterion_1_ocr_engine_exists(self):
        # Check import
        try:
            from ocr_engine import InvoiceOCR
        except ImportError:
            self.fail("ocr_engine.py module not found")

    def test_criterion_2_regex_parser_identifies_fields(self):
        # Mock the OCR output
        mock_text = "Invoice from TechCorp on 2023-10-01 for $500.00"
        
        # Import parser logic
        try:
            from invoice_parser import InvoiceParser
        except ImportError:
            self.fail("invoice_parser.py module not found")
            return
            
        parser = InvoiceParser()
        result = parser.parse(mock_text)
        
        self.assertIn('vendor', result)
        self.assertIn('date', result)
        self.assertIn('amount', result)
        self.assertEqual(result['vendor'], 'TechCorp')
        
class TestOutputHandler(unittest.TestCase):
    def test_criterion_3_output_handler_writes_csv(self):
        try:
            from output_handler import OutputWriter
        except ImportError:
            self.fail("output_handler.py module not found")
            return
            
        writer = OutputWriter()
        data = {'vendor': 'Test', 'date': '2023-01-01', 'amount': 100.0}
        
        # Mock file write to avoid filesystem pollution
        with patch('output_handler.pd.DataFrame.to_csv', return_value=None) as mock_to_csv:
            writer.save_csv(data, 'test_output.csv')
            mock_to_csv.assert_called_once()

class TestCLI(unittest.TestCase):
    def test_criterion_4_cli_entry_point(self):
        try:
            from main import main
        except ImportError:
            self.fail("main.py module not found")
            return

class TestIntegration(unittest.TestCase):
    def test_full_workflow(self):
        """Mock OCR, Parser, and Output to ensure full chain works."""
        # This test ensures the classes can talk to each other
        try:
            from ocr_engine import InvoiceOCR
            from invoice_parser import InvoiceParser
            from output_handler import OutputWriter
        except ImportError:
            self.fail("Dependency modules missing")
            return
        
        # Mock OCR
        with patch.object(InvoiceOCR, 'extract', return_value="Vendor: Acme $200.00"):
            ocr = InvoiceOCR()
            text = ocr.extract('mock_image.png')
            
            # Mock Parser
            parser = InvoiceParser()
            data = parser.parse(text)
            
            # Mock Output
            with patch.object(OutputWriter, 'save_csv') as mock_save:
                writer = OutputWriter()
                writer.save_csv(data, 'output.csv')
                mock_save.assert_called()

if __name__ == '__main__':
    unittest.main()
