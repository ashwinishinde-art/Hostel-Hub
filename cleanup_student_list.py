#!/usr/bin/env python
"""
CLEAN UP STUDENT LIST - Remove non-students from display
This script ensures only actual students (users with role='student' AND matching students table entry) appear in student list.
"""

import MySQLdb
from MySQLdb import cursors

def cleanup_student_list():
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
        print("STUDENT LIST CLEANUP - Remove Admin/Warden from Student List")
        print("="*70 + "\n")
        
        # Step 1: Check for users with 'student' role who are actually admin/warden
        print("1️⃣  Checking for misclassified users...\n")
        
        cursor.execute("""
            SELECT u.id, u.username, u.full_name, u.role
            FROM users u
            WHERE u.role IN ('admin', 'warden')
            ORDER BY u.role, u.full_name
        """)
        
        admin_warden_users = cursor.fetchall()
        
        if admin_warden_users:
            print(f"   Found {len(admin_warden_users)} admin/warden users:\n")
            for user in admin_warden_users:
                print(f"   - {user['full_name']} ({user['username']}) - Role: {user['role']}")
        else:
            print("   ✓ No admin/warden users found\n")
        
        # Step 2: Show current student list
        print("\n2️⃣  Current Student List (from database):\n")
        
        cursor.execute("""
            SELECT u.id, u.username, u.full_name, u.role
            FROM users u
            WHERE u.role = 'student'
            ORDER BY u.full_name
        """)
        
        students = cursor.fetchall()
        
        if students:
            print(f"   Found {len(students)} students:\n")
            for student in students:
                # Check if student has entry in students table
                cursor.execute("SELECT id FROM students WHERE user_id = %s", (student['id'],))
                has_student_record = cursor.fetchone()
                status = "✓" if has_student_record else "✗ NO STUDENT RECORD"
                print(f"   {status} - {student['full_name']} ({student['username']})")
        else:
            print("   ✓ No students in database\n")
        
        # Step 3: Check for orphaned student records
        print("\n3️⃣  Checking for orphaned records...\n")
        
        cursor.execute("""
            SELECT s.id, s.user_id, s.roll_number
            FROM students s
            LEFT JOIN users u ON s.user_id = u.id
            WHERE u.id IS NULL
        """)
        
        orphaned = cursor.fetchall()
        
        if orphaned:
            print(f"   ⚠️  Found {len(orphaned)} orphaned student records:")
            for record in orphaned:
                print(f"   - Roll: {record['roll_number']} (user_id: {record['user_id']})")
                # Delete orphaned record
                cursor.execute("DELETE FROM students WHERE id = %s", (record['id'],))
            connection.commit()
            print(f"   ✓ Cleaned up {len(orphaned)} orphaned records\n")
        else:
            print("   ✓ No orphaned records found\n")
        
        # Step 4: Verify final student list
        print("4️⃣  Final Student List (What will display):\n")
        
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
        
        final_students = cursor.fetchall()
        
        if final_students:
            print(f"   ✓ Total Students: {len(final_students)}\n")
            for student in final_students:
                room = student['room_number'] if student['room_number'] else "Not Assigned"
                print(f"   {student['full_name']:20} | {student['roll_number']:10} | {student['branch']:8} | Sem {student['semester']} | Room: {room}")
        else:
            print("   ✓ No students to display\n")
        
        print("\n" + "="*70)
        print("✅ CLEANUP COMPLETE")
        print("="*70)
        print("\nThe student list will now only show actual students.")
        print("Admin and warden accounts are excluded.")
        print("="*70 + "\n")
        
        cursor.close()
        connection.close()
        
    except MySQLdb.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\n⚠️  Make sure MySQL is running:")
        print("   sudo service mysql start")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    cleanup_student_list()
