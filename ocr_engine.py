import pytesseract
from PIL import Image

class InvoiceOCR:
    def __init__(self):
        # Ensure Tesseract is in PATH
        self.tesseract_cmd = r'/usr/bin/tesseract' # Assumes tesseract is installed in container

    def extract(self, file_path):
        """Extract text from image file using pytesseract."""
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, config='--psm 6')
        return text
