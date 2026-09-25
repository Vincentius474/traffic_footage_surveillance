from ultralytics import YOLO


class PlateDetector:

    def __init__(
        self,
        model_path="../models/license_plate_model.pt",
        confidence=0.30
    ):

        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, vehicle_image):

        results = self.model.predict(
            source=vehicle_image,
            conf=self.confidence,
            verbose=False
        )

        plates = []

        if not results:
            return plates

        result = results[0]

        if result.boxes is None:
            return plates

        for box, confidence in zip(
            result.boxes.xyxy,
            result.boxes.conf
        ):

            x1, y1, x2, y2 = map(int, box)

            plates.append({
                "bbox": (x1, y1, x2, y2),
                "confidence": float(confidence)
            })

        return plates