import tkinter as tk
from tkinter import ttk
from gui.components import *
from db.db_connector import get_db_connection
from db.item_queries import fetch_items, get_categories_with_counts
from db.cart_queries import get_cart_items, get_cart_total, get_cart_item_count
from db.order_queries import get_user_orders, get_order_statistics
from utils.session_manager import session_manager
from utils.constants import *
import json

class Dashboard:
    def __init__(self, session_token):
        self.session_token = session_token
        self.user_data = session_manager.validate_session(session_token)
        self.user_id = session_manager.get_user_id(session_token)
        
        if not self.user_data:
            raise ValueError("Invalid session")
        
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.load_data()
    
    def setup_window(self):
        """Setup the main window"""
        self.root.title(f"{APP_NAME} - Dashboard")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    def create_widgets(self):
        """Create the main dashboard widgets"""
        # Main container
        self.main_frame = ModernFrame(self.root, style="container")
        self.main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_header()
        
        # Navigation
        self.create_navigation()
        
        # Content area
        self.create_content_area()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.main_frame, bg=PRIMARY_COLOR, height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # App title
        title_label = tk.Label(
            header_frame, 
            text=APP_NAME, 
            font=("Arial", 20, "bold"),
            fg="white",
            bg=PRIMARY_COLOR
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # User info
        user_frame = tk.Frame(header_frame, bg=PRIMARY_COLOR)
        user_frame.pack(side="right", padx=20, pady=20)
        
        user_name_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.user_data['name']}!",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=PRIMARY_COLOR
        )
        user_name_label.pack(anchor="e")
        
        user_apt_label = tk.Label(
            user_frame,
            text=f"Apartment: {self.user_data['apartment']}",
            font=("Arial", 10),
            fg="white",
            bg=PRIMARY_COLOR
        )
        user_apt_label.pack(anchor="e")
        
        # Logout button
        logout_button = ModernButton(
            user_frame,
            text="Logout",
            command=self.logout,
            style="danger"
        )
        logout_button.pack(anchor="e", pady=(5, 0))
    
    def create_navigation(self):
        """Create the navigation menu"""
        nav_frame = tk.Frame(self.main_frame, bg=SECONDARY_COLOR, height=50)
        nav_frame.pack(fill="x", pady=(0, 20))
        nav_frame.pack_propagate(False)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("Home", self.show_home),
            ("Shop", self.show_shop),
            ("Cart", self.show_cart),
            ("Orders", self.show_orders),
            ("Profile", self.show_profile)
        ]
        
        for i, (text, command) in enumerate(nav_items):
            button = tk.Button(
                nav_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                bg=SECONDARY_COLOR,
                fg="white",
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2"
            )
            button.pack(side="left", padx=5)
            self.nav_buttons[text] = button
        
        # Highlight current page
        self.current_page = "Home"
        self.highlight_nav_button("Home")
    
    def create_content_area(self):
        """Create the main content area"""
        self.content_frame = ModernFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)
        
        # Create page containers
        self.pages = {}
        self.pages["Home"] = self.create_home_page()
        self.pages["Shop"] = self.create_shop_page()
        self.pages["Cart"] = self.create_cart_page()
        self.pages["Orders"] = self.create_orders_page()
        self.pages["Profile"] = self.create_profile_page()
        
        # Show home page by default
        self.show_page("Home")
    
    def create_home_page(self):
        """Create the home page"""
        page = ModernFrame(self.content_frame)
        
        # Welcome section
        welcome_frame = ModernFrame(page, style="card")
        welcome_frame.pack(fill="x", padx=20, pady=20)
        
        welcome_label = ModernLabel(welcome_frame, text="Welcome to homeMeal!", style="title")
        welcome_label.pack(pady=(0, 10))
        
        desc_label = ModernLabel(
            welcome_frame, 
            text="Your one-stop solution for meal management and ordering.",
            style="normal"
        )
        desc_label.pack()
        
        # Quick stats
        stats_frame = tk.Frame(page, bg=BACKGROUND_COLOR)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Stats cards
        self.stats_cards = {}
        stats_data = [
            ("Total Orders", "0", SUCCESS_COLOR),
            ("Cart Items", "0", PRIMARY_COLOR),
            ("Total Spent", "₹0.00", ACCENT_COLOR)
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card = tk.Frame(stats_frame, bg="white", relief="raised", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            title_label = tk.Label(card, text=title, font=("Arial", 12, "bold"), bg="white")
            title_label.pack(pady=(10, 5))
            
            value_label = tk.Label(card, text=value, font=("Arial", 16, "bold"), fg=color, bg="white")
            value_label.pack(pady=(0, 10))
            
            self.stats_cards[title] = value_label
        
        # Quick actions
        actions_frame = ModernFrame(page, style="card")
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        actions_label = ModernLabel(actions_frame, text="Quick Actions", style="subtitle")
        actions_label.pack(pady=(0, 15))
        
        actions_buttons_frame = tk.Frame(actions_frame, bg="white")
        actions_buttons_frame.pack()
        
        shop_button = ModernButton(
            actions_buttons_frame,
            text="Start Shopping",
            command=self.show_shop,
            style="primary"
        )
        shop_button.pack(side="left", padx=5)
        
        cart_button = ModernButton(
            actions_buttons_frame,
            text="View Cart",
            command=self.show_cart,
            style="secondary"
        )
        cart_button.pack(side="left", padx=5)
        
        orders_button = ModernButton(
            actions_buttons_frame,
            text="My Orders",
            command=self.show_orders,
            style="success"
        )
        orders_button.pack(side="left", padx=5)
        
        return page
    
    def create_shop_page(self):
        """Create the shop page"""
        page = ModernFrame(self.content_frame)
        
        # Search and filter section
        filter_frame = ModernFrame(page, style="card")
        filter_frame.pack(fill="x", padx=20, pady=20)
        
        # Search bar
        self.search_bar = SearchBar(filter_frame, on_search=self.search_items)
        self.search_bar.pack(fill="x", pady=(0, 10))
        
        # Filter bar
        self.filter_bar = FilterBar(
            filter_frame, 
            ITEM_CATEGORIES, 
            on_filter=self.filter_items,
            on_sort=self.sort_items
        )
        self.filter_bar.pack(fill="x")
        
        # Items display area
        items_frame = tk.Frame(page, bg=BACKGROUND_COLOR)
        items_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scrollable canvas for items
        canvas = tk.Canvas(items_frame, bg=BACKGROUND_COLOR)
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        self.items_container = tk.Frame(canvas, bg=BACKGROUND_COLOR)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.create_window((0, 0), window=self.items_container, anchor="nw")
        self.items_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        return page
    
    def create_cart_page(self):
        """Create the cart page"""
        page = ModernFrame(self.content_frame)
        
        # Cart header
        header_frame = ModernFrame(page, style="card")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        self.cart_title_label = ModernLabel(header_frame, text="Shopping Cart", style="title")
        self.cart_title_label.pack(side="left")
        
        self.cart_total_label = ModernLabel(header_frame, text="Total: $0.00", style="subtitle")
        self.cart_total_label.pack(side="right")
        
        # Cart items container
        self.cart_items_frame = tk.Frame(page, bg=BACKGROUND_COLOR)
        self.cart_items_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Checkout button
        self.checkout_button = ModernButton(
            page,
            text="Proceed to Checkout",
            command=self.checkout,
            style="success"
        )
        self.checkout_button.pack(pady=20)
        
        return page
    
    def create_orders_page(self):
        """Create the orders page"""
        page = ModernFrame(self.content_frame)
        
        # Orders header
        header_frame = ModernFrame(page, style="card")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        orders_label = ModernLabel(header_frame, text="My Orders", style="title")
        orders_label.pack()
        
        # Orders container
        self.orders_frame = tk.Frame(page, bg=BACKGROUND_COLOR)
        self.orders_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        return page
    
    def create_profile_page(self):
        """Create the profile page"""
        page = ModernFrame(self.content_frame)
        
        # Profile info
        profile_frame = ModernFrame(page, style="card")
        profile_frame.pack(fill="x", padx=20, pady=20)
        
        profile_label = ModernLabel(profile_frame, text="Profile Information", style="title")
        profile_label.pack(pady=(0, 20))
        
        # Profile details
        details_frame = tk.Frame(profile_frame, bg="white")
        details_frame.pack(fill="x")
        
        fields = [
            ("Name", self.user_data['name']),
            ("Apartment", self.user_data['apartment']),
            ("Phone", self.user_data['phone']),
            ("Email", self.user_data.get('email', 'Not provided'))
        ]
        
        for i, (label, value) in enumerate(fields):
            row_frame = tk.Frame(details_frame, bg="white")
            row_frame.pack(fill="x", pady=5)
            
            label_widget = ModernLabel(row_frame, text=f"{label}:", style="subtitle")
            label_widget.pack(side="left", padx=(0, 10))
            
            value_widget = ModernLabel(row_frame, text=value, style="normal")
            value_widget.pack(side="left")
        
        # Profile actions
        actions_frame = ModernFrame(page, style="card")
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        actions_label = ModernLabel(actions_frame, text="Account Actions", style="subtitle")
        actions_label.pack(pady=(0, 15))
        
        # Action buttons
        edit_button = ModernButton(
            actions_frame,
            text="Edit Profile",
            command=self.edit_profile,
            style="primary"
        )
        edit_button.pack(side="left", padx=5)
        
        change_password_button = ModernButton(
            actions_frame,
            text="Change Password",
            command=self.change_password,
            style="secondary"
        )
        change_password_button.pack(side="left", padx=5)
        
        delete_account_button = ModernButton(
            actions_frame,
            text="Delete Account",
            command=self.delete_account,
            style="danger"
        )
        delete_account_button.pack(side="left", padx=5)
        
        return page
    
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = tk.Frame(self.main_frame, bg=PRIMARY_COLOR, height=30)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 9),
            fg="white",
            bg=PRIMARY_COLOR
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def highlight_nav_button(self, page_name):
        """Highlight the current navigation button"""
        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(bg=ACCENT_COLOR)
            else:
                button.configure(bg=SECONDARY_COLOR)
    
    def show_page(self, page_name):
        """Show a specific page"""
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()
        
        # Show selected page
        self.pages[page_name].pack(fill="both", expand=True)
        
        # Update navigation
        self.current_page = page_name
        self.highlight_nav_button(page_name)
        
        # Load page-specific data
        if page_name == "Home":
            self.load_home_data()
        elif page_name == "Shop":
            self.load_shop_data()
        elif page_name == "Cart":
            self.load_cart_data()
        elif page_name == "Orders":
            self.load_orders_data()
    
    def show_home(self):
        self.show_page("Home")
    
    def show_shop(self):
        self.show_page("Shop")
    
    def show_cart(self):
        self.show_page("Cart")
    
    def show_orders(self):
        self.show_page("Orders")
    
    def show_profile(self):
        self.show_page("Profile")
    
    def load_data(self):
        """Load initial data"""
        self.load_home_data()
    
    def load_home_data(self):
        """Load home page data"""
        try:
            con = get_db_connection()
            if con:
                # Get order statistics
                stats = get_order_statistics(con, self.user_id)
                
                # Update stats cards
                if stats:
                    self.stats_cards["Total Orders"].configure(text=str(stats.get('total_orders', 0)))
                    self.stats_cards["Total Spent"].configure(text=f"₹{stats.get('total_spent', 0):.2f}")
                
                # Get cart count
                cart_count = get_cart_item_count(con, self.user_id)
                self.stats_cards["Cart Items"].configure(text=str(cart_count))
                
                con.close()
        except Exception as e:
            self.update_status(f"Error loading data: {str(e)}", "error")
    
    def load_shop_data(self):
        """Load shop page data"""
        try:
            con = get_db_connection()
            if con:
                items = fetch_items(con)
                self.display_items(items)
                con.close()
        except Exception as e:
            self.update_status(f"Error loading items: {str(e)}", "error")
    
    def load_cart_data(self):
        """Load cart page data"""
        try:
            con = get_db_connection()
            if con:
                cart_items = get_cart_items(con, self.user_id)
                cart_total = get_cart_total(con, self.user_id)
                
                self.display_cart_items(cart_items)
                self.cart_total_label.configure(text=f"Total: ${cart_total:.2f}")
                
                # Show/hide checkout button
                if cart_items:
                    self.checkout_button.pack(pady=20)
                else:
                    self.checkout_button.pack_forget()
                
                con.close()
        except Exception as e:
            self.update_status(f"Error loading cart: {str(e)}", "error")
    
    def load_orders_data(self):
        """Load orders page data"""
        try:
            con = get_db_connection()
            if con:
                orders = get_user_orders(con, self.user_id)
                self.display_orders(orders)
                con.close()
        except Exception as e:
            self.update_status(f"Error loading orders: {str(e)}", "error")
    
    def display_items(self, items):
        """Display items in the shop"""
        # Clear existing items
        for widget in self.items_container.winfo_children():
            widget.destroy()
        
        if not items:
            no_items_label = ModernLabel(self.items_container, text="No items available", style="normal")
            no_items_label.pack(pady=50)
            return
        
        # Create item cards
        for item in items:
            card = ItemCard(
                self.items_container,
                item,
                on_add_to_cart=self.add_to_cart
            )
            card.pack(fill="x", pady=5)
    
    def display_cart_items(self, cart_items):
        """Display cart items"""
        # Clear existing items
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        
        if not cart_items:
            no_items_label = ModernLabel(self.cart_items_frame, text="Your cart is empty", style="normal")
            no_items_label.pack(pady=50)
            return
        
        # Create cart item cards
        for item in cart_items:
            card = CartItemCard(
                self.cart_items_frame,
                item,
                on_update_quantity=self.update_cart_quantity,
                on_remove=self.remove_from_cart
            )
            card.pack(fill="x", pady=5)
    
    def display_orders(self, orders):
        """Display orders"""
        # Clear existing orders
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        
        if not orders:
            no_orders_label = ModernLabel(self.orders_frame, text="No orders found", style="normal")
            no_orders_label.pack(pady=50)
            return
        
        # Create order cards
        for order in orders:
            card = OrderCard(
                self.orders_frame,
                order,
                on_view_details=self.view_order_details,
                on_cancel=self.cancel_order
            )
            card.pack(fill="x", pady=5)
    
    def search_items(self, search_term):
        """Search items"""
        try:
            con = get_db_connection()
            if con:
                items = fetch_items(con, search_term=search_term)
                self.display_items(items)
                con.close()
        except Exception as e:
            self.update_status(f"Error searching items: {str(e)}", "error")
    
    def filter_items(self, category):
        """Filter items by category"""
        try:
            con = get_db_connection()
            if con:
                items = fetch_items(con, category=category)
                self.display_items(items)
                con.close()
        except Exception as e:
            self.update_status(f"Error filtering items: {str(e)}", "error")
    
    def sort_items(self, sort_by, sort_order):
        """Sort items"""
        try:
            con = get_db_connection()
            if con:
                items = fetch_items(con, sort_by=sort_by, sort_order=sort_order)
                self.display_items(items)
                con.close()
        except Exception as e:
            self.update_status(f"Error sorting items: {str(e)}", "error")
    
    def add_to_cart(self, item_id):
        """Add item to cart"""
        try:
            con = get_db_connection()
            if con:
                from db.cart_queries import add_to_cart
                success, message = add_to_cart(con, self.user_id, item_id)
                
                if success:
                    self.update_status("Item added to cart", "success")
                    self.load_home_data()  # Update cart count
                else:
                    self.update_status(f"Error: {message[0]}", "error")
                
                con.close()
        except Exception as e:
            self.update_status(f"Error adding to cart: {str(e)}", "error")
    
    def update_cart_quantity(self, cart_item_id, quantity):
        """Update cart item quantity"""
        try:
            con = get_db_connection()
            if con:
                from db.cart_queries import update_cart_quantity
                success, message = update_cart_quantity(con, cart_item_id, quantity, self.user_id)
                
                if success:
                    self.update_status("Quantity updated", "success")
                    self.load_cart_data()
                else:
                    self.update_status(f"Error: {message[0]}", "error")
                
                con.close()
        except Exception as e:
            self.update_status(f"Error updating quantity: {str(e)}", "error")
    
    def remove_from_cart(self, cart_item_id):
        """Remove item from cart"""
        try:
            con = get_db_connection()
            if con:
                from db.cart_queries import remove_from_cart
                success, message = remove_from_cart(con, cart_item_id, self.user_id)
                
                if success:
                    self.update_status("Item removed from cart", "success")
                    self.load_cart_data()
                    self.load_home_data()
                else:
                    self.update_status(f"Error: {message[0]}", "error")
                
                con.close()
        except Exception as e:
            self.update_status(f"Error removing from cart: {str(e)}", "error")
    
    def checkout(self):
        """Proceed to checkout"""
        # This would open a checkout dialog
        show_message("Checkout", "Checkout functionality will be implemented in the next version", "info")
    
    def view_order_details(self, order_id):
        """View order details"""
        # This would open an order details dialog
        show_message("Order Details", "Order details functionality will be implemented in the next version", "info")
    
    def cancel_order(self, order_id):
        """Cancel an order"""
        if show_confirmation("Cancel Order", "Are you sure you want to cancel this order?"):
            try:
                con = get_db_connection()
                if con:
                    from db.order_queries import cancel_order
                    success, message = cancel_order(con, order_id, self.user_id)
                    
                    if success:
                        self.update_status("Order cancelled", "success")
                        self.load_orders_data()
                    else:
                        self.update_status(f"Error: {message[0]}", "error")
                    
                    con.close()
            except Exception as e:
                self.update_status(f"Error cancelling order: {str(e)}", "error")
    
    def edit_profile(self):
        """Edit profile"""
        show_message("Edit Profile", "Profile editing functionality will be implemented in the next version", "info")
    
    def change_password(self):
        """Change password"""
        show_message("Change Password", "Password change functionality will be implemented in the next version", "info")
    
    def delete_account(self):
        """Delete account"""
        if show_confirmation("Delete Account", "Are you sure you want to delete your account? This action cannot be undone."):
            show_message("Delete Account", "Account deletion functionality will be implemented in the next version", "info")
    
    def logout(self):
        """Logout user"""
        if show_confirmation("Logout", "Are you sure you want to logout?"):
            session_manager.remove_session(self.session_token)
            self.root.destroy()
            # Return to login page
            from gui.login_page import login_page
            login_page()
    
    def update_status(self, message, message_type="info"):
        """Update status bar message"""
        self.status_label.configure(text=message)
        
        # Auto-clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.configure(text="Ready"))
    
    def run(self):
        """Start the dashboard"""
        self.root.mainloop() 