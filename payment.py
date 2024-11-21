import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
from generate_invoice import InvoiceGenerator  # Import the InvoiceGenerator class

# Payment Screen Function
def open_payment_screen(total_amount, invoice_id):
    payment_window = tk.Toplevel()
    payment_window.title("Payment Screen")
    payment_window.geometry("500x400")

    # Display total amount
    final_total = total_amount  # Initialize final total with original total amount
    total_label = tk.Label(
        payment_window, text=f"Total: =N={final_total:.2f}", font=("Arial", 14)
    )
    total_label.pack(pady=10)

    # Discount by percentage
    def apply_discount_percentage():
        nonlocal final_total
        percent = simpledialog.askfloat("Discount", "Enter discount percentage:")
        if percent is not None:
            discount_amount = total_amount * (percent / 100)
            final_total = total_amount - discount_amount
            total_label.config(text=f"Total after discount: =N={final_total:.2f}")

    # Discount by amount
    def apply_discount_amount():
        nonlocal final_total
        discount_amount = simpledialog.askfloat("Discount", "Enter discount amount:")
        if discount_amount is not None:
            final_total = total_amount - discount_amount
            total_label.config(text=f"Total after discount: =N={final_total:.2f}")

    # Fetch payment types from database
    def fetch_payment_types():
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT type FROM payment_types")
        payment_types = [row[0] for row in cursor.fetchall()]
        conn.close()
        return payment_types

    # Payment type selection
    payment_type_label = tk.Label(payment_window, text="Select Payment Type:")
    payment_type_label.pack(pady=5)

    payment_types = fetch_payment_types()
    payment_type_combobox = ttk.Combobox(payment_window, values=payment_types)
    payment_type_combobox.pack(pady=5)

    # Submit payment and print invoice
    def submit_payment():
        selected_payment_type = payment_type_combobox.get()
        if not selected_payment_type:
            messagebox.showwarning("Warning", "Please select a payment type.")
            return

        # Generate and print the invoice with the final discounted amount
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "pos",
            "port": "1207",
        }
        invoice_generator = InvoiceGenerator(db_config, invoice_id, final_total)
        invoice_generator.generate_invoice("customer_invoice.pdf")
        messagebox.showinfo("Success", "Payment successful and invoice printed.")
        payment_window.destroy()  # Close the payment window

    # Apply Discount Buttons
    tk.Button(
        payment_window, text="Discount by %", command=apply_discount_percentage
    ).pack(pady=5)
    tk.Button(
        payment_window, text="Discount by Amount", command=apply_discount_amount
    ).pack(pady=5)

    # Submit Button
    tk.Button(payment_window, text="Submit Payment", command=submit_payment).pack(pady=20)

