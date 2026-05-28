# Local-Invoice-Parser

A privacy-first, local-only CLI tool to scan directories for invoices (PNG, JPG, PDF), extract text using Tesseract OCR, and categorize expenses via regex.

## What it does

Scans a specified directory for image and PDF invoice files, extracts text using local OCR (pytesseract), identifies vendor, date, and amount fields using regex, and outputs results to CSV and JSON formats with tax categorization.

## Installation and Setup

1. **Install Python Dependencies:**
   ```bash
   pip install pytesseract pillow
   ```

2. **Install Tesseract OCR (System Dependency):**
   You must have Tesseract OCR installed on your system. The path must be added to your PATH environment variable.
   - On macOS: `brew install tesseract`
   - On Ubuntu: `sudo apt-get install tesseract-ocr`
   - On Windows: Download the installer from [UB Mannheim](https://github.com/UBMannheim/Tesseract-ocr-for-Windows/releases).

## Usage

Run the CLI tool against a directory to scan for invoices:
```bash
python -m local_invoice_parser /path/to/invoices --output-dir ./output
```

## Configuration

No configuration files are required for basic usage. Tax categorization rules can be added via a `config.yaml` file if needed in future iterations.