import os
import re
import sys
import json
import csv
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Regex Patterns
DATE_PATTERN = r'\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}'
AMOUNT_PATTERN = r'\$?\s*\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?'
VENDOR_PATTERN = r'[A-Z][a-z]+\s[A-Z][a-z]+' # Simple heuristic

class InvoiceParser:
    def __init__(self, input_dir):
        self.input_dir = Path(input_dir)
        self.entries = []

    def scan_directory(self):
        """Scans input directory for images and PDFs."""
        print(f"Scanning {self.input_dir}...")
        supported_extensions = ('.png', '.jpg', '.jpeg', '.pdf')
        
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    file_path = Path(root) / file
                    print(f"Found: {file_path}")
                    self.process_file(file_path)
        
        return self.entries

    def process_file(self, file_path):
        """Processes a single file to extract text."""
        text = ""
        try:
            if file_path.suffix.lower() == '.pdf':
                # Convert PDF to images first
                images = convert_from_path(str(file_path))
                for image in images:
                    text += pytesseract.image_to_string(image)
            else:
                # Process image directly
                img = Image.open(file_path)
                text = pytesseract.image_to_string(img)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return

        data = self.parse_text(text)
        if data:
            data['file_path'] = str(file_path)
            self.entries.append(data)
            print(f"  -> Extracted: {data.get('vendor', 'Unknown')} - {data.get('date', 'N/A')} - ${data.get('amount', 0.00)}")

    def parse_text(self, text):
        """Applies regex rules to extract invoice data."""
        data = {}
        
        # Extract Date
        date_match = re.search(DATE_PATTERN, text)
        if date_match:
            data['date'] = date_match.group()

        # Extract Amount
        amount_match = re.search(AMOUNT_PATTERN, text)
        if amount_match:
            # Clean amount string (remove currency symbols, commas)
            amount_str = amount_match.group().replace(',', '').replace('$', '')
            try:
                data['amount'] = float(amount_str)
            except ValueError:
                data['amount'] = 0.00

        # Extract Vendor (Heuristic)
        lines = text.split('\n')
        for line in lines:
            match = re.match(VENDOR_PATTERN, line.strip())
            if match:
                data['vendor'] = match.group()
                break

        return data

    def save_csv(self, output_path):
        """Saves extracted data to CSV."""
        if not self.entries:
            print("No data to save.")
            return

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['File', 'Vendor', 'Date', 'Amount'])
            for entry in self.entries:
                writer.writerow([
                    entry.get('file_path', ''),
                    entry.get('vendor', ''),
                    entry.get('date', ''),
                    entry.get('amount', '')
                ])
        print(f"Saved to {output_path}")

    def save_json(self, output_path):
        """Saves extracted data to JSON."""
        if not self.entries:
            print("No data to save.")
            return

        with open(output_path, 'w') as f:
            json.dump(self.entries, f, indent=2)
        print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py --input <dir> [--output <file>] [--format csv/json]")
        sys.exit(1)

    input_dir = sys.argv[1].replace('--input', '').lstrip('=').strip()
    output_path = None
    output_format = 'json'

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
        if sys.argv[i] == '--format' and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1].lower()

    parser = InvoiceParser(input_dir)
    parser.scan_directory()

    if output_path:
        if output_format == 'csv':
            parser.save_csv(output_path)
        elif output_format == 'json':
            parser.save_json(output_path)
    else:
        print("\n--- Summary ---")
        for entry in parser.entries:
            print(entry)