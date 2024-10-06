import tkinter as tk
from db.user_queries import insert_user
from db.db_connector import get_db_connection

def register_page():
    root = tk.Tk()
    root.title("Register")

    name_var = tk.StringVar()
    apt_var = tk.StringVar()
    phone_var = tk.StringVar()
    password_var = tk.StringVar()

    tk.Label(root, text="Name").grid(row=0)
    tk.Entry(root, textvariable=name_var).grid(row=0, column=1)

    tk.Label(root, text="Apartment").grid(row=1)
    tk.Entry(root, textvariable=apt_var).grid(row=1, column=1)

    tk.Label(root, text="Phone").grid(row=2)
    tk.Entry(root, textvariable=phone_var).grid(row=2, column=1)

    tk.Label(root, text="Password").grid(row=3)
    tk.Entry(root, textvariable=password_var, show="*").grid(row=3, column=1)

    def submit_registration():
        con = get_db_connection()
        success = insert_user(con, name_var.get(), apt_var.get(), phone_var.get(), password_var.get())
        if success:
            tk.Label(root, text="Registration successful").grid(row=4, column=1)
        else:
            tk.Label(root, text="Registration failed").grid(row=4, column=1)

    tk.Button(root, text="Register", command=submit_registration).grid(row=5, column=1)
    root.mainloop()

