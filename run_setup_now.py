#!/usr/bin/env python3
"""
Direct room setup script - no sudo needed
Connects using the same config as the app
"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

try:
    from config.database import db
    print("✓ Database module imported")
except Exception as e:
    print(f"✗ Error importing database: {e}")
    sys.exit(1)

# Connect to database
try:
    db.connect()
    print("✓ Connected to database")
except Exception as e:
    print(f"✗ Error connecting: {e}")
    sys.exit(1)

cursor = db.connection.cursor()

try:
    print("\n" + "="*80)
    print("HOSTEL ROOM SETUP - DELETE ALL & CREATE NEW")
    print("="*80 + "\n")
    
    # Delete existing
    print("🗑️  Deleting existing rooms and allocations...")
    cursor.execute("DELETE FROM room_occupancy")
    print("   ✓ Deleted room occupancy records")
    
    cursor.execute("DELETE FROM rooms")
    print("   ✓ Deleted existing rooms")
    
    db.connection.commit()
    
    # Create new rooms
    print("\n➕ Creating new rooms (15 total - 5 per floor)...\n")
    
    rooms_data = [
        # Floor 1
        (1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
        (1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        (1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        # Floor 2
        (2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
        (2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        (2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        # Floor 3
        (3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
        (3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        (3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
    ]
    
    for floor, room_num, room_type, capacity, rent, amenities in rooms_data:
        cursor.execute("""
            INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
        """, (floor, room_num, room_type, capacity, rent, amenities))
        print(f"   ✓ Room {room_num} (Floor {floor}) - {room_type}, Cap: {capacity}")
    
    db.connection.commit()
    
    # Verify
    print("\n" + "="*80)
    print("✅ SETUP COMPLETE - VERIFICATION")
    print("="*80 + "\n")
    
    cursor.execute("SELECT floor, COUNT(*) as count FROM rooms GROUP BY floor ORDER BY floor")
    results = cursor.fetchall()
    
    print("Rooms per floor:")
    for row in results:
        floor = row[0] if isinstance(row, tuple) else row.get('floor')
        count = row[1] if isinstance(row, tuple) else row.get('count')
        print(f"  Floor {floor}: {count} rooms")
    
    cursor.execute("SELECT COUNT(*) as total FROM rooms")
    total = cursor.fetchone()
    total_count = total[0] if isinstance(total, tuple) else total.get('total')
    
    print(f"\n  Total: {total_count} rooms ✓")
    
    # Show all rooms
    print("\n" + "="*80)
    print("COMPLETE ROOM LISTING")
    print("="*80 + "\n")
    
    cursor.execute("""
        SELECT room_number, floor, room_type, capacity, rent 
        FROM rooms 
        ORDER BY floor, room_number
    """)
    
    rooms_list = cursor.fetchall()
    for room in rooms_list:
        if isinstance(room, tuple):
            room_num, floor, rtype, cap, r = room
        else:
            room_num = room.get('room_number')
            floor = room.get('floor')
            rtype = room.get('room_type')
            cap = room.get('capacity')
            r = room.get('rent')
        
        print(f"Room {room_num:>3} | Floor {floor} | {rtype:20} | Cap: {cap} | ₹{r:,.2f}")
    
    print("\n" + "="*80)
    print("✅ SUCCESS! All 15 rooms created and ready for allocation")
    print("="*80 + "\n")
    
    cursor.close()
    
except Exception as e:
    db.connection.rollback()
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
