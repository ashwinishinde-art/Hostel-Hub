#!/usr/bin/env python
"""
Apply Hostel Information Updates
This script connects through the running Flask app to update hostel settings.
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, '/home/prajwal/Programs/Hostel')

from app import app
from config.database import get_db_connection

def apply_changes():
    try:
        # Get database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        print("\n" + "="*70)
        print("APPLYING HOSTEL INFORMATION UPDATES")
        print("="*70 + "\n")
        
        # Update settings
        updates = {
            'hostel_address': 'Zeal Chowk, Narhe, Pune',
            'hostel_phone': '7030710886',
            'hostel_email': 'hostelhub@work.com',
            'hostel_name': 'HostelHub',
            'warden_phone': '7030710886'
        }
        
        print("Updating hostel information...\n")
        
        for setting_key, setting_value in updates.items():
            # First try to update existing record
            cursor.execute(
                "UPDATE hostel_settings SET setting_value = %s WHERE setting_key = %s",
                (setting_value, setting_key)
            )
            
            # If no rows were updated, insert new record
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO hostel_settings (setting_key, setting_value) VALUES (%s, %s)",
                    (setting_key, setting_value)
                )
            
            print(f"✓ {setting_key:20} : {setting_value}")
        
        connection.commit()
        
        # Verify updates
        print("\n" + "-"*70)
        print("VERIFICATION - UPDATED SETTINGS:")
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
                print(f"{row[0]:20} : {row[1]}")
        else:
            print("No results found - checking all settings...")
            cursor.execute("SELECT setting_key, setting_value FROM hostel_settings LIMIT 10")
            for row in cursor.fetchall():
                print(f"{row[0]:20} : {row[1]}")
        
        print("\n" + "="*70)
        print("✅ HOSTEL INFORMATION UPDATED SUCCESSFULLY")
        print("="*70)
        print("\nChanges applied to database:")
        print("- Address: Zeal Chowk, Narhe, Pune")
        print("- Phone: 7030710886")
        print("- Email: hostelhub@work.com")
        print("\nTo see the changes:")
        print("1. Hard refresh browser: Ctrl+Shift+R")
        print("2. Visit /contact page")
        print("3. Check footer on any page")
        print("="*70 + "\n")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = apply_changes()
    sys.exit(0 if success else 1)
