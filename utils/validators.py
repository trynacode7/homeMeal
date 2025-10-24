import re
from utils.constants import MIN_PASSWORD_LENGTH, MAX_NAME_LENGTH, MAX_DESCRIPTION_LENGTH, MIN_PRICE, MAX_PRICE

def is_valid_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False, "Phone number is required"
    
    # Remove any non-digit characters
    clean_phone = re.sub(r'\D', '', phone)
    
    if len(clean_phone) != 10:
        return False, "Phone number must be exactly 10 digits"
    
    return True, "Valid phone number"

def is_valid_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Valid password"

def is_valid_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Please enter a valid email address"
    
    return True, "Valid email"

def is_valid_name(name):
    """Validate name format"""
    if not name:
        return False, "Name is required"
    
    if len(name) > MAX_NAME_LENGTH:
        return False, f"Name must be less than {MAX_NAME_LENGTH} characters"
    
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return False, "Name can only contain letters and spaces"
    
    return True, "Valid name"

def is_valid_apartment(apartment):
    """Validate apartment number"""
    if not apartment:
        return False, "Apartment number is required"
    
    if len(apartment) > 10:
        return False, "Apartment number is too long"
    
    return True, "Valid apartment number"

def is_valid_price(price):
    """Validate price format"""
    if not price:
        return False, "Price is required"
    
    try:
        price_float = float(price)
        if price_float < MIN_PRICE:
            return False, f"Price must be at least ₹{MIN_PRICE}"
        if price_float > MAX_PRICE:
            return False, f"Price cannot exceed ₹{MAX_PRICE}"
        return True, "Valid price"
    except ValueError:
        return False, "Please enter a valid price"

def is_valid_quantity(quantity):
    """Validate quantity"""
    if not quantity:
        return False, "Quantity is required"
    
    try:
        qty_int = int(quantity)
        if qty_int <= 0:
            return False, "Quantity must be greater than 0"
        if qty_int > 999:
            return False, "Quantity cannot exceed 999"
        return True, "Valid quantity"
    except ValueError:
        return False, "Please enter a valid quantity"

def is_valid_description(description):
    """Validate item description"""
    if not description:
        return False, "Description is required"
    
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return False, f"Description must be less than {MAX_DESCRIPTION_LENGTH} characters"
    
    return True, "Valid description"

def sanitize_input(text):
    """Sanitize user input to prevent SQL injection"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
    sanitized = text
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def validate_user_registration(name, apartment, phone, password, email=None):
    """Validate all user registration fields"""
    errors = []
    
    name_valid, name_msg = is_valid_name(name)
    if not name_valid:
        errors.append(name_msg)
    
    apt_valid, apt_msg = is_valid_apartment(apartment)
    if not apt_valid:
        errors.append(apt_msg)
    
    phone_valid, phone_msg = is_valid_phone(phone)
    if not phone_valid:
        errors.append(phone_msg)
    
    password_valid, password_msg = is_valid_password(password)
    if not password_valid:
        errors.append(password_msg)
    
    if email:
        email_valid, email_msg = is_valid_email(email)
        if not email_valid:
            errors.append(email_msg)
    
    return len(errors) == 0, errors

def validate_item_data(name, price, description, category):
    """Validate item data"""
    errors = []
    
    name_valid, name_msg = is_valid_name(name)
    if not name_valid:
        errors.append(name_msg)
    
    price_valid, price_msg = is_valid_price(price)
    if not price_valid:
        errors.append(price_msg)
    
    desc_valid, desc_msg = is_valid_description(description)
    if not desc_valid:
        errors.append(desc_msg)
    
    if not category:
        errors.append("Category is required")
    
    return len(errors) == 0, errors
