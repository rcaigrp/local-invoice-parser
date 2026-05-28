import os
import re
import csv
import json
from pathlib import Path
import pytesseract
from pdf2image import convert_path

# Robust Regex Patterns
VENDOR_PATTERN = re.compile(
    r'^([A-Z][A-Za-z\s&]+)\s*\d',  # Starts with capital letter, stops before first number
    re.MULTILINE
)

DATE_PATTERN = re.compile(
    r'\d{1,2}[\/.-]\d{1,2}[\/.-]\d{2,4}', # DD/MM or MM/DD or YYYY-MM
    re.IGNORECASE
)

AMOUNT_PATTERN = re.compile(
    r'[$€£]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?', # Currency with optional thousands and decimals
    re.IGNORECASE
)

def scan_directory(directory):
    """Recursively scans directory for image and pdf files."""
    directory = Path(directory).resolve()
    supported_extensions = {'.png', '.jpg', '.jpeg', '.pdf'}
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(tuple(supported_extensions)):
                files.append(os.path.join(root, filename))
    return files

def extract_text_from_file(filepath):
    """Extracts text using OCR."""
    text = ""
    try:
        if filepath.suffix.lower() == '.pdf':
            # Convert PDF to images for tesseract
            images = convert_path(filepath, grayscale=True, poppler_path=None)
            for img in images:
                text += pytesseract.image_to_string(img) + "\n"
        elif filepath.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            text = pytesseract.image_to_string(filepath)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return text

def parse_invoice_data(text):
    """Applies regex patterns to extract vendor, date, and amount."""
    data = {
        'vendor': None,
        'date': None,
        'amount': None
    }
    
    # Extract Vendor
    vendor_match = VENDOR_PATTERN.search(text)
    if vendor_match:
        data['vendor'] = vendor_match.group(1).strip()
    
    # Extract Date
    date_matches = DATE_PATTERN.findall(text)
    if date_matches:
        # Return the most likely date (usually last one)
        data['date'] = date_matches[-1]
    
    # Extract Amount
    amount_matches = AMOUNT_PATTERN.findall(text)
    if amount_matches:
        # Return the largest amount found
        amounts = [float(a.replace(',', '').replace('$', '').replace('€', '').replace('£', '')) for a in amount_matches]
        data['amount'] = max(amounts)
    
    return data

def main(input_dir, output_file):
    print(f"Scanning directory: {input_dir}")
    files = scan_directory(input_dir)
    
    parsed_data = []
    for file_path in files:
        print(f"Processing: {file_path}")
        text = extract_text_from_file(Path(file_path))
        if text:
            data = parse_invoice_data(text)
            data['filename'] = file_path.name
            parsed_data.append(data)
            print(f"  - Vendor: {data.get('vendor')}, Date: {data.get('date')}, Amount: {data.get('amount')}")
    
    # Write to CSV
    if parsed_data:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['filename', 'vendor', 'date', 'amount'])
            writer.writeheader()
            writer.writerows(parsed_data)
        print(f"\nResults saved to {output_file}")
    else:
        print("No valid invoice data found.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse invoices from images or PDFs.')
    parser.add_argument('directory', help='Directory containing invoice images/PDFs')
    parser.add_argument('--output', default='invoices_parsed.csv', help='Output CSV file')
    args = parser.parse_args()
    main(args.directory, args.output)