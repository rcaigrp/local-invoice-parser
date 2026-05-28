# Local Invoice Parser

A privacy-first, local-only CLI tool to parse invoices from images and PDFs without sending data to the cloud.

## What it does
Scans a directory for images/PDFs, uses local OCR to extract text, applies regex to find vendor, date, and amount, and outputs structured CSV or JSON.

## Installation & Setup

### 1. Install Python Dependencies
```bash
pip install pytesseract pillow pdf2image
```

### 2. Install Tesseract OCR (System Dependency)
This tool requires the Tesseract OCR binary installed on your system.

- **On Ubuntu/Debian:**
  ```bash
  sudo apt-get update && sudo apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
  ```
- **On macOS:**
  ```bash
  brew install tesseract
  ```

## Usage

Run the script from the command line:

```bash
python main.py --input ./invoices --output --format csv
```

### Arguments
- `--input`: Path to the directory containing invoice images/PDFs.
- `--output`: Path to the output file (defaults to stdout).
- `--format`: Output format, either 'csv' or 'json'.

## Configuration
No configuration files required. All processing happens locally.