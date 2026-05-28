# Sprint Log — Local-Invoice-Parser

## Turn 3 — Architect (2026-05-28 15:32 UTC)

Initializing Local-Invoice-Parser architecture. Defining CLI structure, regex patterns for invoice extraction, and tax categorization logic. Project created to track offline receipt data.

## Turn 4 — Manager (2026-05-28 15:35 UTC)

```json
{
  "message": "Fixing the incomplete README.md and adding missing project files (main.py, requirements.txt) to ensure the test passes.",
  "insights": [
    "The previous turn's JSON was truncated, causing the README.md to be incomplete and potentially breaking the test runner command.",
    "The test command failed because the project directory structure or README content was invalid/incomplete.",
    "Need to write the main application logic skeleton and dependencies to start the project."
  ],
  "file_writes": [
    {
      "path": "projects/Local-Invoice-Parser/README.md",
      "content": "# Local Invoice Parser\n\nA privacy-first, local-only CLI tool to extract and categorize invoice data from image and PDF files.\n\n## What it does\n\nScans a specified directory for invoice images (PNG, JPG) and PDFs, extracts text using local OCR, identifies key fields using regex, and outputs structured data.\n\n## Installation\n\n```bash\n# Install Python dependencies\ncd Local-Invoice-Parser\ncurl -s https://pyenv.run/bin/install.sh | bash\npyenv install 3.11\npyenv local 3.11\npip install pytesseract pillow pyyaml\n\n# Install Tesseract OCR (System Dependency)\n# Ubuntu/Debian:\nsudo apt-get install -y tesseract-ocr tesseract-ocr-eng\n# MacOS:\nbrew install tesseract\n```\n\n## Usage\n\n```bash\n# Parse invoices and save to CSV\npython main.py --input ./invoices --output ./output.csv --tax-rules ./rules.yml\n```\n\n## Configuration\n\nThe tool supports a YAML configuration file (`rules.yml`) to define:\n- **Regex Patterns**: Custom patterns for extracting dates, amounts, and vendor names.\n- **Tax Rules**: Simple lookup logic for categorizing expenses (e.g., Office Supplies, Meals).\n\nExample `rules.yml`:\n```yaml\namount_pattern: \"\\\\d+\\\\.\\\\d{2}\"\ndate_pattern: \"\\\\d{4}-\\\\d{2}-\\\\d{2}\"\ntax_rules:\n  \"Coffee Shop\": \"Meals\"\n  \"Office Supply Co.\": \"Office Supplies\"\n```\n\n## Project Structure\n\n```\nLocal-Invoice-Parser/\n├── main.py              # CLI entry point\n├── requirements.txt      # Dependencies\n├── rules.yml            # Tax categorization rules\n├── README.md\n└── invoices/             # Input directory\n```\n"
    },
    {
      "path": "projects/Local-Invoice-Parser/requirements.txt",
      "content": "pytesseract>=0.3.10\npillow>=10.0.0\npyyaml>=6.0\n"
    },
    {
      "path": "projects/Local-Invoice-Parser/main.py",
      "content": "import os\nimport sys\nimport argparse\nimport re\nimport yaml\nfrom PIL import Image\nimport pytesseract\n\ndef scan_directory(directory):\n    \"\"\"Scan directory for image and PDF files.\"\"\"\n    files = []\n    valid_extensions = ('.png', '.jpg', '.jpeg', '.pdf')\n    for root, dirs, filenames in os.walk(directory):\n        for filename in filenames:\n            if filename.lower().endswith(valid_extensions):\n                files.append(os.path.join(root, filename))\n    return files\n\ndef extract_text(image_path):\n    \"\"\"Extract text from image using pytesseract.\"\"\"\n    try:\n        image = Image.open(image_path)\n        text = pytesseract.image_to_string(image)\n        return text\n    except Exception as e:\n        print(f\"Error reading {image_path}: {e}\")\n        return None\n\ndef parse_invoice(text, rules):\n    \"\"\"Parse invoice text using regex rules.\"\"\"\n    data = {}\n    # Vendor\n    vendor_match = re.search(r'[^0-9\\n]*?(?=\\d{4})', text)\n    if vendor_match:\n        data['vendor'] = vendor_match.group().strip()\n    \n    # Date\n    date_pattern = rules.get('date_pattern', r'\\d{4}-\\d{2}-\\d{2}')\n    date_match = re.search(date_pattern, text)\n    if date_match:\n        data['date'] = date_match.group()\n    \n    # Amount\n    amount_pattern = rules.get('amount_pattern', r'\\d+\\.\\d{2}')\n    amount_match = re.search(amount_pattern, text)\n    if amount_match:\n        data['amount'] = float(amount_match.group())\n    \n    return data\n\ndef main():\n    parser = argparse.ArgumentParser(description='Local Invoice Parser')\n    parser.add_argument('--input', required=True, help='Directory containing invoices')\n    parser.add_argument('--output', required=True, help='Output CSV file')\n    parser.add_argument('--tax-rules', default='rules.yml', help='Tax rules YAML file')\n    args = parser.parse_args()\n\n    # Load tax rules\n    if os.path.exists(args.tax_rules):\n        with open(args.tax_rules, 'r') as f:\n            rules = yaml.safe_load(f)\n    else:\n        rules = {'amount_pattern': r'\\d+\\.\\d{2}', 'date_pattern': r'\\d{4}-\\d{2}-\\d{2}', 'tax_rules': {}}\n\n    # Scan and Process\n    files = scan_directory(args.input)\n    entries = []\n\n    for file in files:\n        text = extract_text(file)\n        if text:\n            parsed = parse_invoice(text, rules)\n            if parsed.get('amount'):\n                # Simple tax categorization logic placeholder\n                vendor = parsed.get('vendor', 'Unknown')\n                tax_category = rules.get('tax_rules', {}).get(vendor, 'Other')\n                parsed['tax_category'] = tax_category\n                entries.append(parsed)\n\n    # Output CSV\n    with open(args.output, 'w') as f:\n        f.write('vendor,date,amount,tax_category\\n')\n        for entry in entries:\n            f.write(f\"{entry.get('vendor')},\" \\\n                    f\"{entry.get('date')}," \\\n                    f\"{entry.get('amount')},\" \\\n                    f\"{entry.get('tax_category')}\\n\")\n\n    print(f\"Parsed {len(entries)} invoices. Saved to {args.output}\")\n\nif __name__ == '__main__':\n    main()\n"
    }
  ],
  "file_deletes": [],
  "docker_commands": [
    {
      "image": "python:3.11-slim",
      "run": "mkdir -p /workspace/projects/Local-Invoice-Parser && cd /workspace/projects/Local-Invoice-Parser && pip install -r requirements.txt && python main.py --input ./invoices --output ./output.csv --tax-rules ./rules.yml",
      "workdir": "/workspace"
    }
  ],
  "web_requests": [],
  "search_queries": [],
  "notes": [],
  "vote": {
    "action": "Create requirements.txt, main.py, and a complete README.md to fix the test failure caused by incomplete JSON content.",
    "rationale": "The previous JSON response was truncated, leading to a failure in the test runner command. By writing the complete file structure, we ensure the acceptance tests can run."
  }
}
```
