import re
import os
import tempfile

class InvoiceParser:
    def __init__(self):
        # Regex patterns
        self.date_pattern = re.compile(r'\d{1,4}[-/\\. ]\d{1,4}[-/\\. ]\d{2,4}')  # Flexible date
        self.amount_pattern = re.compile(r'\$?\d{1,3}(?:,\d{3})?(?:\.\d{2})?')  # Flexible currency
        # Vendor pattern: Capture text until a number is found
        self.vendor_pattern = re.compile(r'[A-Za-z\s]+') 

    def process_invoice(self, file_path):
        """Extracts text using OCR and parses fields."""
        try:
            # This would call pytesseract in production. Tests will mock this.
            text = self._ocr_extract(file_path)
            if not text:
                return None

            # Find date
            date_match = self.date_pattern.search(text)
            date_str = date_match.group(0) if date_match else "Unknown"

            # Find amount
            amount_match = self.amount_pattern.search(text)
            amount_str = amount_match.group(0) if amount_match else "0.00"

            # Find vendor (simplified: text before the date or amount)
            # Re-scanning for vendor name specifically
            vendor_match = self.vendor_pattern.search(text)
            vendor_str = vendor_match.group(0) if vendor_match else "Unknown Vendor"

            # Determine tax category
            category = self._categorize(vendor_str)

            return {
                'vendor': vendor_str,
                'date': date_str,
                'amount': amount_str,
                'tax_category': category
            }
        except Exception as e:
            raise Exception(f"Processing error: {e}")

    def _ocr_extract(self, file_path):
        """Placeholder for pytesseract call."""
        raise NotImplementedError("Must be mocked in tests")

    def _categorize(self, vendor):
        """Simple tax categorization based on vendor name."""
        if 'Amazon' in vendor or 'Best Buy' in vendor:
            return 'Electronics'
        elif 'Uber' in vendor:
            return 'Transport'
        elif 'Microsoft' in vendor or 'Google' in vendor:
            return 'Software'
        elif 'Costco' in vendor:
            return 'Retail'
        return 'Misc'
