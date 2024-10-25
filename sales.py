import tkinter as tk
from tkinter import ttk, simpledialog
import mysql.connector


# Function to fetch items from the database
def fetch_items_from_db():
    conn = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        database="pos",
        port="1207",  # Update port if needed
    )
    cursor = conn.cursor()
    cursor.execute("SELECT item_description, price FROM items")
    items = cursor.fetchall()
    conn.close()
    return items


# Function to fetch customers from the database
def fetch_customers_from_db():
    conn = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        database="pos",
        port="1207",  # Update port if needed
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, email, contact_number FROM customers"
    )  # Removed the extra comma
    customers = cursor.fetchall()
    conn.close()
    return customers


# Function to open the Customer Selection Screen
def open_customer_selection(customer_label):
    customer_window = tk.Toplevel()
    customer_window.title("Select Customer")
    customer_window.geometry("500x400")

    # TreeView for displaying customers
    customer_tree = ttk.Treeview(
        customer_window, columns=("Name","email","Phone"), show="headings", height=15
    )
    #customer_tree.heading("ID", text="ID")
    customer_tree.heading("Name", text="Name")
    customer_tree.heading("Email", text="Email")
    customer_tree.heading("Phone", text="Phone Number" )
    customer_tree.pack(fill=tk.BOTH, expand=True)

    # Fetch customers and display in the TreeView
    customers = fetch_customers_from_db()
    for customer in customers:
        customer_tree.insert("", "end", values=(customer[0], customer[1], customer[2]))

    # Function to select customer and display on the main window
    def select_customer():
        selected = customer_tree.selection()
        if selected:
            customer_name = customer_tree.item(selected, "values")[1]
            customer_label.config(text=f"Customer: {customer_name}")
            customer_window.destroy()

    # Button to select customer
    select_button = tk.Button(customer_window, text="Select", command=select_customer)
    select_button.pack(pady=10)


# Function to open the Sales Screen
def open_sales_screen():
    sales_window = tk.Toplevel()
    sales_window.title("Sales Screen")
    sales_window.geometry("1000x600")

    left_frame = tk.Frame(sales_window)
    left_frame.pack(side="left", padx=10, pady=20)

    # TreeView for Order Items
    tree = ttk.Treeview(
        left_frame, columns=("Item", "Price"), show="headings", height=20
    )
    tree.heading("Item", text="Item")
    tree.heading("Price", text="Price")
    tree.pack()

    total_label = tk.Label(left_frame, text="Total: =N=0.00", font=("Arial", 14))
    total_label.pack(pady=10)

    # Label to display selected customer
    customer_label = tk.Label(left_frame, text="Customer: None", font=("Arial", 14))
    customer_label.pack(pady=10)

    total_price = 0

    def update_total_price():
        nonlocal total_price
        total_price = 0
        for row in tree.get_children():
            price_value = float(tree.item(row)["values"][1].strip("=N="))
            total_price += price_value
        total_label.config(text=f"Total: =N={total_price:.2f}")

    def add_to_order(item, price):
        tree.insert("", "end", values=(item, f"=N={price:.2f}"))
        update_total_price()

    right_frame = tk.Frame(sales_window)
    right_frame.pack(pady=20, padx=20, expand=True, fill="both")

    items = fetch_items_from_db()
    row, col = 0, 0
    for item, price in items:
        button = tk.Button(
            right_frame,
            text=f"{item}\n=N={price:.2f}",
            bg="lightgreen",
            font=("Arial", 12),
            width=20,
            height=5,
            command=lambda i=item, p=price: add_to_order(i, p),
        )
        button.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col == 5:
            row += 1
            col = 0

    bottom_frame = tk.Frame(sales_window)
    bottom_frame.pack(side="bottom", pady=20)

    operations = [
        ("Fire", "green"),
        ("Enter", "green"),
        ("Customers", "green"),
        ("Order", "green"),
        ("Back", "red"),
        ("Close", "red"),
    ]

    for operation, color in operations:
        if operation == "Customers":
            op_button = tk.Button(
                bottom_frame,
                text=operation,
                bg=color,
                font=("Arial", 12),
                width=10,
                height=2,
                command=lambda: open_customer_selection(customer_label),
            )
        else:
            op_button = tk.Button(
                bottom_frame,
                text=operation,
                bg=color,
                font=("Arial", 12),
                width=10,
                height=2,
            )
        op_button.pack(side="left", padx=10)

    additional_button_frame = tk.Frame(left_frame)
    additional_button_frame.pack(pady=20)

    def void_item():
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
            update_total_price()

    def delete_item():
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
            update_total_price()

    def change_price():
        selected_item = tree.selection()
        if selected_item:
            item_description = tree.item(selected_item, "values")[0]
            old_price = float(tree.item(selected_item, "values")[1].strip("=N="))
            new_price = simpledialog.askfloat(
                "Change Price",
                f"Enter new price for {item_description}:",
                initialvalue=old_price,
            )
            if new_price is not None:
                tree.item(
                    selected_item, values=(item_description, f"=N={new_price:.2f}")
                )
                update_total_price()

    tk.Button(additional_button_frame, text="Add", width=10).grid(
        row=0, column=0, padx=5
    )
    tk.Button(additional_button_frame, text="Del", width=10, command=delete_item).grid(
        row=0, column=1, padx=5
    )
    tk.Button(additional_button_frame, text="Void", width=10, command=void_item).grid(
        row=0, column=2, padx=5
    )
    tk.Button(
        additional_button_frame, text="Change Price", width=15, command=change_price
    ).grid(row=0, column=3, padx=5)

    sales_window.mainloop()


# Run the sales screen
# open_sales_screen()
