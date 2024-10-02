-- CREATING DATABASE
CREATE DATABASE commerce;

-- Telling interpreter to use commerce;
USE commerce;

-- Creating customer Table
CREATE TABLE customer
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(75) NOT NULL,
    email VARCHAR(150),
    phone CHAR(16)
);

-- Creating products Table with stock column
CREATE TABLE products
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    availability BOOLEAN,
    stock INT NOT NULL  -- Added stock column for stock management
);

-- Creating orders Table
CREATE TABLE orders
(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    order_date DATE NOT NULL,
    delivery_date DATE,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

-- Creating order_products (junction table for many-to-many relationship between orders and products)
CREATE TABLE order_products
(
    order_id INT,
    product_id INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ================== Populating customer Table ================== #
INSERT INTO customer (customer_name, email, phone) VALUES
('John Doe', 'john.doe@example.com', '1234567890'),
('Jane Smith', 'jane.smith@example.com', '0987654321'), 
('Alice Johnson', 'alice.johnson@example.com', '5551234567'), 
('Bob Brown', 'bob.brown@example.com', '5559876543'),
('Charlie Davis', 'charlie.davis@example.com', '5556789123'),
('Diana Evans', 'diana.evans@example.com', '5553456789'),
('Ethan Foster', 'ethan.foster@example.com', '5554567890'),
('Fiona Garcia', 'fiona.garcia@example.com', '5555678901'),
('George Harris', 'george.harris@example.com', '5556789012'),
('Hannah Ingram', 'hannah.ingram@example.com', '5557890123');

-- ================== Populating products Table with stock data ================== #
INSERT INTO products (product_name, price, availability, stock) VALUES
('Wireless Mouse', 25.99, 1, 50),
('Bluetooth Keyboard', 45.50, 1, 30),
('HD Monitor', 150.00, 1, 20),
('USB-C Hub', 35.75, 1, 40),
('External Hard Drive', 80.00, 1, 25),
('Webcam', 60.00, 1, 15),
('Laptop Stand', 30.00, 1, 35),
('Smartphone Charger', 15.99, 1, 100),
('Noise-Cancelling Headphones', 120.00, 1, 10),
('Portable Speaker', 55.00, 1, 22);

-- ================== Populating orders Table ================== #
INSERT INTO orders (order_date, delivery_date, customer_id) VALUES
('2024-08-30', '2024-08-31', 2),
('2024-08-31', '2024-09-02', 1),
('2024-09-01', '2024-09-05', 5),
('2024-09-02', '2024-09-06', 4),
('2024-09-03', '2024-09-07', 3),
('2024-09-04', '2024-09-08', 6),
('2024-09-05', '2024-09-09', 7),
('2024-09-06', '2024-09-10', 8),
('2024-09-07', '2024-09-11', 9),
('2024-09-08', '2024-09-12', 10);

-- ================== Populating order_products (associating orders with products) ================== #
INSERT INTO order_products (order_id, product_id) VALUES
(1, 1),  -- Order 1 includes Wireless Mouse (Product 1)
(1, 3),  -- Order 1 includes HD Monitor (Product 3)
(2, 2),  -- Order 2 includes Bluetooth Keyboard (Product 2)
(3, 5),  -- Order 3 includes External Hard Drive (Product 5)
(4, 4),  -- Order 4 includes USB-C Hub (Product 4)
(5, 6),  -- Order 5 includes Webcam (Product 6)
(6, 7),  -- Order 6 includes Laptop Stand (Product 7)
(7, 8),  -- Order 7 includes Smartphone Charger (Product 8)
(8, 9),  -- Order 8 includes Noise-Cancelling Headphones (Product 9)
(9, 10), -- Order 9 includes Portable Speaker (Product 10)
(10, 1), -- Order 10 includes Wireless Mouse (Product 1)
(10, 2), -- Order 10 includes Bluetooth Keyboard (Product 2)
(10, 3); -- Order 10 includes HD Monitor (Product 3)

-- ================== VIEWING Tables ================== #
SELECT * FROM customer;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_products;

-- ================== DROPPING Tables if needed ================== #
-- DROP TABLE order_products;
-- DROP TABLE products;
-- DROP TABLE orders;
-- DROP TABLE customer;
