-- homeMeal Database Schema
-- Version 2.0.0
-- Advanced Food Management System

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS food1;
USE food1;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    apartment VARCHAR(10) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_email (email)
);

-- Items table
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_name (name),
    INDEX idx_price (price)
);

-- Cart table
CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_item (user_id, item_id),
    INDEX idx_user_id (user_id)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    delivery_address TEXT,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id)
);

-- Insert sample data for testing

-- Sample users (password: Test123!)
INSERT INTO users (name, apartment, phone, password, email) VALUES
('Diya P', 'A101', '1234567890', '54de7f606f2523cba8efac173fab42fb7f59d56ceff974c8fdb7342cf2cfe345', 'diya@example.com'),
('Jane Smith', 'B205', '0987654321', '54de7f606f2523cba8efac173fab42fb7f59d56ceff974c8fdb7342cf2cfe345', 'jane@example.com'),
('Bob Johnson', 'C301', '5551234567', '54de7f606f2523cba8efac173fab42fb7f59d56ceff974c8fdb7342cf2cfe345', 'bob@example.com');

-- Sample items (prices in Indian Rupees, vegetarian only)
INSERT INTO items (name, description, price, category, stock_quantity) VALUES
('Fresh Apples', 'Sweet and juicy red apples', 249.00, 'Fruits & Vegetables', 50),
('Organic Milk', 'Fresh organic whole milk', 289.00, 'Dairy & Eggs', 30),
('Whole Wheat Bread', 'Fresh baked whole wheat bread', 207.00, 'Grains & Bread', 40),
('Orange Juice', '100% pure orange juice', 415.00, 'Beverages', 35),
('Potato Chips', 'Classic salted potato chips', 332.00, 'Snacks', 60),
('Frozen Pizza', 'Margherita frozen pizza', 582.00, 'Frozen Foods', 20),
('Canned Tomatoes', 'Whole peeled tomatoes', 166.00, 'Canned Goods', 45),
('Olive Oil', 'Extra virgin olive oil', 665.00, 'Condiments', 30),
('Bananas', 'Fresh yellow bananas', 124.00, 'Fruits & Vegetables', 75),
('Eggs', 'Farm fresh large eggs', 415.00, 'Dairy & Eggs', 50),
('Rice', 'Long grain white rice', 332.00, 'Grains & Bread', 40),
('Coffee', 'Premium ground coffee', 1082.00, 'Beverages', 25),
('Chocolate Bars', 'Dark chocolate bars', 249.00, 'Snacks', 40),
('Paneer', 'Fresh cottage cheese', 415.00, 'Dairy & Eggs', 30),
('Mixed Vegetables', 'Fresh seasonal vegetables', 166.00, 'Fruits & Vegetables', 40);

-- Sample orders (amounts in Indian Rupees)
INSERT INTO orders (user_id, total_amount, status, delivery_address, special_instructions) VALUES
(1, 1328.00, 'Completed', 'Apartment A101, Building 1', 'Please deliver after 6 PM'),
(2, 747.00, 'Pending', 'Apartment B205, Building 2', 'Leave at door if not home'),
(1, 1870.00, 'Confirmed', 'Apartment A101, Building 1', NULL);

-- Sample order items (prices in Indian Rupees)
INSERT INTO order_items (order_id, item_id, quantity, price) VALUES
(1, 1, 2, 249.00),  -- 2 apples
(1, 2, 1, 289.00),  -- 1 milk
(1, 3, 2, 207.00),  -- 2 bread
(1, 4, 1, 415.00),  -- 1 orange juice
(2, 14, 1, 415.00), -- 1 paneer
(3, 1, 3, 249.00),  -- 3 apples
(3, 5, 2, 332.00),  -- 2 potato chips
(3, 7, 1, 166.00),  -- 1 canned tomatoes
(3, 8, 1, 665.00);  -- 1 olive oil

-- Create views for easier querying

-- View for order details with user and item information
CREATE OR REPLACE VIEW order_details_view AS
SELECT 
    o.id as order_id,
    o.total_amount,
    o.status,
    o.created_at as order_date,
    u.name as customer_name,
    u.phone as customer_phone,
    u.apartment as delivery_address,
    o.special_instructions
FROM orders o
JOIN users u ON o.user_id = u.id;

-- View for cart items with item details
CREATE OR REPLACE VIEW cart_details_view AS
SELECT 
    c.id as cart_id,
    c.user_id,
    c.quantity,
    c.price as cart_price,
    c.created_at as added_date,
    i.name as item_name,
    i.description,
    i.category,
    i.stock_quantity,
    (c.quantity * c.price) as total_price
FROM cart c
JOIN items i ON c.item_id = i.id;

-- View for low stock items
CREATE OR REPLACE VIEW low_stock_items AS
SELECT 
    id,
    name,
    category,
    stock_quantity,
    price
FROM items
WHERE stock_quantity <= 5
ORDER BY stock_quantity ASC;

-- Create stored procedures

-- Procedure to add item to cart
DELIMITER //
CREATE PROCEDURE AddToCart(
    IN p_user_id INT,
    IN p_item_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE item_price DECIMAL(10,2);
    DECLARE current_stock INT;
    DECLARE cart_item_id INT;
    
    -- Get item price and stock
    SELECT price, stock_quantity INTO item_price, current_stock
    FROM items WHERE id = p_item_id;
    
    -- Check if item exists and has sufficient stock
    IF item_price IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Item not found';
    ELSEIF current_stock < p_quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock';
    ELSE
        -- Check if item already in cart
        SELECT id INTO cart_item_id
        FROM cart 
        WHERE user_id = p_user_id AND item_id = p_item_id;
        
        IF cart_item_id IS NOT NULL THEN
            -- Update existing cart item
            UPDATE cart 
            SET quantity = quantity + p_quantity,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = cart_item_id;
        ELSE
            -- Add new cart item
            INSERT INTO cart (user_id, item_id, quantity, price)
            VALUES (p_user_id, p_item_id, p_quantity, item_price);
        END IF;
        
        -- Update stock
        UPDATE items 
        SET stock_quantity = stock_quantity - p_quantity,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = p_item_id;
    END IF;
END //
DELIMITER ;

-- Procedure to create order from cart
DELIMITER //
CREATE PROCEDURE CreateOrderFromCart(
    IN p_user_id INT,
    IN p_delivery_address TEXT,
    IN p_special_instructions TEXT
)
BEGIN
    DECLARE order_id INT;
    DECLARE total_amount DECIMAL(10,2);
    DECLARE done INT DEFAULT FALSE;
    DECLARE cart_item_id INT;
    DECLARE item_id INT;
    DECLARE quantity INT;
    DECLARE price DECIMAL(10,2);
    
    -- Cursor for cart items
    DECLARE cart_cursor CURSOR FOR
        SELECT id, item_id, quantity, price
        FROM cart
        WHERE user_id = p_user_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Calculate total amount
    SELECT COALESCE(SUM(quantity * price), 0) INTO total_amount
    FROM cart
    WHERE user_id = p_user_id;
    
    IF total_amount = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cart is empty';
    ELSE
        -- Create order
        INSERT INTO orders (user_id, total_amount, status, delivery_address, special_instructions)
        VALUES (p_user_id, total_amount, 'Pending', p_delivery_address, p_special_instructions);
        
        SET order_id = LAST_INSERT_ID();
        
        -- Process cart items
        OPEN cart_cursor;
        
        read_loop: LOOP
            FETCH cart_cursor INTO cart_item_id, item_id, quantity, price;
            IF done THEN
                LEAVE read_loop;
            END IF;
            
            -- Add order item
            INSERT INTO order_items (order_id, item_id, quantity, price)
            VALUES (order_id, item_id, quantity, price);
            
        END LOOP;
        
        CLOSE cart_cursor;
        
        -- Clear cart
        DELETE FROM cart WHERE user_id = p_user_id;
    END IF;
END //
DELIMITER ;

-- Create triggers

-- Trigger to update item updated_at timestamp
DELIMITER //
CREATE TRIGGER items_update_trigger
BEFORE UPDATE ON items
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
//
DELIMITER ;

-- Trigger to update user updated_at timestamp
DELIMITER //
CREATE TRIGGER users_update_trigger
BEFORE UPDATE ON users
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
//
DELIMITER ;

-- Trigger to update order updated_at timestamp
DELIMITER //
CREATE TRIGGER orders_update_trigger
BEFORE UPDATE ON orders
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
//
DELIMITER ;

-- Create indexes for better performance
CREATE INDEX idx_items_category_price ON items(category, price);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_cart_user_item ON cart(user_id, item_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON food1.* TO 'root'@'localhost';
-- FLUSH PRIVILEGES;

-- Show table information
SHOW TABLES;
SELECT 'Database schema created successfully!' as status; 