import tkinter as tk
from db.user_queries import login_user
from db.db_connector import get_db_connection

def login_page():
    root = tk.Tk()
    root.title("Login")

    phone_var = tk.StringVar()
    password_var = tk.StringVar()

    tk.Label(root, text="Phone").grid(row=0)
    tk.Entry(root, textvariable=phone_var).grid(row=0, column=1)
    
    tk.Label(root, text="Password").grid(row=1)
    tk.Entry(root, textvariable=password_var, show="*").grid(row=1, column=1)
    
    def submit_login():
        con = get_db_connection()
        if login_user(con, phone_var.get(), password_var.get()):
            tk.Label(root, text="Login successful").grid(row=2, column=1)
        else:
            tk.Label(root, text="Login failed").grid(row=2, column=1)

    tk.Button(root, text="Login", command=submit_login).grid(row=3, column=1)
    root.mainloop()
