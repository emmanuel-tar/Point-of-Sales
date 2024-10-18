# admin_panel.py
import tkinter as tk
from tkinter import messagebox
from items import open_item_form  # Import the open_item_form function


# Function to open admin panel after successful login
def open_admin_panel():
    admin_window = tk.Tk()  # Creates the admin panel window
    admin_window.title("Admin Panel")
    admin_window.geometry("600x400")  # Set window size

    # Title
    title_label = tk.Label(admin_window, text="Admin Panel", font=("Arial", 20))
    title_label.pack(pady=20)

    # Create a frame to hold the boxes in a grid layout
    frame = tk.Frame(admin_window)
    frame.pack(pady=20)

    # Create the buttons (boxes) and place them in a grid
    buttons = [
        ("Items", open_item_form),  # Link the Items button to open_item_form
        ("Customers", lambda: print("Customers page")),
        ("Report", lambda: print("Report page")),
        ("Sales", lambda: print("Sales page")),
        ("Employees", lambda: print("Employees page")),
        ("Dashboard", lambda: print("Dashboard page")),
    ]

    row = 0
    col = 0

    for text, command in buttons:
        button = tk.Button(
            frame,
            text=text,
            command=command,
            font=("Arial", 14),
            width=15,
            height=5,
            bg="lightblue",
        )
        button.grid(row=row, column=col, padx=10, pady=10)

        col += 1
        if col == 3:  # Wrap to next row after 3 buttons
            row += 1
            col = 0

    admin_window.mainloop()  # Keep the admin window open
