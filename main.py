import tkinter as tk
from gui.application import TrafficVehicleCounter

def main():
    '''Main function to run the Traffic Vehicle Counter application.'''
    root = tk.Tk()
    application = TrafficVehicleCounter(root)
    root.protocol("WM_DELETE_WINDOW", application.close_application)
    root.mainloop()

if __name__ == "__main__":
    main()