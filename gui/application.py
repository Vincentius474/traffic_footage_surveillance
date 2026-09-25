import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

import time
import os
import cv2

from core.video_manager import VideoManager
from core.tracker import VehicleTracker
from gui.video_panel import VideoPanel
from gui.control_panel import ControlPanel
from gui.vehicle_panel import VehiclePanel
from gui.vehicle_table import VehicleTable


class TrafficVehicleCounter:

    def __init__(self, root):

        self.root = root
        self.root.title("TrafficVision - Traffic Footage Surveillance")
        self.root.geometry("1500x900")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#e5e7eb")

        # ------------------------------------------------
        # VIDEO
        # ------------------------------------------------

        self.video_manager = VideoManager()
        self.tracker = None
        self.detections = []
        self.detect_vehicles = True
        self.video_path = None
        self.running = False
        self.paused = True
        self.playback_speed = 1.0
        self.current_frame = None
        self.counting_line = 0.50
        self.selected_vehicle_id = None

        # ------------------------------------------------
        # HEADER
        # ------------------------------------------------
        self.create_header()

        # ------------------------------------------------
        # MAIN AREA
        # ------------------------------------------------

        self.main_area = tk.Frame(root, bg="#e5e7eb")
        self.main_area.pack(fill="both", expand=True)

        # Video area
        self.video_area = tk.Frame(
            self.main_area,
            bg="#111827"
        )

        self.video_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Inspector
        self.vehicle_panel = VehiclePanel(
            self.main_area
        )

        # ------------------------------------------------
        # VIDEO PANEL
        # ------------------------------------------------

        self.video_panel = VideoPanel(
            self.video_area
        )

        # ------------------------------------------------
        # CONTROLS
        # ------------------------------------------------

        callbacks = {

            "open": self.open_video,

            "previous_frame":
                self.previous_frame,

            "rewind":
                self.rewind,

            "play":
                self.play_video,

            "pause":
                self.pause_video,

            "fast_forward":
                self.fast_forward,

            "next_frame":
                self.next_frame,

            "zoom_in":
                self.video_panel.zoom_in,

            "zoom_out":
                self.video_panel.zoom_out,

            "reset_zoom":
                self.video_panel.reset_zoom,

            "speed":
                self.set_playback_speed,

            "toggle_ai":
                self.toggle_ai_detection,
        }

        self.controls = ControlPanel(
            self.video_area,
            callbacks
        )

        # self.control_panel = ControlPanel(
        #     controls_area,
        #     callbacks
        # )

        # ------------------------------------------------
        # TIMELINE
        # ------------------------------------------------

        self.create_timeline()

        # ------------------------------------------------
        # VEHICLE TABLE
        # ------------------------------------------------

        self.vehicle_table = VehicleTable(
            root,
            self.select_vehicle
        )

        # ------------------------------------------------
        # STATUS BAR
        # ------------------------------------------------

        self.create_status_bar()

        # ------------------------------------------------
        # KEYBOARD SHORTCUTS
        # ------------------------------------------------

        self.root.bind(
            "<space>",
            lambda event:
                self.toggle_play_pause()
        )

        self.root.bind(
            "<Left>",
            lambda event:
                self.previous_frame()
        )

        self.root.bind(
            "<Right>",
            lambda event:
                self.next_frame()
        )

        self.root.bind(
            "<Control-o>",
            lambda event:
                self.open_video()
        )

    # ====================================================
    # HEADER
    # ====================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#111827",
            height=65
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="TRAFFICVISION",
            bg="#111827",
            fg="white",
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        )

        title.pack(
            side="left",
            padx=25,
            pady=15
        )

        subtitle = tk.Label(
            header,
            text="Traffic Footage Surveillance & Inspection",
            bg="#111827",
            fg="#9ca3af",
            font=(
                "Segoe UI",
                10
            )
        )

        subtitle.pack(
            side="left",
            pady=18
        )

    # ====================================================
    # TIMELINE
    # ====================================================

    def create_timeline(self):

        self.timeline_frame = tk.Frame(
            self.video_area,
            bg="#1f2937"
        )

        self.timeline_frame.pack(
            fill="x"
        )

        self.current_time_label = tk.Label(
            self.timeline_frame,
            text="00:00:00",
            bg="#1f2937",
            fg="white"
        )

        self.current_time_label.pack(
            side="left",
            padx=10
        )

        self.timeline_var = tk.DoubleVar(
            value=0
        )

        self.timeline = ttk.Scale(
            self.timeline_frame,
            from_=0,
            to=100,
            variable=self.timeline_var,
            orient="horizontal",
            command=self.seek_from_slider
        )

        self.timeline.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        self.duration_label = tk.Label(
            self.timeline_frame,
            text="00:00:00",
            bg="#1f2937",
            fg="white"
        )

        self.duration_label.pack(
            side="right",
            padx=10
        )

    # ====================================================
    # STATUS BAR
    # ====================================================

    def create_status_bar(self):

        self.status_frame = tk.Frame(
            self.root,
            bg="#111827"
        )

        self.status_frame.pack(
            fill="x"
        )

        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            bg="#111827",
            fg="#d1d5db"
        )

        self.status_label.pack(
            side="left",
            padx=15,
            pady=8
        )

        self.video_info_label = tk.Label(
            self.status_frame,
            text="No video loaded",
            bg="#111827",
            fg="#9ca3af"
        )

        self.video_info_label.pack(
            side="right",
            padx=15
        )


    # OPEN VIDEO

    def open_video(self):

        path = filedialog.askopenfilename(

            title="Select Traffic Video",

            filetypes=[
                (
                    "Video Files",
                    "*.mp4 *.avi *.mov *.mkv *.wmv"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not path:

            return

        success = (
            self.video_manager.open(path)
        )

        if not success:

            messagebox.showerror(
                "Error",
                "Could not open the selected video."
            )

            return

        self.tracker = VehicleTracker(
                model_path="models/yolov8n.pt",
                confidence=0.5
            )

        self.video_path = path

        self.running = False

        self.paused = True

        self.timeline.configure(
            from_=0,
            to=max(
                self.video_manager.duration,
                1
            )
        )

        self.duration_label.config(
            text=self.format_time(
                self.video_manager.duration
            )
        )

        self.video_info_label.config(
            text=(
                f"{self.video_manager.width} × "
                f"{self.video_manager.height} | "
                f"{self.video_manager.fps:.1f} FPS"
            )
        )

        self.status_label.config(
            text=(
                f"Loaded: "
                f"{os.path.basename(path)}"
            )
        )

        # Display first frame
        success, frame = (
            self.video_manager.seek_frame(0)
        )

        if success:

            self.current_frame = frame

            self.video_panel.show_frame(
                frame
            )

        self.update_timeline()

    # ====================================================
    # PLAY
    # ====================================================

    def play_video(self):

        if self.video_manager.capture is None:

            return

        if self.running:

            return

        self.running = True

        self.paused = False

        self.status_label.config(
            text="Playing"
        )

        self.process_video()

    # ====================================================
    # PAUSE
    # ====================================================

    def pause_video(self):

        self.paused = True

        self.running = False

        self.status_label.config(
            text="Paused"
        )

    # ====================================================
    # TOGGLE
    # ====================================================

    def toggle_play_pause(self):

        if self.running:

            self.pause_video()

        else:

            self.play_video()

    # ====================================================
    # PROCESS VIDEO
    # ====================================================

    def process_video(self):

        if not self.running:
            return

        success, frame = self.video_manager.read()

        if not success:

            self.running = False

            self.status_label.config(
                text="End of video"
            )

            return

        self.current_frame = frame

        # -----------------------------------
        # YOLO VEHICLE DETECTION
        # -----------------------------------

        if (
            self.detect_vehicles
            and self.tracker is not None
        ):

            self.detections = self.tracker.track(
                frame
            )

            # Add newly detected vehicles
            for detection in self.detections:

                vehicle = {
                    "id": detection["id"],
                    "type": detection["type"],
                    "confidence": detection["confidence"],
                    "direction": "-",
                    "plate": "UNKNOWN",
                    "plate_confidence": 0.0,
                    "timestamp": self.video_manager.get_current_time()
                }

                self.vehicle_table.add_vehicle(
                    vehicle
                )

            # Draw detections
            frame = self.draw_detections(
                frame,
                self.detections
            )

        # -----------------------------------
        # COUNTING LINE
        # -----------------------------------

        frame = self.draw_counting_line(
            frame
        )

        # -----------------------------------
        # DISPLAY FRAME
        # -----------------------------------

        self.video_panel.show_frame(
            frame
        )

        # -----------------------------------
        # UPDATE TIMELINE
        # -----------------------------------

        self.update_timeline()

        # -----------------------------------
        # NEXT FRAME
        # -----------------------------------

        delay = int(
            (1000 / self.video_manager.fps)
            / self.playback_speed
        )

        delay = max(delay, 1)

        self.root.after(
            delay,
            self.process_video
        )

    # ====================================================
    # PREVIOUS FRAME
    # ====================================================

    def previous_frame(self):

        self.running = False

        success, frame = (
            self.video_manager.previous_frame()
        )

        if success:

            self.current_frame = frame

            self.video_panel.show_frame(
                frame
            )

            self.update_timeline()

    # ====================================================
    # NEXT FRAME
    # ====================================================

    def next_frame(self):

        self.running = False

        success, frame = (
            self.video_manager.next_frame()
        )

        if success:

            self.current_frame = frame

            self.video_panel.show_frame(
                frame
            )

            self.update_timeline()

    # ====================================================
    # REWIND
    # ====================================================

    def rewind(self):

        current = (
            self.video_manager.get_current_time()
        )

        target = max(
            0,
            current - 10
        )

        success, frame = (
            self.video_manager.seek_time(
                target
            )
        )

        if success:

            self.current_frame = frame

            self.video_panel.show_frame(
                frame
            )

            self.update_timeline()

    # ====================================================
    # FAST FORWARD
    # ====================================================

    def fast_forward(self):

        current = (
            self.video_manager.get_current_time()
        )

        target = min(
            self.video_manager.duration,
            current + 10
        )

        success, frame = (
            self.video_manager.seek_time(
                target
            )
        )

        if success:

            self.current_frame = frame

            self.video_panel.show_frame(
                frame
            )

            self.update_timeline()

    # ====================================================
    # PLAYBACK SPEED
    # ====================================================

    def set_playback_speed(
        self,
        speed
    ):

        self.playback_speed = speed

        self.status_label.config(
            text=f"Playback speed: {speed}x"
        )

    # ====================================================
    # TIMELINE
    # ====================================================

    def seek_from_slider(self, value):

        if self.video_manager.capture is None:

            return

        if self.running:

            return

        seconds = float(value)

        success, frame = (
            self.video_manager.seek_time(
                seconds
            )
        )

        if success:

            self.current_frame = frame

            self.video_panel.show_frame(
                frame
            )

            self.current_time_label.config(
                text=self.format_time(
                    seconds
                )
            )

    def update_timeline(self):

        current = (
            self.video_manager.get_current_time()
        )

        self.timeline_var.set(
            current
        )

        self.current_time_label.config(
            text=self.format_time(
                current
            )
        )

    # ====================================================
    # VEHICLE SELECTION
    # ====================================================

    def select_vehicle(
        self,
        vehicle
    ):

        self.selected_vehicle_id = (
            vehicle["id"]
        )

        self.vehicle_panel.update(
            vehicle
        )

        timestamp = vehicle.get(
            "timestamp"
        )

        if timestamp is not None:

            self.video_manager.seek_time(
                timestamp
            )

    def draw_detections(self, frame, detections):

        output = frame.copy()

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            vehicle_id = detection["id"]

            vehicle_type = detection["type"]

            confidence = detection["confidence"]

            # Highlight selected vehicle
            if vehicle_id == self.selected_vehicle_id:

                box_color = (255, 0, 255)
                thickness = 4

            else:

                box_color = (0, 255, 0)
                thickness = 2

            # Bounding box
            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                box_color,
                thickness
            )

            # Label
            label = (
                f"{vehicle_type} "
                f"ID:{vehicle_id} "
                f"{confidence:.2f}"
            )

            (
                text_width,
                text_height
            ), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                2
            )

            # Label background
            cv2.rectangle(
                output,
                (
                    x1,
                    max(
                        0,
                        y1 - text_height - 10
                    )
                ),
                (
                    x1 + text_width + 10,
                    y1
                ),
                box_color,
                -1
            )

            # Label text
            cv2.putText(
                output,
                label,
                (
                    x1 + 5,
                    max(
                        text_height + 2,
                        y1 - 5
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 0),
                2
            )

            # Center point
            center_x, center_y = detection["center"]

            cv2.circle(
                output,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

        return output

    def draw_counting_line(self, frame):

        height, width = (
            frame.shape[:2]
        )

        line_y = int(
            height *
            self.counting_line
        )

        cv2.line(

            frame,

            (0, line_y),

            (width, line_y),

            (0, 0, 255),

            2
        )

        cv2.putText(

            frame,

            "COUNTING LINE",

            (
                10,
                line_y - 10
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (0, 0, 255),

            2
        )

        return frame

    # ====================================================
    # TIME FORMAT
    # ====================================================

    @staticmethod
    def format_time(seconds):

        seconds = int(
            max(0, seconds)
        )

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        seconds = seconds % 60

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    # ====================================================
    # CLOSE
    # ====================================================

    def close_application(self):

        self.running = False

        self.video_manager.release()

        self.root.destroy()

    def toggle_ai_detection(self):

        self.detect_vehicles = not self.detect_vehicles

        state = "ON" if self.detect_vehicles else "OFF"

        self.status_label.config(
            text=f"Vehicle detection: {state}"
        )