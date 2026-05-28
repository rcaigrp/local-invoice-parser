# Local Invoice Parser

A privacy-first CLI tool that extracts invoice data from local image files using OCR and regex parsing.

## Installation & Setup

1. Clone the repository.
2. Install Python dependencies:
   ```bash
   pip install pytesseract pillow regex pydantic
   ```
3. Download and install Tesseract OCR engine from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) or similar source.

## Usage

Run the tool against a directory of invoices:

```bash
python main.py --input ./invoices/ --output ./parsed_invoices.json --tax-rules ./tax_rules.yml
```

## Configuration

No environment variables required. All processing is local.