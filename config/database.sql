-- Hostel Management System Database Schema
DROP DATABASE IF EXISTS hostel_management;
CREATE DATABASE hostel_management;
USE hostel_management;

-- Users Table (Admin, Student, Warden)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student', 'warden') NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    gender ENUM('Male', 'Female') NULL,
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
    gender_occupancy ENUM('Boys', 'Girls', 'Mixed') DEFAULT 'Mixed',
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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

-- Students Table (Additional student-specific info)
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

-- Hostel Settings Table
CREATE TABLE hostel_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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

-- Create Indexes for Performance
CREATE INDEX idx_student_user ON students(user_id);
CREATE INDEX idx_room_occupancy_student ON room_occupancy(student_id);
CREATE INDEX idx_room_occupancy_room ON room_occupancy(room_id);
CREATE INDEX idx_complaints_student ON complaints(student_id);
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_visitors_student ON visitors(student_id);
CREATE INDEX idx_fees_student ON fees(student_id);
CREATE INDEX idx_notices_created ON notices(created_at);
CREATE INDEX idx_gallery_category ON gallery(category);
CREATE INDEX idx_users_role ON users(role);

-- Insert Sample Data

-- Sample Users (Passwords hashed using bcrypt: admin123, student123, warden123)
INSERT INTO users (username, email, password_hash, role, full_name, phone, gender, is_active) VALUES
('admin', 'admin@hostel.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'admin', 'Admin User', '9000000001', 'Male', TRUE),
('warden', 'warden@hostel.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'warden', 'Hostel Warden', '9000000002', 'Male', TRUE),
('prajwal', 'prajwal@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Prajwal Tandekar', '9876543210', 'Male', TRUE),
('rajdeep', 'rajdeep@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Rajdeep Patil', '9123456789', 'Male', TRUE),
('rutuja', 'rutuja@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Rutuja Patil', '9876123450', 'Female', TRUE);

-- Sample Rooms
INSERT INTO rooms (room_number, floor, room_type, capacity, rent, amenities, is_available) VALUES
('101', 1, 'Double Sharing', 2, 5000, 'WiFi, AC, Cupboard, Study Desk', TRUE),
('102', 1, 'Double Sharing', 2, 5000, 'WiFi, AC, Cupboard, Study Desk', TRUE),
('103', 1, 'Single Deluxe', 1, 7000, 'WiFi, AC, Cupboard, Study Desk, Private Bathroom', TRUE),
('201', 2, 'Triple Sharing', 3, 4000, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
('202', 2, 'Single Deluxe', 1, 7000, 'WiFi, AC, Cupboard, Study Desk, Private Bathroom', TRUE),
('203', 2, 'Double Sharing', 2, 5000, 'WiFi, AC, Cupboard, Study Desk', FALSE),
('301', 3, 'Quad Sharing', 4, 3500, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
('302', 3, 'Triple Sharing', 3, 4000, 'WiFi, AC, Cupboard, Study Desk', TRUE);

-- Sample Students Info
INSERT INTO students (user_id, roll_number, branch, semester, contact_person_name, contact_person_phone, emergency_contact_phone, address, city, state, pincode) VALUES
(3, 'CO1265', 'CSE', 4, 'Ramesh Tandekar', '9876543211', '9876543210', '123 Main St', 'Bangalore', 'Karnataka', '560001'),
(4, 'CO1288', 'E&TC', 4, 'Rajesh Patil', '9123456790', '9123456789', '456 Oak Ave', 'Bangalore', 'Karnataka', '560002'),
(5, 'CO1240', 'IT', 4, 'Suresh Patil', '9876123451', '9876123450', '789 Pine Rd', 'Bangalore', 'Karnataka', '560003');

-- Sample Room Occupancy
INSERT INTO room_occupancy (room_id, student_id, check_in_date, status) VALUES
(1, 3, '2024-06-01', 'Active'),
(3, 4, '2024-06-01', 'Active'),
(4, 5, '2024-06-01', 'Active');

-- Sample Complaints
INSERT INTO complaints (student_id, room_id, category, title, description, status, priority, assigned_to) VALUES
(3, 1, 'Plumbing', 'Water Leakage', 'Water leaking from the common bathroom ceiling', 'In Progress', 'High', 2),
(4, 3, 'Electrical', 'Ceiling Fan Problem', 'Ceiling fan regulator not working properly', 'Resolved', 'Medium', 2),
(5, 4, 'Cleanliness', 'Common Area Not Clean', 'Common room not cleaned regularly', 'Pending', 'Low', NULL);

-- Sample Notices
INSERT INTO notices (title, content, category, created_by, is_pinned, priority, visibility) VALUES
('Welcome to Hostel Management System', 'This is your new hostel management portal. Please update your profile and register complaints as needed.', 'General', 1, TRUE, 'High', 'All'),
('WiFi Maintenance Scheduled', 'WiFi will be down on Saturday 10 AM to 2 PM for maintenance. Please plan accordingly.', 'Maintenance', 1, FALSE, 'Medium', 'All'),
('Fee Payment Deadline', 'All fees must be paid by 30th July 2024. Late payments will incur a 2% fine.', 'Important', 1, TRUE, 'High', 'Students');

-- Sample Gallery
INSERT INTO gallery (title, description, category, image_path, uploaded_by, is_featured, display_order) VALUES
('Hostel Front View', 'Beautiful front view of our hostel building', 'Building', '/static/images/gallery/hostel_front.jpg', 1, TRUE, 1),
('Student Room', 'Comfortable and spacious student rooms', 'Rooms', '/static/images/gallery/student_room.jpg', 1, TRUE, 2),
('Mess Hall', 'Hygienic mess hall with quality food', 'Mess', '/static/images/gallery/mess_hall.jpg', 1, TRUE, 3),
('Gym Facility', 'Well-equipped gym for fitness activities', 'Gym', '/static/images/gallery/gym.jpg', 1, FALSE, 4);

-- Sample Hostel Settings
INSERT INTO hostel_settings (setting_key, setting_value) VALUES
('hostel_name', 'HostelHub'),
('hostel_address', 'Zeal Chowk, Narhe, Pune'),
('hostel_phone', '7030710886'),
('hostel_email', 'hostelhub@work.com'),
('warden_name', 'Hostel Warden'),
('warden_phone', '7030710886'),
('academic_year', '2024-2025'),
('checkout_time', '10:00 AM'),
('checkin_time', '2:00 PM'),
('visitor_hours_start', '10:00 AM'),
('visitor_hours_end', '6:00 PM'),
('room_rent_per_month', '5000');

-- Sample Fees
INSERT INTO fees (student_id, academic_year, semester, room_rent, mess_fee, utilities_fee, other_charges, total_amount, pending_amount, due_date, payment_status) VALUES
(3, '2024-2025', 4, 5000, 2500, 500, 0, 8000, 8000, '2024-07-30', 'Pending'),
(4, '2024-2025', 4, 7000, 2500, 500, 0, 10000, 0, '2024-07-30', 'Paid'),
(5, '2024-2025', 4, 4000, 2500, 500, 0, 7000, 3500, '2024-07-30', 'Partial');

-- Sample Visitors
INSERT INTO visitors (student_id, visitor_name, visitor_phone, visitor_relation, visit_date, visit_time, expected_departure, purpose, status, approved_by) VALUES
(3, 'Ramesh Tandekar', '9876543211', 'Father', '2024-07-20', '10:00:00', '16:00:00', 'Family Visit', 'Approved', 2),
(4, 'Priya Patil', '9123456790', 'Sister', '2024-07-22', '14:00:00', '18:00:00', 'Social Visit', 'Pending', NULL),
(5, 'Suresh Patil', '9876123451', 'Father', '2024-07-18', '10:00:00', '14:00:00', 'Family Visit', 'Approved', 2);


-- Password Reset OTP Table
CREATE TABLE password_reset_otp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    otp_code VARCHAR(10) NOT NULL,
    otp_method ENUM('email', 'sms') DEFAULT 'email',
    is_verified BOOLEAN DEFAULT FALSE,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    verified_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_otp (user_id),
    INDEX idx_email_otp (email),
    INDEX idx_phone_otp (phone),
    INDEX idx_expires_at (expires_at)
);

-- Password Reset Tokens Table
CREATE TABLE password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(100) UNIQUE NOT NULL,
    otp_id INT NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    reset_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (otp_id) REFERENCES password_reset_otp(id) ON DELETE CASCADE,
    INDEX idx_user_token (user_id),
    INDEX idx_token (token),
    INDEX idx_expires_at (expires_at)
);