#!/usr/bin/env python
"""
ROOM CAPACITY FIX - Direct Database Correction
This script checks for rooms with over-capacity allocations and fixes them.
"""

import MySQLdb
from MySQLdb import cursors

def fix_room_capacity():
    try:
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
        
        print("🔍 Checking room capacities...\n")
        
        # Get all rooms with their capacity and current occupancy
        cursor.execute("""
            SELECT r.id, r.room_number, r.capacity,
                   COUNT(ro.id) as active_occupants
            FROM rooms r
            LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
            GROUP BY r.id
            ORDER BY r.room_number
        """)
        
        rooms = cursor.fetchall()
        over_capacity_count = 0
        
        for room in rooms:
            room_id = room['id']
            room_number = room['room_number']
            capacity = room['capacity']
            occupants = room['active_occupants']
            
            if occupants > capacity:
                print(f"⚠️  ROOM {room_number}: OVER CAPACITY!")
                print(f"   Capacity: {capacity}, Active Students: {occupants}")
                print(f"   Excess: {occupants - capacity} student(s)\n")
                
                # Get the excess students
                cursor.execute("""
                    SELECT ro.id, u.full_name, u.id as student_id
                    FROM room_occupancy ro
                    JOIN users u ON ro.student_id = u.id
                    WHERE ro.room_id = %s AND ro.status = 'Active'
                    ORDER BY ro.id DESC
                    LIMIT %s
                """, (room_id, occupants - capacity))
                
                excess_students = cursor.fetchall()
                
                print(f"   Excess students to deallocate:")
                for student in excess_students:
                    print(f"     - {student['full_name']} (ID: {student['student_id']})")
                    # Mark as inactive instead of deleting
                    cursor.execute("""
                        UPDATE room_occupancy 
                        SET status = 'Inactive'
                        WHERE id = %s
                    """, (student['id'],))
                    print(f"       ✓ Deallocated (status set to 'Inactive')")
                
                over_capacity_count += 1
                print()
        
        connection.commit()
        
        if over_capacity_count == 0:
            print("✅ No rooms over capacity found!")
        else:
            print(f"\n✅ Fixed {over_capacity_count} room(s) with over-capacity issues")
            print("\n📊 Current Room Status:")
            
            # Show updated status
            cursor.execute("""
                SELECT r.id, r.room_number, r.capacity,
                       COUNT(ro.id) as active_occupants
                FROM rooms r
                LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
                GROUP BY r.id
                ORDER BY r.room_number
            """)
            
            rooms = cursor.fetchall()
            for room in rooms:
                status = "✓" if room['active_occupants'] <= room['capacity'] else "✗"
                print(f"  {status} Room {room['room_number']}: {room['active_occupants']}/{room['capacity']} occupied")
        
        cursor.close()
        connection.close()
        
    except MySQLdb.Error as e:
        print(f"❌ Database Error: {e}")
        print("\n⚠️  Make sure MySQL is running:")
        print("   sudo service mysql start")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("=" * 70)
    print("ROOM CAPACITY ENFORCEMENT - DATABASE FIX")
    print("=" * 70 + "\n")
    fix_room_capacity()
    print("\n" + "=" * 70)
