import re

def extract_horse_power(ocr_lines):
    for line in ocr_lines:
        text = line["text"]

        patterns = [
            r'(\d{2,3})\s*(HP|H\.P)',
            r'POWER\s*(\d{2,3})',
            r'ENGINE\s*POWER\s*(\d{2,3})',
            r'(\d{2,3})\s*HORSE'
        ]

        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                hp = int(match.group(1))
                if 15 <= hp <= 120:
                    return hp, 1.0

    return None, 0.0
