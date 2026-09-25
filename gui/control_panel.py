import tkinter as tk
from tkinter import ttk


class ControlPanel:

    def __init__(self, parent, callbacks):

        self.parent = parent
        self.callbacks = callbacks

        self.frame = tk.Frame(
            parent,
            bg="#1f2937",
            height=80
        )

        self.frame.pack(fill="x")

        self.create_controls()

    def create_controls(self):

        self.create_button(
            "Open Video",
            self.callbacks["open"],
            0
        )

        self.create_button(
            "◀ Frame",
            self.callbacks["previous_frame"],
            1
        )

        self.create_button(
            "◀◀",
            self.callbacks["rewind"],
            2
        )

        self.create_button(
            "▶ Play",
            self.callbacks["play"],
            3
        )

        self.create_button(
            "⏸ Pause",
            self.callbacks["pause"],
            4
        )

        self.create_button(
            "▶▶",
            self.callbacks["fast_forward"],
            5
        )

        self.create_button(
            "Frame ▶",
            self.callbacks["next_frame"],
            6
        )

        self.create_button(
            "🔍+",
            self.callbacks["zoom_in"],
            7
        )

        self.create_button(
            "🔍-",
            self.callbacks["zoom_out"],
            8
        )

        self.create_button(
            "100%",
            self.callbacks["reset_zoom"],
            9
        )

        # Speed
        ttk.Label(
            self.frame,
            text="Speed:"
        ).grid(
            row=0,
            column=10,
            padx=(20, 5)
        )

        self.speed_var = tk.StringVar(
            value="1.0x"
        )

        speed_box = ttk.Combobox(
            self.frame,
            textvariable=self.speed_var,
            values=[
                "0.25x",
                "0.5x",
                "1.0x",
                "1.5x",
                "2.0x",
                "4.0x",
                "8.0x"
            ],
            width=7,
            state="readonly"
        )

        speed_box.grid(
            row=0,
            column=11,
            padx=5
        )

        speed_box.bind(
            "<<ComboboxSelected>>",
            self.change_speed
        )

        # AI toggle
        self.ai_button = tk.Button(
            self.frame,
            text="AI: ON",
            command=self.toggle_ai,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=8
        )

        self.ai_button.grid(
            row=0,
            column=12,
            padx=10
        )

    def create_button(self, text, command, column):

        button = tk.Button(
            self.frame,
            text=text,
            command=command,
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            padx=8,
            pady=8
        )

        button.grid(
            row=0,
            column=column,
            padx=3,
            pady=15
        )

    def change_speed(self, event=None):

        value = self.speed_var.get()

        speed = float(
            value.replace("x", "")
        )

        self.callbacks["speed"](speed)

    def toggle_ai(self):

        self.callbacks["toggle_ai"]()