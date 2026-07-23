import json

with open('data/mock_db.json', 'r') as f:
    data = json.load(f)

# Fix room_occupancy - student_id must be user_id (what current_user.id returns)
# Nandini(11), Rutuja Chaudhari(12), Srushti(13) -> room 6 (Female Triple)
# Prajwal(14)  -> room 7  (Male Single)
# Rushikesh(10) -> room 9 (Male Triple)
# Anushka(16)  -> room 11 (Female Double)
data['room_occupancy'] = [
    {'id': 1, 'student_id': 11, 'room_id': 6,  'check_in_date': '2026-07-23', 'status': 'Active', 'created_at': '2026-07-23 09:52:00'},
    {'id': 2, 'student_id': 12, 'room_id': 6,  'check_in_date': '2026-07-23', 'status': 'Active', 'created_at': '2026-07-23 09:52:00'},
    {'id': 3, 'student_id': 13, 'room_id': 6,  'check_in_date': '2026-07-23', 'status': 'Active', 'created_at': '2026-07-23 09:52:00'},
    {'id': 4, 'student_id': 14, 'room_id': 7,  'check_in_date': '2026-07-23', 'status': 'Active', 'created_at': '2026-07-23 09:52:00'},
    {'id': 5, 'student_id': 10, 'room_id': 9,  'check_in_date': '2026-07-23', 'status': 'Active', 'created_at': '2026-07-23 09:52:00'},
    {'id': 6, 'student_id': 16, 'room_id': 11, 'check_in_date': '2026-07-23', 'status': 'Active', 'created_at': '2026-07-23 09:52:00'},
]

# Recalculate room occupied_count and status from occupancy
room_counts = {}
for occ in data['room_occupancy']:
    rid = occ['room_id']
    room_counts[rid] = room_counts.get(rid, 0) + 1

gender_map = {6: 'Female', 7: 'Male', 9: 'Male', 11: 'Female'}

for room in data['rooms']:
    count = room_counts.get(room['id'], 0)
    room['occupied_count'] = count
    cap = room.get('capacity', 1)
    if count == 0:
        room['status'] = 'vacant'
        room.pop('gender_occupancy', None)
    elif count >= cap:
        room['status'] = 'full'
    else:
        room['status'] = 'occupied'
    if room['id'] in gender_map:
        room['gender_occupancy'] = gender_map[room['id']]

with open('data/mock_db.json', 'w') as f:
    json.dump(data, f, indent=2)

print('Done! Room occupancy:')
for room in data['rooms']:
    if room.get('occupied_count', 0) > 0:
        print(f"  Room {room['room_number']}: {room['occupied_count']}/{room['capacity']} - {room['status']} ({room.get('gender_occupancy','?')})")

print('\nroom_occupancy entries:')
for o in data['room_occupancy']:
    print(f"  id:{o['id']} student_id:{o['student_id']} room_id:{o['room_id']} status:{o['status']}")
