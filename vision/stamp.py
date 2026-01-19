import cv2

def detect_stamp(image_path):
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    roi = img[int(h*0.6):h, int(w*0.5):w]  # bottom-right
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        if area > 2000:
            return {
                "present": True,
                "bbox": [
                    x + int(w*0.5),
                    y + int(h*0.6),
                    x + cw + int(w*0.5),
                    y + ch + int(h*0.6)
                ]
            }

    return {"present": False, "bbox": None}
