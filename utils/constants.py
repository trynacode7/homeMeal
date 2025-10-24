# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "7Sqlgroot!"
DB_NAME = "food1"

# Application Settings
APP_NAME = "homeMeal"
APP_VERSION = "2.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# UI Colors
PRIMARY_COLOR = "#2E86AB"
SECONDARY_COLOR = "#A23B72"
ACCENT_COLOR = "#F18F01"
SUCCESS_COLOR = "#4CAF50"
ERROR_COLOR = "#F44336"
WARNING_COLOR = "#FF9800"
BACKGROUND_COLOR = "#F5F5F5"
TEXT_COLOR = "#333333"

# Item Categories (Vegetarian Only)
ITEM_CATEGORIES = [
    "Fruits & Vegetables",
    "Dairy & Eggs",
    "Grains & Bread",
    "Beverages",
    "Snacks",
    "Frozen Foods",
    "Canned Goods",
    "Condiments",
    "Other"
]

# Order Status
ORDER_STATUS = {
    "PENDING": "Pending",
    "CONFIRMED": "Confirmed",
    "PREPARING": "Preparing",
    "READY": "Ready for Pickup",
    "COMPLETED": "Completed",
    "CANCELLED": "Cancelled"
}

# Validation Rules
MIN_PASSWORD_LENGTH = 8
MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 500
MIN_PRICE = 0.01
MAX_PRICE = 9999.99