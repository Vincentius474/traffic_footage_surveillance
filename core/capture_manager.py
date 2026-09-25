import csv
import os
from datetime import datetime
import cv2

class CaptureManager:

    def __init__(self, output_directory="output"):

        self.output_directory = output_directory

        self.vehicle_directory = os.path.join(
            output_directory,
            "vehicles"
        )

        self.plate_directory = os.path.join(
            output_directory,
            "plates"
        )

        self.frame_directory = os.path.join(
            output_directory,
            "frames"
        )

        self.report_directory = os.path.join(
            output_directory,
            "reports"
        )

        self.csv_file = os.path.join(
            self.report_directory,
            "traffic_events.csv"
        )

        self.create_directories()

        self.event_number = self.get_existing_event_count()

    # -----------------------------------------
    # CREATE DIRECTORIES
    # -----------------------------------------

    def create_directories(self):

        os.makedirs(
            self.vehicle_directory,
            exist_ok=True
        )

        os.makedirs(
            self.plate_directory,
            exist_ok=True
        )

        os.makedirs(
            self.frame_directory,
            exist_ok=True
        )

        os.makedirs(
            self.report_directory,
            exist_ok=True
        )

    # -----------------------------------------
    # EXISTING EVENTS
    # -----------------------------------------

    def get_existing_event_count(self):

        if not os.path.exists(self.csv_file):
            return 0

        try:

            with open(
                self.csv_file,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                rows = list(reader)

                if len(rows) <= 1:
                    return 0

                return len(rows) - 1

        except Exception:
            return 0

    # -----------------------------------------
    # CAPTURE VEHICLE
    # -----------------------------------------

    def capture_vehicle(
        self,
        vehicle_image,
        vehicle_id,
        vehicle_type,
        confidence,
        direction="UNKNOWN",
        plate_number="UNKNOWN",
        plate_confidence=0.0,
        plate_image=None
    ):

        self.event_number += 1

        timestamp = datetime.now()

        timestamp_string = timestamp.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        event_id = f"{self.event_number:05d}"

        # -------------------------------------
        # VEHICLE IMAGE
        # -------------------------------------

        vehicle_filename = (
            f"vehicle_{event_id}_"
            f"{vehicle_type.lower()}.jpg"
        )

        vehicle_path = os.path.join(
            self.vehicle_directory,
            vehicle_filename
        )

        cv2.imwrite(
            vehicle_path,
            vehicle_image
        )

        # -------------------------------------
        # PLATE IMAGE
        # -------------------------------------

        plate_filename = ""

        if plate_image is not None:

            plate_filename = (
                f"plate_{event_id}.jpg"
            )

            plate_path = os.path.join(
                self.plate_directory,
                plate_filename
            )

            cv2.imwrite(
                plate_path,
                plate_image
            )

        # -------------------------------------
        # CSV
        # -------------------------------------

        self.write_event(
            event_id=event_id,
            timestamp=timestamp_string,
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            direction=direction,
            confidence=confidence,
            plate_number=plate_number,
            plate_confidence=plate_confidence,
            vehicle_image=vehicle_filename,
            plate_image=plate_filename
        )

        return {
            "event_id": event_id,
            "timestamp": timestamp_string,
            "vehicle_id": vehicle_id,
            "vehicle_type": vehicle_type,
            "direction": direction,
            "confidence": confidence,
            "plate_number": plate_number,
            "plate_confidence": plate_confidence,
            "vehicle_image": vehicle_filename,
            "plate_image": plate_filename
        }

    # -----------------------------------------
    # WRITE CSV
    # -----------------------------------------

    def write_event(
        self,
        event_id,
        timestamp,
        vehicle_id,
        vehicle_type,
        direction,
        confidence,
        plate_number,
        plate_confidence,
        vehicle_image,
        plate_image
    ):

        file_exists = os.path.exists(
            self.csv_file
        )

        with open(
            self.csv_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "event_id",
                    "timestamp",
                    "vehicle_id",
                    "vehicle_type",
                    "direction",
                    "confidence",
                    "plate_number",
                    "plate_confidence",
                    "vehicle_image",
                    "plate_image"
                ])

            writer.writerow([
                event_id,
                timestamp,
                vehicle_id,
                vehicle_type,
                direction,
                f"{confidence:.4f}",
                plate_number,
                f"{plate_confidence:.4f}",
                vehicle_image,
                plate_image
            ])