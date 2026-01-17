import sys
import json
from src.ocr import run_ocr
from src.extract_hp_cost import extract_hp, extract_asset_cost
from src.extract_dealer import extract_dealer_name

def main(image_path):
    ocr_data = run_ocr(image_path)

    dealer, dealer_conf = extract_dealer_name(ocr_data)
    hp, hp_conf = extract_hp(ocr_data)
    cost, cost_conf = extract_asset_cost(ocr_data)

    output = {
        "fields": {
            "dealer_name": dealer,
            "horse_power": hp,
            "asset_cost": cost
        },
        "confidence": round(
            (dealer_conf + hp_conf + cost_conf) / 3, 2
        )
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
