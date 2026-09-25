import tkinter as tk
import cv2
from PIL import Image, ImageTk

class VideoPanel:

    def __init__(self, parent):

        self.parent = parent

        # Zoom level
        self.zoom = 1.0

        # Current original frame
        self.frame = None

        # Tkinter image reference
        self.photo = None

        # Pan position
        self.pan_x = 0
        self.pan_y = 0

        # Previous mouse position
        self.last_mouse_x = 0
        self.last_mouse_y = 0

        # --------------------------------------------------
        # FIXED VIDEO CONTAINER
        # --------------------------------------------------

        self.container = tk.Frame(
            parent,
            bg="#111827"
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        # --------------------------------------------------
        # CANVAS
        # --------------------------------------------------

        self.canvas = tk.Canvas(
            self.container,
            bg="#111827",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # --------------------------------------------------
        # MOUSE CONTROLS
        # --------------------------------------------------

        # Windows / Linux
        self.canvas.bind(
            "<MouseWheel>",
            self.mouse_wheel_zoom
        )

        # Linux mouse wheel
        self.canvas.bind(
            "<Button-4>",
            lambda event:
            self.zoom_in()
        )

        self.canvas.bind(
            "<Button-5>",
            lambda event:
            self.zoom_out()
        )

        # Mouse dragging
        self.canvas.bind(
            "<ButtonPress-1>",
            self.start_pan
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.pan
        )

        # --------------------------------------------------
        # RESIZE
        # --------------------------------------------------

        self.canvas.bind(
            "<Configure>",
            self.on_resize
        )

    # ======================================================
    # SHOW FRAME
    # ======================================================

    def show_frame(self, frame):

        if frame is None:

            return

        self.frame = frame.copy()

        self.render()

    # ======================================================
    # RENDER
    # ======================================================

    def render(self):

        if self.frame is None:

            return

        frame = self.frame

        # --------------------------------------------------
        # Convert OpenCV BGR → RGB
        # --------------------------------------------------

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(
            rgb
        )

        # --------------------------------------------------
        # ORIGINAL DIMENSIONS
        # --------------------------------------------------

        original_width = image.width
        original_height = image.height

        # --------------------------------------------------
        # DISPLAY DIMENSIONS
        # --------------------------------------------------

        canvas_width = (
            self.canvas.winfo_width()
        )

        canvas_height = (
            self.canvas.winfo_height()
        )

        if canvas_width <= 1:
            canvas_width = 800

        if canvas_height <= 1:
            canvas_height = 500

        # --------------------------------------------------
        # FIT IMAGE TO VIEWPORT AT 100%
        # --------------------------------------------------

        if self.zoom == 1.0:

            scale_x = (
                canvas_width /
                original_width
            )

            scale_y = (
                canvas_height /
                original_height
            )

            scale = min(
                scale_x,
                scale_y
            )

        else:

            # At zoom > 1, use the normal
            # fit scale multiplied by zoom.

            scale_x = (
                canvas_width /
                original_width
            )

            scale_y = (
                canvas_height /
                original_height
            )

            base_scale = min(
                scale_x,
                scale_y
            )

            scale = (
                base_scale *
                self.zoom
            )

        new_width = max(
            1,
            int(original_width * scale)
        )

        new_height = max(
            1,
            int(original_height * scale)
        )

        # --------------------------------------------------
        # RESIZE
        # --------------------------------------------------

        image = image.resize(
            (
                new_width,
                new_height
            ),
            Image.Resampling.LANCZOS
        )

        self.photo = ImageTk.PhotoImage(
            image
        )

        # --------------------------------------------------
        # CLEAR CANVAS
        # --------------------------------------------------

        self.canvas.delete(
            "all"
        )

        # --------------------------------------------------
        # CENTER IMAGE WHEN POSSIBLE
        # --------------------------------------------------

        if new_width <= canvas_width:

            x = (
                canvas_width -
                new_width
            ) // 2

        else:

            x = (
                canvas_width -
                new_width
            ) // 2 + self.pan_x

        if new_height <= canvas_height:

            y = (
                canvas_height -
                new_height
            ) // 2

        else:

            y = (
                canvas_height -
                new_height
            ) // 2 + self.pan_y

        # --------------------------------------------------
        # DRAW IMAGE
        # --------------------------------------------------

        self.canvas.create_image(
            x,
            y,
            anchor="nw",
            image=self.photo
        )

        # --------------------------------------------------
        # KEEP PAN WITHIN LIMITS
        # --------------------------------------------------

        self.limit_pan(
            new_width,
            new_height,
            canvas_width,
            canvas_height
        )

    # ======================================================
    # ZOOM IN
    # ======================================================

    def zoom_in(self):

        old_zoom = self.zoom

        self.zoom = min(
            self.zoom + 0.25,
            5.0
        )

        if self.zoom != old_zoom:

            self.render()

    # ======================================================
    # ZOOM OUT
    # ======================================================

    def zoom_out(self):

        old_zoom = self.zoom

        self.zoom = max(
            self.zoom - 0.25,
            1.0
        )

        if self.zoom != old_zoom:

            # Reset pan when returning
            # to normal view.

            if self.zoom == 1.0:

                self.pan_x = 0
                self.pan_y = 0

            self.render()

    # ======================================================
    # RESET ZOOM
    # ======================================================

    def reset_zoom(self):

        self.zoom = 1.0

        self.pan_x = 0
        self.pan_y = 0

        self.render()

    # ======================================================
    # MOUSE WHEEL
    # ======================================================

    def mouse_wheel_zoom(
        self,
        event
    ):

        if event.delta > 0:

            self.zoom_in()

        else:

            self.zoom_out()

    # ======================================================
    # START PAN
    # ======================================================

    def start_pan(
        self,
        event
    ):

        self.last_mouse_x = (
            event.x
        )

        self.last_mouse_y = (
            event.y
        )

    # ======================================================
    # PAN
    # ======================================================

    def pan(
        self,
        event
    ):

        if self.zoom <= 1.0:

            return

        dx = (
            event.x -
            self.last_mouse_x
        )

        dy = (
            event.y -
            self.last_mouse_y
        )

        self.pan_x += dx
        self.pan_y += dy

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

        self.render()

    # ======================================================
    # LIMIT PAN
    # ======================================================

    def limit_pan(
        self,
        image_width,
        image_height,
        canvas_width,
        canvas_height
    ):

        if image_width <= canvas_width:

            self.pan_x = 0

        else:

            max_x = (
                image_width -
                canvas_width
            ) // 2

            self.pan_x = max(
                -max_x,
                min(
                    self.pan_x,
                    max_x
                )
            )

        if image_height <= canvas_height:

            self.pan_y = 0

        else:

            max_y = (
                image_height -
                canvas_height
            ) // 2

            self.pan_y = max(
                -max_y,
                min(
                    self.pan_y,
                    max_y
                )
            )

    # ======================================================
    # RESIZE
    # ======================================================

    def on_resize(
        self,
        event
    ):

        if self.frame is not None:

            self.render()