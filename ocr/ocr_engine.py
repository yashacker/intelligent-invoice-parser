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


def run_ocr(image_path):
    img = preprocess(image_path)
    results = reader.readtext(img)

    return [{
        "text": text,
        "conf": conf,
        "bbox": bbox
    } for bbox, text, conf in results]

