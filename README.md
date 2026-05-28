# Local Invoice Parser

A privacy-first CLI tool to extract invoice data from local images using OCR.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Tesseract OCR (System Dependency):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install -y tesseract-ocr libtesseract-dev
   # MacOS
   brew install tesseract
   # Windows (Download from site)
   ```

## Usage

```bash
python -m invoice_parser scan ./invoices --output invoices.csv
```

## Configuration

No external APIs required. All processing happens locally.