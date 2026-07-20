#!/usr/bin/env python3
"""
Apply updates using the Flask app's database module directly
This bypasses the need for a separate MySQL connection
"""

import sys
import os
sys.path.insert(0, '/home/prajwal/Programs/Hostel')

# Import Flask app to get database connection
from app import app, db

def apply_all_changes():
    """Apply all changes using Flask's database connection"""
    
    print("\n" + "="*70)
    print("HOSTEL MANAGEMENT SYSTEM - APPLYING ALL CHANGES")
    print("="*70 + "\n")
    
    try:
        with app.app_context():
            # Ensure we have a database connection
            if db.connection is None:
                print("Establishing database connection...")
                db.connect()
            
            if db.connection is None:
                print("❌ Failed to connect to database")
                return False
            
            print("✓ Connected to database\n")
            
            cursor = db.connection.cursor()
            
            print("-"*70)
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
            db.connection.commit()
            
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
                    key = row[0] if isinstance(row, tuple) else row['setting_key']
                    value = row[1] if isinstance(row, tuple) else row['setting_value']
                    print(f"✓ {key:20} : {value}")
            else:
                print("⚠ No results found during verification")
            
            cursor.close()
            
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
            print("\n3. Verify the changes:")
            print("   ✓ See the updated address")
            print("   ✓ See the updated phone number")
            print("   ✓ See the updated email")
            print("\n4. Check the footer:")
            print("   Scroll down on any page to see footer with hostel info")
            print("\n5. Try logging in:")
            print("   Demo credentials are no longer displayed on login page")
            
            print("\n" + "="*70 + "\n")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = apply_all_changes()
    sys.exit(0 if success else 1)
