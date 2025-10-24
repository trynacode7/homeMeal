from utils.logger import log_database_operation, log_error, log_user_action
from utils.constants import ORDER_STATUS
from db.cart_queries import get_cart_items, clear_cart, check_cart_availability
from db.item_queries import update_stock_quantity
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

def create_order(con, user_id, delivery_address=None, special_instructions=None):
    """Create a new order from user's cart"""
    try:
        cur = con.cursor()
        
        # Check if cart has items
        cart_items = get_cart_items(con, user_id)
        if not cart_items:
            return False, ["Cart is empty"]
        
        # Check availability
        is_available, unavailable_items = check_cart_availability(con, user_id)
        if not is_available:
            error_msg = "Some items are no longer available: "
            for item in unavailable_items:
                error_msg += f"{item['name']} (requested: {item['requested']}, available: {item['available']}); "
            return False, [error_msg]
        
        # Calculate total
        total_amount = sum(item['quantity'] * item['price'] for item in cart_items)
        
        # Create order
        order_query = """
            INSERT INTO orders (user_id, total_amount, status, delivery_address, special_instructions, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cur.execute(order_query, (user_id, total_amount, ORDER_STATUS["PENDING"], delivery_address, special_instructions))
        order_id = cur.lastrowid
        
        # Create order items
        for cart_item in cart_items:
            order_item_query = """
                INSERT INTO order_items (order_id, item_id, quantity, price, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cur.execute(order_item_query, (order_id, cart_item['item_id'], cart_item['quantity'], cart_item['price']))
            
            # Update stock
            update_stock_quantity(con, cart_item['item_id'], -cart_item['quantity'], user_id)
        
        # Clear cart
        clear_cart(con, user_id)
        
        con.commit()
        
        log_database_operation("INSERT", "orders", user_id, True)
        log_user_action("Order created", user_id, f"Order ID: {order_id}, Total: ${total_amount}")
        
        return True, order_id
        
    except Exception as e:
        log_error("Error creating order", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def get_user_orders(con, user_id, status=None):
    """Get all orders for a user"""
    try:
        cur = con.cursor(dictionary=True)
        
        query = "SELECT * FROM orders WHERE user_id = %s"
        params = [user_id]
        
        if status and status in ORDER_STATUS.values():
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        cur.execute(query, params)
        orders = cur.fetchall()
        
        log_database_operation("SELECT", "orders", user_id, True)
        return orders
        
    except Exception as e:
        log_error("Error getting user orders", user_id, e)
        return []

def get_order_details(con, order_id, user_id=None):
    """Get detailed order information including items"""
    try:
        cur = con.cursor(dictionary=True)
        
        # Get order info
        order_query = "SELECT * FROM orders WHERE id = %s"
        params = [order_id]
        
        if user_id:
            order_query += " AND user_id = %s"
            params.append(user_id)
        
        cur.execute(order_query, params)
        order = cur.fetchone()
        
        if not order:
            return None
        
        # Get order items
        items_query = """
            SELECT oi.*, i.name, i.description, i.category
            FROM order_items oi
            JOIN items i ON oi.item_id = i.id
            WHERE oi.order_id = %s
        """
        cur.execute(items_query, (order_id,))
        items = cur.fetchall()
        
        order['items'] = items
        
        log_database_operation("SELECT", "orders", user_id, True)
        return order
        
    except Exception as e:
        log_error("Error getting order details", user_id, e)
        return None

def update_order_status(con, order_id, new_status, user_id=None):
    """Update order status"""
    try:
        if new_status not in ORDER_STATUS.values():
            return False, ["Invalid status"]
        
        cur = con.cursor()
        update_query = "UPDATE orders SET status = %s, updated_at = NOW() WHERE id = %s"
        cur.execute(update_query, (new_status, order_id))
        con.commit()
        
        log_database_operation("UPDATE", "orders", user_id, True)
        log_user_action("Order status updated", user_id, f"Order ID: {order_id}, Status: {new_status}")
        
        return True, "Order status updated successfully"
        
    except Exception as e:
        log_error("Error updating order status", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def cancel_order(con, order_id, user_id):
    """Cancel an order and restore stock"""
    try:
        cur = con.cursor()
        
        # Get order details
        order = get_order_details(con, order_id, user_id)
        if not order:
            return False, ["Order not found"]
        
        if order['status'] not in [ORDER_STATUS["PENDING"], ORDER_STATUS["CONFIRMED"]]:
            return False, ["Order cannot be cancelled at this stage"]
        
        # Restore stock for each item
        for item in order['items']:
            update_stock_quantity(con, item['item_id'], item['quantity'], user_id)
        
        # Update order status
        update_query = "UPDATE orders SET status = %s, updated_at = NOW() WHERE id = %s"
        cur.execute(update_query, (ORDER_STATUS["CANCELLED"], order_id))
        con.commit()
        
        log_database_operation("UPDATE", "orders", user_id, True)
        log_user_action("Order cancelled", user_id, f"Order ID: {order_id}")
        
        return True, "Order cancelled successfully"
        
    except Exception as e:
        log_error("Error cancelling order", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def get_all_orders(con, status=None, limit=50):
    """Get all orders (admin function)"""
    try:
        cur = con.cursor(dictionary=True)
        
        query = """
            SELECT o.*, u.name as user_name, u.phone as user_phone
            FROM orders o
            JOIN users u ON o.user_id = u.id
        """
        params = []
        
        if status and status in ORDER_STATUS.values():
            query += " WHERE o.status = %s"
            params.append(status)
        
        query += " ORDER BY o.created_at DESC LIMIT %s"
        params.append(limit)
        
        cur.execute(query, params)
        orders = cur.fetchall()
        
        log_database_operation("SELECT", "orders", None, True)
        return orders
        
    except Exception as e:
        log_error("Error getting all orders", exception=e)
        return []

def get_order_statistics(con, user_id=None):
    """Get order statistics"""
    try:
        cur = con.cursor(dictionary=True)
        
        if user_id:
            # User-specific statistics
            stats_query = """
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(total_amount) as total_spent,
                    AVG(total_amount) as avg_order_value,
                    COUNT(CASE WHEN status = %s THEN 1 END) as pending_orders,
                    COUNT(CASE WHEN status = %s THEN 1 END) as completed_orders
                FROM orders 
                WHERE user_id = %s
            """
            cur.execute(stats_query, (ORDER_STATUS["PENDING"], ORDER_STATUS["COMPLETED"], user_id))
        else:
            # Overall statistics
            stats_query = """
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value,
                    COUNT(CASE WHEN status = %s THEN 1 END) as pending_orders,
                    COUNT(CASE WHEN status = %s THEN 1 END) as completed_orders
                FROM orders
            """
            cur.execute(stats_query, (ORDER_STATUS["PENDING"], ORDER_STATUS["COMPLETED"]))
        
        stats = cur.fetchone()
        
        log_database_operation("SELECT", "orders", user_id, True)
        return stats
        
    except Exception as e:
        log_error("Error getting order statistics", user_id, e)
        return {}

def get_recent_orders(con, days=7):
    """Get recent orders within specified days"""
    try:
        cur = con.cursor(dictionary=True)
        query = """
            SELECT o.*, u.name as user_name
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
            ORDER BY o.created_at DESC
        """
        cur.execute(query, (days,))
        orders = cur.fetchall()
        
        log_database_operation("SELECT", "orders", None, True)
        return orders
        
    except Exception as e:
        log_error("Error getting recent orders", exception=e)
        return [] 