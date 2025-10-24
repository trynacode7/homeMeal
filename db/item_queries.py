from utils.validators import validate_item_data, sanitize_input, is_valid_price, is_valid_quantity
from utils.logger import log_database_operation, log_error, log_user_action
from utils.constants import ITEM_CATEGORIES
from typing import List, Dict, Any, Optional, Tuple

def fetch_items(con, category=None, search_term=None, sort_by="name", sort_order="ASC"):
    """Fetch items with filtering, searching, and sorting"""
    try:
        cur = con.cursor(dictionary=True)
        
        # Build query with conditions
        query = "SELECT * FROM items WHERE 1=1"
        params = []
        
        if category and category in ITEM_CATEGORIES:
            query += " AND category = %s"
            params.append(category)
        
        if search_term:
            search_term = sanitize_input(search_term)
            query += " AND (name LIKE %s OR description LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        # Add sorting
        valid_sort_fields = ["name", "price", "category", "created_at"]
        if sort_by not in valid_sort_fields:
            sort_by = "name"
        
        sort_order = "ASC" if sort_order.upper() == "ASC" else "DESC"
        query += f" ORDER BY {sort_by} {sort_order}"
        
        cur.execute(query, params)
        items = cur.fetchall()
        
        log_database_operation("SELECT", "items", None, True)
        return items
        
    except Exception as e:
        log_error("Error fetching items", exception=e)
        return []

def get_item_by_id(con, item_id):
    """Get item by ID"""
    try:
        cur = con.cursor(dictionary=True)
        query = "SELECT * FROM items WHERE id = %s"
        cur.execute(query, (item_id,))
        item = cur.fetchone()
        
        if item:
            log_database_operation("SELECT", "items", None, True)
            return item
        return None
        
    except Exception as e:
        log_error("Error getting item by ID", exception=e)
        return None

def add_item(con, name, price, description, category, stock_quantity=0, user_id=None):
    """Add a new item"""
    try:
        # Validate item data
        is_valid, errors = validate_item_data(name, price, description, category)
        if not is_valid:
            log_error(f"Item validation failed: {errors}")
            return False, errors
        
        # Validate stock quantity
        qty_valid, qty_msg = is_valid_quantity(stock_quantity)
        if not qty_valid:
            return False, [qty_msg]
        
        # Sanitize inputs
        name = sanitize_input(name)
        description = sanitize_input(description)
        category = sanitize_input(category)
        
        cur = con.cursor()
        query = """
            INSERT INTO items (name, price, description, category, stock_quantity, created_at) 
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cur.execute(query, (name, price, description, category, stock_quantity))
        con.commit()
        
        item_id = cur.lastrowid
        log_database_operation("INSERT", "items", user_id, True)
        log_user_action("Item added", user_id, f"Item: {name}")
        
        return True, item_id
        
    except Exception as e:
        log_error("Error adding item", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def update_item(con, item_id, name=None, price=None, description=None, category=None, stock_quantity=None, user_id=None):
    """Update an existing item"""
    try:
        cur = con.cursor()
        updates = []
        values = []
        
        if name:
            name = sanitize_input(name)
            updates.append("name = %s")
            values.append(name)
        
        if price is not None:
            price_valid, price_msg = is_valid_price(price)
            if not price_valid:
                return False, [price_msg]
            updates.append("price = %s")
            values.append(price)
        
        if description:
            description = sanitize_input(description)
            updates.append("description = %s")
            values.append(description)
        
        if category:
            category = sanitize_input(category)
            if category not in ITEM_CATEGORIES:
                return False, ["Invalid category"]
            updates.append("category = %s")
            values.append(category)
        
        if stock_quantity is not None:
            qty_valid, qty_msg = is_valid_quantity(stock_quantity)
            if not qty_valid:
                return False, [qty_msg]
            updates.append("stock_quantity = %s")
            values.append(stock_quantity)
        
        if not updates:
            return False, ["No fields to update"]
        
        updates.append("updated_at = NOW()")
        values.append(item_id)
        
        query = f"UPDATE items SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, values)
        con.commit()
        
        log_database_operation("UPDATE", "items", user_id, True)
        log_user_action("Item updated", user_id, f"Item ID: {item_id}")
        
        return True, "Item updated successfully"
        
    except Exception as e:
        log_error("Error updating item", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def delete_item(con, item_id, user_id=None):
    """Delete an item"""
    try:
        cur = con.cursor()
        
        # Check if item exists
        check_query = "SELECT name FROM items WHERE id = %s"
        cur.execute(check_query, (item_id,))
        item = cur.fetchone()
        
        if not item:
            return False, ["Item not found"]
        
        # Delete item
        delete_query = "DELETE FROM items WHERE id = %s"
        cur.execute(delete_query, (item_id,))
        con.commit()
        
        log_database_operation("DELETE", "items", user_id, True)
        log_user_action("Item deleted", user_id, f"Item ID: {item_id}")
        
        return True, "Item deleted successfully"
        
    except Exception as e:
        log_error("Error deleting item", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def update_stock_quantity(con, item_id, quantity_change, user_id=None):
    """Update item stock quantity"""
    try:
        cur = con.cursor()
        
        # Get current stock
        stock_query = "SELECT stock_quantity FROM items WHERE id = %s"
        cur.execute(stock_query, (item_id,))
        result = cur.fetchone()
        
        if not result:
            return False, ["Item not found"]
        
        current_stock = result[0]
        new_stock = current_stock + quantity_change
        
        if new_stock < 0:
            return False, ["Insufficient stock"]
        
        # Update stock
        update_query = "UPDATE items SET stock_quantity = %s, updated_at = NOW() WHERE id = %s"
        cur.execute(update_query, (new_stock, item_id))
        con.commit()
        
        log_database_operation("UPDATE", "items", user_id, True)
        log_user_action("Stock updated", user_id, f"Item ID: {item_id}, Change: {quantity_change}")
        
        return True, new_stock
        
    except Exception as e:
        log_error("Error updating stock", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def get_items_by_category(con, category):
    """Get items by category"""
    try:
        if category not in ITEM_CATEGORIES:
            return []
        
        cur = con.cursor(dictionary=True)
        query = "SELECT * FROM items WHERE category = %s ORDER BY name"
        cur.execute(query, (category,))
        items = cur.fetchall()
        
        log_database_operation("SELECT", "items", None, True)
        return items
        
    except Exception as e:
        log_error("Error getting items by category", exception=e)
        return []

def search_items(con, search_term):
    """Search items by name or description"""
    try:
        search_term = sanitize_input(search_term)
        
        cur = con.cursor(dictionary=True)
        query = """
            SELECT * FROM items 
            WHERE name LIKE %s OR description LIKE %s 
            ORDER BY name
        """
        search_pattern = f"%{search_term}%"
        cur.execute(query, (search_pattern, search_pattern))
        items = cur.fetchall()
        
        log_database_operation("SELECT", "items", None, True)
        return items
        
    except Exception as e:
        log_error("Error searching items", exception=e)
        return []

def get_low_stock_items(con, threshold=5):
    """Get items with low stock"""
    try:
        cur = con.cursor(dictionary=True)
        query = "SELECT * FROM items WHERE stock_quantity <= %s ORDER BY stock_quantity ASC"
        cur.execute(query, (threshold,))
        items = cur.fetchall()
        
        log_database_operation("SELECT", "items", None, True)
        return items
        
    except Exception as e:
        log_error("Error getting low stock items", exception=e)
        return []

def get_categories_with_counts(con):
    """Get categories with item counts"""
    try:
        cur = con.cursor(dictionary=True)
        query = """
            SELECT category, COUNT(*) as count 
            FROM items 
            GROUP BY category 
            ORDER BY count DESC
        """
        cur.execute(query)
        categories = cur.fetchall()
        
        log_database_operation("SELECT", "items", None, True)
        return categories
        
    except Exception as e:
        log_error("Error getting categories with counts", exception=e)
        return []
