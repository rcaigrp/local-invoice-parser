# Local-Invoice-Parser

A privacy-first, local-only CLI tool to parse invoices from images and PDF files using Tesseract OCR and Regex patterns.

## What it does
Scans a directory for image files, extracts text using OCR, and identifies key invoice fields (Vendor, Date, Amount) using robust Regular Expressions.

## Installation and Setup

### System Requirements
You need Tesseract OCR installed on your system. On Ubuntu/Debian: `sudo apt-get install tesseract-ocr tesseract-ocr-eng`.

### Dependencies
```bash
pip install pytesseract pillow pdf2image
```

## Usage

1. Create a folder with invoice images (png/jpg/pdf).
2. Run the script:
```bash
python main.py /path/to/invoices --output invoices_parsed.csv
```

## Configuration
The script looks for the Tesseract executable in your PATH. No cloud services or APIs are used.