import csv
import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from core.tracker import VehicleTracker
from core.counter import VehicleCounter


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
        self.tracker = None
        self.counter = VehicleCounter()
        self.confidence = 0.5

        # Statistics
        self.counts = {
            "Car": 0,
            "Motorcycle": 0,
            "Bus": 0,
            "Truck": 0
        }

        self.fps = 0.0
        self.previous_frame_time = time.time()
        self.output_video = None
        self.output_path = None

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

        ttk.Label(
            control_frame,
            text="Line:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=10
        )

        self.line_var = tk.DoubleVar(
            value=0.50
        )

        self.line_scale = ttk.Scale(
            control_frame,
            from_=0.10,
            to=0.90,
            variable=self.line_var,
            orient="horizontal",
            length=200
        )

        self.line_scale.grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="w"
        )

        self.line_value = ttk.Label(
            control_frame,
            text="50%"
        )

        self.line_value.grid(
            row=1,
            column=3
        )

        self.line_var.trace_add(
            "write",
            self.update_line_label
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

        ttk.Button(
            control_frame,
            text="Reset",
            command=self.reset_application
        ).grid(
            row=0,
            column=8,
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

    def update_statistics(self):

        counts = self.counter.get_counts()

        total = self.counter.get_total()

        for vehicle_type in counts:

            entering = counts[
                vehicle_type
            ]["ENTERING"]

            exiting = counts[
                vehicle_type
            ]["EXITING"]

            total_type = (
                entering + exiting
            )

            self.stats_labels[
                vehicle_type
            ].config(
                text=(
                    f"{vehicle_type}: "
                    f"{total_type}\n"
                    f"  ↓ {entering} "
                    f"↑ {exiting}"
                )
            )

        self.total_label.config(
            text=f"Total: {total}"
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

        # Create tracker
        self.tracker = VehicleTracker(
            confidence=self.confidence
        )

        # Create counter
        self.counter = VehicleCounter(
            line_position=self.line_var.get()
        )

        # Open input video
        self.video = cv2.VideoCapture(
            self.video_path
        )

        if not self.video.isOpened():

            messagebox.showerror(
                "Error",
                "Could not open the selected video."
            )

            return

        # ---------------------------------------------
        # Video information
        # ---------------------------------------------

        width = int(
            self.video.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            self.video.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        fps = self.video.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:
            fps = 30.0

        # ---------------------------------------------
        # Output video
        # ---------------------------------------------



        os.makedirs(
            "output/videos",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.output_path = (
            f"output/videos/"
            f"traffic_processed_{timestamp}.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self.output_video = cv2.VideoWriter(
            self.output_path,
            fourcc,
            fps,
            (width, height)
        )

        # ---------------------------------------------
        # Start processing
        # ---------------------------------------------

        self.running = True
        self.paused = False

        self.previous_frame_time = time.time()

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

        # -------------------------------------------------
        # FPS
        # -------------------------------------------------

        current_time = time.time()

        elapsed = (
            current_time
            - self.previous_frame_time
        )

        if elapsed > 0:

            self.fps = 1 / elapsed

        self.previous_frame_time = current_time

        # -------------------------------------------------
        # Frame dimensions
        # -------------------------------------------------

        height, width = frame.shape[:2]

        # -------------------------------------------------
        # Track vehicles
        # -------------------------------------------------

        detections = self.tracker.track(
            frame
        )

        # -------------------------------------------------
        # Count vehicles
        # -------------------------------------------------

        events = self.counter.process(
            detections,
            height
        )

        # -------------------------------------------------
        # Counting line
        # -------------------------------------------------

        line_y = int(
            height * self.line_var.get()
        )

        cv2.line(
            frame,
            (0, line_y),
            (width, line_y),
            (0, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "COUNTING LINE",
            (20, line_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        # -------------------------------------------------
        # Draw vehicles
        # -------------------------------------------------

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            vehicle_id = detection["id"]

            vehicle_type = detection["type"]

            confidence = detection["confidence"]

            center_x, center_y = detection["center"]

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            # Center
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

            # Vehicle label
            label = (
                f"{vehicle_type} "
                f"ID:{vehicle_id} "
                f"{confidence:.2f}"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

        # -------------------------------------------------
        # Show counting events
        # -------------------------------------------------

        for event in events:

            print(
                f"{event['type']} "
                f"ID:{event['id']} "
                f"{event['direction']}"
            )

            self.status_label.config(
                text=(
                    f"{event['type']} "
                    f"ID:{event['id']} "
                    f"{event['direction']}"
                )
            )

        # -------------------------------------------------
        # FPS overlay
        # -------------------------------------------------

        cv2.putText(
            frame,
            f"FPS: {self.fps:.1f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # -------------------------------------------------
        # Total overlay
        # -------------------------------------------------

        total = self.counter.get_total()

        cv2.putText(
            frame,
            f"Vehicles: {total}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # -------------------------------------------------
        # Save annotated video
        # -------------------------------------------------

        if self.output_video:

            self.output_video.write(
                frame
            )

        # -------------------------------------------------
        # Update GUI
        # -------------------------------------------------

        self.update_statistics()

        self.fps_label.config(
            text=f"FPS: {self.fps:.1f}"
        )

        self.display_frame(frame)

        # -------------------------------------------------
        # Continue
        # -------------------------------------------------

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

    def update_line_label(self, *args):

        value = self.line_var.get()

        self.line_value.config(
            text=f"{value * 100:.0f}%"
        )

    # ---------------------------------------------------------
    # Controls
    # ---------------------------------------------------------
    
    def pause_video(self):

        if not self.running:
            return

        self.paused = not self.paused

        if self.paused:

            self.status_label.config(
                text="Video paused"
            )

        else:

            self.status_label.config(
                text="Video resumed"
            )

    def stop_video(self):

        self.running = False
        self.paused = False

        if self.video:

            self.video.release()

            self.video = None

        if self.output_video:

            self.output_video.release()

            self.output_video = None

        # Save CSV reports
        self.save_reports()

        self.status_label.config(
            text="Processing stopped"
        )

    # ---------------------------------------------
    # Summary report
    # ---------------------------------------------
    
    def save_reports(self):

        if not self.counter:
            return

        os.makedirs(
            "output/reports",
            exist_ok=True
        )

        from datetime import datetime

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        summary_path = (
            f"output/reports/"
            f"vehicle_summary_{timestamp}.csv"
        )

        with open(
            summary_path,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Vehicle Type",
                "Entering",
                "Exiting",
                "Total"
            ])

            counts = self.counter.get_counts()

            for vehicle_type in counts:

                entering = (
                    counts[vehicle_type]["ENTERING"]
                )

                exiting = (
                    counts[vehicle_type]["EXITING"]
                )

                writer.writerow([
                    vehicle_type,
                    entering,
                    exiting,
                    entering + exiting
                ])

            writer.writerow([])

            writer.writerow([
                "TOTAL",
                sum(
                    counts[v]["ENTERING"]
                    for v in counts
                ),
                sum(
                    counts[v]["EXITING"]
                    for v in counts
                ),
                self.counter.get_total()
            ])

        print(
            f"Summary report saved: "
            f"{summary_path}"
        )

    # ---------------------------------------------------------
    # Application close and reset
    # ---------------------------------------------------------

    def reset_application(self):

        self.stop_video()

        self.counter = VehicleCounter(
            line_position=self.line_var.get()
        )

        self.update_statistics()

        self.fps = 0.0

        self.fps_label.config(
            text="FPS: 0.0"
        )

        self.status_label.config(
            text="Reset"
        )

    def close_application(self):

        self.stop_video()

        self.root.destroy()