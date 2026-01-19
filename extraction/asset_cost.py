import re

def extract_asset_cost(ocr_lines):
    """
    Strategy:
    - Collect all large numbers
    - Remove commas & spaces
    - Pick the largest valid amount
    """

    candidates = []

    for line in ocr_lines:
        cleaned = line["text"].replace(",", "").replace(" ", "")
        matches = re.findall(r'\d{5,7}', cleaned)

        for m in matches:
            val = int(m)
            if 50000 < val < 5000000:
                candidates.append(val)

    if candidates:
        return max(candidates), 1.0

    return None, 0.0
