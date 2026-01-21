import re

def normalize_ocr(text):
    """
    Normalize common OCR errors and clean text.
    """
    if text is None:
        return ""

    text = str(text).upper()

    # Common OCR confusions
    text = text.replace("O", "0")
    text = text.replace("S", "5")
    text = text.replace("I", "1")
    text = text.replace("B", "8")

    # Remove junk characters
    text = re.sub(r"[^A-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text
