#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "🗄️  MySQL Setup Script for Hostel Management System"
echo "════════════════════════════════════════════════════════════"

# Start MySQL
echo ""
echo "1️⃣  Starting MySQL service..."
sudo service mysql start

# Wait for MySQL to start
sleep 2

# Create database using sudo mysql
echo ""
echo "2️⃣  Creating database and loading schema..."
sudo mysql -u root << SQL
DROP DATABASE IF EXISTS hostel_management;
CREATE DATABASE hostel_management;
USE hostel_management;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student', 'warden') NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Rooms Table
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    floor INT NOT NULL,
    room_type ENUM('Single Deluxe', 'Double Sharing', 'Triple Sharing', 'Quad Sharing') NOT NULL,
    capacity INT NOT NULL,
    rent DECIMAL(10, 2) NOT NULL,
    amenities VARCHAR(255),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Students Table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    branch VARCHAR(50) NOT NULL,
    semester INT,
    contact_person_name VARCHAR(100),
    contact_person_phone VARCHAR(15),
    emergency_contact_phone VARCHAR(15),
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Room Occupancy Table
CREATE TABLE room_occupancy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    student_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE,
    status ENUM('Active', 'Inactive', 'Completed') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Complaints Table
CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    room_id INT,
    category ENUM('Plumbing', 'Electrical', 'Maintenance', 'Cleanliness', 'Noise', 'Others') NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('Pending', 'In Progress', 'Resolved', 'Closed') DEFAULT 'Pending',
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    assigned_to INT,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

-- Visitors Table
CREATE TABLE visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    visitor_name VARCHAR(100) NOT NULL,
    visitor_phone VARCHAR(15),
    visitor_relation VARCHAR(50),
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    expected_departure TIME,
    purpose VARCHAR(255),
    status ENUM('Pending', 'Approved', 'Rejected', 'Completed') DEFAULT 'Pending',
    approved_by INT,
    rejection_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Fees Table
CREATE TABLE fees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    academic_year VARCHAR(10) NOT NULL,
    semester INT NOT NULL,
    room_rent DECIMAL(10, 2) NOT NULL,
    mess_fee DECIMAL(10, 2),
    utilities_fee DECIMAL(10, 2),
    other_charges DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    paid_amount DECIMAL(10, 2) DEFAULT 0,
    pending_amount DECIMAL(10, 2) NOT NULL,
    due_date DATE,
    payment_status ENUM('Pending', 'Partial', 'Paid', 'Overdue') DEFAULT 'Pending',
    last_payment_date DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_year_sem (student_id, academic_year, semester)
);

-- Notices Table
CREATE TABLE notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    category ENUM('General', 'Important', 'Maintenance', 'Event', 'Academic', 'Rules') DEFAULT 'General',
    created_by INT NOT NULL,
    is_pinned BOOLEAN DEFAULT FALSE,
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    expires_at DATETIME,
    visibility ENUM('All', 'Students', 'Admin', 'Warden') DEFAULT 'All',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Gallery Table
CREATE TABLE gallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    category ENUM('Building', 'Rooms', 'Mess', 'Gym', 'Study Room', 'Garden', 'Common Area', 'Events') NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    uploaded_by INT NOT NULL,
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- Payment History Table
CREATE TABLE payment_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fee_id INT NOT NULL,
    student_id INT NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('Cash', 'Check', 'Bank Transfer', 'Online') DEFAULT 'Cash',
    transaction_id VARCHAR(50),
    payment_date DATETIME NOT NULL,
    recorded_by INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fee_id) REFERENCES fees(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
);

-- Hostel Settings Table
CREATE TABLE hostel_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sample Users
INSERT INTO users (username, email, password_hash, role, full_name, phone, is_active) VALUES
('admin', 'admin@hostel.com', '\$2y\$10\$W2iXpD3tPuxcQz7o1fM.VeK.fT4klyW7e24lK5XbZ/K98c0bXv8jG', 'admin', 'Admin User', '9000000001', TRUE),
('warden', 'warden@hostel.com', '\$2y\$10\$W2iXpD3tPuxcQz7o1fM.VeK.fT4klyW7e24lK5XbZ/K98c0bXv8jG', 'warden', 'Hostel Warden', '9000000002', TRUE),
('prajwal', 'prajwal@student.com', '\$2y\$10\$W2iXpD3tPuxcQz7o1fM.VeK.fT4klyW7e24lK5XbZ/K98c0bXv8jG', 'student', 'Prajwal Tandekar', '9876543210', TRUE),
('rajdeep', 'rajdeep@student.com', '\$2y\$10\$W2iXpD3tPuxcQz7o1fM.VeK.fT4klyW7e24lK5XbZ/K98c0bXv8jG', 'student', 'Rajdeep Patil', '9123456789', TRUE),
('rutuja', 'rutuja@student.com', '\$2y\$10\$W2iXpD3tPuxcQz7o1fM.VeK.fT4klyW7e24lK5XbZ/K98c0bXv8jG', 'student', 'Rutuja Patil', '9876123450', TRUE);

-- Sample Rooms
INSERT INTO rooms (room_number, floor, room_type, capacity, rent, amenities, is_available) VALUES
('101', 1, 'Double Sharing', 2, 5000, 'WiFi, AC, Cupboard, Study Desk', TRUE),
('102', 1, 'Double Sharing', 2, 5000, 'WiFi, AC, Cupboard, Study Desk', TRUE),
('103', 1, 'Single Deluxe', 1, 7000, 'WiFi, AC, Cupboard, Study Desk, Private Bathroom', TRUE),
('201', 2, 'Triple Sharing', 3, 4000, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
('202', 2, 'Single Deluxe', 1, 7000, 'WiFi, AC, Cupboard, Study Desk, Private Bathroom', TRUE);

-- Sample Settings
INSERT INTO hostel_settings (setting_key, setting_value) VALUES
('hostel_name', 'XYZ Hostel'),
('hostel_address', '123 College Street, Bangalore, Karnataka - 560001'),
('hostel_phone', '+91-80-12345678'),
('hostel_email', 'info@xyzhos.com'),
('warden_name', 'Mr. Hostel Warden'),
('warden_phone', '+91-98765432109');

SQL

echo ""
echo "✅ Database setup completed!"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "3️⃣  Verifying connection..."
sudo mysql -u root -e "SELECT COUNT(*) as users FROM hostel_management.users;" 2>&1 | grep -q "users" && echo "✅ Database is working!" || echo "❌ Error verifying database"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ MySQL Setup Complete!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Now you can:"
echo "1. cd /home/prajwal/Programs/Hostel"
echo "2. python app.py"
echo "3. Visit: http://10.252.129.72:5000"
echo ""
