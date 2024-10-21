import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def open_employee_form():
    employee_window = tk.Toplevel()
    employee_window.title("Add New User & Setup Security")
    employee_window.geometry("400x500")

    # Title
    label_title = tk.Label(
        employee_window, text="Add New User & Setup Security", font=("Arial", 16)
    )
    label_title.pack(pady=10)

    # Form fields for user creation
    label_username = tk.Label(employee_window, text="Username")
    label_username.pack(pady=5)
    entry_username = tk.Entry(employee_window)
    entry_username.pack(pady=5)

    label_password = tk.Label(employee_window, text="Password")
    label_password.pack(pady=5)
    entry_password = tk.Entry(employee_window, show="*")
    entry_password.pack(pady=5)

    # Security Roles Combobox
    label_role = tk.Label(employee_window, text="Role")
    label_role.pack(pady=5)
    role_combobox = ttk.Combobox(
        employee_window, values=["Admin", "Cashier", "Manager", "Employee"]
    )
    role_combobox.pack(pady=5)

    # Submit Button
    def submit_user():
        username = entry_username.get()
        password = entry_password.get()
        role = role_combobox.get()

        # Basic validation to ensure all fields are filled
        if username and password and role:
            try:
                # Connect to the database and insert the new user
                conn = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="localhost",
                    database="pos",
                    port="1207",
                )
                cursor = conn.cursor()

                # Insert the new user into the users table
                insert_query = """
                INSERT INTO users (username, password, roles)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (username, password, role))
                conn.commit()  # Commit the transaction
                messagebox.showinfo("Success", "New user added successfully!")

                # Clear fields after submission
                entry_username.delete(0, tk.END)
                entry_password.delete(0, tk.END)
                role_combobox.set("")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    btn_submit = tk.Button(employee_window, text="Add User", command=submit_user)
    btn_submit.pack(pady=20)

    employee_window.mainloop()
