from ultralytics import YOLO

_model = YOLO("yolov8n.pt")


def detect_objects(frame):

    results = _model(frame, verbose=False)

    objects = []

    for r in results:
        for box in r.boxes:

            conf = float(box.conf[0])
            if conf < 0.5:
                continue

            cls_id = int(box.cls[0])
            name = _model.names[cls_id]

            objects.append({
                "name": name,
                "confidence": round(conf, 2)
            })

    objects.sort(key=lambda x: x["confidence"], reverse=True)

    return objects