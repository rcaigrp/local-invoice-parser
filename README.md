# Local Invoice Parser

A privacy-first, local-only CLI tool to scan directories for invoices, extract data using OCR and Regex, and output structured data without cloud dependencies.

## What it does
Scans a directory for PNG/JPG/PDF invoices, extracts text using local OCR, parses for vendor/date/amount using Regex, and saves to CSV/JSON.

## Installation

1.  Clone the repository
2.  Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Scan the current directory and output CSV:
```bash
python -m Local_Invoice_Parser
```

Scan a specific directory:
```bash
python -m Local_Invoice_Parser /path/to/invoices --output json
```

## Configuration
No external config required. All processing is local.

## Tax Categorization
Basic tax logic can be added in `invoice_parser.py` by extending the regex patterns.