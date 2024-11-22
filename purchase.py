import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class PurchaseForm(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.pack(fill="both", expand=True)

        # Connect to database
        self.db_connection = self.connect_to_database()
        self.cursor = self.db_connection.cursor()

        # Upper part
        upper_frame = tk.Frame(self, bg="lightgray")
        upper_frame.pack(fill="x")

        # Supplier
        supplier_label = tk.Label(upper_frame, text="Supplier:", bg="lightgray")
        supplier_label.pack(side="left", padx=5, pady=5)
        self.supplier_combobox = ttk.Combobox(upper_frame, width=30, state="readonly")
        self.supplier_combobox.pack(side="left", padx=5, pady=5)
        self.populate_suppliers()

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
            self.tree.column(header, width=150, anchor="center", stretch=True)

        # Populate items
        self.populate_items()

        # Menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="History/Preview", command=self.preview_history)
        file_menu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

    def connect_to_database(self):
        """Establish a connection to the MySQL database."""
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",  # Replace with your MySQL username
                password="root",  # Replace with your MySQL password
                port="1207",
                database="POS",  # Replace with your database name
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error", f"Error connecting to database: {err}"
            )
            raise

    def fetch_suppliers(self):
        """Fetch supplier data from the database."""
        try:
            self.cursor.execute("SELECT id, name FROM suppliers")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching suppliers: {err}")
            return []

    def fetch_items(self):
        """Fetch item data from the database."""
        try:
            query = """
                SELECT item_code, item_description, cost_price, 0 AS discount_percent, cost_price AS total
                FROM items
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching items: {err}")
            return []

    def populate_suppliers(self):
        """Populate the supplier combobox."""
        suppliers = self.fetch_suppliers()
        if suppliers:
            self.supplier_combobox["values"] = [name for _, name in suppliers]

    def populate_items(self):
        """Populate the items in the treeview."""
        items = self.fetch_items()
        for item in items:
            self.tree.insert("", "end", values=item)

    def new_file(self):
        messagebox.showinfo("File", "New File Clicked")

    def preview_history(self):
        messagebox.showinfo("File", "History/Preview Clicked")

    def __del__(self):
        """Clean up database resources."""
        if self.db_connection.is_connected():
            self.cursor.close()
            self.db_connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Purchase Form")
    PurchaseForm(root)
    root.mainloop()
