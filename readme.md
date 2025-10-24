# homeMeal - Advanced Food Management System

## Overview
homeMeal is a comprehensive food management and ordering system designed for apartment complexes and residential communities. The system provides a modern, user-friendly interface for users to browse items, manage shopping carts, place orders, and track their order history.

## Features

### 🔐 **User Management**
- **Secure Registration & Login**: Password hashing, session management, and input validation
- **User Profiles**: View and manage personal information
- **Session Management**: Secure authentication with automatic timeout
- **Password Security**: Strong password requirements with SHA-256 hashing

### 🛒 **Shopping Experience**
- **Item Catalog**: Browse items by categories with detailed descriptions
- **Advanced Search**: Search items by name or description
- **Filtering & Sorting**: Filter by category, sort by name, price, or category
- **Shopping Cart**: Add, remove, and update quantities
- **Real-time Stock**: Live stock quantity updates

### 📦 **Order Management**
- **Order Creation**: Convert cart to orders with delivery details
- **Order Tracking**: View order status and history
- **Order Cancellation**: Cancel orders (when applicable)
- **Status Updates**: Track order progress (Pending, Confirmed, Preparing, Ready, Completed, Cancelled)

### 🎨 **Modern UI/UX**
- **Responsive Design**: Modern, clean interface with consistent styling
- **Component System**: Reusable UI components for maintainability
- **Color-coded Status**: Visual indicators for order status and stock levels
- **Navigation**: Intuitive navigation between different sections

### 📊 **Data Management**
- **Comprehensive Logging**: Detailed application and error logging
- **Input Validation**: Robust validation for all user inputs
- **SQL Injection Protection**: Sanitized database queries
- **Error Handling**: Graceful error handling with user-friendly messages

### 🗄️ **Database Features**
- **Relational Design**: Properly normalized database schema
- **Stored Procedures**: Optimized database operations
- **Views**: Simplified data access patterns
- **Triggers**: Automatic timestamp updates
- **Indexes**: Optimized query performance

## System Architecture

```
homeMeal/
├── main.py                 # Application entry point
├── database_schema.sql     # Database schema and sample data
├── readme.md              # This file
├── db/                    # Database layer
│   ├── db_connector.py    # Database connection management
│   ├── user_queries.py    # User-related database operations
│   ├── item_queries.py    # Item-related database operations
│   ├── cart_queries.py    # Shopping cart operations
│   └── order_queries.py   # Order management operations
├── gui/                   # User interface layer
│   ├── components.py      # Reusable UI components
│   ├── login_page.py      # User login interface
│   ├── register_page.py   # User registration interface
│   ├── dashboard.py       # Main application dashboard
│   └── home_page.py       # Legacy home page (deprecated)
└── utils/                 # Utility modules
    ├── constants.py       # Application constants and configuration
    ├── validators.py      # Input validation functions
    ├── session_manager.py # Session management system
    └── logger.py          # Logging system
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MySQL Server 5.7 or higher
- Required Python packages (see requirements below)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd homeMeal
```

### 2. Install Dependencies
```bash
pip install mysql-connector-python
```

### 3. Database Setup
1. Start your MySQL server
2. Run the database schema:
```bash
mysql -u root -p < database_schema.sql
```

### 4. Configuration
Update the database configuration in `utils/constants.py`:
```python
DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "food1"
```

### 5. Run the Application
```bash
python main.py
```

## Usage Guide

### For Users

#### Registration
1. Launch the application
2. Click "Sign up" on the login page
3. Fill in your details:
   - Full Name
   - Apartment Number
   - Phone Number (10 digits)
   - Email (optional)
   - Password (minimum 8 characters, must include uppercase, lowercase, and digit)
4. Click "Create Account"

#### Login
1. Enter your phone number and password
2. Click "Sign In"
3. You'll be redirected to the dashboard

#### Shopping
1. **Browse Items**: Navigate to the "Shop" section
2. **Search & Filter**: Use the search bar and category filters
3. **Add to Cart**: Click "Add to Cart" on desired items
4. **Manage Cart**: View cart contents and update quantities
5. **Checkout**: Click "Proceed to Checkout" (feature coming soon)

#### Order Management
1. **View Orders**: Navigate to the "Orders" section
2. **Track Status**: Monitor order progress with color-coded status
3. **Cancel Orders**: Cancel pending orders if needed
4. **Order History**: View all past orders

### For Administrators

#### Database Management
- Monitor logs in the `logs/` directory
- Use the provided database views for reporting
- Execute stored procedures for bulk operations

#### Sample Data
The system comes with sample data:
- **Users**: 3 test accounts (password: Test123!)
- **Items**: 15 sample vegetarian food items across 9 categories (prices in Indian Rupees)
- **Orders**: 3 sample orders with items (amounts in Indian Rupees)

## Technical Details

### Security Features
- **Password Hashing**: SHA-256 with salt
- **Session Management**: Secure token-based sessions
- **Input Sanitization**: Protection against SQL injection
- **Validation**: Comprehensive input validation
- **Error Handling**: Secure error messages

### Database Schema
- **Users**: User accounts and profiles
- **Items**: Product catalog with categories
- **Cart**: Shopping cart items
- **Orders**: Order headers
- **Order Items**: Order line items

### Performance Optimizations
- **Database Indexes**: Optimized for common queries
- **Connection Pooling**: Efficient database connections
- **Caching**: Session data caching
- **Lazy Loading**: Load data on demand

## Logging

The application maintains comprehensive logs:
- **Application Logs**: `logs/app_YYYYMMDD.log`
- **Error Logs**: `logs/errors_YYYYMMDD.log`
- **Console Output**: Real-time application events

## Error Handling

The system includes robust error handling:
- **Database Errors**: Graceful connection and query error handling
- **Validation Errors**: User-friendly validation messages
- **Session Errors**: Automatic session cleanup
- **UI Errors**: Non-blocking error display

## Future Enhancements

### Planned Features
- **Checkout System**: Complete order processing
- **Payment Integration**: Online payment processing
- **Email Notifications**: Order status updates
- **Admin Panel**: Administrative interface
- **Inventory Management**: Advanced stock management
- **Delivery Tracking**: Real-time delivery updates
- **User Reviews**: Product ratings and reviews
- **Promotional System**: Discounts and coupons

### Technical Improvements
- **API Development**: RESTful API for mobile apps
- **Caching Layer**: Redis integration for performance
- **Background Jobs**: Asynchronous task processing
- **Monitoring**: Application performance monitoring
- **Testing**: Comprehensive unit and integration tests

## Troubleshooting

### Common Issues

#### Database Connection Error
```
Error: Cannot connect to database.
```
**Solution**: 
1. Check MySQL server is running
2. Verify database credentials in `utils/constants.py`
3. Ensure database `food1` exists

#### Import Error
```
Error: Missing required dependency
```
**Solution**: Install required packages:
```bash
pip install mysql-connector-python
```

#### Login Issues
```
Error: Invalid phone number or password
```
**Solution**: 
1. Use sample account: Phone: `1234567890`, Password: `Test123!` (Diya P.)
2. Check phone number format (10 digits)
3. Ensure password meets requirements

### Log Files
Check log files for detailed error information:
- `logs/app_YYYYMMDD.log` - General application logs
- `logs/errors_YYYYMMDD.log` - Error-specific logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review the log files
- Create an issue in the repository

## Version History

### Version 2.0.0 (Current)
- Complete UI redesign with modern components
- Session management system
- Shopping cart functionality
- Order management system
- Comprehensive logging
- Advanced validation
- Database optimization

### Version 1.0.0 (Legacy)
- Basic user registration and login
- Simple item display
- Basic database operations

---

**homeMeal** - Making meal management simple and efficient! 🍽️
