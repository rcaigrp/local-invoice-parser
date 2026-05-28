# Local Invoice Parser

A privacy-first, offline CLI tool for extracting invoice data from scanned documents.

## What it does
Extracts vendor, date, and amount fields from invoices found in a directory.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m local_invoice_parser /path/to/invoices --output invoices.csv
```

## Configuration
Place a `config.json` in the root directory to customize regex patterns and tax rules.