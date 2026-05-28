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

## Turn 5 — Steward (2026-05-28 15:39 UTC)

```json
{
  "message": "Creating Local-Invoice-Parser project directory, configuration files, CLI entry point, and acceptance tests. Cleaning up staging artifacts.",
  "insights": [
    "Project structure established for a local-only CLI tool.",
    "Acceptance tests defined before implementation to guide development.",
    "Staging artifacts (.coverage) removed to maintain workspace hygiene."
  ],
  "file_writes": [
    {
      "path": "projects/Local-Invoice-Parser/project.json",
      "content": "{\n  \"goal\": \"Build a Python CLI tool that scans a specified directory for image files (PNG, JPG) and PDF files. It uses a local OCR library (like pytesseract) to extract text, then applies regex rules to identify vendor, date, and amount fields. It outputs a structured CSV/JSON file and supports simple tax categorization rules. No external APIs or cloud sync.\",\n  \"acceptance_criteria\": [\n    \"The CLI can scan a directory and list all supported image files.\",\n    \"The application extracts text from images using pytesseract and handles basic OCR errors.\",\n    \"Regex patterns correctly identify and extract Date, Amount, and Vendor fields from extracted text.\",\n    \"The application outputs parsed data to a CSV or JSON file.\",\n    \"Tax categorization logic correctly assigns categories based on vendor name or amount threshold.\"\n  ],\n  \"meeting_budget\": 5,\n  \"meetings_held\": 0,\n  \"status\": \"active\"\n}"
    },
    {
      "path": "projects/Local-Invoice-Parser/README.md",
      "content": "# Local-Invoice-Parser\n\nA privacy-first, local-only CLI tool that scans directories for invoice images (PNG, JPG, PDF), extracts text using Tesseract OCR, and parses key financial data using regex.\n\n## Installation\n\n1.  Clone this repository.\n2.  Install Python dependencies:\n    ```bash\n    pip install -r requirements.txt\n    ```\n3.  **System Requirement:** Ensure Tesseract OCR is installed on your system (e.g., `apt-get install tesseract-ocr` on Linux).\n\n## Usage\n\n```bash\n# Scan directory and output to CSV\npython -m LocalInvoiceParser --input ./invoices --output invoices.csv --format csv\n\n# Scan directory and output to JSON\npython -m LocalInvoiceParser --input ./invoices --output data.json --format json\n\n# Scan with tax categorization\npython -m LocalInvoiceParser --input ./invoices --output report.json --format json --tax-rules config.yaml\n```\n\n## Configuration\n\nA `config.yaml` file can be used to override default regex patterns and tax thresholds:\n```yaml\npatterns:\n  date: '\\d{{4}}-\\d{{2}}-\\d{{2}}'\n  amount: '\\$\\d+\\.\\d{{2}}'\ntax_rules:\n  software: [Adobe, Microsoft, Apple]\n  food: [Uber, DoorDash, Starbucks]\n  travel: [Expedia, Booking]\n```\n"
    },
    {
      "path": "projects/Local-Invoice-Parser/main.py",
      "content": "import argparse\nimport os\nimport re\nimport yaml\nimport pytesseract\nfrom pathlib import Path\nfrom PIL import Image\nimport json\nimport csv\nfrom typing import List, Dict, Any\n\n# Regex Patterns\nDEFAULT_DATE_REGEX = r'\\d{{4}}[-/.]\\d{{2}}[-/.]\\d{{2}}'\nDEFAULT_AMOUNT_REGEX = r'\\$\\d{{1,3}}(,\\d{{3}})*(\\.\\d{{2}})?'\nDEFAULT_VENDOR_REGEX = r'[A-Z][a-z]+\\s[A-Z][a-z]+|[^\\$\\d\\s]{{3,}}'\n\ndef load_config(config_path: str) -> Dict:\n    \"\"\"Load YAML configuration for regex patterns and tax rules.\"\"\"\n    if not os.path.exists(config_path):\n        return {}\n    with open(config_path) as f:\n        return yaml.safe_load(f) or {}\n\ndef scan_directory(directory: str) -> List[str]:\n    \"\"\"Scan directory for image files.\"\"\"\n    supported_exts = ('.png', '.jpg', '.jpeg', '.pdf')\n    files = []\n    for root, dirs, filenames in os.walk(directory):\n        for filename in filenames:\n            if filename.lower().endswith(supported_exts):\n                files.append(os.path.join(root, filename))\n    return files\n\ndef extract_text_from_image(image_path: str) -> str:\n    \"\"\"Extract text using pytesseract.\"\"\"\n    try:\n        image = Image.open(image_path)\n        # Convert to RGB if necessary\n        if image.mode != 'RGB':\n            image = image.convert('RGB')\n        return pytesseract.image_to_string(image)\n    except pytesseract.TesseractNotFoundError:\n        raise Exception(\"Tesseract OCR not found. Please install Tesseract.")\n    except Exception as e:\n        raise Exception(f\"Error reading {image_path}: {e}\")\n\ndef parse_fields(text: str, config: Dict) -> Dict[str, Any]:\n    \"\"\"Extract date, amount, and vendor using regex.\"\"\"\n    patterns = config.get('patterns', {})\n    date_regex = patterns.get('date', DEFAULT_DATE_REGEX)\n    amount_regex = patterns.get('amount', DEFAULT_AMOUNT_REGEX)\n    vendor_regex = patterns.get('vendor', DEFAULT_VENDOR_REGEX)\n\n    date_match = re.search(date_regex, text)\n    amount_match = re.search(amount_regex, text)\n    vendor_matches = re.findall(vendor_regex, text)\n\n    return {\n        'date': date_match.group() if date_match else None,\n        'amount': float(amount_match.group().replace('$', '').replace(',', '')) if amount_match else None,\n        'vendor': ' '.join(vendor_matches[:1]) if vendor_matches else 'Unknown Vendor'\n    }\n\ndef categorize_tax(amount: float, vendor: str, config: Dict) -> str:\n    \"\"\"Assign tax category based on rules.\"\"\"\n    tax_rules = config.get('tax_rules', {})\n    for category, keywords in tax_rules.items():\n        if isinstance(keywords, str) and keywords.lower() in vendor.lower():\n            return category\n        if isinstance(keywords, list) and any(k.lower() in vendor.lower() for k in keywords):\n            return category\n    return 'Uncategorized'\n\ndef save_output(data: List[Dict], output_path: str, output_format: str):\n    \"\"\"Save data to CSV or JSON.\"\"\"\n    if output_format == 'json':\n        with open(output_path, 'w') as f:\n            json.dump(data, f, indent=2)\n    elif output_format == 'csv':\n        if not data:\n            return\n        keys = data[0].keys()\n        with open(output_path, 'w', newline='') as f:\n            writer = csv.DictWriter(f, fieldnames=keys)\n            writer.writeheader()\n            writer.writerows(data)\n\ndef main():\n    args = argparse.ArgumentParser(description='Local Invoice Parser')\n    args.add_argument('--input', required=True, help='Directory to scan for invoices')\n    args.add_argument('--output', required=True, help='Output file path')\n    args.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')\n    args.add_argument('--tax-rules', default='config.yaml', help='Tax rules config file')\n\n    args = args.parse_args()\n\n    files = scan_directory(args.input)\n    results = []\n    config = load_config(args.tax_rules)\n\n    for file in files:\n        print(f\"Processing {file}...\")\n        text = extract_text_from_image(file)\n        fields = parse_fields(text, config)\n        if fields['amount']:\n            fields['tax_category'] = categorize_tax(fields['amount'], fields['vendor'], config)\n            fields['file_path'] = file\n            results.append(fields)\n\n    save_output(results, args.output, args.format)\n    print(f\"Processed {len(results)} invoices. Output saved to {args.output}\")\n\nif __name__ == '__main__':\n    main()\n"
    },
    {
      "path": "projects/Local-Invoice-Parser/requirements.txt",
      "content": "pytesseract>=0.3.10\nPillow>=10.0.0\npyyaml>=6.0\n"
    },
    {
      "path": "projects/Local-Invoice-Parser/acceptance_tests.py",
      "content": "import pytest\nimport os\nimport re\nimport json\nfrom unittest.mock import patch, MagicMock\nimport sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom main import scan_directory, extract_text_from_image, parse_fields, categorize_tax, save_output\n\n# Mock Tesseract behavior\nMOCK_TEXT = \"Invoice #99: Amazon Web Services $150.00 Date: 2023-10-01 Vendor: Amazon\"\n\ndef test_criterion_1_scan_directory():\n    \"\"\"Criterion: The CLI can scan a directory and list all supported image files.\"\"\"\n    with patch('os.walk') as mock_walk:\n        mock_walk.return_value = [('/fake/path', [], ['invoice.pdf', 'receipt.png'])]\n        files = scan_directory('/fake/path')\n        assert len(files) == 2\n\n    with patch('os.walk') as mock_walk:\n        mock_walk.return_value = [('/fake/path', [], ['photo.jpg'])]\n        files = scan_directory('/fake/path')\n        assert len(files) == 1\n\n    with patch('os.walk') as mock_walk:\n        mock_walk.return_value = [('/fake/path', [], ['document.pdf'])]\n        files = scan_directory('/fake/path')\n        assert len(files) == 1\n\n    # Test non-image files are filtered\n    with patch('os.walk') as mock_walk:\n        mock_walk.return_value = [('/fake/path', [], ['data.txt', 'archive.zip'])]\n        files = scan_directory('/fake/path')\n        assert len(files) == 0\n\ndef test_criterion_2_extract_text():\n    \"\"\"Criterion: The application extracts text from images using pytesseract and handles basic OCR errors.\"\"\"\n    with patch('PIL.Image.open') as mock_img:\n        mock_img.return_value.convert.return_value.__class__ = MagicMock\n        mock_tesseract = MagicMock()\n        mock_tesseract.image_to_string.return_value = MOCK_TEXT\n        with patch('pytesseract.image_to_string', mock_tesseract):\n            text = extract_text_from_image('/fake/invoice.pdf')\n            assert 'Amazon' in text\n            assert '150.00' in text\n\n    # Test TesseractNotFoundError\n    with patch('pytesseract.image_to_string', side_effect=pytesseract.TesseractNotFoundError):\n        with pytest.raises(Exception) as exc_info:\n            extract_text_from_image('/fake/invoice.pdf')\n        assert 'Tesseract' in str(exc_info.value)\n\ndef test_criterion_3_parse_fields():\n    \"\"\"Criterion: Regex patterns correctly identify and extract Date, Amount, and Vendor fields.\"\"\"\n    config = {'patterns': {}}\n    fields = parse_fields(MOCK_TEXT, config)\n    assert fields['date'] == '2023-10-01'\n    assert fields['amount'] == 150.00\n    assert fields['vendor'] == 'Amazon'\n\n    # Test default patterns\n    text_no_date = \"Total: $50.00 from Best Buy\"\n    fields = parse_fields(text_no_date, config)\n    assert fields['date'] is None\n    assert fields['amount'] == 50.00\n    assert fields['vendor'] == 'Best Buy'\n\ndef test_criterion_4_output_format():\n    \"\"\"Criterion: The application outputs parsed data to a CSV or JSON file.\"\"\"\n    test_data = [\n        {'date': '2023-10-01', 'amount': 150.00, 'vendor': 'Amazon', 'tax_category': 'software', 'file_path': 'fake.pdf'},\n        {'date': '2023-10-02', 'amount': 25.50, 'vendor': 'Starbucks', 'tax_category': 'food', 'file_path': 'fake.pdf'}\n    ]\n    \n    # Test JSON output\n    with patch('builtins.open', create=True) as mock_open:\n        mock_open.return_value.__enter__.return_value.write = MagicMock()\n        save_output(test_data, 'test_output.json', 'json')\n        mock_open.assert_called()\n\n    # Test CSV output\n    with patch('builtins.open', create=True) as mock_open:\n        mock_open.return_value.__enter__.return_value.write = MagicMock()\n        save_output(test_data, 'test_output.csv', 'csv')\n        mock_open.assert_called()\n\n    # Test empty data\n    save_output([], 'empty.json', 'json')\n\ndef test_criterion_5_tax_categorization():\n    \"\"\"Criterion: Tax categorization logic correctly assigns categories based on vendor name or amount threshold.\"\"\"\n    config = {\n        'tax_rules': {\n            'software': ['Adobe', 'Microsoft', 'Apple'],\n            'food': ['Uber', 'DoorDash', 'Starbucks'],\n            'travel': ['Expedia']\n        }\n    }\n\n    # Test Software Vendor\n    fields = {'vendor': 'Adobe Systems', 'amount': 500.00}\n    cat = categorize_tax(fields['amount'], fields['vendor'], config)\n    assert cat == 'software'\n\n    # Test Food Vendor\n    fields = {'vendor': 'Uber Eats', 'amount': 50.00}\n    cat = categorize_tax(fields['amount'], fields['vendor'], config)\n    assert cat == 'food'\n\n    # Test Travel Vendor\n    fields = {'vendor': 'Expedia', 'amount': 200.00}\n    cat = categorize_tax(fields['amount'], fields['vendor'], config)\n    assert cat == 'travel'\n\n    # Test Uncategorized\n    fields = {'vendor': 'Local Coffee', 'amount': 10.00}\n    cat = categorize_tax(fields['amount'], fields['vendor'], config)\n    assert cat == 'Uncategorized'\n\nif __name__ == '__main__':\n    pytest.main([__file__, '-v'])\n"
    }
  ],
  "file_deletes": [
    ".coverage"
  ],
  "docker_commands": [
    {
      "image": "python:3.11-slim",
      "run": "mkdir -p /workspace/projects/Local-Invoice-Parser && pip install pytesseract Pillow pyyaml && cd /workspace/projects/Local-Invoice-Parser && python -m pytest acceptance_tests.py -v",
      "workdir": "/workspace",
      "timeout": 60
    }
  ],
  "web_requests": [],
  "search_queries": [],
  "notes": [],
  "vote": {
    "action": "Run the provided docker_commands to verify acceptance tests pass before committing.",
    "rationale": "The acceptance_tests.py defines the Definition of Done. Running them ensures the code matches the criteria."
  }
}
```

## Turn 6 — Craft (2026-05-28 15:45 UTC)

Pivoting away from external HTTP mocking libraries (responses/pytest-mock) to pure `unittest.mock` patching strategy to fix the installation failure. Rewriting parser and main modules to be fully mockable and implementing a clean test suite.
