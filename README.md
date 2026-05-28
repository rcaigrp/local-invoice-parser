# Local-Invoice-Parser

An offline, client-side CLI tool to parse invoice images into structured data using OCR.

## What it does
Scans a folder for images/PDFs, extracts text via Tesseract OCR, and parses fields like Date, Amount, and Vendor using Regex.

## Installation

1.  Clone the repository
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    **Note:** You must have `tesseract-ocr` installed on your system (OS packages or Docker image). PyTesseract depends on this binary.

## Usage

```bash
python main.py --input ./invoices --output ./parsed.csv
```

## Configuration

No external config required. Regex rules are embedded in `parser.py`.

## Example Output (CSV)

```csv
vendor,date,amount,tax_category
Amazon,$120.00,Electronics
Uber,$45.50,Transportation
```