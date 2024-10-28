import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def open_item_form():
    item_window = tk.Toplevel()
    item_window.title("Items Management")
    item_window.geometry("800x400")

    left_frame = tk.Frame(item_window, width=300, bg="lightgray")
    left_frame.pack(side="left", fill="y")

    right_frame = tk.Frame(item_window, width=500)
    right_frame.pack(side="right", fill="both", expand=True)

    # Function to display items alphabetically
    def display_items():
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, item_description FROM items ORDER BY item_description ASC"
        )
        items = cursor.fetchall()
        conn.close()

        item_listbox.delete(0, tk.END)
        for item in items:
            item_listbox.insert(tk.END, item[1])  # Insert item description only

    # Fetch the groups and printout locations
    def fetch_groups():
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT group_name FROM item_groups")
        groups = [row[0] for row in cursor.fetchall()]
        conn.close()
        return groups

    def fetch_printout_locations():
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT location_name FROM printout_locations")
        locations = [row[0] for row in cursor.fetchall()]
        conn.close()
        return locations

    label_item_list = tk.Label(
        left_frame, text="Items", font=("Arial", 14), bg="lightgray"
    )
    label_item_list.pack(pady=10)

    item_listbox = tk.Listbox(left_frame)
    item_listbox.pack(fill="both", expand=True, padx=10, pady=10)
    display_items()

    label_title = tk.Label(right_frame, text="Edit Item", font=("Arial", 16))
    label_title.pack(pady=10)

    # Item Form Fields
    label_item_desc = tk.Label(right_frame, text="Item Description")
    label_item_desc.pack(pady=5)
    entry_item_desc = tk.Entry(right_frame)
    entry_item_desc.pack(pady=5)

    label_kitchen_desc = tk.Label(right_frame, text="Kitchen Description")
    label_kitchen_desc.pack(pady=5)
    entry_kitchen_desc = tk.Entry(right_frame)
    entry_kitchen_desc.pack(pady=5)

    label_price = tk.Label(right_frame, text="Price")
    label_price.pack(pady=5)
    entry_price = tk.Entry(right_frame)
    entry_price.pack(pady=5)

    label_group = tk.Label(right_frame, text="Group")
    label_group.pack(pady=5)
    group_combobox = ttk.Combobox(right_frame, values=fetch_groups())
    group_combobox.pack(pady=5)

    label_printout = tk.Label(right_frame, text="Printout Location")
    label_printout.pack(pady=5)
    printout_combobox = ttk.Combobox(right_frame, values=fetch_printout_locations())
    printout_combobox.pack(pady=5)

    # Fetch and display item details when an item is selected
    def on_item_select(event):
        selected_item = item_listbox.get(item_listbox.curselection())
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, item_description, kitchen_description, price, item_group, printout_location FROM items WHERE item_description = %s",
            (selected_item,),
        )
        item_data = cursor.fetchone()
        conn.close()

        if item_data:
            # Populate the form with item details for editing
            entry_item_desc.delete(0, tk.END)
            entry_item_desc.insert(0, item_data[1])

            entry_kitchen_desc.delete(0, tk.END)
            entry_kitchen_desc.insert(0, item_data[2])

            entry_price.delete(0, tk.END)
            entry_price.insert(0, item_data[3])

            group_combobox.set(item_data[4])
            printout_combobox.set(item_data[5])

            # Store the item ID for updating purposes
            entry_item_desc.item_id = item_data[0]

    # Bind the selection event to fetch item details
    item_listbox.bind("<<ListboxSelect>>", on_item_select)

    # Update item details in the database
    def update_item():
        item_id = getattr(entry_item_desc, "item_id", None)
        item_desc = entry_item_desc.get()
        kitchen_desc = entry_kitchen_desc.get()
        price = entry_price.get()
        group = group_combobox.get()
        printout_location = printout_combobox.get()

        if (
            item_id
            and item_desc
            and kitchen_desc
            and price
            and group
            and printout_location
        ):
            try:
                conn = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="localhost",
                    database="pos",
                    port="1207",
                )
                cursor = conn.cursor()
                update_query = """
                UPDATE items 
                SET item_description = %s, kitchen_description = %s, price = %s, item_group = %s, printout_location = %s 
                WHERE id = %s
                """
                cursor.execute(
                    update_query,
                    (
                        item_desc,
                        kitchen_desc,
                        float(price),
                        group,
                        printout_location,
                        item_id,
                    ),
                )
                conn.commit()
                messagebox.showinfo("Success", "Item updated successfully!")
                display_items()  # Refresh the item list

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    # Button to update item details
    btn_update = tk.Button(right_frame, text="Update", command=update_item)
    btn_update.pack(pady=20)
