import json
import cv2
import os

PRED_PATH = "analysis/predictions.json"
IMG_DIR = "data/images"

OUT_IMG = "yolo_data/images/train"
OUT_LBL = "yolo_data/labels/train"

os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_LBL, exist_ok=True)

with open(PRED_PATH) as f:
    docs = json.load(f)["documents"]

for doc in docs:
    if doc is None:
        continue

    img_path = os.path.join(IMG_DIR, doc["doc_id"])
    img = cv2.imread(img_path)
    if img is None:
        continue

    h, w = img.shape[:2]
    labels = []

    # class ids
    # 0 = signature, 1 = stamp
    for cls, key in enumerate(["signature", "stamp"]):
        det = doc["fields"][key]
        if det["present"] and det["bbox"]:
            x1, y1, x2, y2 = det["bbox"]

            xc = ((x1 + x2) / 2) / w
            yc = ((y1 + y2) / 2) / h
            bw = (x2 - x1) / w
            bh = (y2 - y1) / h

            labels.append(
                f"{cls} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}"
            )

    if labels:
        cv2.imwrite(os.path.join(OUT_IMG, doc["doc_id"]), img)
        with open(
            os.path.join(
                OUT_LBL,
                doc["doc_id"].rsplit(".", 1)[0] + ".txt"
            ),
            "w"
        ) as f:
            f.write("\n".join(labels))

print("Pseudo-label generation complete.")
