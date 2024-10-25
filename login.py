import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from admin_panel import open_admin_panel

# Function to handle login
def login():
    selected_user = combobox.get()  # Get selected username from combobox
    password = entry_password.get()  # Get entered password

    if selected_user and password:
        try:
            conn = mysql.connector.connect(
                user="root", password="root", host="localhost", database="pos", port="1207"
            )
            cursor = conn.cursor()

            # Check if the username and password match in the database
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (selected_user, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Login", "Login Successful")
                # Proceed to admin page or main screen
                root.destroy()  # Close the login window
                open_admin_panel()  # Open the admin panel from the other file
            else:
                messagebox.showerror("Error", "Invalid username or password")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")

# Function to fetch usernames from the database for the combobox
def fetch_usernames():
    try:
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        usernames = [row[0] for row in cursor.fetchall()]  # Fetch all usernames from the database
        conn.close()
        return usernames
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not fetch usernames: {err}")
        return []

# Tkinter GUI for Login
root = tk.Tk()
root.title("Admin Login")
root.geometry("300x200")

# Username Label and Combobox
label_username = tk.Label(root, text="Select Username:")
label_username.pack(pady=5)

usernames = fetch_usernames()  # Fetch usernames from the database
combobox = ttk.Combobox(root, values=usernames)
combobox.pack(pady=5)

# Password Label and Entry
label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")  # Password field (hidden characters)
entry_password.pack(pady=5)

# Login Button
btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=20)

root.mainloop()
