import argparse
import sys
from pathlib import Path
from parser import scan_directory, extract_invoice_data
import pytesseract
from pdf2image import convert_from_path

# Mock pytesseract for testing, real for usage
try:
    # This block will fail if pytesseract isn't installed, but we won't run it yet
    pass 
except ImportError:
    # Stub for CI/CD safety
    print("Tesseract not installed. Running in mock mode.")
    pytesseract.image_to_string = lambda x: "Mock OCR Output"

def main():
    parser = argparse.ArgumentParser(description='Local Invoice Parser')
    parser.add_argument('--directory', '-d', required=True, help='Directory to scan')
    parser.add_argument('--output', '-o', default='output.csv', help='Output file path')
    
    args = parser.parse_args()
    
    # 1. Scan Directory
    files = scan_directory(args.directory)
    print(f"Found {len(files)} invoice files.")
    
    results = []
    
    # 2. Process Files
    for file_path in files:
        print(f"Processing: {file_path.name}...")
        
        try:
            if file_path.suffix.lower() == '.pdf':
                # Convert PDF to image for OCR
                images = convert_from_path(file_path)
                text = pytesseract.image_to_string(images[0])
            else:
                # Read image directly
                text = pytesseract.image_to_string(file_path)
            
            # 3. Extract Data
            data = extract_invoice_data(text)
            
            # Append to results
            results.append({
                'file': file_path.name,
                'vendor': data['vendor'],
                'date': data['date'],
                'amount': data['amount']
            })
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            continue
    
    # 4. Output
    with open(args.output, 'w') as f:
        f.write("file,vendor,date,amount\n")
        for r in results:
            f.write(f"{r['file']},{r['vendor']},{r['date']},{r['amount']}\n")
    
    print(f"Parsed {len(results)} invoices and saved to {args.output}.")

if __name__ == '__main__':
    main()
