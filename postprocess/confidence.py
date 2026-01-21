def compute_confidence(scores):
    """
    Compute document-level confidence using field-level scores.
    scores must contain numeric values only.
    """

    # Base weights
    weights = {
        "dealer": 0.25,
        "model": 0.15,
        "hp": 0.10,
        "cost": 0.25,
        "signature": 0.15,
        "stamp": 0.10
    }

    # 🔹 Government documents: model & hp are optional
    if scores.get("govt_doc"):
        weights["model"] = 0.0
        weights["hp"] = 0.0
        weights["dealer"] += 0.10
        weights["cost"] += 0.10

    # 🔹 If vision failed completely, soften penalty
    vision_sum = scores.get("signature", 0.0) + scores.get("stamp", 0.0)
    if vision_sum == 0.0:
        weights["signature"] = 0.05
        weights["stamp"] = 0.05
        weights["dealer"] += 0.05
        weights["cost"] += 0.05

    # Normalize weights (important safety)
    total_weight = sum(weights.values())
    for k in weights:
        weights[k] /= total_weight

    # Final confidence
    confidence = 0.0
    for field, weight in weights.items():
        confidence += scores.get(field, 0.0) * weight

    return round(min(confidence, 1.0), 2)
