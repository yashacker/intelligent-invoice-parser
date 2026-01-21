import re
from extraction.utils import normalize_ocr

def extract_horse_power(ocr_lines):
    for l in ocr_lines:
        text = normalize_ocr(l["text"])
        match = re.search(r"\b(\d{2,3})\s*HP\b", text)

        if match:
            hp = int(match.group(1))
            if 10 <= hp <= 200:
                return hp, 0.9

    return None, 0.2
