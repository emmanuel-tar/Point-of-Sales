import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class PurchaseForm(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.pack(fill="both", expand=True)

        # Upper part
        upper_frame = tk.Frame(self, bg="lightgray")
        upper_frame.pack(fill="x")

        # Supplier
        supplier_label = tk.Label(upper_frame, text="Supplier:", bg="lightgray")
        supplier_label.pack(side="left", padx=5, pady=5)
        self.supplier_combobox = ttk.Combobox(upper_frame, width=30)
        self.supplier_combobox.pack(side="left", padx=5, pady=5)

        # Location
        location_label = tk.Label(upper_frame, text="Location:", bg="lightgray")
        location_label.pack(side="left", padx=5, pady=5)
        self.location_combobox = ttk.Combobox(upper_frame, width=30)
        self.location_combobox.pack(side="left", padx=5, pady=5)

        # Transaction type
        transaction_type_label = tk.Label(
            upper_frame, text="Transaction Type:", bg="lightgray"
        )
        transaction_type_label.pack(side="left", padx=5, pady=5)
        self.transaction_type_combobox = ttk.Combobox(upper_frame, width=30)
        self.transaction_type_combobox.pack(side="left", padx=5, pady=5)

        # Date of transaction
        date_of_transaction_label = tk.Label(upper_frame, text="Date:", bg="lightgray")
        date_of_transaction_label.pack(side="left", padx=5, pady=5)
        self.date_of_transaction_entry = tk.Entry(upper_frame, width=15)
        self.date_of_transaction_entry.pack(side="left", padx=5, pady=5)

        # Seller
        seller_label = tk.Label(upper_frame, text="Seller:", bg="lightgray")
        seller_label.pack(side="left", padx=5, pady=5)
        self.seller_combobox = ttk.Combobox(upper_frame, width=30)
        self.seller_combobox.pack(side="left", padx=5, pady=5)

        # Invoice number
        invoice_number_label = tk.Label(upper_frame, text="Invoice #:", bg="lightgray")
        invoice_number_label.pack(side="left", padx=5, pady=5)
        self.invoice_number_entry = tk.Entry(upper_frame, width=15)
        self.invoice_number_entry.pack(side="left", padx=5, pady=5)

        # Second part
        second_frame = tk.Frame(self)
        second_frame.pack(fill="both", expand=True)

        # Table headers
        headers = ["Item Code", "Item Description", "Cost Price", "Discount %", "Total"]
        self.tree = ttk.Treeview(
            second_frame, columns=headers, show="headings", height=15
        )
        self.tree.pack(fill="both", expand=True)

        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=200, anchor="center", stretch="no")

        # Menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="History/Preview", command=self.preview_history)
        file_menu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

    def new_file(self):
        messagebox.showinfo("File", "New File Clicked")

    def preview_history(self):
        messagebox.showinfo("File", "History/Preview Clicked")


def create_database_and_tables():
    # Connect to MySQL Server
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Replace with your MySQL username
            password="root",
            port="1207",
            database="POS"# Replace with your MySQL password
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS pos")
        cursor.execute("USE pos")

        # Create supplier table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Suppliers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL
            )
        """
        )

        # Create purchases table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Purchases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                supplier_id INT,
                location VARCHAR(255),
                transaction_type VARCHAR(50),
                date_of_transaction DATE,
                seller VARCHAR(255),
                invoice_number VARCHAR(50),
                FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
            )
        """
        )

        # Create purchase items table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PurchaseItems (
                id INT AUTO_INCREMENT PRIMARY KEY,
                purchase_id INT,
                item_code VARCHAR(50),
                item_description VARCHAR(255),
                cost_price DECIMAL(10, 2),
                discount_percentage DECIMAL(5, 2),
                total DECIMAL(10, 2),
                FOREIGN KEY (purchase_id) REFERENCES Purchases(id)
            )
        """
        )

        print("Database and tables created successfully!")
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    create_database_and_tables()
    root = tk.Tk()
    root.title("Purchase Form")
    PurchaseForm(root)
    #root.mainloop()
