import pyparsing
from typing import Dict, Optional

def parse_invoice(text: str) -> Dict[str, Optional[str]]:
    """
    Uses pyparsing to extract Vendor, Date, and Amount from invoice text.
    """
    result = {"vendor": None, "date": None, "amount": None}
    
    # Define patterns using pyparsing
    # Vendor: Word followed by Word (e.g., Amazon Inc)
    vendor = pyparsing.Word(pyparsing.alphas).setResultsName("vendor")
    vendor_name = vendor + pyparsing.Word(pyparsing.alphas).setResultsName("vendor2")
    vendor_pattern = vendor_name.setResultsName("vendor_full")
    
    # Date: YYYY-MM-DD
    date = pyparsing.numeric.pairs.setResultsName("date")
    
    # Amount: Decimal number
    amount = pyparsing.numeric.numeric.setResultsName("amount")
    
    # Look for patterns in text
    # Vendor
    for match in vendor_pattern.scanString(text):
        result["vendor"] = match[0].vendor_full
    
    # Date
    for match in date.scanString(text):
        result["date"] = match[0].date
    
    # Amount
    for match in amount.scanString(text):
        result["amount"] = match[0].amount
    
    # Defaults
    if not result["date"]:
        result["date"] = "N/A"
    
    return result
