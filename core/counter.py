class VehicleCounter:

    def __init__(self, line_position=0.50):

        self.line_position = line_position

        # Previous center positions
        self.previous_positions = {}

        # Vehicles already counted
        self.counted_ids = set()

        # Statistics
        self.counts = {
            "Car": {
                "ENTERING": 0,
                "EXITING": 0
            },

            "Motorcycle": {
                "ENTERING": 0,
                "EXITING": 0
            },

            "Bus": {
                "ENTERING": 0,
                "EXITING": 0
            },

            "Truck": {
                "ENTERING": 0,
                "EXITING": 0
            }
        }

    def set_line_position(self, position):

        self.line_position = position

    def process(self, detections, frame_height):

        line_y = int(
            frame_height * self.line_position
        )

        events = []

        for detection in detections:

            vehicle_id = detection["id"]
            vehicle_type = detection["type"]

            _, current_y = detection["center"]

            previous_y = self.previous_positions.get(
                vehicle_id
            )

            # Save current position
            self.previous_positions[
                vehicle_id
            ] = current_y

            # We need two positions
            if previous_y is None:
                continue

            # Already counted
            if vehicle_id in self.counted_ids:
                continue

            direction = None

            # -----------------------------------------
            # Vehicle moving DOWN
            # -----------------------------------------

            if (
                previous_y < line_y
                and current_y >= line_y
            ):
                direction = "ENTERING"

            # -----------------------------------------
            # Vehicle moving UP
            # -----------------------------------------

            elif (
                previous_y > line_y
                and current_y <= line_y
            ):
                direction = "EXITING"

            if direction:

                self.counts[
                    vehicle_type
                ][direction] += 1

                self.counted_ids.add(
                    vehicle_id
                )

                events.append({
                    "id": vehicle_id,
                    "type": vehicle_type,
                    "direction": direction
                })

        return events

    def get_counts(self):

        return self.counts

    def get_total(self):

        total = 0

        for vehicle_type in self.counts:

            total += (
                self.counts[vehicle_type]["ENTERING"]
                +
                self.counts[vehicle_type]["EXITING"]
            )

        return total

    def reset(self):

        self.previous_positions.clear()

        self.counted_ids.clear()

        for vehicle_type in self.counts:

            self.counts[
                vehicle_type
            ]["ENTERING"] = 0

            self.counts[
                vehicle_type
            ]["EXITING"] = 0