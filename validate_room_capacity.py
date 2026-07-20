#!/usr/bin/env python
"""
ROOM CAPACITY VALIDATOR - Prevents future over-capacity issues
Run this script periodically to ensure room capacity constraints are maintained.
"""

import MySQLdb
from MySQLdb import cursors

def validate_and_fix_capacity():
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
        
        print("\n🔐 ROOM CAPACITY VALIDATOR")
        print("=" * 70)
        
        # Step 1: Check for over-capacity situations
        print("\n1️⃣  Checking for over-capacity rooms...")
        cursor.execute("""
            SELECT r.id, r.room_number, r.capacity,
                   COUNT(ro.id) as active_count
            FROM rooms r
            LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
            GROUP BY r.id
            HAVING active_count > r.capacity
        """)
        
        over_capacity = cursor.fetchall()
        
        if over_capacity:
            print(f"   ⚠️  Found {len(over_capacity)} room(s) over capacity!")
            
            for room in over_capacity:
                excess = room['active_count'] - room['capacity']
                print(f"\n   Room {room['room_number']}:")
                print(f"     Capacity: {room['capacity']}")
                print(f"     Current: {room['active_count']}")
                print(f"     Excess: {excess} student(s)")
                
                # Get and deallocate excess students (keep oldest, deallocate newest)
                cursor.execute("""
                    SELECT ro.id, u.full_name, ro.check_in_date
                    FROM room_occupancy ro
                    JOIN users u ON ro.student_id = u.id
                    WHERE ro.room_id = %s AND ro.status = 'Active'
                    ORDER BY ro.check_in_date DESC
                    LIMIT %s
                """, (room['id'], excess))
                
                excess_students = cursor.fetchall()
                for student in excess_students:
                    cursor.execute("""
                        UPDATE room_occupancy 
                        SET status = 'Inactive'
                        WHERE id = %s
                    """, (student['id'],))
                    print(f"     ✓ Deallocated: {student['full_name']}")
        else:
            print("   ✅ No over-capacity rooms found!")
        
        connection.commit()
        
        # Step 2: Show current status
        print("\n2️⃣  Current Room Capacity Status:")
        print("   " + "-" * 66)
        
        cursor.execute("""
            SELECT r.id, r.room_number, r.capacity, r.room_type,
                   COUNT(ro.id) as active_count
            FROM rooms r
            LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
            GROUP BY r.id
            ORDER BY r.room_number
        """)
        
        all_rooms = cursor.fetchall()
        valid_count = 0
        
        for room in all_rooms:
            occupancy_pct = (room['active_count'] / room['capacity'] * 100) if room['capacity'] > 0 else 0
            status_icon = "✓" if room['active_count'] <= room['capacity'] else "✗"
            
            print(f"   {status_icon} Room {room['room_number']:4} | Type: {room['room_type']:15} | " +
                  f"Capacity: {room['capacity']} | Occupied: {room['active_count']} ({occupancy_pct:.0f}%)")
            
            if room['active_count'] <= room['capacity']:
                valid_count += 1
        
        print("   " + "-" * 66)
        print(f"   Valid Rooms: {valid_count}/{len(all_rooms)}")
        
        # Step 3: Validate constraints
        print("\n3️⃣  Validation Summary:")
        print("   " + "-" * 66)
        
        # Check for students with multiple active rooms
        cursor.execute("""
            SELECT student_id, COUNT(*) as room_count
            FROM room_occupancy
            WHERE status = 'Active'
            GROUP BY student_id
            HAVING room_count > 1
        """)
        
        multi_room = cursor.fetchall()
        if multi_room:
            print(f"   ⚠️  Found {len(multi_room)} student(s) with multiple active rooms!")
            for item in multi_room:
                cursor.execute("SELECT full_name FROM users WHERE id = %s", (item['student_id'],))
                student = cursor.fetchone()
                print(f"     - {student['full_name']}: {item['room_count']} active rooms")
        else:
            print("   ✓ No students with multiple active rooms")
        
        # Check for duplicate allocations (same student, same room)
        cursor.execute("""
            SELECT room_id, student_id, COUNT(*) as count
            FROM room_occupancy
            WHERE status = 'Active'
            GROUP BY room_id, student_id
            HAVING count > 1
        """)
        
        duplicates = cursor.fetchall()
        if duplicates:
            print(f"   ⚠️  Found {len(duplicates)} duplicate allocation(s)!")
        else:
            print("   ✓ No duplicate allocations")
        
        print("\n" + "=" * 70)
        print("✅ VALIDATION COMPLETE")
        print("=" * 70 + "\n")
        
        cursor.close()
        connection.close()
        
    except MySQLdb.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\n⚠️  Make sure MySQL is running:")
        print("   sudo service mysql start")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    validate_and_fix_capacity()
