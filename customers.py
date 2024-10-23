import tkinter as tk
from tkinter import messagebox
import mysql.connector


def open_customer_form():
    customer_window = tk.Toplevel()  # Create a new window (popup)
    customer_window.title("Add New Customer")
    customer_window.geometry("400x400")

    # Title
    label_title = tk.Label(customer_window, text="Add New Customer", font=("Arial", 16))
    label_title.pack(pady=10)

    # Form fields
    labels_and_entries = [
        ("Customer Name", None),
        ("Contact Number", None),
        ("Email", None),
        ("Address", None),
    ]

    entries = {}

    for label_text, var in labels_and_entries:
        label = tk.Label(customer_window, text=label_text)
        label.pack(pady=5)

        entry = tk.Entry(customer_window)
        entry.pack(pady=5)
        entries[label_text] = entry

    # Submit Button
    def submit_customer():
        # Collect the data from all entries
        customer_data = {key: entry.get() for key, entry in entries.items()}

        # Basic validation: ensure all fields are filled
        if all(customer_data.values()):
            try:
                # Connect to the database and insert the customer
                conn = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="localhost",
                    database="pos",
                    port="1207",
                )
                cursor = conn.cursor()

                # Insert the customer into the database
                insert_query = """
                INSERT INTO customers (name, contact_number, email, address)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    insert_query,
                    (
                        customer_data["Customer Name"],
                        customer_data["Contact Number"],
                        customer_data["Email"],
                        customer_data["Address"],
                    ),
                )
                conn.commit()  # Commit the transaction
                messagebox.showinfo("Success", "Customer added successfully!")

                # Clear the fields after successful submission
                for entry in entries.values():
                    entry.delete(0, tk.END)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()  # Close the database connection

            customer_window.destroy()  # Close the window after submission
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    btn_submit = tk.Button(customer_window, text="Submit", command=submit_customer)
    btn_submit.pack(pady=20)
