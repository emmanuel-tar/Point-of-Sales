# payment.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector


# Payment Screen Function
def open_payment_screen(total_amount):
    payment_window = tk.Toplevel()
    payment_window.title("Payment Screen")
    payment_window.geometry("500x400")

    # Display total amount
    total_label = tk.Label(
        payment_window, text=f"Total: =N={total_amount:.2f}", font=("Arial", 14)
    )
    total_label.pack(pady=10)

    # Discount by percentage
    def apply_discount_percentage():
        percent = simpledialog.askfloat("Discount", "Enter discount percentage:")
        if percent is not None:
            discount_amount = total_amount * (percent / 100)
            discounted_total = total_amount - discount_amount
            total_label.config(text=f"Total after discount: =N={discounted_total:.2f}")

    # Discount by amount
    def apply_discount_amount():
        discount_amount = simpledialog.askfloat("Discount", "Enter discount amount:")
        if discount_amount is not None:
            discounted_total = total_amount - discount_amount
            total_label.config(text=f"Total after discount: =N={discounted_total:.2f}")

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

    # Apply Discount Buttons
    tk.Button(
        payment_window, text="Discount by %", command=apply_discount_percentage
    ).pack(pady=5)
    tk.Button(
        payment_window, text="Discount by Amount", command=apply_discount_amount
    ).pack(pady=5)

    # Print or Close Transaction
    def print_bill():
        messagebox.showinfo("Print", "Printing bill...")

    def close_transaction():
        payment_type = payment_type_combobox.get()
        if not payment_type:
            messagebox.showwarning("Payment Type", "Please select a payment type.")
            return
        messagebox.showinfo("Transaction", "Transaction closed successfully!")
        payment_window.destroy()

    tk.Button(payment_window, text="Print Bill", command=print_bill).pack(pady=10)
    tk.Button(payment_window, text="Close Transaction", command=close_transaction).pack(
        pady=10
    )

    payment_window.mainloop()
