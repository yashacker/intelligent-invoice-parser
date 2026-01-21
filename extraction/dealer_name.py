import csv
import os
from rapidfuzz import fuzz
from extraction.utils import normalize_ocr   # ✅ FIXED IMPORT

# Keywords for private dealers
KEYWORDS = [
    "DEALER",
    "M S",
    "SHOWROOM",
    "AUTHORIZED",
    "AUTHORISED",
    "TRACTORS",
    "TRADERS",
    "MOTORS"
]

# Keywords for government / PSU documents
GOVT_KEYWORDS = [
    "GOVERNMENT",
    "CORPORATION",
    "UNDERTAKING",
    "AGRO",
    "INDUSTRIES",
    "DEPARTMENT",
    "DISTRICT OFFICE"
]


def load_dealers(relative_path):
    """
    Load dealer master CSV safely
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(project_root, relative_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Dealer master file NOT FOUND at: {full_path}"
        )

    with open(full_path, newline="", encoding="utf-8") as f:
        return [row[0] for row in csv.reader(f) if row]


def extract_dealer_name(ocr_lines, dealer_master):
    # Normalize all OCR text ONCE
    norm_lines = [normalize_ocr(l["text"]) for l in ocr_lines]
    full_text = " ".join(norm_lines)

    # =========================================================
    # CASE 1: Government / PSU document
    # =========================================================
    if any(k in full_text for k in GOVT_KEYWORDS):
        for line in norm_lines[:8]:
            # reject numeric-heavy lines
            digit_ratio = sum(c.isdigit() for c in line) / max(len(line), 1)
            if digit_ratio > 0.3:
                continue

            if len(line) < 15:
                continue

            if any(k in line for k in ["CORPORATION", "INDUSTRIES", "DEPARTMENT", "AGRO"]):
                return line, 0.9

        # PSU fallback: longest clean uppercase line
        fallback = max(norm_lines[:8], key=len, default="")
        if len(fallback) > 15:
            return fallback, 0.8

    # =========================================================
    # CASE 2: Private dealer (keyword proximity + fuzzy match)
    # =========================================================
    candidates = []

    # Keyword proximity
    for i, line in enumerate(norm_lines):
        if any(k in line for k in ["DEALER", "M S", "SHOWROOM"]):
            for j in range(i - 2, i + 3):
                if 0 <= j < len(norm_lines) and len(norm_lines[j]) > 8:
                    candidates.append(norm_lines[j])

    # Keyword-based fallback
    if not candidates:
        for line in norm_lines[:7]:
            if any(k in line for k in KEYWORDS) and len(line) > 8:
                candidates.append(line)

    # Last-resort fallback
    if not candidates:
        candidates = [l for l in norm_lines[:6] if len(l) > 8]

    best_match, best_score = None, 0

    for cand in candidates:
        for dealer in dealer_master:
            score = fuzz.token_set_ratio(
                cand,
                normalize_ocr(dealer)
            )
            if score > best_score:
                best_match, best_score = dealer, score

    # Adaptive threshold
    if best_match and best_score >= 60:
        return best_match, round(best_score / 100, 2)

    # Soft failure
    return None, 0.3
