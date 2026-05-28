import argparse
import json
import sys
from invoice_parser import parse_invoice

def main():
    parser = argparse.ArgumentParser(description='Parse invoice files to JSON.')
    parser.add_argument('input_file', help='Path to the invoice text file')
    parser.add_argument('--output', '-o', help='Output file (optional)', default=None)
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            text = f.read()
        
        data = parse_invoice(text)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to {args.output}")
        else:
            print(json.dumps(data, indent=2))
            
    except FileNotFoundError:
        print(f"Error: File {args.input_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing invoice: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
