import tkinter as tk
from tkinter import ttk
import win32print  # Only works on Windows systems


# Function to get the list of installed printers
def get_installed_printers():
    return [
        printer[2]
        for printer in win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
    ]


# Function to save the selected printer assignments
def save_printer_configuration(bar_printer, kitchen_printer, cashier_printer):
    print(f"Assigned Printer for Bar: {bar_printer.get()}")
    print(f"Assigned Printer for Kitchen: {kitchen_printer.get()}")
    print(f"Assigned Printer for Cashier: {cashier_printer.get()}")


def configure_printer():
    # Create a new window for printer configuration
    printer_window = tk.Toplevel()
    printer_window.title("Printer Configuration")
    printer_window.geometry("400x300")

    # Fetch the list of installed printers
    installed_printers = get_installed_printers()

    # Dropdown for Bar location
    tk.Label(printer_window, text="Select Printer for Bar:").pack(pady=10)
    bar_printer = tk.StringVar(printer_window)
    bar_dropdown = ttk.Combobox(
        printer_window,
        textvariable=bar_printer,
        values=installed_printers,
        state="readonly",
    )
    bar_dropdown.pack(pady=5)

    # Dropdown for Kitchen location
    tk.Label(printer_window, text="Select Printer for Kitchen:").pack(pady=10)
    kitchen_printer = tk.StringVar(printer_window)
    kitchen_dropdown = ttk.Combobox(
        printer_window,
        textvariable=kitchen_printer,
        values=installed_printers,
        state="readonly",
    )
    kitchen_dropdown.pack(pady=5)

    # Dropdown for Cashier location
    tk.Label(printer_window, text="Select Printer for Cashier:").pack(pady=10)
    cashier_printer = tk.StringVar(printer_window)
    cashier_dropdown = ttk.Combobox(
        printer_window,
        textvariable=cashier_printer,
        values=installed_printers,
        state="readonly",
    )
    cashier_dropdown.pack(pady=5)

    # Save button to save the configuration
    save_button = tk.Button(
        printer_window,
        text="Save Configuration",
        command=lambda: save_printer_configuration(
            bar_printer, kitchen_printer, cashier_printer
        ),
        bg="green",
        fg="white",
    )
    save_button.pack(pady=20)

    printer_window.mainloop()
