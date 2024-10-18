import tkinter as tk
from tkinter import messagebox
import mysql.connector


def open_item_form():
    item_window = tk.Toplevel()  # Create a new window (popup)
    item_window.title("Add New Item")
    item_window.geometry("400x400")

    # Title
    label_title = tk.Label(item_window, text="Add New Item", font=("Arial", 16))
    label_title.pack(pady=10)

    # Form fields
    labels_and_entries = [
        ("Item Description", None),
        ("Kitchen Description", None),
        ("Price", None),
        ("Group", None),
        ("Printout Location", None),
    ]

    entries = {}

    for label_text, var in labels_and_entries:
        label = tk.Label(item_window, text=label_text)
        label.pack(pady=5)

        entry = tk.Entry(item_window)
        entry.pack(pady=5)
        entries[label_text] = entry

    # Submit Button
    def submit_item():
        # Collect the data from all entries
        item_data = {key: entry.get() for key, entry in entries.items()}

        # Basic validation: ensure all fields are filled
        if all(item_data.values()):
            try:
                # Connect to the database and insert the item
                conn = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="localhost",
                    database="pos",
                    port="1207",
                )
                cursor = conn.cursor()

                # Insert the item into the database
                insert_query = """
                INSERT INTO items (item_description, kitchen_description, price, item_group, printout_location)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(
                    insert_query,
                    (
                        item_data["Item Description"],
                        item_data["Kitchen Description"],
                        float(item_data["Price"]),
                        item_data["Group"],
                        item_data["Printout Location"],
                    ),
                )
                conn.commit()  # Commit the transaction
                messagebox.showinfo("Success", "Item added successfully!")

                # Clear the fields after successful submission
                for entry in entries.values():
                    entry.delete(0, tk.END)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()  # Close the database connection

            item_window.destroy()  # Close the window after submission
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    btn_submit = tk.Button(item_window, text="Submit", command=submit_item)
    btn_submit.pack(pady=20)
