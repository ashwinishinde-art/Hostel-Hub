#!/usr/bin/env python
"""
Update Hostel Information in Database
This script updates the hostel contact details and other information.
"""

import MySQLdb
from MySQLdb import cursors

def update_hostel_info():
    try:
        connection = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        print("\n" + "="*70)
        print("UPDATE HOSTEL INFORMATION")
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
            cursor.execute(
                "UPDATE hostel_settings SET setting_value = %s WHERE setting_key = %s",
                (setting_value, setting_key)
            )
            print(f"✓ {setting_key}: {setting_value}")
        
        connection.commit()
        
        # Verify updates
        print("\n" + "-"*70)
        print("UPDATED INFORMATION:")
        print("-"*70 + "\n")
        
        cursor.execute("""
            SELECT setting_key, setting_value 
            FROM hostel_settings 
            WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 'warden_phone')
            ORDER BY setting_key
        """)
        
        results = cursor.fetchall()
        
        for row in results:
            print(f"{row['setting_key']:20} : {row['setting_value']}")
        
        print("\n" + "="*70)
        print("✅ HOSTEL INFORMATION UPDATED SUCCESSFULLY")
        print("="*70)
        print("\nThe contact information will now display on:")
        print("- Contact Page (/contact)")
        print("- About Page")
        print("- Footer of all pages")
        print("\nHard refresh browser (Ctrl+Shift+R) to see changes")
        print("="*70 + "\n")
        
        cursor.close()
        connection.close()
        
    except MySQLdb.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\nMake sure MySQL is running:")
        print("   sudo service mysql start")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_hostel_info()
