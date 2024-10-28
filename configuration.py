import tkinter as tk


# Function placeholders for each configuration button action
def configure_system_connection():
    print("Configure system connection settings")


def configure_printer():
    print("Configure printer settings")


def configure_label_design():
    print("Configure label design settings")


def configure_employee_roles():
    print("Configure employee roles settings")


def configure_font_size():
    print("Configure font size settings")


def configure_printer_receipt():
    print("Configure printer receipt design")


# Tkinter GUI for Configuration Page
def open_configuration_window():
    # Create a new top-level window for the configuration, so it doesn't interfere with the main Tk instance
    config_window = tk.Toplevel()
    config_window.title("Configuration Page")
    config_window.geometry("800x400")  # Adjust window size to fit horizontal layout

    # Frame to hold the buttons horizontally
    frame_buttons = tk.Frame(config_window)
    frame_buttons.pack(pady=20)

    # Button Configurations
    buttons = [
        ("System Connection", configure_system_connection),
        ("Printer Configuration", configure_printer),
        ("Label Design Settings", configure_label_design),
        ("Employee Role Configuration", configure_employee_roles),
        ("Font Size Setting", configure_font_size),
        ("Printer Receipt Design", configure_printer_receipt),
    ]

    # Create large square buttons arranged horizontally
    for text, command in buttons:
        button = tk.Button(
            frame_buttons,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            width=15,  # Square-like dimensions
            height=5,  # Square-like dimensions
            bg="darkblue",
            fg="white",
        )
        button.pack(side="left", padx=10)  # Arrange horizontally with padding


# This function can be imported and called in admin_panel.py
