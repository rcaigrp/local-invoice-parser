import os
import sys
import argparse
from parser import InvoiceParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Local Invoice Parser')
    parser.add_argument('--input', '-i', required=True, help='Directory containing invoice images')
    parser.add_argument('--output', '-o', required=True, help='Output CSV file path')
    args = parser.parse_args()

    # Basic implementation placeholder
    print(f"Processing invoices in {args.input}")
    print(f"Outputting to {args.output}")
