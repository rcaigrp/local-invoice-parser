# Local-Invoice-Parser

A privacy-first, local-only CLI tool for parsing receipt images and invoices to extract structured financial data without sending data to the cloud.

## Installation

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install System Dependencies (Tesseract OCR):**
   *On Linux (Debian/Ubuntu):*
   ```bash
   sudo apt-get install tesseract-ocr tesseract-ocr-eng libtesseract-dev libpoppler-cpp-dev poppler-utils
   ```
   *On macOS:*
   ```bash
   brew install tesseract
   ```

3. **Download Tesseract Language Data:**
   Ensure the English data file (e.g., `eng.traineddata`) is in your system PATH or tesseract installation directory.

## Usage

Scan a directory of invoices:
```bash
python main.py /path/to/invoices --output report.csv --format csv
```

Generate JSON output:
```bash
python main.py /path/to/invoices --output report.json --format json
```

## Configuration

The tool uses a default `tax_rules.json` included in the project. You can provide a custom tax rule file via `--tax-rules custom_rules.json`.