import tkinter as tk
from tkinter import ttk, messagebox
from utils.constants import *

class ModernButton(tk.Button):
    """Modern styled button component"""
    def __init__(self, parent, text, command=None, style="primary", **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.style = style
        self.apply_style()
    
    def apply_style(self):
        if self.style == "primary":
            self.configure(
                bg=PRIMARY_COLOR,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2"
            )
        elif self.style == "secondary":
            self.configure(
                bg=SECONDARY_COLOR,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2"
            )
        elif self.style == "success":
            self.configure(
                bg=SUCCESS_COLOR,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2"
            )
        elif self.style == "danger":
            self.configure(
                bg=ERROR_COLOR,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2"
            )
        elif self.style == "warning":
            self.configure(
                bg=WARNING_COLOR,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2"
            )

class ModernEntry(tk.Entry):
    """Modern styled entry component"""
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "gray"
        self.default_fg = self.cget("fg")
        
        self.configure(
            font=("Arial", 10),
            relief="flat",
            bd=2,
            highlightthickness=1,
            highlightcolor=PRIMARY_COLOR,
            highlightbackground="lightgray"
        )
        
        if placeholder:
            self.insert(0, placeholder)
            self.configure(fg=self.placeholder_color)
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(fg=self.default_fg)
    
    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg=self.placeholder_color)

class ModernLabel(tk.Label):
    """Modern styled label component"""
    def __init__(self, parent, text, style="normal", **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.style = style
        self.apply_style()
    
    def apply_style(self):
        if self.style == "title":
            self.configure(
                font=("Arial", 16, "bold"),
                fg=TEXT_COLOR,
                bg=BACKGROUND_COLOR
            )
        elif self.style == "subtitle":
            self.configure(
                font=("Arial", 12, "bold"),
                fg=TEXT_COLOR,
                bg=BACKGROUND_COLOR
            )
        elif self.style == "normal":
            self.configure(
                font=("Arial", 10),
                fg=TEXT_COLOR,
                bg=BACKGROUND_COLOR
            )
        elif self.style == "success":
            self.configure(
                font=("Arial", 10, "bold"),
                fg=SUCCESS_COLOR,
                bg=BACKGROUND_COLOR
            )
        elif self.style == "error":
            self.configure(
                font=("Arial", 10, "bold"),
                fg=ERROR_COLOR,
                bg=BACKGROUND_COLOR
            )

class ModernFrame(tk.Frame):
    """Modern styled frame component"""
    def __init__(self, parent, style="normal", **kwargs):
        super().__init__(parent, **kwargs)
        self.style = style
        self.apply_style()
    
    def apply_style(self):
        if self.style == "card":
            self.configure(
                bg="white",
                relief="raised",
                bd=1,
                padx=20,
                pady=20
            )
        elif self.style == "container":
            self.configure(
                bg=BACKGROUND_COLOR,
                padx=20,
                pady=20
            )
        else:
            self.configure(
                bg=BACKGROUND_COLOR
            )

class ItemCard(tk.Frame):
    """Card component for displaying items"""
    def __init__(self, parent, item_data, on_add_to_cart=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.item_data = item_data
        self.on_add_to_cart = on_add_to_cart
        self.create_widgets()
    
    def create_widgets(self):
        # Main card frame
        card_frame = ModernFrame(self, style="card")
        card_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Item name
        name_label = ModernLabel(card_frame, text=self.item_data['name'], style="subtitle")
        name_label.pack(anchor="w", pady=(0, 5))
        
        # Item description
        desc_label = ModernLabel(card_frame, text=self.item_data['description'], style="normal")
        desc_label.pack(anchor="w", pady=(0, 10))
        
        # Price and category row
        info_frame = tk.Frame(card_frame, bg="white")
        info_frame.pack(fill="x", pady=(0, 10))
        
        price_label = ModernLabel(info_frame, text=f"₹{self.item_data['price']:.2f}", style="subtitle")
        price_label.pack(side="left")
        
        category_label = ModernLabel(info_frame, text=self.item_data['category'], style="normal")
        category_label.pack(side="right")
        
        # Stock info
        stock_text = f"Stock: {self.item_data['stock_quantity']}"
        stock_color = SUCCESS_COLOR if self.item_data['stock_quantity'] > 5 else WARNING_COLOR
        stock_label = tk.Label(info_frame, text=stock_text, fg=stock_color, bg="white", font=("Arial", 9))
        stock_label.pack(side="right", padx=(0, 10))
        
        # Add to cart button
        if self.on_add_to_cart and self.item_data['stock_quantity'] > 0:
            add_button = ModernButton(
                card_frame, 
                text="Add to Cart", 
                command=lambda: self.on_add_to_cart(self.item_data['id']),
                style="primary"
            )
            add_button.pack(fill="x")

class CartItemCard(tk.Frame):
    """Card component for displaying cart items"""
    def __init__(self, parent, cart_item, on_update_quantity=None, on_remove=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.cart_item = cart_item
        self.on_update_quantity = on_update_quantity
        self.on_remove = on_remove
        self.create_widgets()
    
    def create_widgets(self):
        # Main card frame
        card_frame = ModernFrame(self, style="card")
        card_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Item info row
        info_frame = tk.Frame(card_frame, bg="white")
        info_frame.pack(fill="x", pady=(0, 10))
        
        # Item name and price
        name_label = ModernLabel(info_frame, text=self.cart_item['name'], style="subtitle")
        name_label.pack(side="left")
        
        price_label = ModernLabel(info_frame, text=f"₹{self.cart_item['price']:.2f}", style="normal")
        price_label.pack(side="right")
        
        # Quantity controls
        qty_frame = tk.Frame(card_frame, bg="white")
        qty_frame.pack(fill="x", pady=(0, 10))
        
        qty_label = ModernLabel(qty_frame, text="Quantity:", style="normal")
        qty_label.pack(side="left")
        
        # Quantity spinbox
        qty_var = tk.StringVar(value=str(self.cart_item['quantity']))
        qty_spinbox = tk.Spinbox(
            qty_frame, 
            from_=1, 
            to=self.cart_item['stock_quantity'], 
            textvariable=qty_var,
            width=5,
            command=lambda: self.on_update_quantity(self.cart_item['id'], int(qty_var.get()))
        )
        qty_spinbox.pack(side="left", padx=(10, 0))
        
        # Remove button
        if self.on_remove:
            remove_button = ModernButton(
                qty_frame,
                text="Remove",
                command=lambda: self.on_remove(self.cart_item['id']),
                style="danger"
            )
            remove_button.pack(side="right")
        
        # Total price
        total = self.cart_item['quantity'] * self.cart_item['price']
        total_label = ModernLabel(card_frame, text=f"Total: ₹{total:.2f}", style="subtitle")
        total_label.pack(anchor="e")

class OrderCard(tk.Frame):
    """Card component for displaying orders"""
    def __init__(self, parent, order_data, on_view_details=None, on_cancel=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.order_data = order_data
        self.on_view_details = on_view_details
        self.on_cancel = on_cancel
        self.create_widgets()
    
    def create_widgets(self):
        # Main card frame
        card_frame = ModernFrame(self, style="card")
        card_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Order header
        header_frame = tk.Frame(card_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 10))
        
        order_id_label = ModernLabel(header_frame, text=f"Order #{self.order_data['id']}", style="subtitle")
        order_id_label.pack(side="left")
        
        # Status with color coding
        status_colors = {
            "Pending": WARNING_COLOR,
            "Confirmed": PRIMARY_COLOR,
            "Preparing": ACCENT_COLOR,
            "Ready": SUCCESS_COLOR,
            "Completed": SUCCESS_COLOR,
            "Cancelled": ERROR_COLOR
        }
        
        status_color = status_colors.get(self.order_data['status'], TEXT_COLOR)
        status_label = tk.Label(
            header_frame, 
            text=self.order_data['status'], 
            fg=status_color, 
            bg="white", 
            font=("Arial", 10, "bold")
        )
        status_label.pack(side="right")
        
        # Order details
        details_frame = tk.Frame(card_frame, bg="white")
        details_frame.pack(fill="x", pady=(0, 10))
        
        total_label = ModernLabel(details_frame, text=f"Total: ₹{self.order_data['total_amount']:.2f}", style="subtitle")
        total_label.pack(side="left")
        
        date_label = ModernLabel(details_frame, text=self.order_data['created_at'].strftime("%Y-%m-%d %H:%M"), style="normal")
        date_label.pack(side="right")
        
        # Action buttons
        if self.on_view_details:
            view_button = ModernButton(
                card_frame,
                text="View Details",
                command=lambda: self.on_view_details(self.order_data['id']),
                style="primary"
            )
            view_button.pack(side="left", padx=(0, 10))
        
        if self.on_cancel and self.order_data['status'] in ["Pending", "Confirmed"]:
            cancel_button = ModernButton(
                card_frame,
                text="Cancel Order",
                command=lambda: self.on_cancel(self.order_data['id']),
                style="danger"
            )
            cancel_button.pack(side="right")

class SearchBar(tk.Frame):
    """Search bar component"""
    def __init__(self, parent, on_search=None, placeholder="Search items...", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search = on_search
        self.create_widgets(placeholder)
    
    def create_widgets(self, placeholder):
        self.configure(bg=BACKGROUND_COLOR)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ModernEntry(self, placeholder=placeholder, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Search button
        search_button = ModernButton(
            self, 
            text="Search", 
            command=self.perform_search,
            style="primary"
        )
        search_button.pack(side="right")
        
        # Bind Enter key
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
    
    def perform_search(self):
        if self.on_search:
            self.on_search(self.search_var.get())

class FilterBar(tk.Frame):
    """Filter bar component"""
    def __init__(self, parent, categories, on_filter=None, on_sort=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.categories = categories
        self.on_filter = on_filter
        self.on_sort = on_sort
        self.create_widgets()
    
    def create_widgets(self):
        self.configure(bg=BACKGROUND_COLOR)
        
        # Category filter
        filter_label = ModernLabel(self, text="Category:", style="normal")
        filter_label.pack(side="left", padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(
            self, 
            textvariable=self.category_var,
            values=["All"] + self.categories,
            state="readonly",
            width=15
        )
        category_combo.pack(side="left", padx=(0, 20))
        category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        
        # Sort options
        sort_label = ModernLabel(self, text="Sort by:", style="normal")
        sort_label.pack(side="left", padx=(0, 5))
        
        self.sort_var = tk.StringVar(value="name")
        sort_combo = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            values=["name", "price", "category"],
            state="readonly",
            width=10
        )
        sort_combo.pack(side="left", padx=(0, 5))
        sort_combo.bind("<<ComboboxSelected>>", self.on_sort_change)
        
        # Sort order
        self.order_var = tk.StringVar(value="ASC")
        order_combo = ttk.Combobox(
            self,
            textvariable=self.order_var,
            values=["ASC", "DESC"],
            state="readonly",
            width=8
        )
        order_combo.pack(side="left")
        order_combo.bind("<<ComboboxSelected>>", self.on_sort_change)
    
    def on_category_change(self, event=None):
        if self.on_filter:
            category = self.category_var.get()
            if category == "All":
                category = None
            self.on_filter(category)
    
    def on_sort_change(self, event=None):
        if self.on_sort:
            self.on_sort(self.sort_var.get(), self.order_var.get())

def show_message(title, message, message_type="info"):
    """Show a message box with consistent styling"""
    if message_type == "error":
        messagebox.showerror(title, message)
    elif message_type == "warning":
        messagebox.showwarning(title, message)
    elif message_type == "success":
        messagebox.showinfo(title, message)
    else:
        messagebox.showinfo(title, message)

def show_confirmation(title, message):
    """Show a confirmation dialog"""
    return messagebox.askyesno(title, message) 