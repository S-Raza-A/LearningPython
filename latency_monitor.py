import tkinter as tk
import threading
import time
import random  # Use an actual ping library like `ping3` for real pinging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
from gui_elements import create_buttons, create_zoom_fields
from ping3 import ping


class LatencyMonitor:
    def __init__(self, master, target):
        self.master = master
        self.target = target
        self.time_values = []
        self.latency_data = []
        self.selected_interval = 'full'  # Default to full graph
        self.upper_zoom = 0
        self.lower_zoom = 0

        # Graph setup
        self.graph_frame = tk.Frame(master)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.setup_graph()

        # Control frame for buttons and zoom
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Create time interval buttons and zoom feature
        create_buttons(self.control_frame, self.set_interval)
        create_zoom_fields(self.control_frame, self.set_zoom_range)

        # Start ping monitoring in a separate thread
        self.ping_thread = threading.Thread(target=self.start_monitoring, daemon=True)
        self.ping_thread.start()

    def setup_graph(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Network Latency Monitor")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Latency (ms)")

        # Embed the graph in the canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    from ping3 import ping

    def ping(self):
        """Perform a real ping to the target and return the latency."""
        try:
            latency = ping(self.target, unit='ms')  # Ping the target in milliseconds
            if latency is None:
                latency = 0  # Handle cases where the ping fails
            return latency
        except Exception as e:
            print(f"Ping failed: {e}")
            return 0  # Return 0 in case of a ping failure


    def start_monitoring(self):
        """Continuously ping the target and update the graph."""
        while True:
            latency = self.ping()  # Perform a ping
            current_time = datetime.now()  # Get current timestamp

            # Append the ping result and time
            self.latency_data.append(latency)
            self.time_values.append(current_time)

            # Keep the data size manageable (e.g., only last 100 points)
            if len(self.latency_data) > 100:
                self.latency_data.pop(0)
                self.time_values.pop(0)

            # Update the graph after each ping
            self.update_graph()

            # Ping every second
            time.sleep(1)

    def update_graph(self):
        # Clear the previous graph
        self.ax.clear()

        # Plot the latency data
        self.ax.plot(self.time_values, self.latency_data, label='Latency (ms)', color='blue')

        # Set the title and labels
        self.ax.set_title("Network Latency Monitor")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Latency (ms)")

        # Adjust x-axis formatting for hours and minutes only
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        # Handle grid based on selected time interval
        if self.selected_interval == '1min':
            self.ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))  # Every 10 sec
        elif self.selected_interval == '5min':
            self.ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))  # Every 1 min
        elif self.selected_interval == '10min':
            self.ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))  # Every 2 min
        elif self.selected_interval == '30min':
            self.ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))  # Every 5 min
        elif self.selected_interval == 'full':
            # For full graph, only show the initial time
            self.ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            self.ax.set_xticks([self.time_values[0]])

        # Handle zoom
        if self.upper_zoom == 0 and self.lower_zoom == 0:
            self.ax.set_ylim(auto=True)  # Default range
        else:
            self.ax.set_ylim([self.lower_zoom, self.upper_zoom])

        # Enable grid for better readability
        self.ax.grid(True)

        # Redraw the canvas to show the updated graph
        self.canvas.draw()

    def set_interval(self, interval):
        """Sets the current time interval for the graph display."""
        self.selected_interval = interval
        self.update_graph()  # Trigger an update when the interval is changed

    def set_zoom_range(self, upper, lower):
        """Set the Y-axis zoom range."""
        self.upper_zoom = upper
        self.lower_zoom = lower
        self.update_graph()

