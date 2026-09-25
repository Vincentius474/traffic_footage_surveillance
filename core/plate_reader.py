import re
import cv2
import easyocr

class PlateReader:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    def preprocess(self, plate_image):

        if plate_image is None:
            return None

        # Resize small plates
        height, width = plate_image.shape[:2]

        scale = 3

        resized = cv2.resize(
            plate_image,
            (
                width * scale,
                height * scale
            ),
            interpolation=cv2.INTER_CUBIC
        )

        # Convert to grayscale
        gray = cv2.cvtColor(
            resized,
            cv2.COLOR_BGR2GRAY
        )

        # Improve contrast
        gray = cv2.equalizeHist(
            gray
        )

        # Reduce noise
        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        return gray

    def clean_text(self, text):

        text = text.upper()

        # Remove spaces and special characters
        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text
        )

        return text

    def read(self, plate_image):

        if plate_image is None:
            return "UNKNOWN", 0.0

        processed = self.preprocess(
            plate_image
        )

        if processed is None:
            return "UNKNOWN", 0.0

        results = self.reader.readtext(
            processed
        )

        if not results:
            return "UNKNOWN", 0.0

        best_text = ""
        best_confidence = 0.0

        for _, text, confidence in results:

            cleaned = self.clean_text(
                text
            )

            if not cleaned:
                continue

            if confidence > best_confidence:

                best_text = cleaned
                best_confidence = float(
                    confidence
                )

        if not best_text:
            return "UNKNOWN", 0.0

        return (
            best_text,
            best_confidence
        )