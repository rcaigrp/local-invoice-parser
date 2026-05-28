import os
import argparse
from ocr_engine import InvoiceOCR
from invoice_parser import InvoiceParser
from output_handler import OutputWriter

def main():
    parser = argparse.ArgumentParser(description='Local Invoice Parser')
    parser.add_argument('directory', help='Directory to scan for invoices')
    parser.add_argument('--output', choices=['csv', 'json'], default='csv', help='Output format')
    args = parser.parse_args()

    ocr = InvoiceOCR()
    invoice_parser = InvoiceParser()
    output_writer = OutputWriter()

    results = []

    # Scan directory
    for filename in os.listdir(args.directory):
        if filename.lower().endswith(('.png', '.jpg', '.pdf')):
            try:
                text = ocr.extract(os.path.join(args.directory, filename))
                data = invoice_parser.parse(text)
                if data:
                    data['file_name'] = filename
                    results.append(data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Save output
    if results:
        output_writer.save_csv(results, f'invoices_{args.output}.{args.output}')
        print(f"Successfully parsed {len(results)} invoices.")

if __name__ == '__main__':
    main()
