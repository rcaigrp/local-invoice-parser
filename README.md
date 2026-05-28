# Local Invoice Parser

A privacy-first, local-only CLI tool to extract and categorize invoice data from image and PDF files.

## What it does

Scans a specified directory for invoice images (PNG, JPG) and PDFs, extracts text using local OCR, identifies key fields using regex, and outputs structured data.

## Installation

```bash
# Install Python dependencies
cd Local-Invoice-Parser
curl -s https://pyenv.run/bin/install.sh | bash
pyenv install 3.11
pyenv local 3.11
pip install pytesseract pillow pyyaml

# Install Tesseract OCR (System Dependency)
# Ubuntu/Debian:
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
# MacOS:
brew install tesseract
```

## Usage

```bash
# Parse invoices and save to CSV
python main.py --input ./invoices --output ./output.csv --tax-rules ./rules.yml
```

## Configuration

The tool supports a YAML configuration file (`rules.yml`) to define:
- **Regex Patterns**: Custom patterns for extracting dates, amounts, and vendor names.
- **Tax Rules**: Simple lookup logic for categorizing expenses (e.g., Office Supplies, Meals).

Example `rules.yml`:
```yaml
amount_pattern: "\\d+\\.\\d{2}"
date_pattern: "\\d{4}-\\d{2}-\\d{2}"
tax_rules:
  "Coffee Shop": "Meals"
  "Office Supply Co.": "Office Supplies"
```
