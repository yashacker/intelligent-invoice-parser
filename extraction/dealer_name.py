import csv
import os
from rapidfuzz import fuzz

KEYWORDS = [
    "dealer",
    "m/s",
    "showroom",
    "authorized",
    "authorised",
    "tractors",
    "traders",
    "motors"
]
GOVT_KEYWORDS = [
    "government",
    "corporation",
    "undertaking",
    "agro industries",
    "department",
    "district office"
]


def extract_dealer_name(ocr_lines, dealer_master):
    full_text = " ".join(l["text"].lower() for l in ocr_lines)

    GOVT_KEYWORDS = [
        "government",
        "corporation",
        "undertaking",
        "agro",
        "industries",
        "department",
        "district office"
    ]

    # 🔥 CASE 1: Government / PSU document
    if any(k in full_text for k in GOVT_KEYWORDS):
        for line in ocr_lines[:8]:  # scan top lines only
            text = line["text"].strip()
            lower = text.lower()

            # ❌ reject phone numbers / mostly digits
            digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
            if digit_ratio > 0.3:
                continue

            # ❌ reject very short or noisy lines
            if len(text) < 12:
                continue

            # ✅ must contain alphabetic characters
            if not any(c.isalpha() for c in text):
                continue

            # ✅ prefer institutional keywords
            if any(k in lower for k in ["corporation", "industries", "department", "agro"]):
                return text.upper(), 0.9

        # fallback: first clean alphabetic line
        for line in ocr_lines[:8]:
            text = line["text"].strip()
            if len(text) > 12 and any(c.isalpha() for c in text):
                return text.upper(), 0.8

    # 🔹 CASE 2: Private dealer (existing fuzzy logic)
    candidates = []

    for line in ocr_lines:
        text = line["text"].strip()
        lower = text.lower()

        if any(k in lower for k in KEYWORDS) and len(text) > 8:
            candidates.append(text)

    if not candidates:
        for line in ocr_lines[:7]:
            if len(line["text"]) > 8:
                candidates.append(line["text"])

    best_match, best_score = None, 0

    for cand in candidates:
        for dealer in dealer_master:
            score = fuzz.token_set_ratio(cand.lower(), dealer.lower())
            if score > best_score:
                best_match, best_score = dealer, score

    if best_score >= 70:
        return best_match, best_score / 100

    return None, 0.0
