def compute_confidence(scores):
    weights = {
        "dealer": 0.20,
        "model": 0.20,
        "hp": 0.15,
        "cost": 0.15,
        "signature": 0.15,
        "stamp": 0.15
    }

    # 🔥 Adjust logic for government documents
    if scores.get("govt_doc"):
        weights["model"] = 0.0
        weights["hp"] = 0.0

        # redistribute weight fairly
        weights["dealer"] += 0.15
        weights["cost"] += 0.10
        weights["signature"] += 0.05

    total = 0.0
    for k, w in weights.items():
        total += scores.get(k, 0.0) * w

    return round(min(total, 1.0), 2)

