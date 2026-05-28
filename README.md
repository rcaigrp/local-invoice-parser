# Local-Invoice-Parser

## What
A privacy-first, local-only CLI tool for parsing invoice images and extracting financial data without sending data to external cloud APIs.

## Installation

```bash
pip install pytesseract pillow
```

## Usage

```bash
# Scan directory and export to CSV
python -m invoice_parser /path/to/invoices --output csv

# Scan directory and export to JSON
python -m invoice_parser /path/to/invoices --output json
```

## Configuration

No configuration files required. All settings are passed via command-line arguments:

- `--input`: Path to the directory containing invoice images/PDFs
- `--output`: Output format (`csv` or `json`)
- `--tax-rules`: Optional path to a YAML file containing tax categorization rules