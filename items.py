import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def open_item_form():
    item_window = tk.Toplevel()  # Create a new window (popup)
    item_window.title("Add New Item")
    item_window.geometry("400x400")

    # Title
    label_title = tk.Label(item_window, text="Add New Item", font=("Arial", 16))
    label_title.pack(pady=10)

    # Function to fetch groups from the database
    def fetch_groups():
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT group_name FROM item_groups"
        )  # Assuming you have an item_groups table
        groups = [row[0] for row in cursor.fetchall()]
        conn.close()
        return groups

    # Function to fetch printout locations from the database
    def fetch_printout_locations():
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT location_name FROM printout_locations"
        )  # Assuming you have a printout_locations table
        locations = [row[0] for row in cursor.fetchall()]
        conn.close()
        return locations

    # Form fields
    label_item_desc = tk.Label(item_window, text="Item Description")
    label_item_desc.pack(pady=5)
    entry_item_desc = tk.Entry(item_window)
    entry_item_desc.pack(pady=5)

    label_kitchen_desc = tk.Label(item_window, text="Kitchen Description")
    label_kitchen_desc.pack(pady=5)
    entry_kitchen_desc = tk.Entry(item_window)
    entry_kitchen_desc.pack(pady=5)

    label_price = tk.Label(item_window, text="Price")
    label_price.pack(pady=5)
    entry_price = tk.Entry(item_window)
    entry_price.pack(pady=5)

    label_group = tk.Label(item_window, text="Group")
    label_group.pack(pady=5)
    group_combobox = ttk.Combobox(item_window, values=fetch_groups())
    group_combobox.pack(pady=5)

    label_printout = tk.Label(item_window, text="Printout Location")
    label_printout.pack(pady=5)
    printout_combobox = ttk.Combobox(item_window, values=fetch_printout_locations())
    printout_combobox.pack(pady=5)

    # Submit Button
    def submit_item():
        item_desc = entry_item_desc.get()
        kitchen_desc = entry_kitchen_desc.get()
        price = entry_price.get()
        group = group_combobox.get()
        printout_location = printout_combobox.get()

        # Basic validation: ensure all fields are filled
        if item_desc and kitchen_desc and price and group and printout_location:
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
                        item_desc,
                        kitchen_desc,
                        float(price),
                        group,
                        printout_location,
                    ),
                )
                conn.commit()  # Commit the transaction
                messagebox.showinfo("Success", "Item added successfully!")

                # Clear the fields after successful submission
                entry_item_desc.delete(0, tk.END)
                entry_kitchen_desc.delete(0, tk.END)
                entry_price.delete(0, tk.END)
                group_combobox.set("")
                printout_combobox.set("")

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
