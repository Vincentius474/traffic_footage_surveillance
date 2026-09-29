import tkinter as tk
from tkinter import ttk

class VehicleTable:

    def __init__(self, parent, select_callback):
        ''' Initialize the vehicle table GUI component '''

        self.select_callback = select_callback
        self.frame = tk.Frame( parent, bg="#f8fafc")
        self.frame.pack(fill="both", expand=False)

        title = tk.Label(
            self.frame,
            text="DETECTED VEHICLES",
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 12, "bold")
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        columns = (
            "id",
            "type",
            "plate",
            "direction",
            "confidence",
            "timestamp"
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=7
        )

        headings = {
            "id": "ID",
            "type": "Type",
            "plate": "Plate",
            "direction": "Direction",
            "confidence": "Confidence",
            "timestamp": "Time"
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            # self.tree.column(column, width=60, stretch=False)

        self.tree.column("id", width=20)
        self.tree.column("type", width=50)
        self.tree.column("plate", width=50)
        self.tree.column("direction", width=50)
        self.tree.column("confidence", width=50)
        self.tree.column("timestamp", width=50)

        scrollbar = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=(0, 10)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=(0, 10)
        )

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.vehicle_data = {}

    def add_vehicle(self, vehicle):
        ''' Add or update a vehicle in the table '''

        vehicle_id = str(vehicle["id"])
        self.vehicle_data[vehicle_id] = vehicle

        values = (
            vehicle_id,
            vehicle.get("type", "-"),
            vehicle.get("plate", "UNKNOWN"),
            vehicle.get("direction", "-"),
            f"{vehicle.get('confidence', 0) * 100:.1f}%",
            vehicle.get("timestamp", "-")
        )

        if self.tree.exists(vehicle_id):
            self.tree.item(vehicle_id, values=values)
        else:
            self.tree.insert("", "end", iid=vehicle_id, values=values)

    def on_select(self, event=None):
        ''' Handle vehicle selection from the table '''

        selection = self.tree.selection()
        if not selection:
            return

        vehicle_id = selection[0]
        vehicle = self.vehicle_data.get(vehicle_id)
        if vehicle:
            self.select_callback(vehicle)

    def clear(self):
        ''' Clear the vehicle table and data '''
  
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.vehicle_data.clear()