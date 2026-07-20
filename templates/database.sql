CREATE DATABASE portal_hostel;
USE portal_hostel;

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Seed an admin account (Password: admin123)
INSERT INTO admins (username, password) VALUES 
('admin', '$2y$10$W2iXpD3tPuxcQz7o1fM.VeK.fT4klyW7e24lK5XbZ/K98c0bXv8jG');