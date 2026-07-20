#!/usr/bin/env python
"""
FIX ADMIN/WARDEN ROLES - Remove them from appearing in Student List
This script corrects the roles for admin and warden users.
"""

import MySQLdb
from MySQLdb import cursors

def fix_admin_warden_roles():
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
        print("FIX ADMIN/WARDEN ROLES - Remove from Student List")
        print("="*70 + "\n")
        
        # Step 1: Show current state
        print("1️⃣  Current User Roles:\n")
        
        cursor.execute("SELECT id, username, full_name, role FROM users ORDER BY role, full_name")
        users = cursor.fetchall()
        
        for user in users:
            print(f"   {user['username']:10} | {user['full_name']:20} | Role: {user['role']}")
        
        # Step 2: Fix admin and warden roles
        print("\n2️⃣  Fixing roles...\n")
        
        # Fix 'admin' user
        cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
        admin_updated = cursor.rowcount
        
        if admin_updated > 0:
            print(f"   ✓ Updated 'admin' user to role='admin'")
        
        # Fix 'warden' user  
        cursor.execute("UPDATE users SET role = 'warden' WHERE username = 'warden'")
        warden_updated = cursor.rowcount
        
        if warden_updated > 0:
            print(f"   ✓ Updated 'warden' user to role='warden'")
        
        if admin_updated == 0 and warden_updated == 0:
            print("   ℹ️  Admin and warden already have correct roles")
        
        connection.commit()
        
        # Step 3: Remove student records for admin/warden
        print("\n3️⃣  Removing student records for non-students...\n")
        
        cursor.execute("""
            DELETE FROM students 
            WHERE user_id IN (SELECT id FROM users WHERE role IN ('admin', 'warden'))
        """)
        deleted = cursor.rowcount
        
        if deleted > 0:
            print(f"   ✓ Deleted {deleted} orphaned student record(s)")
        else:
            print(f"   ℹ️  No orphaned student records found")
        
        connection.commit()
        
        # Step 4: Show final state
        print("\n4️⃣  Final User Roles:\n")
        
        cursor.execute("SELECT id, username, full_name, role FROM users ORDER BY role, full_name")
        users = cursor.fetchall()
        
        for user in users:
            status = "✓" if (user['username'] == 'admin' and user['role'] == 'admin') or \
                          (user['username'] == 'warden' and user['role'] == 'warden') or \
                          (user['role'] == 'student') else "✗"
            print(f"   {status} {user['username']:10} | {user['full_name']:20} | Role: {user['role']}")
        
        # Step 5: Show what student list will display
        print("\n5️⃣  Student List (What will display in Admin Dashboard):\n")
        
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.full_name, u.phone, u.role,
                   s.roll_number, s.branch, s.semester,
                   r.room_number
            FROM users u
            JOIN students s ON u.id = s.user_id
            LEFT JOIN room_occupancy ro ON u.id = ro.student_id AND ro.status = 'Active'
            LEFT JOIN rooms r ON ro.room_id = r.id
            WHERE u.role = 'student'
            ORDER BY u.full_name
        """)
        
        students = cursor.fetchall()
        
        if students:
            print(f"   Total Students: {len(students)}\n")
            for student in students:
                room = student['room_number'] if student['room_number'] else "Not Assigned"
                print(f"   {student['full_name']:20} | {student['roll_number']:10} | {student['branch']:8} | Room: {room}")
        else:
            print("   No students in the system")
        
        print("\n" + "="*70)
        print("✅ FIX COMPLETE")
        print("="*70)
        print("\nAdmin and warden are now removed from Student List!")
        print("Only actual students will appear in Admin Dashboard → Student Management")
        print("\nNext Steps:")
        print("1. Hard refresh browser: Ctrl+Shift+R")
        print("2. Navigate to Admin Dashboard → Student Management")
        print("3. Verify only students are displayed")
        print("="*70 + "\n")
        
        cursor.close()
        connection.close()
        
    except MySQLdb.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\n⚠️  MySQL is not running!")
        print("\nStart MySQL first:")
        print("   sudo service mysql start")
        print("\nThen run this script again:")
        print("   python fix_admin_warden_roles.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_admin_warden_roles()
