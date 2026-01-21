from ultralytics import YOLO

_model = YOLO("runs/detect/train2/weights/best.pt")

def detect_stamp_signature(image_path):
    result = _model(image_path, conf=0.25, verbose=False)[0]

    output = {
        "signature": {"present": False, "bbox": None},
        "stamp": {"present": False, "bbox": None}
    }

    for box in result.boxes:
        cls = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if cls == 0:
            output["signature"] = {
                "present": True,
                "bbox": [x1, y1, x2, y2]
            }
        elif cls == 1:
            output["stamp"] = {
                "present": True,
                "bbox": [x1, y1, x2, y2]
            }

    return output
