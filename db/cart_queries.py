from utils.validators import is_valid_quantity, sanitize_input
from utils.logger import log_database_operation, log_error, log_user_action
from typing import List, Dict, Any, Optional, Tuple

def add_to_cart(con, user_id, item_id, quantity=1):
    """Add item to user's cart"""
    try:
        # Validate quantity
        qty_valid, qty_msg = is_valid_quantity(quantity)
        if not qty_valid:
            return False, [qty_msg]
        
        cur = con.cursor()
        
        # Check if item exists and has sufficient stock
        item_query = "SELECT name, price, stock_quantity FROM items WHERE id = %s"
        cur.execute(item_query, (item_id,))
        item = cur.fetchone()
        
        if not item:
            return False, ["Item not found"]
        
        if item[2] < quantity:
            return False, [f"Insufficient stock. Available: {item[2]}"]
        
        # Check if item already in cart
        cart_query = "SELECT id, quantity FROM cart WHERE user_id = %s AND item_id = %s"
        cur.execute(cart_query, (user_id, item_id))
        existing_item = cur.fetchone()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item[1] + quantity
            if new_quantity > item[2]:
                return False, [f"Insufficient stock. Available: {item[2]}"]
            
            update_query = "UPDATE cart SET quantity = %s, updated_at = NOW() WHERE id = %s"
            cur.execute(update_query, (new_quantity, existing_item[0]))
        else:
            # Add new item to cart
            insert_query = """
                INSERT INTO cart (user_id, item_id, quantity, price, created_at) 
                VALUES (%s, %s, %s, %s, NOW())
            """
            cur.execute(insert_query, (user_id, item_id, quantity, item[1]))
        
        con.commit()
        
        log_database_operation("INSERT/UPDATE", "cart", user_id, True)
        log_user_action("Item added to cart", user_id, f"Item ID: {item_id}, Qty: {quantity}")
        
        return True, "Item added to cart successfully"
        
    except Exception as e:
        log_error("Error adding item to cart", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def get_cart_items(con, user_id):
    """Get all items in user's cart"""
    try:
        cur = con.cursor(dictionary=True)
        query = """
            SELECT c.id, c.item_id, c.quantity, c.price, c.created_at,
                   i.name, i.description, i.category, i.stock_quantity
            FROM cart c
            JOIN items i ON c.item_id = i.id
            WHERE c.user_id = %s
            ORDER BY c.created_at DESC
        """
        cur.execute(query, (user_id,))
        items = cur.fetchall()
        
        log_database_operation("SELECT", "cart", user_id, True)
        return items
        
    except Exception as e:
        log_error("Error getting cart items", user_id, e)
        return []

def update_cart_quantity(con, cart_item_id, quantity, user_id):
    """Update quantity of item in cart"""
    try:
        # Validate quantity
        qty_valid, qty_msg = is_valid_quantity(quantity)
        if not qty_valid:
            return False, [qty_msg]
        
        cur = con.cursor()
        
        # Check if cart item exists and belongs to user
        check_query = """
            SELECT c.id, i.stock_quantity 
            FROM cart c
            JOIN items i ON c.item_id = i.id
            WHERE c.id = %s AND c.user_id = %s
        """
        cur.execute(check_query, (cart_item_id, user_id))
        cart_item = cur.fetchone()
        
        if not cart_item:
            return False, ["Cart item not found"]
        
        if quantity > cart_item[1]:
            return False, [f"Insufficient stock. Available: {cart_item[1]}"]
        
        # Update quantity
        update_query = "UPDATE cart SET quantity = %s, updated_at = NOW() WHERE id = %s"
        cur.execute(update_query, (quantity, cart_item_id))
        con.commit()
        
        log_database_operation("UPDATE", "cart", user_id, True)
        log_user_action("Cart quantity updated", user_id, f"Cart item ID: {cart_item_id}, Qty: {quantity}")
        
        return True, "Quantity updated successfully"
        
    except Exception as e:
        log_error("Error updating cart quantity", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def remove_from_cart(con, cart_item_id, user_id):
    """Remove item from cart"""
    try:
        cur = con.cursor()
        
        # Check if cart item exists and belongs to user
        check_query = "SELECT id FROM cart WHERE id = %s AND user_id = %s"
        cur.execute(check_query, (cart_item_id, user_id))
        if not cur.fetchone():
            return False, ["Cart item not found"]
        
        # Remove item
        delete_query = "DELETE FROM cart WHERE id = %s"
        cur.execute(delete_query, (cart_item_id,))
        con.commit()
        
        log_database_operation("DELETE", "cart", user_id, True)
        log_user_action("Item removed from cart", user_id, f"Cart item ID: {cart_item_id}")
        
        return True, "Item removed from cart successfully"
        
    except Exception as e:
        log_error("Error removing item from cart", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def clear_cart(con, user_id):
    """Clear all items from user's cart"""
    try:
        cur = con.cursor()
        delete_query = "DELETE FROM cart WHERE user_id = %s"
        cur.execute(delete_query, (user_id,))
        con.commit()
        
        log_database_operation("DELETE", "cart", user_id, True)
        log_user_action("Cart cleared", user_id)
        
        return True, "Cart cleared successfully"
        
    except Exception as e:
        log_error("Error clearing cart", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def get_cart_total(con, user_id):
    """Calculate total price of items in cart"""
    try:
        cur = con.cursor()
        query = "SELECT SUM(quantity * price) FROM cart WHERE user_id = %s"
        cur.execute(query, (user_id,))
        total = cur.fetchone()[0]
        
        return total if total else 0
        
    except Exception as e:
        log_error("Error calculating cart total", user_id, e)
        return 0

def get_cart_item_count(con, user_id):
    """Get number of items in cart"""
    try:
        cur = con.cursor()
        query = "SELECT COUNT(*) FROM cart WHERE user_id = %s"
        cur.execute(query, (user_id,))
        count = cur.fetchone()[0]
        
        return count
        
    except Exception as e:
        log_error("Error getting cart item count", user_id, e)
        return 0

def check_cart_availability(con, user_id):
    """Check if all items in cart are still available"""
    try:
        cur = con.cursor(dictionary=True)
        query = """
            SELECT c.id, c.quantity as cart_qty, i.name, i.stock_quantity as available_qty
            FROM cart c
            JOIN items i ON c.item_id = i.id
            WHERE c.user_id = %s
        """
        cur.execute(query, (user_id,))
        items = cur.fetchall()
        
        unavailable_items = []
        for item in items:
            if item['cart_qty'] > item['available_qty']:
                unavailable_items.append({
                    'name': item['name'],
                    'requested': item['cart_qty'],
                    'available': item['available_qty']
                })
        
        return len(unavailable_items) == 0, unavailable_items
        
    except Exception as e:
        log_error("Error checking cart availability", user_id, e)
        return False, [] 