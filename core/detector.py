from ultralytics import YOLO

class VehicleDetector:

    # COCO class IDs
    VEHICLE_CLASSES = {
        2: "Car",
        3: "Motorcycle",
        5: "Bus",
        7: "Truck"
    }

    def __init__(self, model_path="../model/yolov8n.pt", confidence=0.5):

        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):

        results = self.model(
            frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # Only keep vehicle classes
                if class_id not in self.VEHICLE_CLASSES:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                vehicle_type = self.VEHICLE_CLASSES[class_id]

                detections.append({
                    "class_id": class_id,
                    "type": vehicle_type,
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2)
                })

        return detections