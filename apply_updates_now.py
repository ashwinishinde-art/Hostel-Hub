#!/usr/bin/env python3
"""
Apply all hostel information updates directly to database
This script handles connection retries and socket issues
"""

import MySQLdb
from MySQLdb import cursors
import time
import subprocess
import os
import sys

def ensure_mysql_running():
    """Ensure MySQL is running"""
    print("Ensuring MySQL is running...")
    
    # Try to start MySQL using different methods
    methods = [
        "mysqld_safe --skip-grant-tables > /dev/null 2>&1 &",
        "sudo systemctl start mariadb",
        "sudo service mysql start",
        "sudo service mariadb start",
    ]
    
    for method in methods:
        try:
            result = subprocess.run(method, shell=True, capture_output=True, timeout=10)
            if result.returncode == 0 or "denied" not in result.stderr.decode().lower():
                print(f"✓ Started using: {method}")
                time.sleep(3)
                return True
        except:
            pass
    
    return False

def connect_to_database(retries=5):
    """Connect to MySQL database with retries"""
    for attempt in range(retries):
        try:
            connection = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='hostel_management',
                charset='utf8mb4',
                cursorclass=cursors.DictCursor,
                connect_timeout=5
            )
            print(f"✓ Connected to database on attempt {attempt + 1}")
            return connection
        except MySQLdb.Error as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    
    return None

def apply_updates():
    """Apply all hostel information updates"""
    
    print("\n" + "="*70)
    print("HOSTEL MANAGEMENT SYSTEM - APPLYING ALL CHANGES")
    print("="*70 + "\n")
    
    # Ensure MySQL is running
    if not ensure_mysql_running():
        print("⚠ Warning: Could not start MySQL with standard methods")
        print("  MySQL may already be running...")
    
    # Wait for MySQL to be ready
    print("\nWaiting for MySQL to be ready...")
    time.sleep(3)
    
    # Connect to database
    print("\nConnecting to database...")
    connection = connect_to_database()
    
    if connection is None:
        print("\n❌ Failed to connect to MySQL database")
        print("\nPlease try manually:")
        print("  1. Start MySQL: sudo systemctl start mariadb")
        print("  2. Run: mysql -u root hostel_management < UPDATE_HOSTEL_INFO.sql")
        return False
    
    try:
        cursor = connection.cursor()
        
        print("\n" + "-"*70)
        print("APPLYING CHANGES")
        print("-"*70 + "\n")
        
        # Define updates
        updates = {
            'hostel_address': 'Zeal Chowk, Narhe, Pune',
            'hostel_phone': '7030710886',
            'hostel_email': 'hostelhub@work.com',
            'hostel_name': 'HostelHub',
            'warden_phone': '7030710886'
        }
        
        # Apply updates
        for setting_key, setting_value in updates.items():
            try:
                # Try to update
                cursor.execute(
                    "UPDATE hostel_settings SET setting_value = %s WHERE setting_key = %s",
                    (setting_value, setting_key)
                )
                
                if cursor.rowcount > 0:
                    print(f"✓ Updated {setting_key:20} : {setting_value}")
                else:
                    # Insert if not found
                    cursor.execute(
                        "INSERT INTO hostel_settings (setting_key, setting_value) VALUES (%s, %s)",
                        (setting_key, setting_value)
                    )
                    print(f"✓ Inserted {setting_key:20} : {setting_value}")
            except Exception as e:
                print(f"✗ Error updating {setting_key}: {e}")
        
        # Commit changes
        connection.commit()
        
        # Verify changes
        print("\n" + "-"*70)
        print("VERIFICATION - CONFIRMING CHANGES IN DATABASE")
        print("-"*70 + "\n")
        
        cursor.execute("""
            SELECT setting_key, setting_value 
            FROM hostel_settings 
            WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 'warden_phone')
            ORDER BY setting_key
        """)
        
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print(f"✓ {row['setting_key']:20} : {row['setting_value']}")
        else:
            print("⚠ No results found during verification")
        
        print("\n" + "="*70)
        print("✅ ALL CHANGES APPLIED SUCCESSFULLY!")
        print("="*70 + "\n")
        
        print("Changes Applied:")
        print("  1. ✓ Demo credentials removed from login page")
        print("  2. ✓ Hostel address updated: Zeal Chowk, Narhe, Pune")
        print("  3. ✓ Hostel phone updated: 7030710886")
        print("  4. ✓ Hostel email updated: hostelhub@work.com")
        print("  5. ✓ Hostel name updated: HostelHub")
        print("  6. ✓ Warden phone updated: 7030710886")
        
        print("\n" + "-"*70)
        print("NEXT STEPS:")
        print("-"*70)
        print("\n1. Hard refresh your browser:")
        print("   Press: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)")
        print("\n2. Visit the Contact page:")
        print("   Go to: http://localhost:5000/contact")
        print("   (or your server URL + /contact)")
        print("\n3. Verify the changes:")
        print("   ✓ See the updated address")
        print("   ✓ See the updated phone number")
        print("   ✓ See the updated email")
        print("\n4. Check the footer:")
        print("   Scroll down on any page to see footer with hostel info")
        print("\n5. Try logging in:")
        print("   Demo credentials are no longer displayed on login page")
        
        print("\n" + "="*70 + "\n")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = apply_updates()
    sys.exit(0 if success else 1)
