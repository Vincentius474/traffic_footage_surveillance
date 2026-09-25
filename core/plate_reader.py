import cv2
import pytesseract


class PlateReader:

    def __init__(self):

        self.tesseract_available = True

    def read(self, plate_image):

        if plate_image is None:
            return "UNKNOWN", 0.0

        if plate_image.size == 0:
            return "UNKNOWN", 0.0

        try:

            gray = cv2.cvtColor(
                plate_image,
                cv2.COLOR_BGR2GRAY
            )

            # Increase plate size
            gray = cv2.resize(
                gray,
                None,
                fx=4,
                fy=4,
                interpolation=cv2.INTER_CUBIC
            )

            # Reduce noise
            gray = cv2.GaussianBlur(
                gray,
                (3, 3),
                0
            )

            # Threshold
            threshold = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

            text = pytesseract.image_to_string(
                threshold,
                config="--psm 7"
            )

            text = "".join(
                character
                for character in text
                if character.isalnum()
            )

            text = text.upper()

            if not text:

                return "UNKNOWN", 0.0

            return text, 1.0

        except Exception as error:

            print(
                f"OCR error: {error}"
            )

            return "UNKNOWN", 0.0