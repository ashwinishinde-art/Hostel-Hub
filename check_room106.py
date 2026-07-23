from config.database_mock import db
cursor = db.connection.cursor()

print("=== All rooms with occupants and genders ===")
cursor.execute("SELECT * FROM room_occupancy")
occupancies = cursor.fetchall()

from collections import defaultdict
rooms = defaultdict(list)
for o in occupancies:
    cursor.execute("SELECT id, full_name, gender FROM users WHERE id = %s", (o['student_id'],))
    u = cursor.fetchone()
    if u:
        rooms[o['room_id']].append({
            'user_id': u['id'],
            'name': u['full_name'],
            'gender': u.get('gender', 'NOT SET'),
            'status': o.get('status', 'N/A')
        })

for room_id, people in sorted(rooms.items()):
    cursor.execute("SELECT room_number, room_type, capacity FROM rooms WHERE id = %s", (room_id,))
    r = cursor.fetchone()
    genders = set(p['gender'] for p in people)
    mixed = "*** MIXED GENDER ***" if len(genders) > 1 else ""
    print(f"\nRoom {r['room_number']} ({r['room_type']}, cap={r['capacity']}) {mixed}")
    for p in people:
        print(f"  - {p['name']} | gender={p['gender']} | status={p['status']}")

cursor.close()
