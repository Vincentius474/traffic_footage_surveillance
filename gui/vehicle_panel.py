import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class VehiclePanel:

    def __init__(self, parent):
        ''' Initialize the vehicle inspector panel '''
        self.frame = tk.Frame(
            parent,
            bg="#f3f4f6",
            width=350
        )

        self.frame.pack(
            fill="y",
            side="right"
        )

        self.frame.pack_propagate(False)
        self.vehicle_photo = None
        self.plate_photo = None
        self.vehicle_img_width = 200
        self.plate_img_width = 100

        title = tk.Label(
            self.frame,
            text="VEHICLE INSPECTOR",
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 14, "bold")
        )

        title.pack(pady=(0, 15))

        ttk.Separator(self.frame).pack(
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
                pady=5
            )

            label = tk.Label(
                row,
                text=f"{field}:",
                bg="#f8fafc",
                fg="#475569",
                font=("Segoe UI", 9, "bold"),
                width=15,
                anchor="w"
            )

            label.pack(
                side="left"
            )

            value = tk.Label(
                row,
                text="-",
                bg="#f8fafc",
                fg="#111827",
                font=("Segoe UI", 9),
                anchor="w"
            )

            value.pack(
                side="left",
                fill="x",
                expand=True
            )

            self.details[field] = value

        ttk.Separator(self.frame).pack(
            fill="y",
            padx=15,
            pady=10
        )

        vehicle_title = tk.Label(
            self.frame,
            text="VEHICLE IMAGE",
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 10, "bold")
        )

        vehicle_title.pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )

        self.vehicle_image_label = tk.Label(
            self.frame,
            text="No vehicle image",
            bg="#e2e8f0",
            fg="#64748b",
            width=150,
            height=150
        )

        self.vehicle_image_label.pack(
            fill="x",
            padx=20
        )

        plate_title = tk.Label(
            self.frame,
            text="PLATE IMAGE",
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 10, "bold")
        )

        plate_title.pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        self.plate_image_label = tk.Label(
            self.frame,
            text="No plate image",
            bg="#e2e8f0",
            fg="#64748b",
            width=80,
            height=40
        )

        self.plate_image_label.pack(
            fill="x",
            padx=20
        )

        button_row = tk.Frame(
            self.frame,
            bg="#f8fafc"
        )

        button_row.pack(
            fill="x",
            padx=20,
            pady=(12, 0)
        )

        self.capture_button = tk.Button(
            button_row,
            text="📷 Capture Vehicle",
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        self.capture_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 4)
        )

        self.plate_button = tk.Button(
            button_row,
            text="🔢 Capture Plate",
            bg="#475569",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        self.plate_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0)
        )

    def update(self, vehicle):
        ''' Update the inspector with vehicle details and images '''

        if not vehicle:
            self.clear()
            return

        self.details["Vehicle ID"].config(
            text=str(vehicle.get("id", "-"))
        )

        self.details["Vehicle Type"].config(
            text=vehicle.get("type", "-")
        )

        self.details["Confidence"].config(
            text=f"{vehicle.get('confidence', 0) * 100:.1f}%"
        )

        self.details["Direction"].config(
            text=vehicle.get("direction", "-")
        )

        self.details["Plate"].config(
            text=vehicle.get("plate", "UNKNOWN")
        )

        self.details["Plate Confidence"].config(
            text=f"{vehicle.get('plate_confidence', 0) * 100:.1f}%"
        )

        self.details["Timestamp"].config(
            text=vehicle.get("timestamp", "-")
        )

        self.show_vehicle_image(
            vehicle.get("vehicle_image")
        )

        self.show_plate_image(
            vehicle.get("plate_image")
        )

    def _resize_to_width(self, image, target_width):
        ''' Resize an image to the target width, preserving aspect ratio. '''
        w, h = image.size
        if w == 0:
            return image
        scale = target_width / float(w)
        new_size = (int(w * scale), int(h * scale))
        return image.resize(new_size, Image.Resampling.LANCZOS)

    def show_vehicle_image(self, image_path):
        ''' Display the vehicle image in the inspector (full width) '''

        if not image_path:
            self.vehicle_image_label.config(
                image="",
                text="No vehicle image"
            )

            self.vehicle_photo = None
            return

        if not os.path.exists(image_path):
            self.vehicle_image_label.config(
                image="",
                text="Vehicle image unavailable"
            )

            self.vehicle_photo = None
            return

        try:

            image = Image.open(image_path)
            image = self._resize_to_width(image, self.vehicle_img_width)
            self.vehicle_photo = ImageTk.PhotoImage(image)
            self.vehicle_image_label.config(image=self.vehicle_photo, text="")

        except Exception:

            self.vehicle_image_label.config(image="", text="Unable to load image")
            self.vehicle_photo = None

    def show_plate_image(self, image_path):
        ''' Display the plate image in the inspector (full width) '''

        if not image_path:
            self.plate_image_label.config(image="", text="No plate image")
            self.plate_photo = None
            return

        if not os.path.exists(image_path):
            self.plate_image_label.config(image="", text="Plate image unavailable")
            self.plate_photo = None
            return

        try:

            image = Image.open(image_path)
            image = self._resize_to_width(image, self.plate_img_width)
            self.plate_photo = ImageTk.PhotoImage(image)
            self.plate_image_label.config(image=self.plate_photo, text="")

        except Exception:

            self.plate_image_label.config(image="", text="Unable to load image")
            self.plate_photo = None

    def clear(self):
        ''' Clear the inspector details and images '''

        for label in self.details.values():
            label.config(text="-")

        self.vehicle_image_label.config(image="", text="No vehicle image")
        self.plate_image_label.config(image="", text="No plate image")
        self.vehicle_photo = None
        self.plate_photo = None