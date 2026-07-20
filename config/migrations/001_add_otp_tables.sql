-- Add OTP Password Reset Table to Hostel Management System

CREATE TABLE IF NOT EXISTS password_reset_otp (
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

-- Add password_reset_token to track reset requests
CREATE TABLE IF NOT EXISTS password_reset_tokens (
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
