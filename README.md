# Local Invoice Parser

A privacy-focused, offline-capable CLI tool to extract invoice data from local image and PDF files using OCR.

## What it does
Extracts structured invoice data (vendor, date, amount) from local image/PDF files using OCR and Regex, and outputs the results to CSV or JSON.

## Installation & Setup

### System Dependencies
**Crucial:** This tool requires Tesseract OCR installed on your system.

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**macOS:**
```bash
brew install tesseract
```

### Python Dependencies
```bash
pip install pytesseract pillow pdf2image requests regex
```

## Usage

Run the parser against a directory:
```bash
python main.py --directory ./invoices --output output.csv --format csv
```

## Configuration
No configuration files required. Use command line arguments for directory path and output format.