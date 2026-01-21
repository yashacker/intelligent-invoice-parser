# ocr/ocr_engine.py
import easyocr
import cv2

reader = easyocr.Reader(['en', 'hi'], gpu=False)

def preprocess(image_path):
    img = cv2.imread(image_path)

    # ✅ RESIZE if too large
    h, w = img.shape[:2]
    if max(h, w) > 1800:
        scale = 1800 / max(h, w)
        img = cv2.resize(img, None, fx=scale, fy=scale)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    return gray


# ocr/ocr_engine.py
def run_ocr(image_path):
    img = cv2.imread(image_path)

    results = reader.readtext(img)

    structured = []
    for r in results:
        structured.append({
            "bbox": r[0],
            "text": r[1],
            "conf": r[2]
        })

    return structured

