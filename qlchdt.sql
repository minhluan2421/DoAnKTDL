CREATE DATABASE ElectronicsStore;
go
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Name NVARCHAR(50),
    Age INT,
    Gender NVARCHAR(10),
    Address NVARCHAR(100)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(50),
    Category NVARCHAR(50),
    Price DECIMAL(10, 2)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    TransactionDate DATE
);

INSERT INTO Users (UserID, Name, Age, Gender, Address)
VALUES (1, 'John Smith', 25, 'Male', 'New York'),
       (2, 'Jane Doe', 30, 'Female', 'Los Angeles');

INSERT INTO Products (ProductID, ProductName, Category, Price)
VALUES (1, 'iPhone 14', 'Smartphone', 999),
       (2, 'Samsung Galaxy S', 'Smartphone', 899);

INSERT INTO Transactions (TransactionID, UserID, ProductID, TransactionDate)
VALUES (1, 1, 1, '2025-05-01'),
       (2, 2, 2, '2025-05-02');


	   select*from products


	   USE ElectronicsStore;
SELECT * FROM Products;

ALTER TABLE Products ADD ImagePath NVARCHAR(255);
UPDATE Products
SET ImagePath = 'static/images/iphone14.jpg'
WHERE ProductID = 1;

UPDATE Products
SET ImagePath = 'static/images/galaxy_s.jpg'
WHERE ProductID = 2;


-- Thêm 20 sản phẩm mới
INSERT INTO Products (ProductID, ProductName, Category, Price, ImagePath) VALUES
(3, 'MacBook Pro 16"', 'Laptop', 2499.99, 'static/images/macbook_pro.jpg'),
(4, 'Dell XPS 13', 'Laptop', 1399.00, 'static/images/dell_xps13.jpg'),
(5, 'iPad Pro 11"', 'Tablet', 799.00, 'static/images/ipad_pro.jpg'),
(6, 'Samsung Galaxy Tab S8', 'Tablet', 749.00, 'static/images/galaxy_tab_s8.jpg'),
(7, 'Apple Watch Series 9', 'Smartwatch', 399.00, 'static/images/apple_watch9.jpg'),
(8, 'Samsung Galaxy Watch 6', 'Smartwatch', 349.00, 'static/images/galaxy_watch6.jpg'),
(9, 'Sony WH-1000XM5', 'Headphones', 379.99, 'static/images/sony_xm5.jpg'),
(10, 'Bose QuietComfort 45', 'Headphones', 329.00, 'static/images/bose_qc45.jpg'),
(11, 'Canon EOS R10', 'Camera', 999.00, 'static/images/canon_r10.jpg'),
(12, 'Nikon Z50', 'Camera', 1099.00, 'static/images/nikon_z50.jpg'),
(13, 'PlayStation 5', 'Game Console', 499.00, 'static/images/ps5.jpg'),
(14, 'Xbox Series X', 'Game Console', 499.00, 'static/images/xbox_series_x.jpg'),
(15, 'Google Pixel 8', 'Smartphone', 799.00, 'static/images/pixel8.jpg'),
(16, 'ASUS ROG Phone 7', 'Smartphone', 999.00, 'static/images/rog_phone7.jpg'),
(17, 'LG OLED CX 55"', 'TV', 1299.00, 'static/images/lg_oled_cx.jpg'),
(18, 'Samsung QLED Q80B 55"', 'TV', 1199.00, 'static/images/samsung_qled_q80b.jpg'),
(19, 'DJI Mini 3 Pro', 'Drone', 759.00, 'static/images/dji_mini3pro.jpg'),
(20, 'GoPro Hero 12', 'Action Camera', 399.00, 'static/images/gopro_hero12.jpg'),
(21, 'Anker PowerCore 26800mAh', 'Accessories', 69.99, 'static/images/anker_powercore.jpg'),
(22, 'Logitech MX Master 3S', 'Accessories', 99.99, 'static/images/logitech_mx3s.jpg');



INSERT INTO Users (UserID, Name, Age, Gender, Address) VALUES
(3, 'Alice Johnson', 27, 'Female', 'Chicago'),
(4, 'Bob Williams', 35, 'Male', 'Houston'),
(5, 'Emily Brown', 22, 'Female', 'San Francisco'),
(6, 'Michael Davis', 40, 'Male', 'Seattle'),
(7, 'Sarah Wilson', 29, 'Female', 'Boston'),
(8, 'David Martinez', 31, 'Male', 'Miami'),
(9, 'Olivia Garcia', 26, 'Female', 'Denver'),
(10, 'James Anderson', 38, 'Male', 'Austin'),
(11, 'Sophia Thomas', 24, 'Female', 'Portland'),
(12, 'Liam Jackson', 33, 'Male', 'Atlanta'),
(13, 'Isabella White', 28, 'Female', 'Phoenix'),
(14, 'Ethan Harris', 36, 'Male', 'Philadelphia'),
(15, 'Mia Lewis', 23, 'Female', 'San Diego'),
(16, 'Alexander Clark', 41, 'Male', 'Las Vegas'),
(17, 'Charlotte Robinson', 30, 'Female', 'Minneapolis'),
(18, 'Benjamin Lee', 34, 'Male', 'Detroit'),
(19, 'Amelia Walker', 25, 'Female', 'Orlando'),
(20, 'Daniel Young', 32, 'Male', 'Nashville'),
(21, 'Harper Hall', 27, 'Female', 'Columbus'),
(22, 'Joseph Allen', 39, 'Male', 'Salt Lake City');


INSERT INTO Transactions (TransactionID, UserID, ProductID, TransactionDate) VALUES
(3, 3, 3, '2025-05-03'),
(4, 4, 5, '2025-05-03'),
(5, 5, 7, '2025-05-04'),
(6, 6, 6, '2025-05-04'),
(7, 7, 8, '2025-05-05'),
(8, 8, 9, '2025-05-05'),
(9, 9, 10, '2025-05-05'),
(10, 10, 4, '2025-05-06'),
(11, 11, 13, '2025-05-06'),
(12, 12, 12, '2025-05-07'),
(13, 13, 11, '2025-05-07'),
(14, 14, 15, '2025-05-08'),
(15, 15, 14, '2025-05-08'),
(16, 16, 18, '2025-05-08'),
(17, 17, 16, '2025-05-09'),
(18, 18, 17, '2025-05-09'),
(19, 19, 20, '2025-05-10'),
(20, 20, 19, '2025-05-10'),
(21, 21, 21, '2025-05-11'),
(22, 22, 22, '2025-05-11');
