DROP TABLE IF EXISTS Customer;

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,  -- Unique ID for the customer
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DROP TABLE IF EXISTS Product;

CREATE TABLE Product (
    product_id INT PRIMARY KEY,  -- Unique ID for the product
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0  -- The amount available in stock
);

DROP TABLE IF EXISTS `Order`;
CREATE TABLE `Order` (
    order_id INT PRIMARY KEY,  -- Unique ID for the order
    customer_id INT,           -- Foreign key linking to the Customer table
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',  -- Order status, e.g., Pending, Shipped, Completed
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

DROP TABLE IF EXISTS ORDER_ITEM;
CREATE TABLE Order_Item (
    order_item_id INT PRIMARY KEY,   -- Unique ID for the order-item relationship
    order_id INT,                    -- Foreign key linking to the Order table
    product_id INT,                  -- Foreign key linking to the Product table
    quantity INT NOT NULL,           -- Quantity of the product in the order
    unit_price DECIMAL(10, 2) NOT NULL,  -- Price per unit of the product at the time of order
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);