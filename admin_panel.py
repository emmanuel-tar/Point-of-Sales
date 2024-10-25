import tkinter as tk
from tkinter import messagebox
from items import open_item_form  # Import the open_item_form function
from employee_form import open_employee_form
from customers import open_customer_form
from currencies import open_currency_form
from sales import open_sales_screen


# Function to open admin panel after successful login
def open_admin_panel():
    admin_window = tk.Tk()  # Creates the admin panel window
    admin_window.title("Admin Panel")
    admin_window.geometry("600x400")  # Set window size

    # Create the menubar
    menubar = tk.Menu(admin_window)

    # Create a File menu with sub-options
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(
        label="New", command=lambda: messagebox.showinfo("File", "New File Clicked")
    )
    file_menu.add_command(
        label="Open", command=lambda: messagebox.showinfo("File", "Open File Clicked")
    )
    file_menu.add_command(
        label="Save", command=lambda: messagebox.showinfo("File", "Save File Clicked")
    )
    file_menu.add_command(
        label="Preview Older Sales", command=lambda:messagebox.showinfo("File", "Preview Older Sale Clicked")
    )
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=admin_window.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # Create an Employee  menu with Sub-menu
    employee_menu = tk.Menu(menubar, tearoff=0)
    employee_menu.add_command(
        label="Employee Setup",
        command=lambda: messagebox.showinfo("Employee Setup", "New File Clicked"),
    )
    employee_menu.add_command(
        label="Employee Roles", command=lambda: messagebox.showinfo("Employee Roles", "Open File Clicked")
    )

    employee_menu.add_command(
        label="Employee Configuration", command=lambda: messagebox.showinfo("Employee Configuration", "Save File Clicked")
    )

    employee_menu.add_separator()
    employee_menu.add_command(label="Exit", command=admin_window.quit)
    menubar.add_cascade(label="Employee", menu=employee_menu)

    # Create a Payment menu with sub-options
    payment_menu = tk.Menu(menubar, tearoff=0)
    payment_menu.add_command(
        label="Make Payment",
        command=lambda: messagebox.showinfo("Payment", "Make Payment Clicked"),
    )
    payment_menu.add_command(
        label="View Payment History",
        command=lambda: messagebox.showinfo("Payment", "Payment History Clicked"),
    )
    payment_menu.add_command(
        label="Currency",
        command=open_currency_form)

    menubar.add_cascade(label="Payment", menu=payment_menu)

    # Create a Setups menu with sub-options
    setups_menu = tk.Menu(menubar, tearoff=0)
    setups_menu.add_command(
        label="System Setup",
        command=lambda: messagebox.showinfo("Setups", "System Setup Clicked"),
    )
    setups_menu.add_command(
        label="POS Setup",
        command=lambda: messagebox.showinfo("Setups", "POS Setup Clicked"),
    )
    menubar.add_cascade(label="Setups", menu=setups_menu)

    # Configure the menubar
    admin_window.config(menu=menubar)

    # Title
    title_label = tk.Label(admin_window, text="Admin Panel", font=("Arial", 20))
    title_label.pack(pady=20)

    # Create a frame to hold the boxes in a grid layout
    frame = tk.Frame(admin_window)
    frame.pack(pady=20)

    # Create the buttons (boxes) and place them in a grid
    buttons = [
        ("Items", open_item_form),  # Link the Items button to open_item_form
        ("Customers", open_customer_form),
        ("Report", lambda: print("Report page")),
        ("Sales", open_sales_screen),
        ("Employees", open_employee_form),
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
        if col == 3:  # Wrap to the next row after 3 buttons
            row += 1
            col = 0

    admin_window.mainloop()  # Keep the admin window open
