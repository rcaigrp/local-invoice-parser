# Local-Invoice-Parser

## What the app does
A privacy-first, local-only CLI tool that scans directories for invoices, extracts data using local OCR and regex, and outputs structured reports.

## Installation and setup steps

1. Clone the repository.
2. Install Python dependencies:
   ```bash
   pip install regex pytest pytest-mock
   ```
3. *Note: System-level Tesseract OCR is required for production use, but tests will mock this dependency.*

## Usage examples

Run the parser on a directory:
```bash
python main.py /path/to/invoices
```

## Configuration
No environment variables or config files required for basic usage.