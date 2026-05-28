import argparse
import os
import glob
import sys
from parser import InvoiceParser

def main():
    parser = argparse.ArgumentParser(description='Parse invoices from a directory.')
    parser.add_argument('--input', '-i', required=True, help='Directory containing invoice images/PDFs')
    parser.add_argument('--output', '-o', required=True, help='Output CSV file path')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input directory '{args.input}' does not exist.")
        return 1

    # Scan for supported image files
    file_patterns = ['*.png', '*.jpg', '*.jpeg', '*.pdf']
    files = []
    for ext in file_patterns:
        files.extend(glob.glob(os.path.join(args.input, ext)))

    if not files:
        print(f"No invoice files found in {args.input}")
        return 1

    # Process files
    extractor = InvoiceParser()
    results = []

    for file_path in files:
        print(f"Processing {os.path.basename(file_path)}...")
        try:
            extracted = extractor.process_invoice(file_path)
            if extracted:
                results.append(extracted)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
            continue

    # Write CSV
    try:
        with open(args.output, 'w') as f:
            f.write('vendor,date,amount,tax_category\n')
            for row in results:
                f.write(f"{row['vendor']},{row['date']},{row['amount']},{row['tax_category']}\n")
        print(f"Successfully parsed {len(results)} invoices to {args.output}")
    except Exception as e:
        print(f"Error writing output: {e}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
