import tkinter as tk

def create_buttons(frame, set_interval_callback):
    """Create buttons for time intervals and pack them into the given frame."""
    buttons = [
        ("1 min", lambda: set_interval_callback("1min")),
        ("5 min", lambda: set_interval_callback("5min")),
        ("10 min", lambda: set_interval_callback("10min")),
        ("30 min", lambda: set_interval_callback("30min")),
        ("Full", lambda: set_interval_callback("full")),
        ("Close", lambda: exit())  # Close application button
    ]

    for (text, command) in buttons:
        button = tk.Button(frame, text=text, command=command)
        button.pack(side=tk.TOP, padx=5, pady=5)

def create_zoom_fields(frame, set_zoom_callback):
    """Create text fields for zoom feature and pack them into the given frame."""
    tk.Label(frame, text="Upper range:").pack(side=tk.TOP, padx=5, pady=5)
    upper_entry = tk.Entry(frame)
    upper_entry.pack(side=tk.TOP, padx=5, pady=5)

    tk.Label(frame, text="Lower range:").pack(side=tk.TOP, padx=5, pady=5)
    lower_entry = tk.Entry(frame)
    lower_entry.pack(side=tk.TOP, padx=5, pady=5)

    # Trigger zoom range setting with entered values
    def apply_zoom():
        try:
            upper = float(upper_entry.get())
            lower = float(lower_entry.get())
        except ValueError:
            upper, lower = 0, 0  # Default zoom if invalid input
        set_zoom_callback(upper, lower)

    tk.Button(frame, text="Apply Zoom", command=apply_zoom).pack(side=tk.TOP, padx=5, pady=5)
