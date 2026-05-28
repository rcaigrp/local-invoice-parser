import pytest
from main import parse_invoice_text

def test_parse_invoice_basic():
    """Test basic parsing of invoice text."""
    text = "Vendor: Amazon Inc.\nDate: 2023-10-27\nAmount: 45.99"
    result = parse_invoice_text(text)
    assert result['vendor'] == "Amazon Inc."
    assert result['date'] == "2023-10-27"
    assert result['amount'] == "45.99"

def test_parse_invoice_missing_fields():
    """Test handling of incomplete invoice data."""
    text = "Vendor: Unknown Vendor"
    result = parse_invoice_text(text)
    assert result['vendor'] == "Unknown Vendor"
    assert result['date'] == "Unknown"
    assert result['amount'] == "0"

def test_save_to_csv():
    """Test CSV output capability."""
    data = [{'vendor': 'Test', 'date': '2023-01-01', 'amount': '10.00'}]
    save_to_csv(data)
    with open('invoices.csv', 'r') as f:
        content = f.read()
        assert 'Test' in content
