import os
import re

def load_models(relative_path):
    """
    Load model master list safely using absolute path
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(project_root, relative_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Model master file NOT FOUND at: {full_path}"
        )

    with open(full_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def normalize(text):
    """
    Normalize OCR text for exact (but OCR-tolerant) matching
    """
    text = text.upper()

    # Common OCR confusions
    text = text.replace("DL", "DI")
    text = text.replace("D1", "DI")

    text = re.sub(r'[^A-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_model_name(ocr_lines, model_master):
    """
    Exact match against model master.
    Longest match wins.
    """
    full_text = " ".join(line["text"] for line in ocr_lines)
    full_text_norm = normalize(full_text)

    best_model = None
    best_len = 0

    for model in model_master:
        model_norm = normalize(model)

        if model_norm in full_text_norm:
            if len(model_norm) > best_len:
                best_model = model
                best_len = len(model_norm)

    if best_model:
        return best_model, 1.0

    return None, 0.0
