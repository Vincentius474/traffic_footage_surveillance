import tkinter as tk

from gui.application import TrafficVehicleCounter


def main():

    root = tk.Tk()

    application = TrafficVehicleCounter(
        root
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        application.close_application
    )

    root.mainloop()


if __name__ == "__main__":
    main()