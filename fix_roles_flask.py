#!/usr/bin/env python
"""
FIX ADMIN/WARDEN ROLES using Flask app context
Run this from the Hostel directory: python fix_roles_flask.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '/home/prajwal/Programs/Hostel')

from app import app
from config.database import get_db_connection

def fix_roles():
    with app.app_context():
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            print("\n" + "="*70)
            print("FIX ADMIN/WARDEN ROLES - Remove from Student List")
            print("="*70 + "\n")
            
            # Step 1: Show current state
            print("1️⃣  Current User Roles:\n")
            
            cursor.execute("SELECT id, username, full_name, role FROM users ORDER BY role, full_name")
            users = cursor.fetchall()
            
            for user in users:
                print(f"   {user[1]:10} | {user[2]:20} | Role: {user[3]}")
            
            # Step 2: Fix admin and warden roles
            print("\n2️⃣  Fixing roles...\n")
            
            # Fix 'admin' user
            cursor.execute("UPDATE users SET role = %s WHERE username = %s", ('admin', 'admin'))
            admin_updated = cursor.rowcount
            
            if admin_updated > 0:
                print(f"   ✓ Updated 'admin' user to role='admin'")
            
            # Fix 'warden' user  
            cursor.execute("UPDATE users SET role = %s WHERE username = %s", ('warden', 'warden'))
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
                status = "✓" if (user[1] == 'admin' and user[3] == 'admin') or \
                              (user[1] == 'warden' and user[3] == 'warden') or \
                              (user[3] == 'student') else "✗"
                print(f"   {status} {user[1]:10} | {user[2]:20} | Role: {user[3]}")
            
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
                    room = student[9] if student[9] else "Not Assigned"
                    print(f"   {student[3]:20} | {student[6]:10} | {student[7]:8} | Room: {room}")
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
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_roles()
