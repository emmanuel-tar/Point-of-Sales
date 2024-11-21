import tkinter as tk
from tkinter import messagebox
import mysql.connector
from admin_panel import open_admin_panel


# Function to handle login
def login(username):
    def check_password():
        password = entry_password.get()  # Get entered password

        if password:
            try:
                conn = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="localhost",
                    database="pos",
                    port="1207",
                )
                cursor = conn.cursor()

                # Check if the username and password match in the database
                query = "SELECT * FROM users WHERE username=%s AND password=%s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Login", "Login Successful")
                    root.destroy()  # Close the login window
                    open_admin_panel()  # Open the admin panel
                else:
                    messagebox.showerror("Error", "Invalid username or password")

                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Database Error", f"Error connecting to database: {err}"
                )
        else:
            messagebox.showwarning("Input Error", "Please enter the password.")

    # Set the selected username label and link the button to check the password
    label_selected_user.config(text=f"Selected User: {username}")
    button_login.config(command=check_password)
    entry_password.delete(0, tk.END)  # Clear password entry field


# Function to fetch usernames from the database
def fetch_usernames():
    try:
        conn = mysql.connector.connect(
            user="root", password="root", host="localhost", database="pos", port="1207"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        usernames = [row[0] for row in cursor.fetchall()]  # Fetch usernames
        conn.close()
        return usernames
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not fetch usernames: {err}")
        return []


# Tkinter GUI for Login
root = tk.Tk()
root.title("Admin Login")
root.geometry("500x400")  # Increased the window size

# Frame for user buttons
frame_users = tk.Frame(root)
frame_users.pack(pady=20)

# Fetch usernames from the database and create a button for each
usernames = fetch_usernames()
for user in usernames:
    user_button = tk.Button(
        frame_users,
        text=user,
        bg="light green",  # Set the background color to light green
        fg="black",
        font=("Arial", 14, "bold"),  # Increase font size for better visibility
        width=25,  # Adjusted width for larger button appearance
        height=10,  # Adjusted height for a larger button
        relief="raised",  # Makes the button look a bit elevated
        command=lambda u=user: login(u),  # Pass the username to login function
    )
    user_button.pack(side="left", padx=10, pady=10)  # Add padding around buttons

# Frame for password prompt at the bottom
frame_login = tk.Frame(root)
frame_login.pack(pady=20)

# Selected user label for feedback
label_selected_user = tk.Label(
    frame_login, text="Select a user to log in", font=("Arial", 10)
)
label_selected_user.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="w")

# Password entry field
label_password = tk.Label(frame_login, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_password = tk.Entry(frame_login, show="*", width=20)
entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Login button
button_login = tk.Button(frame_login, text="Enter Password", font=("Arial", 12, "bold"))
button_login.grid(row=2, column=1, padx=10, pady=10, sticky="w")

root.mainloop()
