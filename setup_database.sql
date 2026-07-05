-- FuelDash Database Setup Script
-- Run this in MySQL to create the required database and tables

CREATE DATABASE IF NOT EXISTS fuel;
USE fuel;

-- Manager table
CREATE TABLE IF NOT EXISTS manager (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Customer table
CREATE TABLE IF NOT EXISTS customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Delivery table
CREATE TABLE IF NOT EXISTS delivery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fuelAmount VARCHAR(50),
    fuelType VARCHAR(50),
    userLocationLat DOUBLE,
    userLocationLng DOUBLE,
    petrolBunkLocationLat DOUBLE,
    petrolBunkLocationLng DOUBLE,
    timestamp_booked DATETIME,
    timestamp_delivered DATETIME,
    status VARCHAR(50) DEFAULT 'Pending',
    delivered VARCHAR(50) DEFAULT 'Not Delivered'
);

-- Insert sample users (for testing)
INSERT IGNORE INTO manager (username, password) VALUES ('admin', 'admin123');
INSERT IGNORE INTO customer (username, password) VALUES ('customer1', 'cust123');
INSERT IGNORE INTO delivery (username, password) VALUES ('delivery1', 'del123');

SELECT 'Database setup complete!' AS Status;
