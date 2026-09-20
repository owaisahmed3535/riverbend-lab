CREATE DATABASE riverbend_shop;
CREATE USER 'shopuser'@'localhost' IDENTIFIED BY 'StrongPass123!';
GRANT ALL PRIVILEGES ON riverbend_shop.* TO 'shopuser'@'localhost';
FLUSH PRIVILEGES;

USE riverbend_shop;
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  stock INT DEFAULT 0
);
INSERT INTO products (name, description, price, stock) VALUES
('Handmade Bracelet', 'Beaded bracelet, adjustable', 12.99, 25),
('Wool Scarf', 'Hand-knitted, winter collection', 24.50, 10),
('Leather Wallet', 'Full-grain leather, hand-stitched', 39.00, 8),
('Silver Earrings', 'Sterling silver, hypoallergenic', 18.75, 15),
('Canvas Tote Bag', 'Screen-printed, reusable', 22.00, 20);
