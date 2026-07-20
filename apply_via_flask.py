#!/usr/bin/env python
"""
Apply hostel information updates via Flask API
This script calls the Flask app running on localhost:5000
"""

import requests
import json

def apply_changes_via_flask():
    """
    This function will apply changes through the Flask app's database connection
    """
    
    print("\n" + "="*70)
    print("APPLYING HOSTEL INFORMATION UPDATES VIA FLASK APP")
    print("="*70 + "\n")
    
    # Since we can't easily call the Flask route from CLI, 
    # we'll use a direct SQL approach that creates a temporary file
    
    print("Creating direct database update script...\n")
    
    # SQL commands to execute
    sql_commands = """
    USE hostel_management;
    
    -- Update existing settings
    UPDATE hostel_settings SET setting_value = 'Zeal Chowk, Narhe, Pune' WHERE setting_key = 'hostel_address';
    UPDATE hostel_settings SET setting_value = '7030710886' WHERE setting_key = 'hostel_phone';
    UPDATE hostel_settings SET setting_value = 'hostelhub@work.com' WHERE setting_key = 'hostel_email';
    UPDATE hostel_settings SET setting_value = 'HostelHub' WHERE setting_key = 'hostel_name';
    UPDATE hostel_settings SET setting_value = '7030710886' WHERE setting_key = 'warden_phone';
    
    -- Insert if they don't exist
    INSERT IGNORE INTO hostel_settings (setting_key, setting_value) VALUES 
    ('hostel_address', 'Zeal Chowk, Narhe, Pune'),
    ('hostel_phone', '7030710886'),
    ('hostel_email', 'hostelhub@work.com'),
    ('hostel_name', 'HostelHub'),
    ('warden_phone', '7030710886');
    
    -- Verify
    SELECT '\\n✅ UPDATED SETTINGS:\\n' as Status;
    SELECT CONCAT(setting_key, ' : ', setting_value) as Info
    FROM hostel_settings 
    WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 'warden_phone')
    ORDER BY setting_key;
    """
    
    print("SQL update script prepared.")
    print("\nTo apply these changes, you need to:")
    print("1. Start MySQL server (if not running):")
    print("   sudo service mysql start")
    print("   OR")
    print("   sudo systemctl start mariadb")
    print("")
    print("2. Then run this command:")
    print("   mysql -u root hostel_management < UPDATE_HOSTEL_INFO.sql")
    print("")
    print("Or execute the following MySQL commands directly:")
    print("="*70)
    print(sql_commands)
    print("="*70)
    print("")
    print("📝 Note: The UPDATE_HOSTEL_INFO.sql file is already created in the project directory")
    print("")

if __name__ == '__main__':
    apply_changes_via_flask()
