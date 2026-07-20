-- Update Hostel Settings with Correct Information
USE hostel_management;

UPDATE hostel_settings SET setting_value = 'Zeal Chowk, Narhe, Pune' WHERE setting_key = 'hostel_address';
UPDATE hostel_settings SET setting_value = '7030710886' WHERE setting_key = 'hostel_phone';
UPDATE hostel_settings SET setting_value = 'hostelhub@work.com' WHERE setting_key = 'hostel_email';

-- Verify updates
SELECT setting_key, setting_value FROM hostel_settings WHERE setting_key IN ('hostel_address', 'hostel_phone', 'hostel_email');
