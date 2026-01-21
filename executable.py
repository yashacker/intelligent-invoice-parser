import os, time, json
from ocr.ocr_engine import run_ocr
from extraction.dealer_name import extract_dealer_name, load_dealers
from extraction.model_name import extract_model_name, load_models
from extraction.horse_power import extract_horse_power
from extraction.asset_cost import extract_asset_cost
from postprocess.confidence import compute_confidence
from vision.signature import detect_signature
from vision.stamp import detect_stamp
from vision.yolo_detector import detect_stamp_signature



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "data", "images")


def process_image(image_path, dealers, models):
    try:
        ocr_lines = run_ocr(image_path)

        full_text = " ".join(l["text"].lower() for l in ocr_lines)
        is_govt_doc = any(k in full_text for k in [
            "government",
            "corporation",
            "undertaking",
            "agro industries",
            "district office"
        ])

        dealer, dealer_conf = extract_dealer_name(ocr_lines, dealers)
        model, model_conf = extract_model_name(ocr_lines, models)
        hp, hp_conf = extract_horse_power(ocr_lines)
        cost, cost_conf = extract_asset_cost(ocr_lines)

        # YOLO detection
        yolo_out = detect_stamp_signature(image_path)

        # fallback to heuristic if YOLO fails
        if not yolo_out["signature"]["present"]:
            yolo_out["signature"] = detect_signature(image_path)

        if not yolo_out["stamp"]["present"]:
            yolo_out["stamp"] = detect_stamp(image_path)

        signature = yolo_out["signature"]
        stamp = yolo_out["stamp"]


        scores = {
            "dealer": dealer_conf,
            "model": model_conf,
            "hp": hp_conf,
            "cost": cost_conf,
            "signature": 1.0 if signature["present"] else 0.0,
            "stamp": 1.0 if stamp["present"] else 0.0,
            "govt_doc": is_govt_doc
        }

        return {
            "doc_id": os.path.basename(image_path),
            "fields": {
                "dealer_name": dealer,
                "model_name": model,
                "horse_power": hp,
                "asset_cost": cost,
                "signature": signature,
                "stamp": stamp
            },
            "confidence": compute_confidence(scores)
        }

    except Exception as e:
        # 🔥 FAIL-SAFE (never return None)
        print(f"[ERROR] Failed to process {image_path}: {e}")

        return {
            "doc_id": os.path.basename(image_path),
            "fields": {
                "dealer_name": None,
                "model_name": None,
                "horse_power": None,
                "asset_cost": None,
                "signature": {"present": False, "bbox": None},
                "stamp": {"present": False, "bbox": None}
            },
            "confidence": 0.0,
            "error": str(e)
        }


def main():
    start = time.time()

    dealers = load_dealers("data/master/dealer_master.csv")
    models = load_models("data/master/model_master.txt")

    results = []
    if not os.listdir(INPUT_DIR):
        print("No images found in input directory.")
        return


    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(INPUT_DIR, file)

            result = process_image(path, dealers, models)
            results.append(result)

    output = {
        "processing_time_sec": round(time.time() - start, 2),
        "documents": results,
        "cost_estimate_usd": round(len(results) * 0.002, 4)
    }

    os.makedirs("analysis", exist_ok=True)
    with open("analysis/predictions.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Processed {len(results)} documents")


if __name__ == "__main__":
    main()
