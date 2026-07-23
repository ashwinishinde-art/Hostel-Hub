#!/usr/bin/env python
"""Debug login issue"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from config.database_mock import db

print("Testing login query...")
print("=" * 60)

try:
    cursor = db.connection.cursor()
    print("✓ Got cursor")
    
    # Test the login query
    username = "prajwal"
    print(f"\nQuery: SELECT id, username, email, role, full_name, password_hash, phone, gender FROM users WHERE username = '{username}' AND is_active = TRUE")
    
    cursor.execute("SELECT id, username, email, role, full_name, password_hash, phone, gender FROM users WHERE username = %s AND is_active = TRUE", (username,))
    print("✓ Query executed")
    
    result = cursor.fetchone()
    print(f"✓ Result: {result}")
    
    if result:
        print(f"\nUser data retrieved:")
        print(f"  ID: {result.get('id')}")
        print(f"  Username: {result.get('username')}")
        print(f"  Email: {result.get('email')}")
        print(f"  Role: {result.get('role')}")
        print(f"  Full Name: {result.get('full_name')}")
        print(f"  Password Hash: {str(result.get('password_hash'))[:30]}...")
        print(f"  Phone: {result.get('phone')}")
        print(f"  Gender: {result.get('gender')}")
    else:
        print(f"✗ No user found with username '{username}'")
        
        # List all users
        print("\nAll users in database:")
        cursor.execute("SELECT id, username, role FROM users")
        all_users = cursor.fetchall()
        for u in all_users:
            print(f"  ID {u.get('id')}: {u.get('username')} ({u.get('role')})")
    
    cursor.close()
    print("\n✓ Test completed successfully")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
