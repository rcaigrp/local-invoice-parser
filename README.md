# Local Invoice Parser

A privacy-first CLI tool for extracting invoice data from images and PDFs locally.

## What it does
Local Invoice Parser scans a directory for image files (PNG, JPG) and PDFs. It uses pytesseract to extract text and regex to find vendor, date, and amount fields. It outputs structured CSV/JSON data with tax categorization.

## Installation
```bash
pip install pytesseract pillow pandas tesseract-ocr
```

## Usage
```bash
python main.py --directory /path/to/invoices
```

## Configuration
Create a `config.json` file in the project directory:
```json
{
  "tax_rules": {
    "food": "groceries",
    "transport": "fuel",
    "misc": "office supplies"
  }
}
```

## Output
The tool will generate `invoices.csv` and `invoices.json` in the output directory.