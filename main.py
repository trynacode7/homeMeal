#!/usr/bin/env python3
"""
homeMeal - Advanced Food Management System
Version 2.0.0

A comprehensive food management and ordering system with modern UI,
session management, shopping cart, and order tracking.
"""

import sys
import os
from utils.logger import app_logger, log_error
from utils.constants import APP_NAME, APP_VERSION

def print_banner():
    """Print application banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                        {APP_NAME} v{APP_VERSION}                        ║
║                                                              ║
║              Advanced Food Management System                 ║
║                                                              ║
║  Features:                                                   ║
║  • User Registration & Authentication                       ║
║  • Modern GUI with Session Management                       ║
║  • Shopping Cart & Order Management                         ║
║  • Item Categories & Search                                 ║
║  • Real-time Stock Management                               ║
║  • Comprehensive Logging & Error Handling                   ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import tkinter
        import mysql.connector
        return True
    except ImportError as e:
        print(f"Error: Missing required dependency - {e}")
        print("Please install required packages:")
        print("pip install mysql-connector-python")
        return False

def check_database_connection():
    """Check if database connection is available"""
    try:
        from db.db_connector import get_db_connection
        con = get_db_connection()
        if con:
            con.close()
            return True
        else:
            return False
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def main():
    """Main application entry point"""
    try:
        # Print banner
        print_banner()
        
        # Check dependencies
        if not check_dependencies():
            print("Please install missing dependencies and try again.")
            sys.exit(1)
        
        # Check database connection
        print("Checking database connection...")
        if not check_database_connection():
            print("Error: Cannot connect to database.")
            print("Please check your database configuration in utils/constants.py")
            print("Make sure MySQL server is running and the database exists.")
            sys.exit(1)
        
        print("Database connection successful!")
        print("Starting application...\n")
        
        # Log application start
        app_logger.info(f"Application started - Version {APP_VERSION}")
        
        # Start with login page
        from gui.login_page import login_page
        login_page()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        app_logger.info("Application interrupted by user")
    except Exception as e:
        print(f"Critical error: {e}")
        log_error("Critical application error", exception=e)
        sys.exit(1)

if __name__ == "__main__":
    main()