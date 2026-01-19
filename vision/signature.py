import cv2
import numpy as np

def detect_signature(image_path):
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    roi = img[int(h*0.6):h, 0:int(w*0.5)]  # bottom-left
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        if 500 < area < 15000:
            return {
                "present": True,
                "bbox": [
                    x,
                    y + int(h*0.6),
                    x + cw,
                    y + ch + int(h*0.6)
                ]
            }

    return {"present": False, "bbox": None}
