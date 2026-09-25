import os
import csv
from datetime import datetime


class CaptureManager:

    def __init__(self):

        self.vehicle_folder = "output/vehicles"
        self.plate_folder = "output/plates"
        self.report_folder = "output/reports"

        os.makedirs(self.vehicle_folder, exist_ok=True)
        os.makedirs(self.plate_folder, exist_ok=True)
        os.makedirs(self.report_folder, exist_ok=True)

        self.vehicle_counter = 0
        self.plate_counter = 0

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.events_file = os.path.join(
            self.report_folder,
            f"vehicle_events_{timestamp}.csv"
        )

        self.create_csv()

    def create_csv(self):

        with open(
            self.events_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "vehicle_id",
                "vehicle_type",
                "direction",
                "vehicle_confidence",
                "plate_detected",
                "plate_confidence",
                "plate_number",
                "ocr_confidence",
                "vehicle_image",
                "plate_image"
            ])

    def save_vehicle(self, vehicle_image, vehicle_type):

        self.vehicle_counter += 1

        filename = (
            f"vehicle_{self.vehicle_counter:05d}_"
            f"{vehicle_type.lower()}.jpg"
        )

        path = os.path.join(
            self.vehicle_folder,
            filename
        )

        return path, filename

    def save_plate(self, plate_image):

        self.plate_counter += 1

        filename = (
            f"plate_{self.plate_counter:05d}.jpg"
        )

        path = os.path.join(
            self.plate_folder,
            filename
        )

        return path, filename

    def save_event(
        self,
        vehicle_id,
        vehicle_type,
        direction,
        vehicle_confidence,
        plate_detected,
        plate_confidence,
        plate_number,
        ocr_confidence,
        vehicle_image,
        plate_image
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            self.events_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                vehicle_id,
                vehicle_type,
                direction,
                f"{vehicle_confidence:.2f}",
                plate_detected,
                f"{plate_confidence:.2f}",
                plate_number,
                f"{ocr_confidence:.2f}",
                vehicle_image,
                plate_image
            ])