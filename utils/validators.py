def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_password(password):
    return len(password) >= 8
