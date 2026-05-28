# Local-Invoice-Parser

A local-first CLI tool for parsing invoice images and PDFs into structured CSV/JSON data using local OCR.

## What it does
Scans a directory for invoice images (PNG, JPG, PDF), extracts text using Tesseract OCR, parses fields (Vendor, Date, Amount) via regex, and categorizes them for tax purposes. All processing happens locally.

## Installation

Requires Python 3.8+.

```bash
pip install pytesseract pillow pandas
```

You also need Tesseract OCR installed on your system path.

## Usage

Scan a folder of invoices and output a CSV:

```bash
python main.py --directory ./invoices --output ./output.csv
```

Output a JSON file:

```bash
python main.py --directory ./invoices --output ./output.json --format json
```

## Configuration

Create a `config.json` file in the project directory to define regex patterns:

```json
{
  "patterns": {
    "date": "\\d{4}-\\d{2}-\\d{2}",
    "amount": "\\d+(.\\d*)?",
    "vendor": "[A-Za-z ]+"
  },
  "tax_rules": {
    "food": "(dining|restaurant|food)",
    "travel": "(flight|hotel|taxi)"
  }
}
```

## Development

Start the sprint to build the core parsing logic and regex engine.