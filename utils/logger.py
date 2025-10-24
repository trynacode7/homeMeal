import logging
import os
from datetime import datetime
from typing import Optional

class AppLogger:
    def __init__(self, name: str = "homeMeal"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # File handler for all logs
        file_handler = logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for important logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Error file handler
        error_handler = logging.FileHandler(f'logs/errors_{datetime.now().strftime("%Y%m%d")}.log')
        error_handler.setLevel(logging.ERROR)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Set formatters
        file_handler.setFormatter(detailed_formatter)
        console_handler.setFormatter(simple_formatter)
        error_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)
    
    def info(self, message: str, user_id: Optional[int] = None):
        """Log info message"""
        if user_id:
            message = f"[User:{user_id}] {message}"
        self.logger.info(message)
    
    def warning(self, message: str, user_id: Optional[int] = None):
        """Log warning message"""
        if user_id:
            message = f"[User:{user_id}] {message}"
        self.logger.warning(message)
    
    def error(self, message: str, user_id: Optional[int] = None, exception: Optional[Exception] = None):
        """Log error message"""
        if user_id:
            message = f"[User:{user_id}] {message}"
        if exception:
            message = f"{message} - Exception: {str(exception)}"
        self.logger.error(message)
    
    def debug(self, message: str, user_id: Optional[int] = None):
        """Log debug message"""
        if user_id:
            message = f"[User:{user_id}] {message}"
        self.logger.debug(message)
    
    def critical(self, message: str, user_id: Optional[int] = None, exception: Optional[Exception] = None):
        """Log critical message"""
        if user_id:
            message = f"[User:{user_id}] {message}"
        if exception:
            message = f"{message} - Exception: {str(exception)}"
        self.logger.critical(message)

# Global logger instance
app_logger = AppLogger()

def log_user_action(action: str, user_id: Optional[int] = None, details: Optional[str] = None):
    """Log user actions"""
    message = f"User Action: {action}"
    if details:
        message += f" - {details}"
    app_logger.info(message, user_id)

def log_database_operation(operation: str, table: str, user_id: Optional[int] = None, success: bool = True):
    """Log database operations"""
    status = "SUCCESS" if success else "FAILED"
    message = f"Database {operation} on {table} - {status}"
    app_logger.info(message, user_id)

def log_error(error_message: str, user_id: Optional[int] = None, exception: Optional[Exception] = None):
    """Log errors"""
    app_logger.error(error_message, user_id, exception)

def log_security_event(event: str, user_id: Optional[int] = None, ip_address: Optional[str] = None):
    """Log security-related events"""
    message = f"Security Event: {event}"
    if ip_address:
        message += f" - IP: {ip_address}"
    app_logger.warning(message, user_id) 