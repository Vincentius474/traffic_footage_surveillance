from ultralytics import YOLO

class VehicleTracker:

    VEHICLE_CLASSES = {
        2: "Car",
        3: "Motorcycle",
        5: "Bus",
        7: "Truck"
    }

    def __init__(self, model_path="../models/yolov8n.pt", confidence=0.5):

        self.model = YOLO(model_path)
        self.confidence = confidence

    def track(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            conf=self.confidence,
            classes=list(self.VEHICLE_CLASSES.keys()),
            verbose=False
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        # Tracking IDs are not available yet
        if result.boxes.id is None:
            return detections

        boxes = result.boxes

        for box, track_id, class_id, confidence in zip(
            boxes.xyxy,
            boxes.id,
            boxes.cls,
            boxes.conf
        ):

            class_id = int(class_id)
            track_id = int(track_id)
            confidence = float(confidence)

            if class_id not in self.VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(
                int,
                box
            )

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            detections.append({
                "id": track_id,
                "type": self.VEHICLE_CLASSES[class_id],
                "confidence": confidence,
                "bbox": (x1, y1, x2, y2),
                "center": (center_x, center_y)
            })

        return detections