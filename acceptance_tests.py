import pytest
import json
import os
import sys
from unittest.mock import patch

sys.path.insert(0, '/workspace')

# Mock the file reading so we don't need real files
def mock_open(filepath, mode='r', *args, **kwargs):
    # Mock file content based on filename
    mock_dict = {
        'valid_invoice.txt': 'Vendor: Acme Corp Date: 2023-01-15 Amount: 500.50',
        'missing_date.txt': 'Vendor: Cheap Co Amount: 25.00',
        'other.txt': 'Some random text not an invoice'
    }
    
    class MockFile:
        def __init__(self, content):
            self.content = content
        def read(self):
            return self.content
    
    # Simple mock to return text based on key
    filename = os.path.basename(filepath)
    
    if filename in mock_dict:
        return MockFile(mock_dict[filename])
    elif filename == 'missing_date.txt':
         return MockFile('Vendor: Cheap Co Amount: 25.00')
    else:
        raise FileNotFoundError(filepath)

# Patch open and sys.stdin to simulate file input
class InputMock:
    def __init__(self, data):
        self.data = data
    def read(self):
        return self.data

def test_parse_valid_invoice():
    """Test standard invoice parsing."""
    with patch('builtins.open', side_effect=mock_open):
        with patch('sys.stdin', InputMock('valid_invoice.txt')):
            # Import main after patching
            from main import main
            main()
    
    output = sys.stdout.getvalue().strip()
    data = json.loads(output)
    
    assert data['vendor'] == 'Acme Corp'
    assert data['date'] == '2023-01-15'
    assert float(data['amount']) == 500.50

def test_parse_missing_date():
    """Test invoice with missing date field."""
    with patch('builtins.open', side_effect=mock_open):
        with patch('sys.stdin', InputMock('missing_date.txt')):
            from main import main
            main()
    
    output = sys.stdout.getvalue().strip()
    data = json.loads(output)
    
    assert data['vendor'] == 'Cheap Co'
    # date should default to N/A
    assert data['date'] == 'N/A'
    assert float(data['amount']) == 25.00
