import tkinter as tk
from tkinter import ttk


class VehiclePanel:

    def __init__(self, parent):

        self.frame = tk.Frame(
            parent,
            bg="#f8fafc",
            width=300
        )

        self.frame.pack(
            fill="y",
            side="right"
        )

        self.frame.pack_propagate(False)

        title = tk.Label(
            self.frame,
            text="VEHICLE INSPECTOR",
            bg="#f8fafc",
            fg="#111827",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        title.pack(
            pady=(20, 15)
        )

        separator = ttk.Separator(
            self.frame
        )

        separator.pack(
            fill="x",
            padx=15
        )

        self.details = {}

        fields = [
            "Vehicle ID",
            "Vehicle Type",
            "Confidence",
            "Direction",
            "Plate",
            "Plate Confidence",
            "Timestamp"
        ]

        for field in fields:

            row = tk.Frame(
                self.frame,
                bg="#f8fafc"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=7
            )

            label = tk.Label(
                row,
                text=f"{field}:",
                bg="#f8fafc",
                fg="#475569",
                font=(
                    "Segoe UI",
                    10,
                    "bold"
                )
            )

            label.pack(
                anchor="w"
            )

            value = tk.Label(
                row,
                text="-",
                bg="#f8fafc",
                fg="#111827",
                font=(
                    "Segoe UI",
                    10
                )
            )

            value.pack(
                anchor="w"
            )

            self.details[field] = value

        ttk.Separator(
            self.frame
        ).pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.capture_button = tk.Button(
            self.frame,
            text="📷 Capture Vehicle",
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=10,
            pady=10
        )

        self.capture_button.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.plate_button = tk.Button(
            self.frame,
            text="🔢 Capture Plate",
            bg="#475569",
            fg="white",
            relief="flat",
            padx=10,
            pady=10
        )

        self.plate_button.pack(
            fill="x",
            padx=20,
            pady=5
        )

    def update(self, vehicle):

        if not vehicle:

            self.clear()

            return

        self.details[
            "Vehicle ID"
        ].config(
            text=str(
                vehicle.get("id", "-")
            )
        )

        self.details[
            "Vehicle Type"
        ].config(
            text=vehicle.get(
                "type",
                "-"
            )
        )

        self.details[
            "Confidence"
        ].config(
            text=f"{vehicle.get('confidence', 0) * 100:.1f}%"
        )

        self.details[
            "Direction"
        ].config(
            text=vehicle.get(
                "direction",
                "-"
            )
        )

        self.details[
            "Plate"
        ].config(
            text=vehicle.get(
                "plate",
                "UNKNOWN"
            )
        )

        self.details[
            "Plate Confidence"
        ].config(
            text=f"{vehicle.get('plate_confidence', 0) * 100:.1f}%"
        )

        self.details[
            "Timestamp"
        ].config(
            text=vehicle.get(
                "timestamp",
                "-"
            )
        )

    def clear(self):

        for label in self.details.values():

            label.config(
                text="-"
            )