import tkinter as tk
from tkinter import messagebox
from gui.components import *
from db.user_queries import login_user
from db.db_connector import get_db_connection
from utils.validators import is_valid_phone, is_valid_password
from utils.logger import log_user_action, log_error
from gui.dashboard import Dashboard

def login_page():
    root = tk.Tk()
    root.title(f"{APP_NAME} - Login")
    root.geometry("400x500")
    root.configure(bg=BACKGROUND_COLOR)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 200
    y = (root.winfo_screenheight() // 2) - 250
    root.geometry(f"400x500+{x}+{y}")
    
    # Main container
    main_frame = ModernFrame(root, style="container")
    main_frame.pack(fill="both", expand=True, padx=40, pady=40)
    
    # App title
    title_label = ModernLabel(main_frame, text=APP_NAME, style="title")
    title_label.pack(pady=(0, 10))
    
    subtitle_label = ModernLabel(main_frame, text="Sign in to your account", style="subtitle")
    subtitle_label.pack(pady=(0, 30))
    
    # Login form
    form_frame = ModernFrame(main_frame, style="card")
    form_frame.pack(fill="x", pady=(0, 20))
    
    # Phone number
    phone_label = ModernLabel(form_frame, text="Phone Number", style="subtitle")
    phone_label.pack(anchor="w", pady=(0, 5))
    
    phone_entry = ModernEntry(form_frame, placeholder="Enter your phone number")
    phone_entry.pack(fill="x", pady=(0, 15))
    
    # Password
    password_label = ModernLabel(form_frame, text="Password", style="subtitle")
    password_label.pack(anchor="w", pady=(0, 5))
    
    password_entry = ModernEntry(form_frame, placeholder="Enter your password", show="*")
    password_entry.pack(fill="x", pady=(0, 20))
    
    # Error message label
    error_label = ModernLabel(form_frame, text="", style="error")
    error_label.pack(pady=(0, 20))
    
    # Login button
    def submit_login():
        phone = phone_entry.get()
        password = password_entry.get()
        
        # Clear previous error
        error_label.configure(text="")
        
        # Validate inputs
        phone_valid, phone_msg = is_valid_phone(phone)
        if not phone_valid:
            error_label.configure(text=phone_msg)
            return
        
        password_valid, password_msg = is_valid_password(password)
        if not password_valid:
            error_label.configure(text=password_msg)
            return
        
        # Attempt login
        try:
            con = get_db_connection()
            if con:
                success, session_token, user_data = login_user(con, phone, password)
                con.close()
                
                if success:
                    log_user_action("User logged in successfully", user_data.get('id'))
                    root.destroy()
                    
                    # Open dashboard
                    try:
                        dashboard = Dashboard(session_token)
                        dashboard.run()
                    except Exception as e:
                        log_error("Error opening dashboard", exception=e)
                        messagebox.showerror("Error", "Failed to open dashboard")
                        login_page()  # Return to login
                else:
                    error_label.configure(text="Invalid phone number or password")
                    log_user_action("Failed login attempt", None, f"Phone: {phone}")
            else:
                error_label.configure(text="Database connection failed")
        except Exception as e:
            log_error("Error during login", exception=e)
            error_label.configure(text="An error occurred during login")
    
    login_button = ModernButton(
        form_frame,
        text="Sign In",
        command=submit_login,
        style="primary"
    )
    login_button.pack(fill="x", pady=(0, 15))
    
    # Register link
    def go_to_register():
        root.destroy()
        from gui.register_page import register_page
        register_page()
    
    register_frame = tk.Frame(form_frame, bg="white")
    register_frame.pack()
    
    register_text = ModernLabel(register_frame, text="Don't have an account? ", style="normal")
    register_text.pack(side="left")
    
    register_link = tk.Label(
        register_frame,
        text="Sign up",
        font=("Arial", 10, "underline"),
        fg=PRIMARY_COLOR,
        bg="white",
        cursor="hand2"
    )
    register_link.pack(side="left")
    register_link.bind("<Button-1>", lambda e: go_to_register())
    
    # Bind Enter key to login
    def on_enter(event):
        submit_login()
    
    phone_entry.bind("<Return>", on_enter)
    password_entry.bind("<Return>", on_enter)
    
    # Focus on phone entry
    phone_entry.focus()
    
    root.mainloop()
