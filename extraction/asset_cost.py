import re
from extraction.utils import normalize_ocr

def extract_asset_cost(ocr_lines):
    values = []

    for l in ocr_lines:
        text = normalize_ocr(l["text"])
        nums = re.findall(r"\b\d{5,}\b", text)

        for n in nums:
            val = int(n)
            if val > 10000:
                values.append(val)

    if values:
        return max(values), 1.0

    return None, 0.0
