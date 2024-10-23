import tkinter as tk
from tkinter import messagebox
import mysql.connector


def open_currency_form():
    currency_window = tk.Toplevel()  # Create a new window (popup)
    currency_window.title("Add New Currency")
    currency_window.geometry("400x400")

    # Title
    label_title = tk.Label(currency_window, text="Add New Currency", font=("Arial", 16))
    label_title.pack(pady=10)

    # Form fields
    labels_and_entries = [
        ("Currency Name", None),
        ("Currency Code", None),
        ("Exchange Rate", None),
        ("Decimal Point", None),
    ]

    entries = {}

    for label_text, var in labels_and_entries:
        label = tk.Label(currency_window, text=label_text)
        label.pack(pady=5)

        entry = tk.Entry(currency_window)
        entry.pack(pady=5)
        entries[label_text] = entry

    # Submit Button
    def submit_currency():
        # Collect the data from all entries
        currency_data = {key: entry.get() for key, entry in entries.items()}

        # Basic validation: ensure all fields are filled
        if all(currency_data.values()):
            try:
                # Connect to the database and insert the currency
                conn = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="localhost",
                    database="pos",
                    port="1207",
                )
                cursor = conn.cursor()

                # Insert the currency into the database
                insert_query = """
                INSERT INTO currencies (currency_name, currency_code, exchange_rate, decimal_point)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    insert_query,
                    (
                        currency_data["Currency Name"],
                        currency_data["Currency Code"],
                        float(currency_data["Exchange Rate"]),
                        int(currency_data["Decimal Point"]),
                    ),
                )
                conn.commit()  # Commit the transaction
                messagebox.showinfo("Success", "Currency added successfully!")

                # Clear the fields after successful submission
                for entry in entries.values():
                    entry.delete(0, tk.END)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()  # Close the database connection

            currency_window.destroy()  # Close the window after submission
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    btn_submit = tk.Button(currency_window, text="Submit", command=submit_currency)
    btn_submit.pack(pady=20)
