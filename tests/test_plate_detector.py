import cv2

from core.plate_detector import PlateDetector


def main():

    detector = PlateDetector()

    image = cv2.imread("test_vehicle.jpg")

    if image is None:
        print("Could not load test_vehicle.jpg")
        return

    plates = detector.detect(image)

    print(f"Plates detected: {len(plates)}")

    for i, plate in enumerate(plates, start=1):

        x1, y1, x2, y2 = plate["bbox"]

        confidence = plate["confidence"]

        print(
            f"Plate {i}: "
            f"({x1}, {y1}, {x2}, {y2}) "
            f"confidence={confidence:.2f}"
        )

        plate_crop = image[y1:y2, x1:x2]

        if plate_crop.size > 0:

            filename = f"test_plate_{i}.jpg"

            cv2.imwrite(
                filename,
                plate_crop
            )

            print(f"Saved: {filename}")


if __name__ == "__main__":
    main()