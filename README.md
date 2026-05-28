# Local Invoice Parser

A robust CLI tool to parse invoice text files and convert them into structured JSON data.

## What it does

Extracts vendor name, invoice date, and total amount from text-based invoice files using the `pyparsing` library.

## Installation

```bash
cd storage/projects/Local-Invoice-Parser
pip install pyparsing pytest responses
```

## Usage

Run the parser on a file:
```bash
python main.py invoice.txt
```

Expected output to stdout:
```json
{ "vendor": "VendorName", "date": "2023-10-01", "amount": 100.00 }
```

## Configuration

No configuration required. Default output format is JSON.