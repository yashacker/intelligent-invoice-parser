def extract_model_name(ocr_data, model_master_list):
    """
    Exact match model name extraction from OCR text
    """
    texts = [d["text"].strip() for d in ocr_data]

    for text in texts:
        for model in model_master_list:
            if model.upper() in text.upper():
                return model, 0.9  # high confidence for exact match

    return None, 0.0
