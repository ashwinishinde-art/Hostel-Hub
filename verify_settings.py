#!/usr/bin/env python3
"""
Verify that hostel settings are in database and can be retrieved
"""

import sys
sys.path.insert(0, '/home/prajwal/Programs/Hostel')

from app import app
from config.database import get_db_connection

def verify_settings():
    with app.app_context():
        try:
            connection = get_db_connection()
            if connection is None:
                print("❌ Database connection failed")
                return False
            
            cursor = connection.cursor()
            
            print("\n" + "="*70)
            print("VERIFYING HOSTEL SETTINGS IN DATABASE")
            print("="*70 + "\n")
            
            # Fetch all settings
            cursor.execute("SELECT setting_key, setting_value FROM hostel_settings ORDER BY setting_key")
            settings = cursor.fetchall()
            
            if not settings:
                print("❌ No settings found in database!")
                cursor.close()
                connection.close()
                return False
            
            print("✓ Settings found in database:\n")
            
            required_keys = ['hostel_address', 'hostel_email', 'hostel_name', 'hostel_phone', 
                            'warden_name', 'warden_phone', 'checkin_time', 'checkout_time',
                            'visitor_hours_start', 'visitor_hours_end']
            
            found_keys = set()
            for setting in settings:
                key = setting[0] if isinstance(setting, tuple) else setting['setting_key']
                value = setting[1] if isinstance(setting, tuple) else setting['setting_value']
                print(f"  {key:25} : {value}")
                found_keys.add(key)
            
            print("\n" + "-"*70)
            print("REQUIRED SETTINGS CHECK:")
            print("-"*70 + "\n")
            
            for key in required_keys:
                if key in found_keys:
                    print(f"  ✓ {key}")
                else:
                    print(f"  ✗ {key} - MISSING!")
            
            print("\n" + "="*70)
            
            # Specifically check the contact details
            print("CONTACT DETAILS VERIFICATION:")
            print("="*70 + "\n")
            
            contact_keys = {
                'hostel_address': 'Address',
                'hostel_phone': 'Phone',
                'hostel_email': 'Email'
            }
            
            cursor.execute("""
                SELECT setting_key, setting_value FROM hostel_settings 
                WHERE setting_key IN ('hostel_address', 'hostel_phone', 'hostel_email')
            """)
            
            contact_settings = cursor.fetchall()
            
            print("Expected values:")
            print("  Address: Zeal Chowk, Narhe, Pune")
            print("  Phone: 7030710886")
            print("  Email: hostelhub@work.com\n")
            
            print("Actual values in database:")
            for setting in contact_settings:
                key = setting[0] if isinstance(setting, tuple) else setting['setting_key']
                value = setting[1] if isinstance(setting, tuple) else setting['setting_value']
                print(f"  {contact_keys.get(key, key)}: {value}")
            
            print("\n" + "="*70)
            print("✅ VERIFICATION COMPLETE")
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
    verify_settings()
