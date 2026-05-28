# Local Invoice Parser

A CLI tool to extract invoice data (vendor, date, amount) from images and PDFs using local OCR and regex, outputting structured CSV/JSON data.

## What it does
Scans a directory for invoice images, extracts text using OCR, identifies key fields via regex, and generates structured data files.

## Installation
1. Install Python dependencies:
   ```bash
   pip install pytesseract pillow pandas
   ```
2. Install Tesseract OCR engine (system dependency):
   * Ubuntu: `sudo apt-get install tesseract-ocr`
   * Mac: `brew install tesseract`
   * Windows: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

## Usage
Scan a directory of invoices and save results to CSV:
```bash
python local_invoice_parser.py /path/to/invoices --output invoices.csv
```

## Configuration
The tool looks for images in the input directory. Output format (CSV/JSON) is selected via the `--output` flag. Tax rules are defined in a simple JSON config file located in the project root.