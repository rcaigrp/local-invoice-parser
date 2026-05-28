# Local Invoice Parser

## What it does
Extracts vendor, date, and amount data from invoices using OCR and regex.

## Installation & Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. *Note: pytesseract requires Tesseract OCR installed on the system. Please install it via your OS package manager (e.g., apt-get install tesseract-ocr).*

## Usage
Run the CLI tool:
```bash
python main.py --input ./invoices --output ./output.csv
```

## Configuration
No configuration files required. Input and output paths are passed as command-line arguments.