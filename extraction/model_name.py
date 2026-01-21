import os
from extraction.utils import normalize_ocr


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


def extract_model_name(ocr_lines, model_master):
    """
    Extract model name using normalized exact matching.
    Longest valid match wins.
    Conservative by design (no hallucination).
    """

    # Normalize full OCR text once
    full_text_norm = " ".join(
        normalize_ocr(line["text"]) for line in ocr_lines
    )

    best_model = None
    best_len = 0

    for model in model_master:
        model_norm = normalize_ocr(model)

        # Skip very short model names (noise protection)
        if len(model_norm) < 4:
            continue

        if model_norm in full_text_norm:
            if len(model_norm) > best_len:
                best_model = model
                best_len = len(model_norm)

    if best_model:
        return best_model, 0.9

    # Soft failure (model often missing in govt docs)
    return None, 0.2
