from tkinter import Tk
from latency_monitor import LatencyMonitor

if __name__ == "__main__":
    root = Tk()
    monitor = LatencyMonitor(root, "www.google.com")  # Replace with desired target
    root.mainloop()
