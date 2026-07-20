#!/usr/bin/env python
"""
Direct update of hostel information by connecting to the running Flask database
"""

import MySQLdb
from MySQLdb import cursors

def update_hostel_info():
    try:
        print("\n" + "="*70)
        print("APPLYING HOSTEL INFORMATION UPDATES")
        print("="*70 + "\n")
        
        # Connect to database
        connection = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        # Updates to apply
        updates = {
            'hostel_address': 'Zeal Chowk, Narhe, Pune',
            'hostel_phone': '7030710886',
            'hostel_email': 'hostelhub@work.com',
            'hostel_name': 'HostelHub',
            'warden_phone': '7030710886'
        }
        
        print("Updating hostel information...\n")
        
        for setting_key, setting_value in updates.items():
            # Try to update
            cursor.execute(
                "UPDATE hostel_settings SET setting_value = %s WHERE setting_key = %s",
                (setting_value, setting_key)
            )
            
            # If no rows affected, insert
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
        
        for row in results:
            print(f"{row['setting_key']:20} : {row['setting_value']}")
        
        print("\n" + "="*70)
        print("✅ HOSTEL INFORMATION UPDATED SUCCESSFULLY")
        print("="*70)
        print("\nChanges applied:")
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
        
    except MySQLdb.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\nMake sure:")
        print("- MySQL is running")
        print("- Database 'hostel_management' exists")
        print("- Correct credentials (user: root, password: empty)")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = update_hostel_info()
    sys.exit(0 if success else 1)
