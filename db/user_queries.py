from utils.session_manager import hash_password, verify_password, session_manager
from utils.validators import validate_user_registration, sanitize_input
from utils.logger import log_database_operation, log_error, log_user_action
from typing import Optional, Dict, Any, Tuple

def insert_user(con, name, apartment, phone, password, email=None):
    """Insert a new user with validation and password hashing"""
    try:
        # Validate input data
        is_valid, errors = validate_user_registration(name, apartment, phone, password, email)
        if not is_valid:
            log_error(f"User registration validation failed: {errors}")
            return False, errors
        
        # Sanitize inputs
        name = sanitize_input(name)
        apartment = sanitize_input(apartment)
        phone = sanitize_input(phone)
        email = sanitize_input(email) if email else None
        
        # Hash password
        hashed_password = hash_password(password)
        
        cur = con.cursor()
        
        # Check if user already exists
        check_query = "SELECT id FROM users WHERE phone = %s"
        cur.execute(check_query, (phone,))
        if cur.fetchone():
            log_error(f"User registration failed: Phone number already exists - {phone}")
            return False, ["Phone number already registered"]
        
        # Insert new user
        query = "INSERT INTO users (name, apartment, phone, password, email, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
        cur.execute(query, (name, apartment, phone, hashed_password, email))
        con.commit()
        
        user_id = cur.lastrowid
        log_database_operation("INSERT", "users", user_id, True)
        log_user_action("User registered", user_id, f"Phone: {phone}")
        
        return True, user_id
        
    except Exception as e:
        log_error("Error during user registration", exception=e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def login_user(con, phone, password):
    """Login user with session creation"""
    try:
        # Sanitize inputs
        phone = sanitize_input(phone)
        
        cur = con.cursor(dictionary=True)
        query = "SELECT id, name, apartment, phone, password, email FROM users WHERE phone = %s"
        cur.execute(query, (phone,))
        user = cur.fetchone()
        
        if user and verify_password(password, user['password']):
            # Create session
            user_data = {
                'name': user['name'],
                'apartment': user['apartment'],
                'phone': user['phone'],
                'email': user['email']
            }
            session_token = session_manager.create_session(user['id'], user_data)
            
            log_user_action("User logged in", user['id'])
            log_database_operation("SELECT", "users", user['id'], True)
            
            return True, session_token, user_data
        else:
            log_user_action("Failed login attempt", None, f"Phone: {phone}")
            return False, None, None
            
    except Exception as e:
        log_error("Error during login", exception=e)
        return False, None, None

def get_user_by_id(con, user_id):
    """Get user by ID"""
    try:
        cur = con.cursor(dictionary=True)
        query = "SELECT id, name, apartment, phone, email, created_at FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        
        if user:
            log_database_operation("SELECT", "users", user_id, True)
            return user
        return None
        
    except Exception as e:
        log_error("Error getting user by ID", user_id, e)
        return None

def update_user_profile(con, user_id, name=None, apartment=None, email=None):
    """Update user profile information"""
    try:
        cur = con.cursor()
        updates = []
        values = []
        
        if name:
            name = sanitize_input(name)
            updates.append("name = %s")
            values.append(name)
        
        if apartment:
            apartment = sanitize_input(apartment)
            updates.append("apartment = %s")
            values.append(apartment)
        
        if email:
            email = sanitize_input(email)
            updates.append("email = %s")
            values.append(email)
        
        if not updates:
            return False, ["No fields to update"]
        
        updates.append("updated_at = NOW()")
        values.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, values)
        con.commit()
        
        log_database_operation("UPDATE", "users", user_id, True)
        log_user_action("Profile updated", user_id)
        
        return True, "Profile updated successfully"
        
    except Exception as e:
        log_error("Error updating user profile", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def change_password(con, user_id, current_password, new_password):
    """Change user password"""
    try:
        # Get current password hash
        cur = con.cursor(dictionary=True)
        query = "SELECT password FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        
        if not user:
            return False, ["User not found"]
        
        # Verify current password
        if not verify_password(current_password, user['password']):
            log_user_action("Failed password change attempt", user_id)
            return False, ["Current password is incorrect"]
        
        # Hash new password
        new_hashed_password = hash_password(new_password)
        
        # Update password
        update_query = "UPDATE users SET password = %s, updated_at = NOW() WHERE id = %s"
        cur.execute(update_query, (new_hashed_password, user_id))
        con.commit()
        
        log_database_operation("UPDATE", "users", user_id, True)
        log_user_action("Password changed", user_id)
        
        return True, "Password changed successfully"
        
    except Exception as e:
        log_error("Error changing password", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def delete_user(con, user_id, password):
    """Delete user account"""
    try:
        # Verify password before deletion
        cur = con.cursor(dictionary=True)
        query = "SELECT password FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        
        if not user:
            return False, ["User not found"]
        
        if not verify_password(password, user['password']):
            log_user_action("Failed account deletion attempt", user_id)
            return False, ["Password is incorrect"]
        
        # Delete user
        delete_query = "DELETE FROM users WHERE id = %s"
        cur.execute(delete_query, (user_id,))
        con.commit()
        
        log_database_operation("DELETE", "users", user_id, True)
        log_user_action("Account deleted", user_id)
        
        return True, "Account deleted successfully"
        
    except Exception as e:
        log_error("Error deleting user", user_id, e)
        con.rollback()
        return False, [f"Database error: {str(e)}"]

def get_all_users(con):
    """Get all users (admin function)"""
    try:
        cur = con.cursor(dictionary=True)
        query = "SELECT id, name, apartment, phone, email, created_at FROM users ORDER BY created_at DESC"
        cur.execute(query)
        users = cur.fetchall()
        
        log_database_operation("SELECT", "users", None, True)
        return users
        
    except Exception as e:
        log_error("Error getting all users", exception=e)
        return []
