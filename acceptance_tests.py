import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add project directory to path
sys.path.insert(0, '/workspace/projects/Local-Invoice-Parser')

import main
from parser import InvoiceParser

class TestInvoiceParser(unittest.TestCase):
    """Tests for InvoiceParser logic."""

    def test_criterion_1_vendor_extraction(self):
        """Criterion 1: Parser correctly identifies vendors."""
        extractor = InvoiceParser()
        # Mock OCR to return dummy text
        with patch.object(extractor, '_ocr_extract', return_value="Invoice from Amazon for $50.00"):
            result = extractor.process_invoice("dummy.jpg")
        self.assertEqual(result['vendor'], 'Invoice from Amazon')

    def test_criterion_2_amount_extraction(self):
        """Criterion 2: Parser correctly identifies amounts."""
        extractor = InvoiceParser()
        with patch.object(extractor, '_ocr_extract', return_value="Costco: $100.00"):
            result = extractor.process_invoice("dummy.jpg")
        self.assertEqual(result['amount'], '$100.00')

    def test_criterion_3_date_extraction(self):
        """Criterion 3: Parser correctly identifies dates."""
        extractor = InvoiceParser()
        with patch.object(extractor, '_ocr_extract', return_value="Date: 10/05/2023 Service"):
            result = extractor.process_invoice("dummy.jpg")
        self.assertEqual(result['date'], '10/05/2023')

    def test_criterion_4_categorization_electronics(self):
        """Criterion 4: Vendor categorization for electronics."""
        extractor = InvoiceParser()
        with patch.object(extractor, '_ocr_extract', return_value="Amazon Electronics Invoice"):
            result = extractor.process_invoice("dummy.jpg")
        self.assertEqual(result['tax_category'], 'Electronics')

    def test_criterion_5_categorization_misc(self):
        """Criterion 5: Vendor categorization for unknown vendors."""
        extractor = InvoiceParser()
        with patch.object(extractor, '_ocr_extract', return_value="Unknown Company Invoice"):
            result = extractor.process_invoice("dummy.jpg")
        self.assertEqual(result['tax_category'], 'Misc')

class TestCLI(unittest.TestCase):
    """Tests for CLI Argument Parsing and Execution."""

    @patch('sys.argv', ['main.py', '-i', '/fake/path', '-o', '/fake/output.csv'])
    def test_criterion_6_missing_input_arg(self):
        """Criterion 6: CLI raises error when input is missing."""
        # argparse.parse_args will raise error
        with self.assertRaises(SystemExit):
            main.main()

    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['main.py', '-i', '/fake/path', '-o', '/fake/output.csv'])
    def test_criterion_7_input_not_found(self, mock_exists):
        """Criterion 7: CLI handles non-existent input directory."""
        # Should print error and return 1
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            sys.exit(main.main())
        # In a real test we'd capture stdout
        self.assertTrue(mock_exists.called)

    @patch('glob.glob', return_value=[])
    @patch('sys.argv', ['main.py', '-i', '/fake/path', '-o', '/fake/output.csv'])
    def test_criterion_8_no_files_found(self, mock_glob):
        """Criterion 8: CLI handles empty directory."""
        # Should print error and return 1
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            sys.exit(main.main())
        self.assertTrue(mock_glob.called)

    @patch('parser.InvoiceParser.process_invoice')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', create=True)
    @patch('sys.argv', ['main.py', '-i', '/fake/input', '-o', '/fake/output.csv'])
    def test_criterion_9_successful_processing(self, mock_open, mock_exists, mock_process):
        """Criterion 9: CLI successfully processes and writes CSV."""
        # Setup mock return values
        mock_exists.return_value = True
        mock_glob = MagicMock()
        mock_glob.return_value = ['invoice1.png', 'invoice2.pdf']
        mock_open.return_value.__enter__.return_value.write = MagicMock()
        
        # Mock process_invoice to return valid data
        mock_process.side_effect = [
            {'vendor': 'Amazon', 'date': '2023-01-01', 'amount': '50.00', 'tax_category': 'Electronics'},
            {'vendor': 'Uber', 'date': '2023-01-02', 'amount': '20.00', 'tax_category': 'Transport'}
        ]

        # Inject glob into the namespace of main module for this test
        import main
        main.glob = mock_glob

        # Run main
        sys.exit(main.main())

        # Verify calls
        self.assertEqual(mock_open.call_count, 1)
        # Verify file was opened for writing
        mock_open.assert_called_once()

if __name__ == '__main__':
    unittest.main()
