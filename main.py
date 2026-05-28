# Local Invoice Parser
# Architecture: Local-first, standard library only.
import csv
import re
from typing import Dict

def parse_invoice_text(text: str) -> Dict[str, str]:
    """Parses raw invoice text into structured data."""
    vendor_pattern = re.compile(r'Vendor:\s*(.*?)\n')
    date_pattern = re.compile(r'Date:\s*(\d{4}-\d{2}-\d{2})')
    amount_pattern = re.compile(r'Amount:\s*([\d.,]+)')
    
    vendor_match = vendor_pattern.search(text)
    date_match = date_pattern.search(text)
    amount_match = amount_pattern.search(text)
    
    invoice_data = {
        'vendor': vendor_match.group(1).strip() if vendor_match else 'Unknown',
        'date': date_match.group(1) if date_match else 'Unknown',
        'amount': amount_match.group(1) if amount_match else '0'
    }
    return invoice_data

def save_to_csv(data: list, filename: str = "invoices.csv"):
    """Saves parsed invoices to a CSV file."""
    if not data:
        return
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['vendor', 'date', 'amount'])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    sample = "Vendor: Amazon Inc.\nDate: 2023-10-27\nAmount: 45.99"
    result = parse_invoice_text(sample)
    print(f"Parsed: {result}")
    save_to_csv([result])
