import tkinter as tk
from tkinter import messagebox
from gui.components import *
from db.user_queries import insert_user
from db.db_connector import get_db_connection
from utils.validators import validate_user_registration
from utils.logger import log_user_action, log_error

def register_page():
    root = tk.Tk()
    root.title(f"{APP_NAME} - Register")
    root.geometry("500x600")
    root.configure(bg=BACKGROUND_COLOR)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 250
    y = (root.winfo_screenheight() // 2) - 300
    root.geometry(f"500x600+{x}+{y}")
    
    # Main container
    main_frame = ModernFrame(root, style="container")
    main_frame.pack(fill="both", expand=True, padx=40, pady=40)
    
    # App title
    title_label = ModernLabel(main_frame, text=APP_NAME, style="title")
    title_label.pack(pady=(0, 10))
    
    subtitle_label = ModernLabel(main_frame, text="Create your account", style="subtitle")
    subtitle_label.pack(pady=(0, 30))
    
    # Registration form
    form_frame = ModernFrame(main_frame, style="card")
    form_frame.pack(fill="x", pady=(0, 20))
    
    # Name
    name_label = ModernLabel(form_frame, text="Full Name", style="subtitle")
    name_label.pack(anchor="w", pady=(0, 5))
    
    name_entry = ModernEntry(form_frame, placeholder="Enter your full name")
    name_entry.pack(fill="x", pady=(0, 15))
    
    # Apartment
    apartment_label = ModernLabel(form_frame, text="Apartment Number", style="subtitle")
    apartment_label.pack(anchor="w", pady=(0, 5))
    
    apartment_entry = ModernEntry(form_frame, placeholder="Enter your apartment number")
    apartment_entry.pack(fill="x", pady=(0, 15))
    
    # Phone number
    phone_label = ModernLabel(form_frame, text="Phone Number", style="subtitle")
    phone_label.pack(anchor="w", pady=(0, 5))
    
    phone_entry = ModernEntry(form_frame, placeholder="Enter your phone number")
    phone_entry.pack(fill="x", pady=(0, 15))
    
    # Email (optional)
    email_label = ModernLabel(form_frame, text="Email (Optional)", style="subtitle")
    email_label.pack(anchor="w", pady=(0, 5))
    
    email_entry = ModernEntry(form_frame, placeholder="Enter your email address")
    email_entry.pack(fill="x", pady=(0, 15))
    
    # Password
    password_label = ModernLabel(form_frame, text="Password", style="subtitle")
    password_label.pack(anchor="w", pady=(0, 5))
    
    password_entry = ModernEntry(form_frame, placeholder="Enter your password", show="*")
    password_entry.pack(fill="x", pady=(0, 15))
    
    # Confirm password
    confirm_password_label = ModernLabel(form_frame, text="Confirm Password", style="subtitle")
    confirm_password_label.pack(anchor="w", pady=(0, 5))
    
    confirm_password_entry = ModernEntry(form_frame, placeholder="Confirm your password", show="*")
    confirm_password_entry.pack(fill="x", pady=(0, 20))
    
    # Error message label
    error_label = ModernLabel(form_frame, text="", style="error")
    error_label.pack(pady=(0, 20))
    
    # Success message label
    success_label = ModernLabel(form_frame, text="", style="success")
    success_label.pack(pady=(0, 20))
    
    # Register button
    def submit_registration():
        name = name_entry.get()
        apartment = apartment_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        # Clear previous messages
        error_label.configure(text="")
        success_label.configure(text="")
        
        # Check if passwords match
        if password != confirm_password:
            error_label.configure(text="Passwords do not match")
            return
        
        # Validate all inputs
        is_valid, errors = validate_user_registration(name, apartment, phone, password, email)
        if not is_valid:
            error_label.configure(text="; ".join(errors))
            return
        
        # Attempt registration
        try:
            con = get_db_connection()
            if con:
                success, result = insert_user(con, name, apartment, phone, password, email)
                con.close()
                
                if success:
                    success_label.configure(text="Registration successful! You can now login.")
                    log_user_action("User registered successfully", result)
                    
                    # Clear form
                    name_entry.delete(0, tk.END)
                    apartment_entry.delete(0, tk.END)
                    phone_entry.delete(0, tk.END)
                    email_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    confirm_password_entry.delete(0, tk.END)
                    
                    # Focus on name entry
                    name_entry.focus()
                else:
                    if isinstance(result, list):
                        error_label.configure(text="; ".join(result))
                    else:
                        error_label.configure(text="Registration failed")
            else:
                error_label.configure(text="Database connection failed")
        except Exception as e:
            log_error("Error during registration", exception=e)
            error_label.configure(text="An error occurred during registration")
    
    register_button = ModernButton(
        form_frame,
        text="Create Account",
        command=submit_registration,
        style="primary"
    )
    register_button.pack(fill="x", pady=(0, 15))
    
    # Login link
    def go_to_login():
        root.destroy()
        from gui.login_page import login_page
        login_page()
    
    login_frame = tk.Frame(form_frame, bg="white")
    login_frame.pack()
    
    login_text = ModernLabel(login_frame, text="Already have an account? ", style="normal")
    login_text.pack(side="left")
    
    login_link = tk.Label(
        login_frame,
        text="Sign in",
        font=("Arial", 10, "underline"),
        fg=PRIMARY_COLOR,
        bg="white",
        cursor="hand2"
    )
    login_link.pack(side="left")
    login_link.bind("<Button-1>", lambda e: go_to_login())
    
    # Bind Enter key to registration
    def on_enter(event):
        submit_registration()
    
    name_entry.bind("<Return>", on_enter)
    apartment_entry.bind("<Return>", on_enter)
    phone_entry.bind("<Return>", on_enter)
    email_entry.bind("<Return>", on_enter)
    password_entry.bind("<Return>", on_enter)
    confirm_password_entry.bind("<Return>", on_enter)
    
    # Focus on name entry
    name_entry.focus()
    
    root.mainloop()

