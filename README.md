# Local Invoice Parser

A privacy-first, local-only CLI tool to scan directories for invoices, extract data using OCR, and categorize expenses.

## What the app does
Scans a specified directory for image files (PNG, JPG, PDF), extracts text using local OCR, and identifies vendor, date, and amount fields using regex patterns.

## Installation and Setup
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install pytesseract pdf2image re pandas
   ```
3. **System Dependencies:**
   - **Tesseract OCR**: Must be installed on the host system. (Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) or brew install tesseract on Mac).

## Usage Examples

1. **Run the parser:**
   ```bash
   python main.py --directory ./invoices --output ./output.csv
   ```

2. **Run with tax rules:**
   ```bash
   python main.py --directory ./invoices --tax-rules ./config.json
   ```

## Configuration
- No external configuration needed. All rules are embedded in the code for this initial version.
