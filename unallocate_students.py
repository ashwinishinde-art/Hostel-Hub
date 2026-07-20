#!/usr/bin/env python3
"""
Script to unallocate all students from rooms without unregistering them.
This sets all active room allocations to 'Inactive' status.
"""

import os
import sys

# Try importing database
try:
    from config.database import db
    use_app_db = True
except Exception as e:
    print(f"Warning: Could not import database module: {e}")
    print("Attempting direct MySQL connection...\n")
    use_app_db = False
    import MySQLdb
    from MySQLdb.cursors import DictCursor

def unallocate_all_students():
    """Unallocate all students from their rooms"""
    try:
        # Connect to database directly if app db not available
        if use_app_db:
            cursor = db.connection.cursor()
        else:
            from dotenv import load_dotenv
            load_dotenv()
            connection = MySQLdb.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                passwd=os.getenv('MYSQL_PASSWORD', ''),
                db=os.getenv('MYSQL_DB', 'hostel_management'),
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            cursor = connection.cursor()
        
        # Get count of students to be unallocated
        cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE status = 'Active'")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        if count == 0:
            print("✓ No students currently allocated to rooms.")
            cursor.close()
            if not use_app_db:
                connection.close()
            return True
        
        print(f"\n📊 Found {count} student(s) allocated to rooms.")
        print("\n" + "="*60)
        
        # Get details of students to be unallocated
        cursor.execute("""
            SELECT ro.id, u.full_name, s.roll_number, r.room_number, ro.check_in_date
            FROM room_occupancy ro
            JOIN users u ON ro.student_id = u.id
            JOIN students s ON u.id = s.user_id
            JOIN rooms r ON ro.room_id = r.id
            WHERE ro.status = 'Active'
            ORDER BY r.room_number
        """)
        
        students_to_unallocate = cursor.fetchall()
        
        print("\n📋 Students Currently Allocated:")
        print("-" * 60)
        for i, student in enumerate(students_to_unallocate, 1):
            print(f"{i}. {student['full_name']} ({student['roll_number']}) - Room {student['room_number']}")
        
        print("\n" + "="*60)
        
        # Ask for confirmation
        confirmation = input(f"\n⚠️  Are you sure you want to unallocate all {count} student(s)? (yes/no): ").strip().lower()
        
        if confirmation != 'yes':
            print("❌ Operation cancelled.")
            cursor.close()
            if not use_app_db:
                connection.close()
            return False
        
        # Unallocate all students
        cursor.execute("""
            UPDATE room_occupancy 
            SET status = 'Inactive'
            WHERE status = 'Active'
        """)
        
        if use_app_db:
            db.connection.commit()
        else:
            connection.commit()
        
        print(f"\n✅ Successfully unallocated {count} student(s) from rooms!")
        print("\n📝 Details:")
        print("-" * 60)
        for student in students_to_unallocate:
            print(f"✓ {student['full_name']} unallocated from Room {student['room_number']}")
        
        print("\n✨ All students remain registered. They just lost their room allocations.")
        print("="*60 + "\n")
        
        cursor.close()
        if not use_app_db:
            connection.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error during unallocation: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            if use_app_db:
                db.connection.rollback()
            else:
                connection.rollback()
        except:
            pass
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏠 HOSTEL MANAGEMENT SYSTEM - STUDENT UNALLOCATION")
    print("="*60)
    
    success = unallocate_all_students()
    sys.exit(0 if success else 1)
