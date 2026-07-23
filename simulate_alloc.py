"""
Simulate the full admin allocate_room POST flow to find the exact error.
"""
import traceback
from config.database_mock import db
from datetime import datetime

def simulate_allocate(student_id, room_id):
    print(f"\n--- Allocating student_id={student_id} to room_id={room_id} ---")
    try:
        cursor = db.connection.cursor()
        check_in_date = datetime.now().strftime('%Y-%m-%d')

        # Step 1: Get student gender
        cursor.execute("SELECT gender FROM users WHERE id = %s", (student_id,))
        student_result = cursor.fetchone()
        print(f"  Student result: {student_result}")
        if not student_result:
            print("  ERROR: Student not found")
            return

        student_gender = student_result.get('gender') if isinstance(student_result, dict) else student_result[0]
        print(f"  Gender: {student_gender}")

        if not student_gender:
            print("  ERROR: No gender set")
            return

        # Step 2: Get room capacity and gender
        cursor.execute("SELECT capacity, gender_occupancy FROM rooms WHERE id = %s", (room_id,))
        room_result = cursor.fetchone()
        print(f"  Room result: {room_result}")

        room_capacity = room_result.get('capacity') if isinstance(room_result, dict) else room_result[0]
        room_gender = room_result.get('gender_occupancy') if isinstance(room_result, dict) else room_result[1]
        print(f"  Capacity: {room_capacity}, Gender: {room_gender}")

        # Step 3: Count current occupants
        cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE room_id = %s AND status = 'Active'", (room_id,))
        count_result = cursor.fetchone()
        current_count = count_result.get('count', 0) if count_result else 0
        print(f"  Current occupants: {current_count}/{room_capacity}")

        if current_count >= room_capacity:
            print(f"  ERROR: Room is full")
            return

        # Step 4: Check existing allocation
        cursor.execute("SELECT id FROM room_occupancy WHERE student_id = %s AND status = 'Active'", (student_id,))
        existing = cursor.fetchone()
        print(f"  Existing allocation: {existing}")
        if existing:
            print("  ERROR: Student already has a room")
            return

        # Step 5: INSERT
        cursor.execute("""
            INSERT INTO room_occupancy (room_id, student_id, check_in_date, status)
            VALUES (%s, %s, %s, 'Active')
        """, (room_id, student_id, check_in_date))
        db.connection.commit()

        # Step 6: Verify it was saved
        cursor.execute("SELECT * FROM room_occupancy WHERE student_id = %s AND status = 'Active'", (student_id,))
        saved = cursor.fetchone()
        print(f"  Saved record: {saved}")

        # Step 7: Test dashboard query
        cursor.execute("SELECT * FROM room_occupancy WHERE student_id = %s", (student_id,))
        dash = cursor.fetchone()
        if dash:
            cursor.execute("SELECT * FROM rooms WHERE id = %s", (dash.get('room_id'),))
            room = cursor.fetchone()
            print(f"  Dashboard would show: Room {room.get('room_number') if room else 'N/A'}")
        
        print("  SUCCESS!")
        cursor.close()

    except Exception as e:
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()

# Check current state first
print("=== Current room_occupancy ===")
cursor = db.connection.cursor()
cursor.execute("SELECT * FROM room_occupancy")
for r in cursor.fetchall():
    print(f"  {r}")
cursor.close()

# Try allocating a room to a student that has no room yet
# Since all students are allocated, let's test with a fresh scenario
# First check who has rooms
print("\n=== Who has rooms ===")
cursor = db.connection.cursor()
for uid in [10,11,12,13,14,16]:
    cursor.execute("SELECT * FROM room_occupancy WHERE student_id = %s AND status = 'Active'", (uid,))
    r = cursor.fetchone()
    print(f"  user_id={uid}: {'Room '+str(r.get('room_id')) if r else 'NO ROOM'}")
cursor.close()

print("\n=== Simulating allocation of Rushikesh(10) to room 9 (he already has it - expect error) ===")
simulate_allocate(10, 9)

print("\n=== Simulating allocation of Rushikesh(10) to room 15 (empty room) ===")
# First remove his current allocation temporarily
cursor = db.connection.cursor()
cursor.execute("SELECT * FROM room_occupancy WHERE student_id = %s", (10,))
print(f"Rushikesh current: {cursor.fetchall()}")
cursor.close()
