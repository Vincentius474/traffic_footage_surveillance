import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from core.detector import VehicleDetector


class TrafficVehicleCounter:

    def __init__(self, root):

        self.root = root
        self.root.title("Traffic Vehicle Counter")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        # Video variables
        self.video_path = None
        self.video = None
        self.running = False
        self.paused = False

        # Detection
        self.detector = None
        self.confidence = 0.5

        # Statistics
        self.counts = {
            "Car": 0,
            "Motorcycle": 0,
            "Bus": 0,
            "Truck": 0
        }

        self.setup_ui()

    # ---------------------------------------------------------
    # GUI
    # ---------------------------------------------------------

    def setup_ui(self):

        # Main title
        title = ttk.Label(
            self.root,
            text="TRAFFIC VEHICLE COUNTER",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=15)

        # Control frame
        control_frame = ttk.Frame(self.root)

        control_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Select video
        ttk.Button(
            control_frame,
            text="Select Video",
            command=self.select_video
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.video_label = ttk.Label(
            control_frame,
            text="No video selected"
        )

        self.video_label.grid(
            row=0,
            column=1,
            padx=10
        )

        # Confidence
        ttk.Label(
            control_frame,
            text="Confidence:"
        ).grid(
            row=0,
            column=2,
            padx=(20, 5)
        )

        self.confidence_var = tk.DoubleVar(
            value=0.5
        )

        self.confidence_scale = ttk.Scale(
            control_frame,
            from_=0.1,
            to=0.9,
            variable=self.confidence_var,
            orient="horizontal",
            length=150
        )

        self.confidence_scale.grid(
            row=0,
            column=3
        )

        self.confidence_value = ttk.Label(
            control_frame,
            text="0.50"
        )

        self.confidence_value.grid(
            row=0,
            column=4,
            padx=5
        )

        self.confidence_var.trace_add(
            "write",
            self.update_confidence_label
        )

        # Start
        ttk.Button(
            control_frame,
            text="Start",
            command=self.start_video
        ).grid(
            row=0,
            column=5,
            padx=5
        )

        # Pause
        ttk.Button(
            control_frame,
            text="Pause",
            command=self.pause_video
        ).grid(
            row=0,
            column=6,
            padx=5
        )

        # Stop
        ttk.Button(
            control_frame,
            text="Stop",
            command=self.stop_video
        ).grid(
            row=0,
            column=7,
            padx=5
        )

        # Main content
        content = ttk.Frame(self.root)

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Video panel
        video_frame = ttk.LabelFrame(
            content,
            text="Live Video"
        )

        video_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.video_display = ttk.Label(
            video_frame,
            text="Select a traffic video to begin",
            anchor="center"
        )

        self.video_display.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Statistics panel
        stats_frame = ttk.LabelFrame(
            content,
            text="Statistics",
            width=250
        )

        stats_frame.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        stats_frame.pack_propagate(False)

        self.stats_labels = {}

        for vehicle_type in self.counts:

            label = ttk.Label(
                stats_frame,
                text=f"{vehicle_type}: 0",
                font=("Arial", 14)
            )

            label.pack(
                anchor="w",
                padx=20,
                pady=10
            )

            self.stats_labels[vehicle_type] = label

        ttk.Separator(
            stats_frame,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.total_label = ttk.Label(
            stats_frame,
            text="Total: 0",
            font=("Arial", 16, "bold")
        )

        self.total_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        self.fps_label = ttk.Label(
            stats_frame,
            text="FPS: 0.0",
            font=("Arial", 14)
        )

        self.fps_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # Status
        self.status_label = ttk.Label(
            self.root,
            text="Ready",
            relief="sunken",
            anchor="w"
        )

        self.status_label.pack(
            fill="x",
            side="bottom"
        )

    # ---------------------------------------------------------
    # GUI actions
    # ---------------------------------------------------------

    def select_video(self):

        path = filedialog.askopenfilename(
            title="Select Traffic Video",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                ("MP4 Files", "*.mp4"),
                ("AVI Files", "*.avi"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        self.video_path = path

        self.video_label.config(
            text=path
        )

        self.status_label.config(
            text="Video selected"
        )

    def update_confidence_label(self, *args):

        value = self.confidence_var.get()

        self.confidence_value.config(
            text=f"{value:.2f}"
        )

    # ---------------------------------------------------------
    # Video processing
    # ---------------------------------------------------------

    def start_video(self):

        if not self.video_path:

            messagebox.showwarning(
                "No Video",
                "Please select a traffic video first."
            )

            return

        if self.running:
            return

        self.confidence = self.confidence_var.get()

        # Create detector
        self.detector = VehicleDetector(
            confidence=self.confidence
        )

        self.video = cv2.VideoCapture(
            self.video_path
        )

        if not self.video.isOpened():

            messagebox.showerror(
                "Error",
                "Could not open the selected video."
            )

            return

        self.running = True
        self.paused = False

        self.status_label.config(
            text="Processing video..."
        )

        self.process_video()

    def process_video(self):

        if not self.running:
            return

        if self.paused:

            self.root.after(
                100,
                self.process_video
            )

            return

        ret, frame = self.video.read()

        if not ret:

            self.stop_video()

            return

        # Detect vehicles
        detections = self.detector.detect(
            frame
        )

        # Draw detections
        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            vehicle_type = detection["type"]
            confidence = detection["confidence"]

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            label = (
                f"{vehicle_type} "
                f"{confidence:.2f}"
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        # Display frame
        self.display_frame(frame)

        # Continue processing
        self.root.after(
            1,
            self.process_video
        )

    def display_frame(self, frame):

        # Convert BGR → RGB
        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame)

        # Resize while maintaining aspect ratio
        image.thumbnail(
            (850, 600)
        )

        photo = ImageTk.PhotoImage(
            image=image
        )

        self.video_display.config(
            image=photo,
            text=""
        )

        self.video_display.image = photo

    # ---------------------------------------------------------
    # Controls
    # ---------------------------------------------------------

    def pause_video(self):

        if not self.running:
            return

        self.paused = True

        self.status_label.config(
            text="Video paused"
        )

    def stop_video(self):

        self.running = False
        self.paused = False

        if self.video:

            self.video.release()
            self.video = None

        self.status_label.config(
            text="Stopped"
        )

    # ---------------------------------------------------------
    # Application close
    # ---------------------------------------------------------

    def close_application(self):

        self.stop_video()

        self.root.destroy()