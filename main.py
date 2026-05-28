import argparse
import os
import sys
import re
from pathlib import Path
from typing import List, Dict

# Import modules
from ocr_engine import extract_text_from_file
from parser import parse_invoice
from formatter import generate_csv, generate_json

def main():
    parser = argparse.ArgumentParser(description='Local Invoice Parser')
    parser.add_argument('directory', type=str, help='Directory containing invoice images (png, jpg, pdf)')
    parser.add_argument('--output', type=str, required=True, help='Output filename (report.csv or report.json)')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output format')
    args = parser.parse_args()

    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        sys.exit(1)

    # Find files
    extensions = ('.png', '.jpg', '.jpeg', '.pdf')
    files = [f for f in os.listdir(args.directory) if f.lower().endswith(extensions)]

    if not files:
        print(f"No invoice files found in {args.directory}")
        sys.exit(0)

    print(f"Found {len(files)} invoice(s). Processing...")
    all_entries = []

    for filename in files:
        filepath = os.path.join(args.directory, filename)
        try:
            text = extract_text_from_file(filepath)
            if text:
                parsed_data = parse_invoice(text)
                if parsed_data:
                    parsed_data['filename'] = filename
                    all_entries.append(parsed_data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Output
    if args.format == 'csv':
        generate_csv(all_entries, args.output)
    else:
        generate_json(all_entries, args.output)

    print(f"Done. Results saved to {args.output}")

if __name__ == '__main__':
    main()
